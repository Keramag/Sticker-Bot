"""The shared bot object that every command file uses.

There is no mini-framework anymore. This file creates ONE plain
pyTelegramBotAPI bot, and your command files hang their handlers on it:

    from bot import bot

    @bot.message_handler(commands=["help"])
    def help_command(message):
        bot.send_message(message.chat.id, "Hi!")

`message` is the Telegram message that arrived — it comes in as a normal
function argument, so there is nothing hidden to import or look up.
"""

import os

import telebot

# The one and only bot. `threaded=False` means messages are handled one at a
# time, in order — simplest to reason about, and it keeps the FSM in bot/fsm.py
# safe without any locks.
bot = telebot.TeleBot(os.environ["BOT_TOKEN"], threaded=False)

# Optional: the Telegram user id of the teacher. If set, only that user may run
# the teacher commands. If unset, everyone is allowed (handy while developing).
TEACHER_ID = os.environ.get("TEACHER_ID")


def is_teacher(user_id: int) -> bool:
    """True if this user is allowed to run teacher-only commands.

    Call it explicitly at the top of a command, e.g.:

        if not is_teacher(message.from_user.id):
            bot.send_message(message.chat.id, "Teacher only.")
            return
    """
    if not TEACHER_ID:
        return True  # no teacher configured -> allow everyone (dev mode)
    return str(user_id) == str(TEACHER_ID)
