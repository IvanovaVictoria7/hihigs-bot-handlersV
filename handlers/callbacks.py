import logging
import string
from random import choices
from aiogram import Router, types
from sqlalchemy import insert
from db import User, async_session

router = Router()

#  Кнопка: Преподаватель
@router.callback_query(lambda c: c.data == "button_tutor")
async def callback_start_tutor(callback: types.CallbackQuery):
    logging.info(f"Пользователь {callback.from_user.id} выбрал преподавателя")

    async with async_session() as session:
        tutor_code = "".join(choices(string.ascii_letters + string.digits, k=6))
        new_user = {
            "user_id": callback.from_user.id,
            "user_name": callback.from_user.username or "Unknown",
            "role": "teacher",
            "extra": None
        }
        await session.execute(insert(User).values(**new_user))
        await session.commit()

    await callback.message.answer(
        f"Вы зарегистрированы как преподаватель!\n"
        f"Код для студентов: tutorcode-{tutor_code}\n\n"
        f"Проверьте статус: /status"
    )
    await callback.answer()

# Кнопка: Студент
@router.callback_query(lambda c: c.data == "button_student")
async def callback_start_student(callback: types.CallbackQuery):
    logging.info(f"Пользователь {callback.from_user.id} выбрал студента")
    await callback.message.answer("Введите код преподавателя (в формате tutorcode-XXXXXX):")
    await callback.answer()

# Обработка сообщения от студента с кодом
@router.message(lambda m: m.text and m.text.startswith("tutorcode-"))
async def handle_student_registration(message: types.Message):
    tutor_code = message.text.replace("tutorcode-", "").strip()

    async with async_session() as session:
        new_user = {
            "user_id": message.from_user.id,
            "user_name": message.from_user.username or "Unknown",
            "role": "student",
            "extra": None
        }

        await session.execute(insert(User).values(**new_user))
        await session.commit()

    await message.answer("Вы зарегистрированы как студент! Проверьте статус: /status")
    logging.info(f"Пользователь {message.from_user.username} зарегистрирован как студент с кодом {tutor_code}")

#  Пример: кнопка нажата
@router.callback_query(lambda c: c.data == "button_pressed")
async def handle_button_press(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text("Вы нажали кнопку!")