from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tg_bot.misc.logger import logger
from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback
from tg_bot.services.db_api.db_commands import get_types

menu_cd = CallbackData(
    "show_menu",
    "level",
    "discipline",
    "type_name",
    "id_"
)
buy_item = CallbackData(
    "buy",
    "item_id"
)


def make_callback_data(level=0, discipline="", type_name="", id_=0):
    return menu_cd.new(
        level=level,
        discipline=discipline,
        type_name=type_name,
        id_=id_
    )


async def choice(discipline, id_):
    CURRENT_LEVEL = 0
    markup_s = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Материалы",
                    callback_data=make_callback_data(
                        level=CURRENT_LEVEL + 1,
                        discipline=discipline,
                        id_=id_
                    )
                ),
                InlineKeyboardButton(
                    text="Консультация",
                    callback_data="info"
                )
            ]
        ]
    )
    logger.info(markup_s)
    return markup_s


async def type_keyboard(discipline, id_):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()
    types = await get_types(discipline)
    for i in types:
        button_text = i.type.name
        logger.info(make_callback_data)
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            discipline=discipline,
            type_name=i.type.name,
            id_=id_
        )
        logger.info(callback_data)
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1,
                discipline=discipline,
                id_=id_
            )
        )
    )
    return markup


def next_answ(discipline, type_name, id_):
    CURRENT_LEVEL = 2
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
                        discipline=discipline,
                        type_name=type_name,
                        id_=id_
                    ),
                )
            ]
        ]
    )
    return markup
