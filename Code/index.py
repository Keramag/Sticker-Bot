import os
from telethon import TelegramClient, events
import asyncio

# Credentials are supplied via environment variables (configured in the
# Portainer stack). See docker-compose.yml.
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']

# Persist the session (and future SQLite DB) under the data volume so login
# and sticker counts survive container restarts.
DATA_DIR = os.environ.get('DATA_DIR', 'data')
os.makedirs(DATA_DIR, exist_ok=True)
SESSION_PATH = os.path.join(DATA_DIR, 'sticker_bot')

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)


@client.on(events.NewMessage(pattern='/help'))
async def handle_help(event):
    """Respond to /help command"""
    await event.respond('Hi, I am a sticker tracking bot')


async def main():
    """Start the bot"""
    async with client:
        await client.start(bot_token=BOT_TOKEN)
        print('Sticker tracking bot is running...')
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
