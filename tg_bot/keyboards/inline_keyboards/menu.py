from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback
from tg_bot.services.db_api.db_commands import get_types, get_item

menu_cd = CallbackData(
    "show_menu",
    "level",
    "discipline",
    "type_name"
)
buy_item = CallbackData(
    "buy",
    "item_id"
)


def make_callback_data(level, discipline="", type_name=""):
    return menu_cd.new(
        level=level,
        discipline=discipline,
        type_name=type_name
    )


async def type_keyboard(message):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()
    types = await get_types(message)
    for i in types["types"]:
        button_text = f"{i.type.name}"
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            discipline=types["name"],
            type_name=i.type.name
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )
    return markup


def next_answ(discipline, type_name):
    CURRENT_LEVEL = 1
    # await get_item(discipline, type_name)
    markup = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить в корзину",
                    callback_data=add_callback.new(
                        item_name="ss",
                        quantity=1
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Отменить выбор",
                    callback_data=make_callback_data(
                        level=CURRENT_LEVEL - 1,
                        # discipline='discipline',
                        type_name=type_name
                    ),
                )
            ],
            # [
            #     InlineKeyboardButton(
            #         text="Оформить заказа",
            #         callback_data=buy_item.new(item_id='Купить'),
            #     ),
            # ]
        ]
    )
    return markup


def cart():
    markup = InlineKeyboardMarkup(

    )