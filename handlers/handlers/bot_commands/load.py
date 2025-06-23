from aiogram import Router, types
from aiogram.filters import Command
from db import async_session, Profile, User
from sqlalchemy import select, insert
import logging

router = Router()

@router.message(Command("load"))
async def load_profiles_handler(message: types.Message):
    # Проверяем, что пользователь зарегистрирован и является преподавателем
    async with async_session() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            await message.answer("Вы не зарегистрированы. Пожалуйста, используйте /start")
            return

        if not user.tutorcode:
            await message.answer("Команда доступна только преподавателям.")
            return

    await message.answer("Отправьте список Codewars-профилей через запятую (например:\nhttps://www.codewars.com/users/user1,https://www.codewars.com/users/user2)")

    # Далее нужно добавить обработчик следующего сообщения с профилями,
    # чтобы сохранить их в базу. Можно использовать FSM или временно сохранять состояние.

# Для простоты пример с ожиданием следующего сообщения — добавь такой обработчик:

@router.message()
async def receive_profiles(message: types.Message):
    urls = message.text.split(",")
    async with async_session() as session:
        for url in urls:
            url = url.strip()
            # Проверяем, есть ли уже такой профиль для пользователя
            query = select(Profile).where(Profile.profile_url == url)
            result = await session.execute(query)
            existing_profile = result.scalar()
            if not existing_profile:
                # Добавляем профиль, привязанный к пользователю
                new_profile = Profile(user_id=message.from_user.id, profile_url=url)
                session.add(new_profile)
        await session.commit()
    await message.answer(f"Загружено {len(urls)} профилей.")
    logging.info(f"Пользователь {message.from_user.id} загрузил профили: {urls}")