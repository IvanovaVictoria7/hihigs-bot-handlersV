import logging
from aiogram import types, Router
from aiogram.filters import Command
from sqlalchemy import select, insert
from db import async_session, User, Profile, Task, Subscription
from .keyboard import keyboard_start

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
        elif user.subscribe:
            query = select(User).where(User.tutorcode == user.subscribe)
            result = await session.execute(query)
            tutor = result.scalar()
            tutor_name = tutor.user_name if tutor else "Неизвестно"
            info += f"\nПреподаватель: {tutor_name}"
        info += "\n\nЧтобы загрузить Codewars-профили, используйте команду:\n/load <url1>, <url2>, ..."

        await message.answer(info)
    logging.info(f"Статус для {message.from_user.id}")


@router.message(Command("load"))
async def command_load_handler(message: types.Message):
    async with async_session() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()

        if not user:
            await message.answer("Вы не зарегистрированы. Сначала введите /start")
            return

        text = message.text.replace("/load", "").strip()
        urls = [url.strip() for url in text.split(",") if url.strip()]

        if not urls:
            await message.answer("Пожалуйста, укажите хотя бы один URL профиля через запятую.")
            return

        existing_query = select(Profile.profile_url).where(Profile.user_id == user.user_id)
        existing_result = await session.execute(existing_query)
        existing_urls = set(row[0] for row in existing_result.all())

        new_profiles = [
            Profile(user_id=user.user_id, profile_url=url)
            for url in urls if url not in existing_urls
        ]

        if not new_profiles:
            await message.answer("Эти профили уже были добавлены ранее.")
            return

        session.add_all(new_profiles)
        await session.commit()
        await message.answer(f" Загружено новых профилей: {len(new_profiles)}")


@router.message(Command("getres"))
async def command_getres_handler(message: types.Message):
    async with async_session() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()

        if not user or not user.tutorcode:
            await message.answer("Эта команда доступна только преподавателям.")
            return

        subs = await session.execute(
            select(Subscription.student_id).where(Subscription.teacher_id == user.user_id)
        )
        student_ids = [row[0] for row in subs.all()]
        if not student_ids:
            await message.answer("У вас нет зарегистрированных студентов.")
            return

        profiles = await session.execute(
            select(Profile.id).where(Profile.user_id.in_(student_ids))
        )
        profile_ids = [row[0] for row in profiles.all()]
        if not profile_ids:
            await message.answer("У студентов пока нет загруженных профилей.")
            return

        tasks_query = await session.execute(
            select(Task.task_name).where(Task.profile_id.in_(profile_ids))
        )
        tasks = sorted(set(row[0] for row in tasks_query.all()))

        if not tasks:
            await message.answer("У студентов ещё нет решённых задач.")
        else:
            task_list = "\n".join(f"• {task}" for task in tasks)
            await message.answer(f"Решённые задачи студентов:\n\n{task_list}")

    logging.info(f"Проверка задач по /getres — {message.from_user.id}")

    @router.message(Command("help"))
    async def help_handler(message: types.Message):
        await message.answer(text="Доступные команды:\n"
                                  "/start - Начать\n"
                                  "/help - Справка\n"
                                  "/status - Статус\n"
                                  "/load - Загрузить профили Codewars\n"
                                  "/getres - Задачи студентов (для преподавателей)")

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

    @router.message(lambda message: message.text == "📖 О нас")
    async def about_handler(message: types.Message):
        await message.answer("Это информация о нас!")

    @router.message(lambda message: message.text == "👤 Профиль")
    async def profile_handler(message: types.Message):
        await message.answer(f"Ваш профиль: ID {message.from_user.id}")

    @router.message()
    async def echo_message(message: types.Message):
        logging.debug(f"Пользователь {message.from_user.id} прислал необрабатываемую команду")
        await message.answer("Неизвестная команда. Выведите /help для списка доступных.")

        
