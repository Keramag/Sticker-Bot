"""The /addstudent command — a finished, worked example.

This is the one command that is already written for you, so you have a
reference to copy from. It shows the simplest way to have a short back-and-forth
conversation:

    Teacher: /addstudent
    Bot:     Enter student name:
    Teacher: John Smith
    Bot:     Student John Smith added successfully.

The trick is `ctx.ask()`: it sends a question and then waits for the teacher to
type a reply, handing the text back to you. No states, no callbacks — just plain
top-to-bottom code.
"""

from bot import storage
from bot.framework import command


@command("addstudent", description="Add a new student")
def addstudent(ctx):
    name = ctx.ask("Enter student name:")          # wait for the typed name
    student = storage.add_student(name)            # save them in the database
    ctx.say(f"Student {student.name} added successfully.")
