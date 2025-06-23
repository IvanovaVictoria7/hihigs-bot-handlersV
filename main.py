# version 1.0.0
import asyncio
import logging
import sys
from os import name as os_name

from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router as handlers_router
from handlers.callbacks import router as callbacks_router
from handlers.bot_commands import set_my_commands
from utils.logging import setup_logger
from db import async_create_table


async def main():
    setup_logger()
    # Создание таблиц (вызывается один раз)
    await async_create_table()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем все хендлеры
    dp.include_router(handlers_router)
    dp.include_router(callbacks_router)

    # Устанавливаем команды бота
    await set_my_commands(bot)

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        sys.exit(1)