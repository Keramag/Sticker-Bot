"""A STANDALONE example of aiogram's Finite State Machine (FSM).

This file is NOT part of the bot — it's a tiny playground you can read and run
on its own. It teaches one idea: how a bot remembers "where it is" in a
conversation.

------------------------------------------------------------------------------
What is a Finite State Machine (FSM)?
------------------------------------------------------------------------------
A conversation has steps. After "/hello" the bot is waiting for your NAME. That
"waiting for…" situation is called a STATE. The bot is in one state at a time
(or in no state), and it moves between them. That's all an FSM is.

aiogram gives you three tools:
  * StatesGroup / State          -> name the steps
  * await state.set_state(...)   -> move into a step
  * @router.message(SomeState)   -> a handler that runs ONLY during that step
  * await state.clear()          -> the conversation is over; forget the state

------------------------------------------------------------------------------
Run it on its own (you need a bot token from @BotFather):
    BOT_TOKEN="123:abc" python Code/examples/fsm_example.py
Then send /hello to your bot.
------------------------------------------------------------------------------
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

router = Router()


# 1) Name the step(s). Here there is just one: we're waiting for a name.
class Form(StatesGroup):
    waiting_for_name = State()


# 2) /hello starts the conversation and moves into the waiting_for_name step.
@router.message(Command("hello"))
async def start(message: Message, state: FSMContext):
    await message.answer("What is your name?")
    await state.set_state(Form.waiting_for_name)


# 3) This handler runs ONLY while we are waiting for the name (notice we filter
#    by the STATE, not by a command). Then it ends the conversation.
@router.message(Form.waiting_for_name)
async def got_name(message: Message, state: FSMContext):
    await message.answer(f"Hello, {message.text}! 🎉")
    await state.clear()  # done -> back to no state


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.environ["BOT_TOKEN"])
    dispatcher = Dispatcher()          # uses in-memory FSM storage by default
    dispatcher.include_router(router)
    logging.info("FSM example running — send /hello in Telegram.")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
