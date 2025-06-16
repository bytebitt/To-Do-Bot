from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add Task"), KeyboardButton(text="Remove Task")],
        [
            KeyboardButton(text="Show Task List"),
            KeyboardButton(text="Set Reminder"),
        ],
        [KeyboardButton(text="Help")],
    ]
)
