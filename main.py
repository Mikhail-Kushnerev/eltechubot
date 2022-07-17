import os


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

    from aiogram import executor
    from tg_bot import middlewares
    from tg_bot.handlers import dp

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
    except Exception as error:
        # redis_cli.close()
        raise logger.error(f'ПРОБЛЕМА {error=}! Бот остановлен')
