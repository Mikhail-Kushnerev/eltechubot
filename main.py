import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tg_bot.config import load_config, Config
from tg_bot.handlers.start_help import register_handler


logger = logging.getLogger(__name__)


def register_all_filters(dp):
    dp.filters_factory.bind()


def register_all_handlers(dp):
    register_handler(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="|\t%(asctime)s – [%(levelname)s]: %(message)s. "\
            "Исполняемый файл – '%(filename)s': функция – '%(funcName)s'(%(lineno)d)",
    )
    config: Config = load_config(".env")

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(bot, storage=storage)
    bot['config'] = config

    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
