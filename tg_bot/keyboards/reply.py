from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Выбор дисциплины")],
        [
            KeyboardButton(text="/start"),
            KeyboardButton(text="/help")
        ],
        [KeyboardButton(text="donats")],
    ],
    resize_keyboard=True
)
