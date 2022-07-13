import os

from dotenv import load_dotenv
from dataclasses import dataclass
from environs import Env


load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_ID')

@dataclass
class TgBot:
    token: str
    # admin_ids: List[str]


# @dataclass
# class DbConfig:
#     host: str
#     user: str
#     password: str
#     database: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    # db: DbConfig
    misc: Miscellaneous


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
    )
