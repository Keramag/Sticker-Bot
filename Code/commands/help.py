"""The /help command.

The simplest possible command — a good place to start. No conversation, no
state: one message comes in, one message goes out. Anyone may run it.
"""

from bot import bot


@bot.message_handler(commands=["help"])
def help_command(message):
    # TODO: Reply with a short, friendly message describing the bot.
    #   Hint: bot.send_message(message.chat.id, "Hi, I am a sticker tracking bot")
    ...
