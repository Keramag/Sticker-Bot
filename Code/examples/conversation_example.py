"""A STANDALONE example of a multi-step conversation in pyTelegramBotAPI.

This file is NOT part of the bot — it's a tiny playground you can read and run
on its own. It teaches one idea: how a bot can ask a question and then wait for
the answer.

------------------------------------------------------------------------------
The idea: "what happens after I ask a question?"
------------------------------------------------------------------------------
A bot reacts to messages one at a time. So when it asks "What is your name?", it
needs a way to say: "the NEXT message from this person is the answer — send it
here." In pyTelegramBotAPI that tool is:

    bot.register_next_step_handler(message, some_function)

It means: when this chat sends its next message, call `some_function(message)`
instead of the normal handlers.

That is exactly what the bot's `ctx.ask()` helper does for you behind the
scenes — except `ctx.ask()` hides it so your command can read as simple
top-to-bottom code. This example shows the raw version so you can see the gears.

------------------------------------------------------------------------------
Run it on its own (you need a bot token from @BotFather):
    BOT_TOKEN="123:abc" python Code/examples/conversation_example.py
Then send /hello to your bot.
------------------------------------------------------------------------------
"""

import os

import telebot

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])


# 1) /hello asks the question, then says "the next message is the answer".
@bot.message_handler(commands=["hello"])
def start(message):
    bot.send_message(message.chat.id, "What is your name?")
    bot.register_next_step_handler(message, got_name)


# 2) This runs when the next message arrives — it IS the answer.
def got_name(message):
    bot.send_message(message.chat.id, f"Hello, {message.text}! 🎉")


print("Conversation example running — send /hello in Telegram.")
bot.infinity_polling()
