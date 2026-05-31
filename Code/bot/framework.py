"""The Sticker Bot mini-framework.

You normally do NOT need to read or change this file. It exists so that writing
a command stays simple. In your command files you only ever use three things:

    from bot.framework import command

    @command("hello", description="Say hello")
    async def hello(ctx):
        name = await ctx.ask("What is your name?")        # wait for a typed reply
        pick = await ctx.choose("Pick one:", ["A", "B"])  # wait for a button tap
        await ctx.say(f"Hi {name}, you picked {pick}")    # send a message

Behind the scenes this uses aiogram and Telegram inline buttons, but you don't
have to learn any of that to write a command.
"""

import asyncio
import importlib
import os
import pkgutil

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

router = Router()

# Everything registered with @command, so /help and the menu can list them.
_REGISTERED: list[dict] = []

# When a command is "waiting" for the teacher's next reply or button tap, we
# park an asyncio Future here, keyed by the user's id, and resolve it when the
# reply/tap arrives. This is what lets ctx.ask / ctx.choose read like normal
# top-to-bottom code instead of a tangle of separate handler functions.
_waiting_for_text: dict[int, asyncio.Future] = {}
_waiting_for_choice: dict[int, tuple[asyncio.Future, list]] = {}

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

    def __init__(self, message: Message):
        self.message = message
        self.bot = message.bot
        self.chat_id = message.chat.id
        self.user_id = message.from_user.id

    async def say(self, text: str, **kwargs):
        """Send a plain message to the chat."""
        return await self.bot.send_message(self.chat_id, text, **kwargs)

    async def ask(self, question: str) -> str:
        """Ask a question and wait for the teacher to TYPE a reply.

        Returns the text they sent.
        """
        await self.say(question)
        future = asyncio.get_running_loop().create_future()
        _waiting_for_text[self.user_id] = future
        return await future

    async def choose(self, question: str, options: list, label=None):
        """Ask a question and wait for the teacher to TAP a button.

        `options` is a list of anything (numbers, strings, Student objects...).
        `label` is an optional function turning one option into its button text,
        e.g. label=lambda student: student.name. Returns the chosen option.
        """
        to_label = label or (lambda option: str(option))
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=to_label(option), callback_data=f"choose:{index}")]
                for index, option in enumerate(options)
            ]
        )
        await self.say(question, reply_markup=keyboard)
        future = asyncio.get_running_loop().create_future()
        _waiting_for_choice[self.user_id] = (future, list(options))
        return await future


def command(name: str, description: str = "", teacher_only: bool = True):
    """Decorator that turns an async function into a /command.

    Example:
        @command("leaderboard", description="Show standings")
        async def leaderboard(ctx):
            ...
    """

    def decorator(func):
        async def handler(message: Message):
            ctx = Conversation(message)
            # Starting a fresh command cancels any half-finished flow.
            _waiting_for_text.pop(ctx.user_id, None)
            _waiting_for_choice.pop(ctx.user_id, None)
            if teacher_only and not is_teacher(ctx.user_id):
                await ctx.say("Sorry, only the teacher can use this command.")
                return
            await func(ctx)

        router.message.register(handler, Command(name))
        _REGISTERED.append({"name": name, "description": description or name})
        return func

    return decorator


def registered_commands() -> list[dict]:
    return list(_REGISTERED)


# --- internal plumbing: resolve the Futures that ask()/choose() are waiting on -

async def _on_text_reply(message: Message):
    """Any non-command message: if a command is waiting for text, deliver it."""
    future = _waiting_for_text.pop(message.from_user.id, None)
    if future and not future.done():
        future.set_result(message.text or "")


async def _on_button_tap(callback: CallbackQuery):
    """A 'choose' button was tapped: deliver the chosen option."""
    entry = _waiting_for_choice.pop(callback.from_user.id, None)
    await callback.answer()
    if not entry:
        return
    future, options = entry
    index = int(callback.data.split(":")[1])
    if not future.done():
        future.set_result(options[index])
    # Remove the buttons so they can't be tapped twice.
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass


def load_commands():
    """Import every file in the commands/ folder so their @command runs."""
    import commands as commands_package

    for module in pkgutil.iter_modules(commands_package.__path__):
        importlib.import_module(f"commands.{module.name}")


def build_dispatcher() -> Dispatcher:
    """Wire up aiogram. Call this AFTER load_commands()."""
    # Registered last, so the catch-all reply/tap handlers have lower priority
    # than the real /command handlers.
    router.message.register(_on_text_reply)
    router.callback_query.register(_on_button_tap, F.data.startswith("choose:"))

    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    return dispatcher
