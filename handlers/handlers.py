__all__ = ["router"]

from aiogram import types, Router,F
from sqlalchemy import select
from db import async_session, User
from .keyboard import get_main_keyboard, get_continue_keyboard, get_role_selection_keyboard
import logging
from aiogram.filters import Command
from .callbacks import router as callback_router

router = Router()

# Объединённый обработчик /start и /status с проверкой пользователя
@router.message(Command(commands=["start", "status"]))
async def start_handler(message: types.Message):
    async with async_session() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)

        if result.scalars().all():
            # Пользователь найден в БД
            await message.answer(
                f"Привет, {message.from_user.full_name}!\nТвой ID: {message.from_user.id}",
                reply_markup=get_main_keyboard()
            )
            logging.info(f"Пользователь с id={message.from_user.id} запустил бота ")
        else:
            # Пользователь не найден — предложить выбрать роль
            await message.answer(
                text="Выберите роль",
                reply_markup=get_role_selection_keyboard()
            )

# Хендлер справки
@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(text="Доступные команды:\n"
                              "/start - Начать\n"
                              "/help - Справка\n"
                              "/status - Статус")

# Кнопка "О нас"
@router.message(lambda message: message.text == "📖 О нас")
async def about_handler(message: types.Message):
    await message.answer("Это информация о нас!")

# Кнопка "Профиль"
@router.message(lambda message: message.text == "👤 Профиль")
async def profile_handler(message: types.Message):
    await message.answer(f"Ваш профиль: ID {message.from_user.id}")

# Хендлер на неизвестные команды
@router.message()
async def echo_message(message: types.Message):
    logging.debug(f"Пользователь с id={message.from_user.id} прислал необрабатываемую команду ")
    await message.answer("Неизвестная команда. Введите /help для списка доступных.")