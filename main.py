# version1.0.0
import asyncio
imrort asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import register_message_handlers, set_my_commands


# тест клавиатур
from handlers.keyboard import main_keyboard

#экземпляр бота
bot = Bot(token="Your Token")
dp = Dispatcher()

7011b75bde5ff449548cf543e19e12742fe9dc75

async def main():
    """
    Основная функция для установки конфигурации бота.
    Для создания бота необходимо получить token в telegram https://t.me/BotFather
    и добавить полученный токен в файл .env
    """

#Бот принимает команды, например /start.
# Создадим хендлер - обработчик сообщений, и будет возвращать сообщение
@dp.message(Command('start'))
async def process_start_command(message):
    await message.answer("Привет!", reply_markup=main_keyboard)

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
7011b75bde5ff449548cf543e19e12742fe9dc75

    # Здесь функция для вызова хендлеров из handlers.py
    register_message_handlers()

    # Здесь вызов меню с командами бота
    set_my_commands

#функция запуска проекта
async def main():
    # Запуск бота в polling-режиме
 7011b75bde5ff449548cf543e19e12742fe9dc75
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())