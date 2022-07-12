from aiogram import Dispatcher
from aiogram.utils.markdown import hbold


async def get_help(message):
    print(message.to_python())
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
        text = "Wellcome " + hbold("студент") + " ту зэ клаб! Хотя, это мы сейчас проверим"
    await message.answer(text)


def register_handler(dp: Dispatcher):
    dp.register_message_handler(get_help, commands=["start", "help"])
    # dp.register_message_handler(get_help, commands=["help"])
