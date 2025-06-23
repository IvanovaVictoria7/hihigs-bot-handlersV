import logging

import Update
from aiogram import types, Router
from aiogram.filters import Command
from sqlalchemy import select, insert
from .keyboard import keyboard_start
from db import async_session, User
from utils.logging import logger

router = Router()

@router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message):
    async with async_session() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()
        if user:
            await message.answer("Вы уже зарегистрированы! Проверьте статус: /status")
        else:
            await message.answer("Выберите роль:", reply_markup=keyboard_start)
    logging.info(f"Пользователь {message.from_user.id} запустил бота")

@router.message(Command(commands=["status"]))
async def command_status_handler(message: types.Message):
    async with async_session() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            await message.answer("Вы не зарегистрированы. Нажмите /start")
            return
        info = f"UserId: {user.user_id}\nUserName: {user.user_name}"
        if user.tutorcode:
            info += f"\nКод преподавателя: {user.tutorcode}"
            info += "\n\nВведите /load чтобы загрузить Codewars-профили студентов."
        elif user.subscribe:
            query = select(User).where(User.tutorcode == user.subscribe)
            result = await session.execute(query)
            tutor = result.scalar()
            tutor_name = tutor.user_name if tutor else "Неизвестно"
            info += f"\nПреподаватель: {tutor_name}"
        await message.answer(info)
    logging.info(f"Пользователь {message.from_user.id} запросил статус")

@router.message(lambda message: message.text.startswith("tutorcode-"))
async def handle_tutorcode_input(message: types.Message):
    async with async_session() as session:
        code = message.text.split("-")[1]
        new_user = {
            "user_id": message.from_user.id,
            "user_name": message.from_user.username or "Unknown",
            "subscribe": code
        }
        await session.execute(insert(User).values(**new_user))
        await session.commit()
        await message.answer("Вы зарегистрированы как слушатель! Проверьте статус: /status")
    logging.info(f"Пользователь {message.from_user.id} зарегистрирован как слушатель")

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(text="Доступные команды:\n"
                         "/start - Начать\n"
                         "/help - Справка\n"
                         "/status - Статус")

@router.message(lambda message: message.text == "📖 О нас")
async def about_handler(message: types.Message):
    await message.answer("Это информация о нас!")

@router.message(lambda message: message.text == "👤 Профиль")
async def profile_handler(message: types.Message):
    await message.answer(f"Ваш профиль: ID {message.from_user.id}")

@router.message()
async def echo_message(message:types.Message):
    logging.debug(f"Пользователь с id={message.from_user.id} прислал необрабатываемую команду ")
    await message.answer("Неизвестная команда.Выведите /help для списка доступных")