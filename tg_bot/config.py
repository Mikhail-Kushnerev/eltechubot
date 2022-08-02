import os

from dotenv import load_dotenv
from dataclasses import dataclass
from environs import Env


load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_ID')

TOKEN_YOOMONEY = os.getenv('TOKEN_YOOMONEY')

@dataclass
class TgBot:
    token: str
    # admin_ids: List[str]


@dataclass
class Redis:
    host: str
    port: int
    # user: str
    # password: str
    database: int


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    # db: DbConfig
    misc: Miscellaneous
    # redis: Redis


def load_config(path: str):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('TELEGRAM_BOT_ID')
        ),
        # db=DbConfig(
        #     host=env.str('DB_HOST'),
        #     user=env.str('POSTGRES_USERNAME'),
        #     password=env.str('POSTGRES_PASSWORD'),
        #     database=env.str('DB_NAME'),
        # ),
        misc=Miscellaneous(),
        # redis=Redis(
        #     host=env['REDIS_HOST'],
        #     port=env['REDIS_PORT'],
        #     database=env['REDIS_DB']
        # )
    )
