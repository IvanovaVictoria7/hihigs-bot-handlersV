# version1.0.0
import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router, set_my_commands
from handlers import setup_logger
from handlers import register_message_handlers, set_my_commands
from utils import setup_logger


async def main():
# установка логирования по умолчанию
#logging.basicConfig(level=logging.INFO)


    """
    Основная функция для установки конфигурации бота.
    Для создания бота необходимо получить token в telegram https://t.me/BotFather
    и добавить полученный токен в файл .env
    """

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Здесь функция для вызова хендлеров из handlers.py
    dp.include_routers(router)

    # Здесь вызов меню с командами бота
    set_my_commands

    # # Установить общий уровень логирования
    # logging.basicConfig(level=logging.DEBUG)

    # запуск логирования
    setup_logger(fname=__name__)

    # Запуск бота в polling-режиме
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())