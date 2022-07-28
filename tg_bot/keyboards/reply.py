from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


pay_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оплатить")],
    ],
    resize_keyboard=True
)
