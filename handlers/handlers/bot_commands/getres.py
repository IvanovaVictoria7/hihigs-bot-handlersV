from aiogram import Router, types
from aiogram.filters import Command
from db import async_session, Profile, Task, User
from sqlalchemy import select
import logging

router = Router()

@router.message(Command("getres"))
async def get_results_handler(message: types.Message):
    async with async_session() as session:
        # Проверяем регистрацию пользователя
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            await message.answer("Вы не зарегистрированы. Пожалуйста, используйте /start")
            return

        # Получаем профили пользователя
        query = select(Profile).where(Profile.user_id == user.user_id)
        result = await session.execute(query)
        profiles = result.scalars().all()
        if not profiles:
            await message.answer("Профили не загружены. Используйте /load для загрузки профилей.")
            return

        tasks_set = set()
        # Собираем все задачи по профилям
        for profile in profiles:
            query = select(Task).where(Task.profile_id == profile.id)
            result = await session.execute(query)
            tasks = result.scalars().all()
            for task in tasks:
                tasks_set.add(task.task_name)

        if tasks_set:
            tasks_list = "\n".join(tasks_set)
            await message.answer(f"Список пройденных задач:\n{tasks_list}")
        else:
            await message.answer("Пока нет данных о пройденных задачах.")
    logging.info(f"Пользователь {message.from_user.id} запросил результаты")