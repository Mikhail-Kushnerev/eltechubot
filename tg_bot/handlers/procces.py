import asyncio
import time
import decimal
import os

from aiogram import types
from aiogram.utils import markdown
from dotenv import load_dotenv
from yoomoney import Quickpay

from loader import dp, redis_cli, client
from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback
from tg_bot.keyboards.inline_keyboards.inline import continue_keyboard
from tg_bot.keyboards.inline_keyboards.menu import (
    type_keyboard,
    next_answ,
    menu_cd,
    choice
)
from tg_bot.keyboards.reply import pay_button
from tg_bot.misc import rate_limit
from tg_bot.misc.logger import logger
from tg_bot.services.db_api.db_commands import (
    get_product,
    packing,
    get_item,
    find_type, info_func, check_price, del_packing, get_purchase_for_pay
)
from tg_bot.services.redis_db_cache import (
    write_data,
    checker,
    CACHE,
    changer_data
)


load_dotenv()

@dp.message_handler(commands="clear")
async def clear_cache(message):
    person: int = message.from_user.id
    redis_cli.delete(person)
    await dp.bot.delete_message(
        chat_id=person,
        message_id=message.message_id
    )
    del_info_msg: types.Message = await dp.bot.send_message(
        text="Кэш очищен!\nВведи запрос заново",
        chat_id=person
    )
    await asyncio.sleep(1.3)
    await dp.bot.delete_message(
        chat_id=person,
        message_id=del_info_msg.message_id
    )


async def delete_item(
        call: types.CallbackQuery
) -> object:
    text: str = call.message.text.split()[3]
    msg: int = call.message.message_id
    person: int = call.from_user.id
    history = CACHE[person]
    cart: dict[int, list[object]] = history["cart"]
    if cart:
        while msg not in cart:
            msg += 1
        product_pos: int = msg
        target: list[object] = cart[product_pos]
        for i in range(len(target)):
            msg: int = call.message.message_id
            while msg not in CACHE[person]:
                msg -= 1
            call_del_product: object = history[msg][0][1]
            if target[i] == call_del_product:
                product: object = await del_packing(person, call_del_product)
                del (target[i], history[msg])
                redis_cli.hdel(person, text.encode())
                await dp.bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id
                )
                return product

    else:
        while msg not in history:
            msg -= 1
        del history[msg]
        redis_cli.hdel(person, text.encode())
        await dp.bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )


@dp.callback_query_handler(text="continue")
@dp.message_handler(text="Оплатить")
@dp.message_handler(commands=("pay",))
async def pay(message: types.Message | types.CallbackQuery):
    person: int = message.from_user.id
    markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    if isinstance(message, types.Message):
        del_list: list[int] = []
        try:
            cart: dict[int | str, list[object] | object] = CACHE[person]["cart"]
            msg_id: int = message.message_id
            cart[msg_id]: list[object] = []

            for i in CACHE[person]:
                match i:
                    case "cart":
                        continue
                    case _:
                        if isinstance(CACHE[person][i][0], tuple):
                            cart[msg_id].append(CACHE[person][i][0][1])
                            del_list.append(i)
            if not cart:
                raise Exception
            purchase: decimal = await packing(person, cart[msg_id])
            text: str = f"Сумма заказа: {purchase.amount}"
        except Exception:
            await dp.bot.delete_message(
                chat_id=message.from_user.id,
                message_id=message.message_id
            )
            msg: types.Message = await message.answer(
                text='Коризна пуста, друг...'
            )
            await asyncio.sleep(2)
            await dp.bot.delete_message(
                chat_id=message.from_user.id,
                message_id=msg.message_id
            )
        else:
            hide_keyboard = types.ReplyKeyboardRemove()
            await message.answer(
                text="Совершить платёж",
                reply_markup=hide_keyboard
            )
            price = await message.answer(text=text)
            CACHE[person].update({"price": price})
    else:
        call: types.CallbackQuery = message
        key: int = CACHE[call.from_user.id]["price"].message_id
        msg: int = call.message.message_id
        while msg != key:
            msg += 1
        product: object = await delete_item(call)
        await dp.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=int(msg),
            text=str(product)
        )
        await call.answer("Удалено")
    obj: object = await get_purchase_for_pay(person)
    if obj.amount != 0:
        quickpay: Quickpay = Quickpay(
            receiver=os.getenv('RECEIVER'),
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="AC",
            sum=obj.amount,
            label=obj.id
        )
        markup.insert(
            types.InlineKeyboardButton(
                text="Совершить платёж",
                url=quickpay.redirected_url

            )
        )
        info_msg: types.Message = await dp.bot.edit_message_text(
            text=obj,
            chat_id=person,
            message_id=CACHE[person]["price"].message_id,
            reply_markup=markup,
        )
        if obj.amount == 0:
            await CACHE[person]["price"].delete()
            await info_msg.delete()
        print(obj.amount)
        print(quickpay.base_url)
        print(quickpay.redirected_url)
        del quickpay

async def check_trans(cart, message, person, del_list, purchase):
    history = client.operation_history(label=purchase)
    if history:
        for i in cart:
            await message.answer_document(types.InputFile(i.doc.path.split("/")[-1]))
        cart.clear()
        target = CACHE[person]
        for i in del_list:
            obj: str = target[i][-1]
            redis_cli.hdel(person, obj.encode())
            await dp.bot.delete_message(
                chat_id=message.from_user.id,
                message_id=target[i][1]
            )
            del target[i]
    else:
        await message.answer(
            text="Платёж не прошёл"
        )


