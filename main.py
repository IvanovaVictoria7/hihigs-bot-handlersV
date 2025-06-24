# version 1.0.0
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router as handlers_router
from handlers.callbacks import router as callbacks_router
from handlers.bot_commands import set_my_commands
from utils import setup_logger
from db import async_create_table

async def main():
    setup_logger()  # ← логгер нужно запускать перед всем, чтобы ловить ошибки

    await async_create_table()  # создаём таблицы в БД

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем хендлеры
    dp.include_router(handlers_router)
    dp.include_router(callbacks_router)

    # Команды бота (меню)
    await set_my_commands(bot)

    # Запуск бота
    logging.info("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")