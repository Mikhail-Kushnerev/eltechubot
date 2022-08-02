from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.markdown import hlink

pay_button: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Оплатить',
            )
        ],
    ],
    resize_keyboard=True
)
