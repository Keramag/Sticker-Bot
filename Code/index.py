import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Only the bot token is required (aiogram uses the HTTP Bot API).
BOT_TOKEN = os.environ['BOT_TOKEN']

# Persist the future SQLite student DB under the data volume so sticker
# counts survive container restarts.
DATA_DIR = os.environ.get('DATA_DIR', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

dp = Dispatcher()


@dp.message(Command('help'))
async def handle_help(message: Message) -> None:
    """Respond to /help command."""
    await message.answer('Hi, I am a sticker tracking bot')


async def main() -> None:
    """Start the bot."""
    bot = Bot(token=BOT_TOKEN)
    logging.info('Sticker tracking bot is running...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
