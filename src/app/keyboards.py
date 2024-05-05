from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/add"), KeyboardButton(text="/tsk")],
    [KeyboardButton(text="/del")]
])
