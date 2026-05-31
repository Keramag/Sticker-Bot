"""The /award command.

Goal (from the PRD):
    Teacher: /award
    Bot:     Select student:  [John] [Emma] [Alex]
    Teacher: taps John
    Bot:     How many stickers?  [1] [2] [3] [5]
    Teacher: taps 2
    Bot:     John Smith now has 14 stickers.

This teaches you how to show BUTTONS and react to the teacher's choice.
This is the trickiest command — take it one TODO at a time.
"""

from bot import storage
from bot.framework import command


@command("award", description="Award stickers to a student")
def award(ctx):
    # TODO 1: Get the list of all students from storage.
    #   Hint: students = storage.list_students()

    # TODO 2: If there are no students yet, tell the teacher and stop.
    #   Hint: if not students:
    #             ctx.say("No students yet. Add one with /addstudent.")
    #             return

    # TODO 3: Show the students as buttons and wait for the teacher to pick one.
    #   The `label` tells the button what text to show for each student.
    #   Hint: student = ctx.choose("Select student:", students, label=lambda s: s.name)

    # TODO 4: Ask how many stickers, offering a few handy amounts as buttons.
    #   Hint: amount = ctx.choose("How many stickers?", [1, 2, 3, 5])

    # TODO 5: Award the stickers and confirm the new total.
    #   Hint: total = storage.award_stickers(student.id, amount)
    #         ctx.say(f"{student.name} now has {total} stickers.")
    ...
