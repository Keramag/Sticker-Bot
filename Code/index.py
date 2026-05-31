"""Entry point. You normally don't need to touch this file.

It (1) prepares the database, (2) imports every command file, (3) tells Telegram
the command list for the "/" menu, and (4) starts listening.

Step 2 is the important one: importing a command file runs its
`@bot.message_handler(...)` lines, and THAT is what turns the command on. When
you add a new command file, add one `import commands.<name>` line below.
"""

from telebot import types

from bot import bot, storage

# Importing each command file registers its handlers on the shared bot.
import commands.help
import commands.addstudent
import commands.award
import commands.leaderboard


def main():
    storage.init_db()  # create the database table if needed

    # Show the command list in Telegram's "/" menu.
    bot.set_my_commands(
        [
            types.BotCommand("help", "Show what this bot does"),
            types.BotCommand("addstudent", "Add a new student"),
            types.BotCommand("award", "Award stickers to a student"),
            types.BotCommand("leaderboard", "Show sticker standings"),
        ]
    )

    print("Sticker tracking bot is running...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
