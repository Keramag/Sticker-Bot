"""The /leaderboard command.

Goal (from the PRD):
    1. Emma Jones — 18 stickers
    2. John Smith — 14 stickers
    3. Alex Brown — 11 stickers

This teaches you how to READ data and build a message from a list.
"""

from bot import storage
from bot.framework import command


@command("leaderboard", description="Show sticker standings", teacher_only=False)
def leaderboard(ctx):
    # TODO 1: Get all students sorted by sticker count (highest first).
    #   Hint: students = storage.get_leaderboard()

    # TODO 2: If there are no students yet, say so and stop.
    #   Hint: if not students:
    #             ctx.say("No students yet. Add one with /addstudent.")
    #             return

    # TODO 3: Build a numbered list, one student per line, then send it.
    #   Hint: lines = []
    #         for position, student in enumerate(students, start=1):
    #             lines.append(f"{position}. {student.name} — {student.sticker_count} stickers")
    #         ctx.say("\n".join(lines))
    ...
