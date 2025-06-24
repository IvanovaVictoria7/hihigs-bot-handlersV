# version 1.0.0
import asyncio
import logging
from os import name

from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router as handlers_router
from handlers.callbacks import router as callbacks_router
from handlers.bot_commands import set_my_commands
from utils.logging import setup_logger  #  импорт логгера
from db import async_create_table


async def main():
    setup_logger()  #  логгер нужно вызывать до запуска

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем все хендлеры
    dp.include_router(handlers_router)
    dp.include_router(callbacks_router)

    # Устанавливаем команды бота
    await set_my_commands(bot)

    # Запускаем бота
    await dp.start_polling(bot)


if name == "__main__":  #  исправлено с name → name
    asyncio.run(async_create_table())  # создаём таблицы в БД
    asyncio.run(main())
    logging.info("Бот остановлен")

from telegram.ext import Updater
from handlers import setup_handlers


def main() -> None:
    updater = Updater("7706411868:AAEjg7NEHAqryZ3xPNaSKMFUmU2smFIlv1Y")

    setup_handlers(updater)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()