import os
import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from loader import dp
from tg_bot.config import load_config, Config
# from tg_bot.handlers.start_help import register_handler

logger = logging.getLogger(__name__)


def register_all_filters(dp):
    dp.filters_factory.bind()


# def register_all_handlers(dp):
#     register_handler(dp)


logging.basicConfig(
    level=logging.INFO,
    format="|\t%(asctime)s – [%(levelname)s]: %(message)s. " \
           "Исполняемый файл – '%(filename)s': функция – '%(funcName)s'(%(lineno)d)",
)
# config: Config = load_config(".env")
#
# bot: Bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
# storage: MemoryStorage = MemoryStorage()
# dp: Dispatcher = Dispatcher(bot, storage=storage)
# bot['config'] = config

# register_all_handlers(dp)
#
# try:
#     # setup_django()
#     await dp.start_polling()
# finally:
#     await dp.storage.close()
#     await dp.storage.wait_closed()
#     await bot.session.close()


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "django_project.telegrambot.telegrambot.settings"
    )
    os.environ.update(
        {
            "DJANGO_ALLOW_ASYNC_UNSAFE": "true"
        }
    )
    import django
    django.setup()


if __name__ == "__main__":
    setup_django()
    from aiogram import executor
    from tg_bot.handlers import dp
    executor.start_polling(dp)

    # try:
    #     setup_django()
    #     asyncio.run(main())
    # except (KeyboardInterrupt, SystemExit):
    #     logger.error("Bot stopped!")
