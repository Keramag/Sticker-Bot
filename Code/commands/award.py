"""The /award command — award stickers to a student by tapping buttons.

This one is mostly written for you; you finish the final step (see the TODO).

Goal (from the PRD):
    Teacher: /award
    Bot:     Select student:  [John] [Emma] [Alex]
    Teacher: taps John
    Bot:     How many stickers?  [1] [2] [3] [5]
    Teacher: taps 2
    Bot:     John Smith now has 14 stickers.

It shows two ideas the typed-reply commands don't:

1) BUTTONS. Instead of typing, the teacher taps. You build a keyboard and attach
   it to a message; each button carries a hidden `callback_data` string so you
   know which one was tapped. A tap runs a `@bot.callback_query_handler`, which
   receives a `call`:
       call.data            -> the callback_data string of the tapped button
       call.message.chat.id -> the chat it was tapped in
   Always finish a callback with `bot.answer_callback_query(call.id)` so Telegram
   stops the little loading spinner on the button.

2) REMEMBERING between taps. After the first tap we know the student but not the
   amount yet, so we stash the student with the FSM's data helper and read it back
   on the next tap:
       set_data(chat_id, "student_id", 4)            # the student tap remembers
       student_id = get_data(chat_id, "student_id")  # the amount tap reads it back

The flow is three handlers: /award shows the students -> a tap picks the student
and shows the amounts -> a tap picks the amount and awards the stickers.
"""

from telebot import types

from bot import bot, is_teacher, storage
from bot.fsm import clear, get_data, set_data


# --- step 1: /award shows the student buttons -------------------------------
@bot.message_handler(commands=["award"])
def award(message):
    if not is_teacher(message.from_user.id):
        bot.send_message(message.chat.id, "Sorry, only the teacher can use this command.")
        return

    students = storage.list_students()
    if not students:
        bot.send_message(message.chat.id, "No students yet. Add one with /addstudent.")
        return

    keyboard = types.InlineKeyboardMarkup()
    for student in students:
        keyboard.add(
            types.InlineKeyboardButton(student.name, callback_data=f"award_student:{student.id}")
        )
    bot.send_message(message.chat.id, "Select student:", reply_markup=keyboard)


# --- step 2: a student button was tapped -> show the amount buttons ----------
@bot.callback_query_handler(func=lambda call: call.data.startswith("award_student:"))
def award_pick_student(call):
    bot.answer_callback_query(call.id)  # stop the button's loading spinner
    chat_id = call.message.chat.id

    # "award_student:4" -> 4, and remember it for the next tap.
    student_id = int(call.data.split(":")[1])
    set_data(chat_id, "student_id", student_id)

    keyboard = types.InlineKeyboardMarkup()
    for amount in [1, 2, 3, 5]:
        keyboard.add(
            types.InlineKeyboardButton(str(amount), callback_data=f"award_amount:{amount}")
        )
    bot.send_message(chat_id, "How many stickers?", reply_markup=keyboard)


# --- step 3: an amount button was tapped -> award the stickers ---------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("award_amount:"))
def award_pick_amount(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id

    amount = int(call.data.split(":")[1])         # which amount was tapped
    student_id = get_data(chat_id, "student_id")  # the student we saved in step 2

    total = storage.award_stickers(student_id, amount)
    student = storage.get_student(student_id)
    if student is None:
        bot.send_message(chat_id, "Student not found. Please try again.")
    else:
        bot.send_message(chat_id, f"{student.name} now has {total} stickers.")
    clear(chat_id)
