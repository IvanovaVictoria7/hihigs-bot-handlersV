import logging
import string
from random import choices
from aiogram import Router, types
from sqlalchemy import insert
from db import User, async_session


router = Router()

@router.callback_query(lambda c: c.data == "button_pressed")
async def handle_button_press(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Подтверждаем нажатие
    await callback_query.message.edit_text("Вы нажали кнопку!")

@router.callback_query(lambda c: c.data.endswith("_tutor"))
async def callback_start_tutor(callback: types.CallbackQuery):
    """Регистрация преподавателя"""
    async with async_session() as session:
        # Генерация случайного tutorcode
        chars = string.ascii_letters + string.digits + string.punctuation
        tutor_code = "".join(choices(chars, k=6))

        new_user = {
            "user_id": callback.from_user.id,
            "user_name": callback.from_user.full_name or callback.from_user.username or "Unknown",
            "tutorcode": tutor_code,
            "subscribe": None,
            "extra": None
        }

        insert_query = insert(User).values(**new_user)
        await session.execute(insert_query)
        await session.commit()

    await callback.answer()
    await callback.message.answer("Вы зарегистрированы как преподаватель!")
    await callback.message.answer("Чтобы продолжить, вызовите команду /status")
    logging.info(f"Пользователь {callback.from_user.username} добавлен в базу данных с ролью преподаватель!")

async def callback_message(callback: types.CallbackQuery):
    """Ответ на кнопку"""
    await callback.message.answer("Успешно!")
