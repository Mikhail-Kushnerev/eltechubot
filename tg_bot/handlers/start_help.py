from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text

from tg_bot.keyboards.reply import menu
from tg_bot.keyboards.inline_keyboards.callback_datas import add_callback
from tg_bot.keyboards.inline_keyboards.inline import continue_keyboard, choice

from loader import dp

from tg_bot.services.db_api.db_commands import add_user, get_product


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
    elif message.text.startswith("/s"):
        user = await add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
        )
        text = "Wellcome " + hbold("студент") + " ту зэ клаб! Ты в БД"
    await message.answer(text)


@dp.message_handler(commands=["menu"])
async def get_menu(message):
    await message.answer("Боты должны работать", reply_markup=menu)


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


@dp.callback_query_handler(text="continue")
async def continue_func(call):
    await call.message.answer('q')
    print(call.data, sep="\n")


@dp.message_handler()
async def get_to_cart(message):
    target = await get_product(message.text.upper())
    if target:
        await message.answer(
            text='\n'.join(
                (
                    "Мои поздравление, мой друг. Такая есть",
                    f" - {target['target'].name};",
                    f" - {target['target'].lektor}.",
                )
            ),
            reply_markup=choice
        )
        await message.answer_document(types.InputFile(target['file']))
        # await dp.bot.send_document(
        #     message.from_user.id,
        #     document=target[1],
        # )
    else:
        await message.answer(text="Нет такой")

# def register_handler(dp: Dispatcher):
# dp.register_message_handler(get_help, commands=["start", "help"])
# dp.register_message_handler(get_menu, commands=["menu"])
# dp.register_message_handler(get_item, Text(equals=("Выбор дисциплины",)))
# dp.register_message_handler(get_input)
# dp.register_callback_query_handler(add_item, add_callback.filter(item_name="ss"))
