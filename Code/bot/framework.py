"""The Sticker Bot mini-framework.

You normally do NOT need to read or change this file. It exists so that writing
a command stays simple. In your command files you only ever use three things:

    from bot.framework import command

    @command("hello", description="Say hello")
    def hello(ctx):
        name = ctx.ask("What is your name?")        # wait for a typed reply
        pick = ctx.choose("Pick one:", ["A", "B"])  # wait for a button tap
        ctx.say(f"Hi {name}, you picked {pick}")    # send a message

Notice there is no `async` and no `await` anywhere — your commands are plain,
ordinary functions that read top to bottom. Behind the scenes this uses the
pyTelegramBotAPI library and a little threading so that `ctx.ask()` can pause
and wait for a reply, but you don't have to learn any of that to write a
command.
"""

import importlib
import logging
import os
import pkgutil
import queue
import threading

import telebot
from telebot import types

# Created in start(). Your commands use it indirectly, through `ctx`.
bot: telebot.TeleBot | None = None

# Everything registered with @command, so the "/" menu can list them.
_REGISTERED: list[dict] = []

# When a command is "waiting" for the teacher's next reply or button tap, we
# park a queue here, keyed by the chat id, and drop the answer into it when the
# reply/tap arrives. This is what lets ctx.ask / ctx.choose read like normal
# top-to-bottom code instead of a tangle of separate handler functions.
_waiting_for_text: dict[int, queue.Queue] = {}
_waiting_for_choice: dict[int, tuple[queue.Queue, list]] = {}

# Optional: the Telegram user id of the teacher. If set, only that user may run
# commands marked teacher_only. If unset, everyone is allowed (handy while you
# are still developing and testing).
TEACHER_ID = os.environ.get("TEACHER_ID")


def is_teacher(user_id: int) -> bool:
    if not TEACHER_ID:
        return True  # no teacher configured -> allow everyone (dev mode)
    return str(user_id) == str(TEACHER_ID)


class Conversation:
    """The `ctx` your command receives. Your friendly toolbox."""

    def __init__(self, message: types.Message):
        self.message = message
        self.chat_id = message.chat.id
        self.user_id = message.from_user.id

    def say(self, text: str, **kwargs):
        """Send a plain message to the chat."""
        return bot.send_message(self.chat_id, text, **kwargs)

    def ask(self, question: str) -> str:
        """Ask a question and wait for the teacher to TYPE a reply.

        Returns the text they sent.
        """
        self.say(question)
        answer: queue.Queue = queue.Queue(maxsize=1)
        _waiting_for_text[self.chat_id] = answer
        return answer.get()  # pauses here until the reply arrives

    def choose(self, question: str, options: list, label=None):
        """Ask a question and wait for the teacher to TAP a button.

        `options` is a list of anything (numbers, strings, Student objects...).
        `label` is an optional function turning one option into its button text,
        e.g. label=lambda student: student.name. Returns the chosen option.
        """
        to_label = label or (lambda option: str(option))
        keyboard = types.InlineKeyboardMarkup()
        for index, option in enumerate(options):
            keyboard.add(
                types.InlineKeyboardButton(to_label(option), callback_data=f"choose:{index}")
            )
        self.say(question, reply_markup=keyboard)
        answer: queue.Queue = queue.Queue(maxsize=1)
        _waiting_for_choice[self.chat_id] = (answer, list(options))
        return answer.get()  # pauses here until a button is tapped


def command(name: str, description: str = "", teacher_only: bool = True):
    """Decorator that turns a function into a /command.

    Example:
        @command("leaderboard", description="Show standings")
        def leaderboard(ctx):
            ...
    """

    def decorator(func):
        _REGISTERED.append(
            {
                "name": name,
                "description": description or name,
                "teacher_only": teacher_only,
                "func": func,
            }
        )
        return func

    return decorator


def registered_commands() -> list[dict]:
    return [{"name": c["name"], "description": c["description"]} for c in _REGISTERED]


# --- internal plumbing: run commands and deliver replies/taps to them ----------

def _run_command(cmd: dict, message: types.Message):
    """Run one command's function, having prepared its `ctx`."""
    ctx = Conversation(message)
    # Starting a fresh command cancels any half-finished flow for this chat.
    _waiting_for_text.pop(ctx.chat_id, None)
    _waiting_for_choice.pop(ctx.chat_id, None)
    if cmd["teacher_only"] and not is_teacher(ctx.user_id):
        ctx.say("Sorry, only the teacher can use this command.")
        return
    try:
        cmd["func"](ctx)
    except Exception:
        logging.exception("Command /%s crashed", cmd["name"])
        ctx.say("Oops, something went wrong running that command.")


def _make_handler(cmd: dict):
    def handler(message: types.Message):
        # Run the command in its own thread so it can pause inside ctx.ask /
        # ctx.choose (waiting for a reply) without freezing the whole bot.
        threading.Thread(target=_run_command, args=(cmd, message), daemon=True).start()

    return handler


def _on_reply(message: types.Message):
    """Any ordinary message: if a command is waiting for text, deliver it."""
    if message.text and message.text.startswith("/"):
        return  # a slash command, not a reply — let the command handlers take it
    answer = _waiting_for_text.pop(message.chat.id, None)
    if answer:
        answer.put(message.text or "")


def _on_choice(call: types.CallbackQuery):
    """A 'choose' button was tapped: deliver the chosen option."""
    bot.answer_callback_query(call.id)
    entry = _waiting_for_choice.pop(call.message.chat.id, None)
    if not entry:
        return
    answer, options = entry
    index = int(call.data.split(":")[1])
    answer.put(options[index])
    # Remove the buttons so they can't be tapped twice.
    try:
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id, reply_markup=None
        )
    except Exception:
        pass


def load_commands():
    """Import every file in the commands/ folder so their @command runs."""
    import commands as commands_package

    for module in pkgutil.iter_modules(commands_package.__path__):
        importlib.import_module(f"commands.{module.name}")


def start():
    """Create the bot, wire everything up, and start listening. Call this once."""
    global bot
    logging.basicConfig(level=logging.INFO)
    bot = telebot.TeleBot(os.environ["BOT_TOKEN"], threaded=False)

    load_commands()  # import every command file so their @command runs

    # Real /commands first...
    for cmd in _REGISTERED:
        bot.register_message_handler(_make_handler(cmd), commands=[cmd["name"]])
    # ...then the catch-alls that feed ctx.ask() / ctx.choose(), registered last
    # so they only handle leftovers (replies and button taps).
    bot.register_message_handler(_on_reply, func=lambda m: True)
    bot.register_callback_query_handler(_on_choice, func=lambda c: True)

    # Show the command list in Telegram's "/" menu.
    bot.set_my_commands(
        [types.BotCommand(c["name"], c["description"]) for c in registered_commands()]
    )

    logging.info("Sticker tracking bot is running...")
    bot.infinity_polling()
