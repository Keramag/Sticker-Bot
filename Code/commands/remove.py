from telebot import types

from bot import bot, is_teacher, storage


@bot.message_handler(commands=["remove"])
def remove(message):
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
            types.InlineKeyboardButton(student.name, callback_data=f"remove_student:{student.id}")
        )
    bot.send_message(message.chat.id, "Select student to remove:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_student:"))
def remove_pick_student(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id

    student_id = int(call.data.split(":")[1])
    student = storage.get_student(student_id)
    if student is None:
        bot.send_message(chat_id, "Student not found. Please try again.")
        return

    storage.delete_student(student_id)
    bot.send_message(chat_id, f"Removed student {student.name}.")
