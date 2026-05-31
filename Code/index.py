from telethon import TelegramClient, events
import asyncio

# Replace these with your actual credentials
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'

client = TelegramClient('sticker_bot', API_ID, API_HASH)


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
