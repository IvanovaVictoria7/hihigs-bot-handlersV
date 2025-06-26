__all__ = [
    "ScriptClass"
]

from sqlalchemy import select, insert, update
from db import async_session, User, Profile, Task, Subscription
import logging
import asyncio


class ScriptClass:
    """Класс бизнес-логики для работы с базой данных и обработки данных."""

    def __init__(self):
        """Инициализация класса."""
        self.logger = logging.getLogger(__name__)

    async def add_task_for_user(self, user_id: int, profile_url: str, task_name: str) -> bool:
        """
        Асинхронно добавляет задачу для пользователя по профилю.

        Args:
            user_id (int): ID пользователя.
            profile_url (str): URL профиля Codewars.
            task_name (str): Название задачи.

        Returns:
            bool: True, если задача добавлена, False в случае ошибки.
        """
        try:
            async with async_session() as session:
                # Проверяем, существует ли пользователь
                user_query = select(User).where(User.user_id == user_id)
                user_result = await session.execute(user_query)
                user = user_result.scalar()

                if not user:
                    self.logger.error(f"Пользователь {user_id} не найден.")
                    return False

                # Проверяем или добавляем профиль
                profile_query = select(Profile).where(Profile.user_id == user_id, Profile.profile_url == profile_url)
                profile_result = await session.execute(profile_query)
                profile = profile_result.scalar()

                if not profile:
                    profile_data = {"user_id": user_id, "profile_url": profile_url}
                    await session.execute(insert(Profile).values(**profile_data))
                    await session.flush()
                    profile_query = select(Profile).where(Profile.user_id == user_id,
                                                          Profile.profile_url == profile_url)
                    profile_result = await session.execute(profile_query)
                    profile = profile_result.scalar()

                # Добавляем задачу
                task_data = {"profile_id": profile.id, "task_name": task_name}
                await session.execute(insert(Task).values(**task_data))
                await session.commit()
                self.logger.info(f"Задача '{task_name}' добавлена для пользователя {user_id}.")
                return True
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении задачи: {e}")
            await session.rollback()
            return False

    async def update_subscription_status(self, student_id: int, teacher_id: int, active: bool) -> bool:
        """
        Обновляет статус подписки между студентом и преподавателем.

        Args:
            student_id (int): ID студента.
            teacher_id (int): ID преподавателя.
            active (bool): Статус подписки (True - активна, False - неактивна).

        Returns:
            bool: True, если подписка обновлена, False в случае ошибки.
        """
        try:
            async with async_session() as session:
                subscription_query = select(Subscription).where(
                    Subscription.student_id == student_id,
                    Subscription.teacher_id == teacher_id
                )
                result = await session.execute(subscription_query)
                subscription = result.scalar()

                if not subscription:
                    self.logger.error(
                        f"Подписка между студентом {student_id} и преподавателем {teacher_id} не найдена.")
                    return False

                # Для простоты предположим, что у нас есть поле `active` в модели Subscription
                # Если его нет, можно добавить в модель или использовать другой способ
                await session.execute(
                    update(Subscription)
                    .where(Subscription.student_id == student_id, Subscription.teacher_id == teacher_id)
                    .values(active=active)
                )
                await session.commit()
                self.logger.info(
                    f"Статус подписки обновлён: student_id={student_id}, teacher_id={teacher_id}, active={active}")
                return True
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении подписки: {e}")
            await session.rollback()
            return False

    def sync_method_example(self, data: str) -> str:
        """
        Синхронный метод для обработки данных (пример).

        Args:
            data (str): Входные данные.

        Returns:
            str: Обработанные данные.
        """
        self.logger.info(f"Обработка данных в sync_method: {data}")
        return f"Processed: {data}"

    async def async_method_example(self, data: str) -> str:
        """
        Асинхронный метод для обработки данных (пример).

        Args:
            data (str): Входные данные.

        Returns:
            str: Обработанные данные.
        """
        await asyncio.sleep(2)  # Имитация асинхронной работы
        self.logger.info(f"Обработка данных в async_method: {data}")
        return f"Async Processed: {data}"