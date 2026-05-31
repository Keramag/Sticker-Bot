"""The /addstudent command — written with a real aiogram FSM.

Most commands in this project use the simple `ctx.ask()` helper. This one is
written the "real aiogram" way ON PURPOSE, so you can see how a multi-step
conversation actually works underneath. Read Code/examples/fsm_example.py first
for a gentle, standalone introduction to FSM.

The flow (from the PRD):
    Teacher: /addstudent
    Bot:     Enter student name:
    Teacher: John Smith          <- handled while in the waiting_for_name state
    Bot:     Student John Smith added successfully.
"""

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot import storage
from bot.framework import add_to_menu, is_teacher, router

# The @command decorator would normally register this command and add it to the
# Telegram "/" menu. Because we are doing it the raw FSM way, we add the menu
# entry ourselves:
add_to_menu("addstudent", "Add a new student")


# 1) The steps this conversation can be in. /addstudent has just one: we are
#    waiting for the teacher to type a name.
class AddStudent(StatesGroup):
    waiting_for_name = State()


# 2) /addstudent starts the conversation and moves into the waiting_for_name step.
@router.message(Command("addstudent"))
async def addstudent_start(message: Message, state: FSMContext):
    if not is_teacher(message.from_user.id):
        await message.answer("Sorry, only the teacher can use this command.")
        return
    await message.answer("Enter student name:")
    await state.set_state(AddStudent.waiting_for_name)


# 3) This handler runs ONLY while we are waiting for the name (because of the
#    state filter). It saves the student and ends the conversation.
@router.message(AddStudent.waiting_for_name)
async def addstudent_got_name(message: Message, state: FSMContext):
    student = storage.add_student(message.text)
    await message.answer(f"Student {student.name} added successfully.")
    await state.clear()  # conversation finished -> back to no state
