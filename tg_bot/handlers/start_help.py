from aiogram import types
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text

from tg_bot.keyboards.reply import pay_button
from tg_bot.misc.logger import logger

from loader import dp
from tg_bot.misc import rate_limit
from tg_bot.services.db_api.db_commands import add_user


@rate_limit(limit=5, key="/start")
@dp.message_handler(commands=["start", "help"])
async def get_help(message: types.Message):
    if message.text.startswith("/h"):
        user: str = message.chat.username
        text: str = "\n".join(
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
        logger.info(
            'Польователь отправил команду help. Сообщение получено',
            # f'{middleware_data}'
        )
        # logger.error('Польователь отправил команду help. Сообщение НЕ получено')
    elif message.text.startswith("/st"):
        user = await add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        text: str = "Wellcome " + hbold("студент") + " ту зэ клаб! Ты в БД"
    await message.answer(
        text,
        reply_markup=pay_button
    )


@dp.message_handler(Text(equals=("Выбор дисциплины",)))
async def get_item(message):
    await message.answer("Введи интересующую тебя дисциплину. Возможно, она у меня есть")
