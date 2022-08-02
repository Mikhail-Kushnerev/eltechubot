import redis
import os

from aiogram import Bot
from aiogram import Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv
from yoomoney import Client, Quickpay

from tg_bot.config import load_config, Config, TOKEN_YOOMONEY


load_dotenv()

redis_cli = redis.Redis(
    # host='localhost',
    # port=6379,
    # db=0
)

config: Config = load_config(".env")
bot: Bot = Bot(
    token=config.tg_bot.token,
    parse_mode="HTML"
)
storage: RedisStorage2 = RedisStorage2(
    # host=os.getenv('REDIS_HOST'),
    # port=int(os.getenv('REDIS_PORT')),
    # db=0
)
dp: Dispatcher = Dispatcher(bot, storage=storage)

client: Client = Client(TOKEN_YOOMONEY)
