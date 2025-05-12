# version1.0.0
import asyncio
import logging

from aiogram import Bot, Dispatcher,types
from config import TOKEN
from handlers import router as handlers_router,bot_commands
from handlers.callbacks import router as callbacks_router
from handlers.bot_commands import set_my_commands
from utils import setup_logger
from db import async_create_table



async def main():

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Здесь функция для вызова хендлеров из handlers.py
    dp.include_router(handlers_router)
    dp.include_router(callbacks_router)

    # Здесь вызов меню с командами бота
    await set_my_commands(bot)

    # # Установить общий уровень логирования
    logging.basicConfig(level=logging.INFO)

    # запуск логирования
    setup_logger(fname=__name__)

    # Запуск бота в polling-режиме
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(async_create_table())
        asyncio.run(main())
    except(KeyboardInterrupt,SystemExit):
        logging.info("End Script")