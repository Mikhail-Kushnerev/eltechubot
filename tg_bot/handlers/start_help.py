from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text

from tg_bot.keyboards.inline_keyboards.menu import type_keyboard, next_answ, menu_cd
from tg_bot.keyboards.reply import menu
from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback
from tg_bot.keyboards.inline_keyboards.inline import continue_keyboard, choice

from loader import dp

from tg_bot.services.db_api.db_commands import add_user, get_product, get_item


@dp.message_handler(commands=["start", "help"])
async def get_help(message):
    if message.text.startswith("/h"):
        user = message.chat.username
        text = "\n".join(
            (
                f"Привет, {hbold(user)}!",
                "Я – суперсекретная разработка ЛЭТИ, созданная для помощи ",
                "студентам магического и электротехнического. Помощь похожа на",
                "казино и заключается (да, я уважаю то самое легендарное видео.",
                " Кто понял, тот понял) в следующем:",
                "- я храню ПОДГОНЫ с 1-го курса по текущий год всех дисциплин,",
                " которые читались в мои молодые годы;",
                "- и я готов ими с тобой поделиться, за небольшой прайс, чтобы",
                " хватило на нестыдную шаву ~200-400 руб."
            )
        )
    elif message.text.startswith("/st"):
        user = await add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
        )
        text = "Wellcome " + hbold("студент") + " ту зэ клаб! Ты в БД"
    await message.answer(text)


# @dp.message_handler(commands=["menu"])
# async def get_menu(message):
#     await message.answer("Боты должны работать", reply_markup=menu)


@dp.message_handler(Text(equals=("Выбор дисциплины",)))
async def get_item(message):
    await message.answer("Введи интересующую тебя дисциплину. Возможно, она у меня есть")


@dp.callback_query_handler(add_callback.filter(item_name="ss"))
async def add_item(call: CallbackQuery, callback_data):
    # await call.answer(cache_time=60)
    quantity = callback_data.get("quantity")
    await call.message.answer(
        f"{quantity}",
        reply_markup=continue_keyboard
    )
    print(call.data, callback_data, sep="\n")


@dp.callback_query_handler(text="Контрольная работа")
async def continue_func(call):
    await call.message.answer('q')
    print(call.data, sep="\n")


@dp.message_handler()
async def start_shopping(message):
    message = message.text.strip().upper()
    target = await get_product((obj := message))
    if target:
        await get_to_cart(message, target=target, obj=obj)
    else:
        await message.answer(text="Нет такой")


async def get_to_cart(message, *args, **kwargs):
    if isinstance(message, types.Message):
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
        text = call.message.text.split()[2][:-1]
        markup = await type_keyboard(text)
        await call.message.edit_text(call.message.text, reply_markup=markup)


async def buy(callback: types.CallbackQuery, discipline, type_name):
    markup = next_answ(discipline, type_name)
    # await get_item(discipline, type_name)
    print(callback)
    await callback.message.edit_text(
        f"Заказ:\n - {discipline};\n - {type_name}"
    )
    await callback.message.edit_reply_markup(markup)


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
