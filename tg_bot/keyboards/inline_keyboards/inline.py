from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback


continue_keyboard = InlineKeyboardMarkup()
answer = InlineKeyboardButton(
    text="Удалить",
    callback_data="continue"
)
continue_keyboard.insert(answer)
# answer_2 = InlineKeyboardButton(
#     text="Оформить заказ",
#     callback_data="buy"
# )
# for answ in (answer, answer_2):
#     continue_keyboard.insert(answ)
