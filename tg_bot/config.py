from typing import List
from dataclasses import dataclass

from environs import Env

@dataclass
class TgBot:
    token: str
    # admin_ids: List[str]


@dataclass
class DbConfig:
    host: str
    user: str
    password: str
    database: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: str
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('5590707713:AAEzGab1K21piH0Ayfixih0ReuYohTanjXI')
        )
    )