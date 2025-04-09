# version1.0.0
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router as handlers_router
from handlers.callbacks import router as callbacks_router
from handlers.bot_commands import set_my_commands
from utils import setup_logger



async def main():

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Здесь функция для вызова хендлеров из handlers.py
    dp.include_router(handlers_router)
    dp.include_router(callbacks_router)

    # Здесь вызов меню с командами бота
    await set_my_commands(bot)

    # # Установить общий уровень логирования
    # logging.basicConfig(level=logging.DEBUG)

    # запуск логирования
    setup_logger(fname=__name__)

    # Запуск бота в polling-режиме
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())