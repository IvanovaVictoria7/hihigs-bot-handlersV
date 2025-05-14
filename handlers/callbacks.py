import logging
import string
from random import choices
from aiogram import Router, types
from sqlalchemy import insert
from db import User, async_session

router = Router()

@router.callback_query(lambda c: c.data == "button_tutor")
async def callback_start_tutor(callback: types.CallbackQuery):
    logging.info(f"Пользователь {callback.from_user.id} выбрал преподавателя")
    async with async_session() as session:
        new_user = {
            "user_id": callback.from_user.id,
            "user_name": callback.from_user.username or "Unknown",
            "tutorcode": "".join(choices(string.ascii_letters + string.digits, k=6))
        }
        await session.execute(insert(User).values(**new_user))
        await session.commit()
    await callback.message.answer("Вы зарегистрированы как преподаватель! Проверьте статус: /status")
    await callback.answer()

@router.callback_query(lambda c: c.data == "button_student")
async def callback_start_student(callback: types.CallbackQuery):
    logging.info(f"Пользователь {callback.from_user.id} выбрал слушателя")
    await callback.message.answer("Введите код преподавателя (в формате tutorcode-CODE):")

async def start_student(message):
        """Регистрация слушателя"""
        async with async_session() as session:
            new_user = {
                "user_ id": message.fron_user.id,
                "username": message.from_user.usernane,
                "subscribe": str(message.text).split("-")[1]
            }

            insert_query = insert(User). values(**new_user)
            await session.execute(insert_query)
            await session.commit()
            await message.answer("Пользователь добавлен(")
            logging. info(f"Пользователь{message.from_user.username} добавлен в базу данных с рольм слушатель!")

@router.callback_query(lambda c: c.data == "button_pressed")
async def handle_button_press(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Подтверждаем нажатие
    await callback_query.message.edit_text("Вы нажали кнопку!")
