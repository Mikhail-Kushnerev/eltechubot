from aiogram import types
from aiogram.dispatcher import FSMContext

from tg_bot.keyboards.inline_keyboards.menu import (
    type_keyboard,
    next_answ,
    menu_cd
)
from tg_bot.services.redis_db_cache import write_data, changer_data, dd
from tg_bot.services.db_api.db_commands import get_product
from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback
from tg_bot.keyboards.inline_keyboards.inline import continue_keyboard
from loader import dp
from tg_bot.misc import rate_limit


@dp.callback_query_handler(add_callback.filter(item_name="ss"))
async def add_item(call: types.CallbackQuery, callback_data, state: FSMContext):
    id_ = call.message.message_id - 1
    try:
        await dp.bot.edit_message_text(
            text='Ждёт оплаты:\n'
            f"{dd[id_][1]}",
            chat_id=call.message.chat.id,
            message_id=dd[id_][0][0],
            reply_markup=continue_keyboard
        )
        await call.answer('Добавлено в корзину', )
    except Exception:
        await call.message.edit_text(
            text="сломал бота, типичный ЛЭТИ'шник...\nПиши запрос заново :D",
            # reply_markup=""
        )


async def get_to_cart(message, *args, **kwargs):
    if isinstance(message, types.Message):
        id_ = message.message_id
        print(message, '\n', id_)
        obj = (
            id_,
            [],
            kwargs['target']["target"].name,
        )
        await write_data(obj)
        markup = await type_keyboard(kwargs["obj"])
        await message.answer(
            text='\n'.join(
                (
                    "Мои поздравление, мой друг. Такая есть",
                    f" - {kwargs['target']['target'].name};",
                    f" - {kwargs['target']['target'].lektor}.",
                )
            ),
            reply_markup=markup
        )
    else:
        call = message
        inline_text = call.message.text.split()[2][:-1]
        markup = await type_keyboard(inline_text)
        await dp.bot.edit_message_text(
            text=call.message.text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )


async def buy(callback: types.CallbackQuery, discipline, type_name):
    markup = next_answ(discipline, type_name)
    id_ = callback.message.message_id
    print(callback, '\n', id_)
    await changer_data(id_)
    await callback.message.edit_text(
        f"Заказ:\n - {discipline};\n - {type_name}"
    )
    await dp.bot.edit_message_text(
        text=f"Заказ:\n - {discipline};\n - {type_name}",
        chat_id=callback.message.chat.id,
        message_id=id_,
        reply_markup=markup
    )


@rate_limit(limit=4)
@dp.message_handler()
async def start_shopping(message):
    find_target = message.text.strip().upper()
    target = await get_product((obj := find_target))
    if target:
        await get_to_cart(message, target=target, obj=obj)
        print("add_cart\n", message.message_id)
    else:
        await message.answer(text="Нет такой")


@dp.callback_query_handler(menu_cd.filter())
async def navigation(call: types.CallbackQuery, callback_data):
    current_lvl = callback_data.get("level")
    discipline = callback_data.get("discipline")
    ttypy = callback_data.get("type_name")
    levels = {
        "0": get_to_cart,
        "1": buy,
    }
    current_lvl_f = levels[current_lvl]
    await current_lvl_f(call, discipline, ttypy)
