from aiogram import Dispatcher


async def get_start(message):
    text = "Wellcome, студент, ту зэ клаб! Хотя, это мы сейчас проверим"
    await message.answer(text)


async def get_help(message):
    user = message.chat.username
    text = "Я – суперсекретная разработка ЛЭТИ, созданная для помощи студентам"\
    " магического и электротехнического. Помощь похожа на казино и заключается"\
    " (да, я уважаю то самое легендарное видео. Кто понял, тот понял) в"\
    " следующем:\n- я храню ПОДГОНЫ с 1-го курса по текущий год всех дисциплин,"\
    " которые читались в мои молодые годы;\n- и я готов ими с тобой поделиться," \
    " за небольшой прайс, чтобы хватило на нестыдную шаву ~200-400 руб."\
    " (в студенчистве не наелся)."
    await message.answer(text)


def register_handler(dp: Dispatcher):
    dp.register_message_handler(get_start, commands=["start"])
    dp.register_message_handler(get_help, commands=["help"])
