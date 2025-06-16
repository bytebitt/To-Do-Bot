import asyncio
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from typing import List
from datetime import datetime
import app.keyboards as kb

router = Router()

tasks: List = []

HELP_TEXT: str = """
Hello! I'm To-Do List bot

Bot Functionallity:
 - /start - start the bot
 - Add task (add a task to your task list)
 - Remove task (remove a task from your task list)
 - Set reminder (bot will remind you your task at passed time)
 
author of the bot: @bytebit1
"""


class AddTask(StatesGroup):
    waiting_for_task = State()


class RemoveTask(StatesGroup):
    waiting_for_task = State()


class SetReminder(StatesGroup):
    waiting_for_task = State()
    waiting_for_time = State()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.reply("Hello! I'm To-Do List bot", reply_markup=kb.main_keyboard)


@router.message(F.text == "Help")
async def handle_help(message: Message) -> None:
    await message.reply(HELP_TEXT)


@router.message(F.text == "Add Task")
async def get_task(message: Message, state: FSMContext) -> None:
    await message.reply("Enter your task:")
    await state.set_state(AddTask.waiting_for_task)


@router.message(AddTask.waiting_for_task)
async def add_task(message: Message, state: FSMContext) -> None:
    task = message.text
    tasks.append(task)
    await message.answer("Task successfully added to your task list")
    await state.clear()


@router.message(F.text == "Remove Task")
async def get_task(message: Message, state: FSMContext) -> None:
    if not tasks:
        await message.answer("List empty")
        return

    await handle_task_list(message)
    await message.reply("Enter your task number:")
    await state.set_state(RemoveTask.waiting_for_task)


@router.message(RemoveTask.waiting_for_task)
async def add_task(message: Message, state: FSMContext) -> None:
    try:
        task_number = int(message.text) - 1
    except ValueError:
        await message.reply("Incorrect Input")
        return

    if task_number < 0 or task_number >= len(tasks):
        await message.answer("Task doesn't exists")

    tasks.pop(task_number)
    await message.answer("Task successfully removed from your task list")
    await state.clear()


@router.message(F.text == "Show Task List")
async def handle_task_list(message: Message):
    if not tasks:
        await message.answer("List empty")
        return

    task_list = ""

    for index, task in enumerate(tasks, start=1):
        task_list += f"{index}. {task}\n"

    await message.answer(task_list)


@router.message(F.text == "Set Reminder")
async def ask_datetime(message: Message, state: FSMContext):
    await message.reply("Enter the date in the format DD.MM.YYYY HH.MM")
    await state.set_state(SetReminder.waiting_for_time)


@router.message(SetReminder.waiting_for_time)
async def process_datetime(message: Message, state: FSMContext):
    date = message.text
    try:
        reminder_time = datetime.strptime(date, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.reply("Incorrect date format. Use DD.MM.YYYY HH:MM")
        return

    if reminder_time <= datetime.now():
        await message.reply("You can't set reminder to the past")
        return

    await state.update_data(reminder_time=reminder_time)
    await message.reply("Enter task text:")
    await state.set_state(SetReminder.waiting_for_task)


@router.message(SetReminder.waiting_for_task)
async def process_task(message: Message, state: FSMContext):
    user_data = await state.get_data()
    reminder_time = user_data.get("reminder_time")

    if reminder_time is None:
        await message.reply("Something went wrong, please start over.")
        await state.clear()
        return 

    task_text = message.text
    now = datetime.now()
    delay = (reminder_time - now).total_seconds()

    await message.reply(f"Reminder set for {reminder_time.strftime('%d.%m.%Y %H:%M')}")

    async def reminder():
        await asyncio.sleep(delay)
        await message.answer(f"Reminder: {task_text}")

    asyncio.create_task(reminder())
    await state.clear()
