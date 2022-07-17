import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from loader import dp
from tg_bot.config import load_config, Config


# def register_all_handlers(dp):
#     register_handler(dp)


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


# async def on_startup(dispatcher):
#     await on_startup_notify


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
    from tg_bot.misc.logger import logger

    try:
        setup_django()
        logger.info('Django активирован')
    except Exception:
        raise logger.error('проблемы с установкой Django')

    # import redis, os
    from dotenv import load_dotenv

    from aiogram import executor
    from tg_bot import middlewares
    from tg_bot.handlers import dp

    # load_dotenv()

    # print()

    try:
        logger.info('Бот работает')
        # redis_cli = redis.Redis(
        #     host='localhost',
        #     port=6379,
        #     db=0
        # )
        # print(redis_cli.set(name="test_key", value=10))
        middlewares.setup(dp)
        executor.start_polling(dp, skip_updates=True)
    except Exception:
        # redis_cli.close()
        raise logger.error('ПРОБЛЕМА! Бот остановлен')
