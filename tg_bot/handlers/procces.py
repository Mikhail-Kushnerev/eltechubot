import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback
from tg_bot.keyboards.inline_keyboards.inline import continue_keyboard
from tg_bot.keyboards.inline_keyboards.menu import (
    type_keyboard,
    next_answ,
    menu_cd,
    choice
)
from tg_bot.misc import rate_limit
from tg_bot.misc.logger import logger
from tg_bot.services.db_api.db_commands import get_product
from tg_bot.services.redis_db_cache import write_data, changer_data, checker, CACHE


@rate_limit(limit=4)
@dp.message_handler()
async def start_shopping(message):
    await dp.bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    find_target = message.text.strip().upper()
    target = await get_product(find_target)
    if target:
        await make_choice(message, target=target, obj=find_target)
        print("add_cart\n", message.message_id)
    else:
        await message.answer(text="Нет такой")



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
    print(call, call.message.text.split(" - ")[-1], sep="\n")
    await call.answer('Добавлено в корзину', )


@dp.callback_query_handler(text="info")
async def info_answer(callback: types.CallbackQuery):
    await callback.answer(
        text="@yandex"
    )


async def buy(callback: types.CallbackQuery, discipline, type_name):
    print(callback)
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


async def make_choice(message, *args, **kwargs):

    if isinstance(message, types.Message):
        way = await checker(
            (obj := kwargs['target']["target"].name.upper()),
            message.from_user.id
        )
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
                name=obj
            )
            markup = await choice(obj)
            print(obj)
            await message.answer(
                text='\n'.join(
                    (
                        "Мои поздравление, мой друг. Такая есть5",
                        f" - {obj};",
                        # f" - {kwargs['target']['target'].lektor}.",
                    )
                ),
                reply_markup=markup
            )
        else:
            await message.answer('Уже добавлено')
            logger.info('Повторяющийся товар. Сработал Redis')
            time.sleep(2)
            await dp.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id + 1
            )
        print('--------------------------------------------------')
    else:
        logger.info('Отмена выбора. Сработал Callback')
        call = message
        markup = await choice(call.data.split(":")[2])
        await dp.bot.edit_message_text(
            text=call.message.text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
        print('--------------------------------------------------')


async def get_to_cart(callback: types.CallbackQuery, discipline, *args):
    print(discipline)
    logger.info(callback)
    markup = await type_keyboard(discipline)
    await dp.bot.edit_message_text(
        text='\n'.join(
            (
                "Мои поздравление, мой друг. Такая есть!",
                f" - {discipline};",
                # f" - {kwargs['target']['target'].lektor}.",
            )
        ),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=markup
    )
    # await callback.message.edit_text(
    #     text='\n'.join(
    #         (
    #             "Мои поздравление, мой друг. Такая есть!",
    #             f" - {discipline};",
    #             # f" - {kwargs['target']['target'].lektor}.",
    #         )
    #     ),
    #     reply_markup=markup
    # )


@dp.callback_query_handler(menu_cd.filter())
async def navigation(call: types.CallbackQuery, callback_data):
    logger.info(callback_data)
    current_lvl = callback_data.get("level")
    discipline = callback_data.get("discipline")
    ttypy = callback_data.get("type_name")
    levels = {
        "0": make_choice,
        "1": get_to_cart,
        "2": buy,
    }
    current_lvl_f = levels[current_lvl]
    await current_lvl_f(call, discipline, ttypy)
