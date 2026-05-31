"""The /addstudent command — a finished, worked example.

This is the one command already written for you, so you have a reference to
copy. It shows the simplest multi-step conversation, built with our tiny FSM
(see bot/fsm.py):

    Teacher: /addstudent
    Bot:     Enter student name:
    Teacher: John Smith      <- handled while the chat is on the "awaiting_name" step
    Bot:     Student John Smith added successfully.

It works in two handlers:

  1. `addstudent` runs when the teacher types /addstudent. It asks the question
     and moves the chat onto the "awaiting_name" step with set_state().

  2. `addstudent_got_name` runs ONLY while the chat is on that step — that is what
     `func=lambda m: waiting_for(m, "awaiting_name")` means. So when the next
     message arrives, we know it is the name. We save the student and then call
     clear() to end the conversation (back to no step).

Tip: add `print(get_state(message.chat.id))` anywhere to watch the step change.
"""

from bot import bot, is_teacher, storage
from bot.fsm import clear, set_state, waiting_for


@bot.message_handler(commands=["addstudent"])
def addstudent(message):
    if not is_teacher(message.from_user.id):
        bot.send_message(message.chat.id, "Sorry, only the teacher can use this command.")
        return
    bot.send_message(message.chat.id, "Enter student name:")
    set_state(message.chat.id, "awaiting_name")  # move to the next step


@bot.message_handler(func=lambda m: waiting_for(m, "awaiting_name"))
def addstudent_got_name(message):
    name = message.text                          # this message IS the name
    student = storage.add_student(name)          # save them in the database
    bot.send_message(message.chat.id, f"Student {student.name} added successfully.")
    clear(message.chat.id)                       # conversation finished -> no step
