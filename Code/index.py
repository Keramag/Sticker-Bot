"""Entry point. You normally don't need to touch this file.

It (1) prepares the database and (2) starts the bot. Starting the bot loads
every command from the commands/ folder, tells Telegram about them, and begins
listening for messages.
"""

from bot import storage
from bot.framework import start


def main():
    storage.init_db()  # create the database table if needed
    start()            # load commands and run the bot (this blocks)


if __name__ == "__main__":
    main()
