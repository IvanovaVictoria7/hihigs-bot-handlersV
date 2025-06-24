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


from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from bs4 import BeautifulSoup
import re

# Хранение данных (временное, лучше использовать БД)
users = {}  # {user_id: {'subscribed': bool, 'profiles': list}}
checked_tasks = {}  # {profile_url: set(task_ids)}


# 1. Обработчик /start
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {'subscribed': False, 'profiles': []}
    update.message.reply_text(
        "Добро пожаловать! Я бот для проверки задач Codewars.\n"
        "Используйте /status для просмотра статуса."
    )


# 2. Обработчик /status
def status(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in users:
        update.message.reply_text("Вы не зарегистрированы. Используйте /start")
        return

    status_text = "Ваш статус:\n"
    status_text += f"Подписка: {'активна' if users[user_id]['subscribed'] else 'не активна'}\n"
    status_text += f"Загружено профилей: {len(users[user_id]['profiles'])}\n"
    status_text += "Используйте /load для загрузки профилей"

    update.message.reply_text(status_text)


# 3. Обработчик /load
def load(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in users:
        update.message.reply_text("Сначала зарегистрируйтесь с помощью /start")
        return

    if not context.args:
        update.message.reply_text(
            "Укажите профили через запятую. Пример:\n/load https://codewars.com/users/user1,https://codewars.com/users/user2")
        return

    profiles = [p.strip() for p in " ".join(context.args).split(",")]
    users[user_id]['profiles'] = profiles

    # Инициализация хранилища для задач
    for profile in profiles:
        if profile not in checked_tasks:
            checked_tasks[profile] = set()

    update.message.reply_text(f"Загружено {len(profiles)} профилей. Используйте /getres для проверки задач.")


# 4. Обработчик /getres
def getres(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in users or not users[user_id]['profiles']:
        update.message.reply_text("Сначала загрузите профили с помощью /load")
        return

    all_tasks = set()

    for profile in users[user_id]['profiles']:
        try:
            # Получаем HTML страницы профиля
            response = requests.get(profile)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Ищем задачи (пример селектора, может потребоваться адаптация)
            tasks = soup.select('.problem-title a')
            new_tasks = set()

            for task in tasks:
                task_id = task['href'].split('/')[-1]
                if task_id not in checked_tasks[profile]:
                    new_tasks.add(task_id)

            # Обновляем список проверенных задач
            checked_tasks[profile].update(new_tasks)
            all_tasks.update(new_tasks)

        except Exception as e:
            update.message.reply_text(f"Ошибка при обработке профиля {profile}: {str(e)}")

    if all_tasks:
        tasks_list = "\n".join(f"- {task_id}" for task_id in all_tasks)
        update.message.reply_text(f"Новые решенные задачи:\n{tasks_list}")

        # 5. Уведомление подписчиков
        notify_subscribers(update, context, f"Проверены новые задачи Codewars:\n{tasks_list}")
    else:
        update.message.reply_text("Новых решенных задач не найдено.")


def notify_subscribers(update: Update, context: CallbackContext, message: str) -> None:
    for user_id, user_data in users.items():
        if user_data['subscribed'] and user_id != update.effective_user.id:
            context.bot.send_message(user_id, message)


def setup_handlers(updater: Updater) -> None:
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("load", load))
    dp.add_handler(CommandHandler("getres", getres))