@rate_limit(limit=4)
@dp.message_handler()
async def start_shopping(message: types.Message):
    await dp.bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    find_target: str = message.text.strip().upper()
    target: object = await get_product(find_target)
    if target:
        await make_choice(
            message,
            target=target,
            obj=find_target,
            msg_id=message.message_id
        )
    else:
        del_info_msg: types.Message = await message.answer(text="Нет такой")
        time.sleep(1.7)
        await dp.bot.delete_message(
            chat_id=message.chat.id,
            message_id=del_info_msg.message_id
        )


@dp.callback_query_handler(add_callback.filter(item_name="ss"))
async def add_item(call: types.CallbackQuery, callback_data):
    msg_id: int = call.message.message_id
    person: int = call.from_user.id
    while msg_id not in CACHE[person]:
        msg_id -= 1
    type_name: object = await find_type(type_name=(name_type := call.message.text.split("\n")[-2].split()[-1]))
    product: object = await get_item(
        dis=CACHE[person][msg_id][0],
        type_name=type_name
    )
    text: str = "\n".join(
        (
            "Ждёт оплаты:",
            f"{markdown.hbold('Дисциплина')}: {CACHE[person][msg_id][2]}",
            f"{markdown.hbold('Вид работы')}: {name_type}",
            f"{markdown.hbold('Цена')}: {product.price};",
        )
    )
    await dp.bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=continue_keyboard
    )
    CACHE[person][msg_id][0] = True, product
    await call.answer('Добавлено в корзину', )


@dp.callback_query_handler(text="info")
async def info_answer(callback: types.CallbackQuery):
    person: int = callback.from_user.id
    msg_id: int = callback.message.message_id
    while msg_id not in CACHE[person]:
        msg_id -= 1
    info_consult_msg: str = await info_func(CACHE[person][msg_id][0])
    await callback.answer(
        text=markdown.link("VK\t", info_consult_msg),
        show_alert=True
    )


async def buy(
        callback: types.CallbackQuery,
        discipline: str,
        type_name: str,
        msg_id: int
):
    markup: types.InlineKeyboardMarkup = next_answ(discipline, type_name, msg_id)
    callback_id: int = callback.message.message_id
    person: int = callback.from_user.id
    price: decimal = await check_price(discipline, type_name)
    target: dict[str | int, list[int, str]] = CACHE[person]
    while callback_id not in target:
        callback_id -= 1
    await changer_data(
        int(callback_id),
        callback.from_user.id,
        int(callback.message.message_id)
    )
    text: str = "\n".join(
        (
            f"Товар:",
            f"{markdown.hbold('Дисциплина')}: {discipline};",
            f"{markdown.hbold('Вид работы')}: {type_name}",
            f"{markdown.hbold('Цена')}: {price}",
        )
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=markup
    )


async def make_choice(
        message: types.Message | types.CallbackQuery,
        *args,
        **kwargs
):
    if isinstance(message, types.Message):
        way: bool = await checker(
            (obj := kwargs['target'].name.upper()),
            message.from_user.id
        )
        logger.info(
            'Полeчено сообщение\n'
            f'{message}'
        )
        if way:
            msg_id: int = message.message_id
            logger.info('Сообщение добавлено в кэш пользователя')
            user_id: int = message.from_id
            await write_data(
                user_id=user_id,
                msg_id=msg_id,
                target=kwargs['target'].id,
                name=obj
            )
            markup: types.InlineKeyboardMarkup = await choice(obj, kwargs["msg_id"])
            await message.answer(
                text='\n'.join(
                    (
                        "Мои поздравление, мой друг. Такая есть!",
                        f"Предмет: {obj};",
                        f"Преподаватель: {kwargs['target'].lektor}"
                    )
                ),
                reply_markup=markup
            )
        else:
            text = "\n".join(
                (
                    'Уже добавлено',
                    f'Если это тех. сбой, введи команду - {markdown.hcode("/clear")}'
                )
            )
            del_info_msg: types.Message = await message.answer(text)
            logger.info('Повторяющийся товар. Сработал Redis')
            time.sleep(3)
            await dp.bot.delete_message(
                chat_id=message.chat.id,
                message_id=del_info_msg.message_id
            )
        print('--------------------------------------------------')
    else:
        logger.info('Отмена выбора. Сработал Callback')
        call: types.CallbackQuery = message
        person: int = call.message.chat.id
        msg_id: int = call.message.message_id
        while msg_id not in CACHE[person]:
            msg_id -= 1
        markup: types.InlineKeyboardMarkup = await choice(
            call.data.split(":")[2],
            msg_id
        )
        await dp.bot.edit_message_text(
            text=call.message.text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
        print('--------------------------------------------------')


async def get_to_cart(
        callback: types.CallbackQuery,
        discipline: str,
        ttype,
        msg_id: int
):
    logger.info(callback)
    markup: types.InlineKeyboardMarkup = await type_keyboard(
        discipline,
        msg_id
    )
    await dp.bot.edit_message_text(
        text='\n'.join(
            (
                "Мои поздравление, мой друг. Такая есть!",
                f"\t{markdown.hbold('Дисциплина')}: {discipline};",
                f"\t{markdown.hbold('Лектор')}: {discipline};",
                # f" - {kwargs['target']['target'].lektor}.",
            )
        ),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=markup
    )


@dp.callback_query_handler(menu_cd.filter())
async def navigation(call: types.CallbackQuery, callback_data):
    logger.info(callback_data)
    current_lvl: int = callback_data.get("level")
    discipline: str = callback_data.get("discipline")
    ttypy: str = callback_data.get("type_name")
    msg_id: int = callback_data.get("msg_id")
    levels = {
        "0": make_choice,
        "1": get_to_cart,
        "2": buy,
    }
    current_lvl_func = levels[current_lvl]
    await current_lvl_func(call, discipline, ttypy, msg_id)
