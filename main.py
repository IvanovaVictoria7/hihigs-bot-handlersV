# version1.0.0
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router, set_my_commands


async def main():
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

    # Запуск бота в polling-режиме
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())