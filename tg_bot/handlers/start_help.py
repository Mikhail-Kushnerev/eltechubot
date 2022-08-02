import os

from aiogram import types
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

from tg_bot.keyboards.reply import pay_button
from tg_bot.misc.logger import logger

from loader import dp
from tg_bot.services.db_api.db_commands import add_user


load_dotenv()

# @rate_limit(limit=5, key="/start")
@dp.message_handler(commands=["start", "help"])
async def get_help(message: types.Message):
    if message.text.startswith("/h"):
        user: str = nick if (nick := message.chat.username) is not None else message.chat.first_name
        answer_text: str = "\n".join(
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
        )
    elif message.text.startswith("/st"):
        answer_text: str = await add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    await message.answer(
        text=answer_text,
        reply_markup=pay_button
    )


@dp.message_handler(commands="donats")
async def donat(message):
    text: str = "Поддержать проект чеканной монетой"
    markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    markup.insert(types.InlineKeyboardButton(
            text="Сбор средств",
            url=os.getenv("DONATE_URL")
        )
    )
    await message.answer(
        text=text,
        reply_markup=markup
    )
