from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tg_bot.config import load_config, Config


config: Config = load_config(".env")
bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot, storage=storage)
