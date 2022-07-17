from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оплатить")],
    ],
    resize_keyboard=True
)
