from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback

choice = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="В корзину",
                callback_data=add_callback.new(
                    item_name="ss",
                    quantity=1
                ),
            ),
            InlineKeyboardButton(
                text="Отменить покупку",
                callback_data="buy",
            )
        ],
        [
            InlineKeyboardButton(
                text="Оформить заказа",
                callback_data="clear",
            ),
        ]
    ]
)

continue_keyboard = InlineKeyboardMarkup()
answer = InlineKeyboardButton(
    text="Продолжить покупку?",
    callback_data="continue"
)
continue_keyboard.insert(answer)
# answer_2 = InlineKeyboardButton(
#     text="Оформить заказ",
#     callback_data="buy"
# )
# for answ in (answer, answer_2):
#     continue_keyboard.insert(answ)
