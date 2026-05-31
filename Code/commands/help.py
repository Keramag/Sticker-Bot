"""The /help command.

This is the simplest possible command — a good place to start.
Your job: make the bot reply with a short, friendly description of itself.
"""

from bot.framework import command


# `teacher_only=False` means ANYONE can run /help (students too).
@command("help", description="Show what this bot does", teacher_only=False)
async def help_command(ctx):
    # TODO: Send a friendly message describing the bot.
    #   Hint: await ctx.say("Hi, I am a sticker tracking bot")
    ...
