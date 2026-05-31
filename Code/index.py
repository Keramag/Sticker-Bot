"""Entry point. You normally don't need to touch this file.

It (1) prepares the database, (2) loads every command from the commands/
folder, (3) tells Telegram about the commands, and (4) starts the bot.
"""

import asyncio
import logging
import os

from aiogram import Bot
from aiogram.types import BotCommand

from bot import storage
from bot.framework import build_dispatcher, load_commands, registered_commands


async def main():
    logging.basicConfig(level=logging.INFO)

    storage.init_db()       # create the database table if needed
    load_commands()         # import every file in commands/
    dispatcher = build_dispatcher()

    bot = Bot(token=os.environ["BOT_TOKEN"])

    # Show the command list in Telegram's "/" menu.
    await bot.set_my_commands(
        [BotCommand(command=c["name"], description=c["description"]) for c in registered_commands()]
    )

    logging.info("Sticker tracking bot is running...")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
