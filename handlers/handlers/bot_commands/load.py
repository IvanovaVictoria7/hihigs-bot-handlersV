import logging
from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import delete, select
from db import async_session
from db.models import User, Profile
from bs4 import BeautifulSoup
import requests

router = Router()

@router.message(Command("load"))
async def load_profiles_handler(message: types.Message):
    async with async_session() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()

        if not user or not user.tutorcode:
            await message.answer("Команда доступна только преподавателям.")
            return

        await message.answer("Отправьте список профилей Codewars через запятую:\n"
                             "`https://www.codewars.com/users/user1,https://www.codewars.com/users/user2`")

        # Ждём следующее сообщение с профилями
        @router.message()
        async def process_profile_links(msg: types.Message):
            urls = [url.strip() for url in msg.text.split(",")]
            if not all("codewars.com/users/" in url for url in urls):
                await msg.answer("Некорректный формат ссылок. Повторите попытку.")
                return

            # Удалим старые профили преподавателя
            await session.execute(delete(Profile).where(Profile.user_id == user.user_id))
            await session.commit()

            # Добавим новые профили
            created = 0
            for url in urls:
                try:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Простая проверка, что профиль существует
                    if soup.title and "404" not in soup.title.text:
                        new_profile = Profile(user_id=user.user_id, profile_url=url)
                        session.add(new_profile)
                        created += 1
                except Exception as e:
                    logging.warning(f"Ошибка при обработке профиля {url}: {e}")
                    continue

            await session.commit()
            await msg.answer(f"Загружено профилей: {created}")

            # Уведомим подписчиков
            students_query = select(User).where(User.subscribe == user.tutorcode)
            students_result = await session.execute(students_query)
            students = students_result.scalars().all()

            for student in students:
                try:
                    await msg.bot.send_message(student.user_id, "Ваши задачи на Codewars были проверены преподавателем.")
                except Exception as e:
                    logging.warning(f"Не удалось уведомить {student.user_id}: {e}")

            logging.info(f"{message.from_user.id} загрузил {created} профилей.")