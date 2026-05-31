"""A STANDALONE example of a multi-step conversation, built with a tiny FSM.

This file is NOT part of the bot — it's a small playground you can read and run
on its own. It teaches ONE idea: how a bot remembers what it is waiting for.

------------------------------------------------------------------------------
The idea: "what step is this chat on?"
------------------------------------------------------------------------------
A bot reacts to messages one at a time. So when it asks "What is your name?", the
NEXT message it gets is the answer — but only if the bot remembers it was waiting
for a name. That memory is the whole trick, and here it is just ONE dictionary:

    states = {chat_id: "awaiting_name"}

This is a finite state machine (FSM): each chat is on a "step" (a state), and the
incoming message means different things depending on the step. The real bot wraps
this same idea in tidy helpers (see Code/bot/fsm.py); here it is laid bare.

------------------------------------------------------------------------------
Run it on its own (you need a bot token from @BotFather):
    BOT_TOKEN="123:abc" python Code/examples/conversation_example.py
Then send /hello to your bot.
------------------------------------------------------------------------------
"""

import os

import telebot

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])

# The entire "machine": which step each chat is on. A chat not listed here is on
# no step at all. Try adding `print(states)` inside the handlers to watch it.
states = {}


# 1) /hello asks the question and moves this chat onto the "awaiting_name" step.
@bot.message_handler(commands=["hello"])
def start(message):
    bot.send_message(message.chat.id, "What is your name?")
    states[message.chat.id] = "awaiting_name"


# 2) This handler runs ONLY while the chat is on "awaiting_name", so we know the
#    message is the answer. Then we forget the step — the conversation is over.
@bot.message_handler(func=lambda m: states.get(m.chat.id) == "awaiting_name")
def got_name(message):
    bot.send_message(message.chat.id, f"Hello, {message.text}! 🎉")
    states.pop(message.chat.id, None)


print("Conversation example running — send /hello in Telegram.")
bot.infinity_polling()
