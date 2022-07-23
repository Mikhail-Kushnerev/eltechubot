import json
import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import redis_cli
from tg_bot.keyboards.inline_keyboards.menu import (
    type_keyboard,
    next_answ,
    menu_cd
)
from tg_bot.misc.logger import logger
from tg_bot.services.redis_db_cache import write_data, changer_data, CACHE, checker
from tg_bot.services.db_api.db_commands import get_product, add_to_cart
from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback
from tg_bot.keyboards.inline_keyboards.inline import continue_keyboard
from loader import dp
from tg_bot.misc import rate_limit


@dp.callback_query_handler(add_callback.filter(item_name="ss"))
async def add_item(call: types.CallbackQuery, callback_data, state: FSMContext):
    id_ = call.message.message_id - 1
    person = call.from_user.id
    print(CACHE)
    await dp.bot.edit_message_text(
        text='Ждёт оплаты:\n'
             f"{CACHE[person][id_][1]} {call.message.text.split(' - ')[-1]}",
        chat_id=call.message.chat.id,
        message_id=CACHE[person][id_][0][0],
        reply_markup=continue_keyboard
    )
    q = await add_to_cart(
        2,
        1
    )
    print(q)
    await call.answer('Добавлено в корзину', )
# except Exception:
#     await call.message.edit_text(
#         text="сломал бота, типичный ЛЭТИ'шник...\nПиши запрос заново :D",
#         # reply_markup=""
#     )


async def get_to_cart(message, *args, **kwargs):
    print('--------------------------------------------------')
    if isinstance(message, types.Message):
        way = await checker(kwargs['target']["target"].name, message.from_user.id)
        logger.info(
            'Полeчено сообщение\n'
            f'{message}'
        )
        if way:
            id_ = message.message_id
            logger.info('Сообщение добавлено в кэш пользователя')
            user_id = message.from_id
            await write_data(
                user_id=user_id,
                id_=id_,
                name=kwargs['target']["target"].name
            )
            markup = await type_keyboard(kwargs["obj"])
            print(CACHE)
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
            await message.answer('Уже добавлено')
            logger.info('Повторяющийся товар. Сработал Redis')
            time.sleep(3)
            await dp.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id + 1
            )
        print('--------------------------------------------------')
    else:
        logger.info('Отмена выбора. Сработал Callback')
        call = message
        inline_text = call.message.text.split()[2][:-1]
        markup = await type_keyboard(inline_text)
        await dp.bot.edit_message_text(
            text=call.message.text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
        print('--------------------------------------------------')


async def buy(callback: types.CallbackQuery, discipline, type_name):
    markup = next_answ(discipline, type_name)
    person = callback.from_user.id
    id_ = callback.message.message_id
    print(callback, '\n', id_, person)
    await changer_data(id_, person)
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
    await dp.bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
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
