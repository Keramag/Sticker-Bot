"""The /addstudent command.

Goal (from the PRD):
    Teacher: /addstudent
    Bot:     Enter student name:
    Teacher: John Smith
    Bot:     Student John Smith added successfully.

This teaches you how to ASK a question and SAVE the answer.
"""

from bot import storage
from bot.framework import command


@command("addstudent", description="Add a new student")
async def addstudent(ctx):
    # TODO 1: Ask the teacher for the student's name and remember the answer.
    #   Hint: name = await ctx.ask("Enter student name:")

    # TODO 2: Save the new student using the storage layer.
    #   Hint: storage.add_student(name)

    # TODO 3: Confirm it worked.
    #   Hint: await ctx.say(f"Student {name} added successfully.")
    ...
