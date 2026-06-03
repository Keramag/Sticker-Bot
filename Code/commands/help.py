"""The /help command.

The simplest possible command — a good place to start. No conversation, no
state: one message comes in, one message goes out. Anyone may run it.
"""

from bot import bot


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Hi, I am a sticker tracking bot."
        "\n\nType /addstudent to add a student, /award to award a sticker, /leaderboard to see the leaderboard,"
        " /clear to reset a student's sticker total, and /help to see this message again."
    )