from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from tg_bot.services.db_api.db_commands import get_student
from tg_bot.misc.logger import logger


class DbMan(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data):
        data["middleware_data"] = 'middle'
        logger.info(data)
        if update.message:
            user = update.message.from_user.id
        else:
            return

        if get_student(user) is False:
            return CancelHandler()

    async def on_process_message(self, update: types.Update, data):
        data["middleware_data"] = 'q'
        logger.info(data)

    async def on_pre_process_message(self, message: types.Message, data):
        data["middleware_data"] = 'q'
        logger.info(data)
