__all__ = [
    "router",
]

import logging

# TODO - Опишите вызов функций обработчиков через маршрутизацию
# Работа c Router - https://docs.aiogram.dev/en/v3.14.0/dispatcher/router.html
# Пример работы с Router через декораторы @router - https://mastergroosha.github.io/aiogram-3-guide/routers/
# Пример работы с Router через функцию сборщик https://stackoverflow.com/questions/77809738/how-to-connect-a-router-in-aiogram-3-x-x#:~:text=1-,Answer,-Sorted%20by%3A


from aiogram import types, Router
from aiogram.filters import Command
#создание экземпляра объекта Router
router=Router()
@router.message(Command(commands=["start", "status"]))
async def start_handler(message: types.Message):
    #print("Команда /start вызвана") #отладочный ввод
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Твой ID: {message.from_user.id}")
    logging.info(f"Пользователь с id={message.from_user.id} запустил бота ")


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(text="Доступные команды:\n"
                         "/start - Начать\n"
                         "/help - Справка\n"
                         "/status - Статус")
@router.message()
async def echo_message(message:types.Message):
    logging.debug(f"Пользователь с id={message.from_user.id} прислал необрабатываемую команду ")
    await message.answer("Неизвестная команда.Выведите /help для списка доступных")


# @router.message(Command("status"))
# async def status_handler(message: types.Message):
#     await message.answer(f"Ваш ID: {message.from_user.id}\n"
#                          f"Ваш username: @{message.from_user.username}")
from aiogram.filters import Command
from .keyboard import keyboard  # импорт из клавиатур
from .callbacks import callback_message  # импорт из коллбека





# Здесь описывается маршрутизация

def register_message_handlers():
    """''Маршрутизация обработчиков''"""
    pass
