import logging


logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    format="|\t%(asctime)s – [%(levelname)s]: %(message)s. "
           "Исполняемый файл – '%(filename)s': функция – '%(funcName)s'(%(lineno)d)",
)
logger = logging.getLogger(__name__)
