from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Выбор дисциплины")],
    ],
    resize_keyboard=True
)
