import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from classes import ScriptClass
from db import async_create_table

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
    datefmt="[%d-%m-%Y %H:%M:%S]",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/script.log", mode='w'),
    ],
)

_executor = ThreadPoolExecutor(1)

async def main():
    """
    Основная функция для запуска бизнес-логики.
    """
    logger = logging.getLogger(__name__)
    logger.info("Запуск скрипта бизнес-логики.")

    # Инициализация базы данных
    await async_create_table()

    # Создание экземпляра класса
    script = ScriptClass()

    # Пример вызова асинхронного метода
    result = await script.async_method_example("Test Data")
    logger.info(f"Результат асинхронного метода: {result}")

    # Пример вызова синхронного метода через ThreadPoolExecutor
    loop = asyncio.get_event_loop()
    sync_result = await loop.run_in_executor(_executor, script.sync_method_example, "Sync Test Data")
    logger.info(f"Результат синхронного метода: {sync_result}")

    # Пример добавления задачи
    user_id = 12345  # Замените на реальный user_id
    profile_url = "https://www.codewars.com/users/testuser"
    task_name = "Sample Task"
    task_added = await script.add_task_for_user(user_id, profile_url, task_name)
    logger.info(f"Задача добавлена: {task_added}")

    # Пример обновления подписки
    student_id = 12345  # Замените на реальный student_id
    teacher_id = 67890  # Замените на реальный teacher_id
    subscription_updated = await script.update_subscription_status(student_id, teacher_id, True)
    logger.info(f"Подписка обновлена: {subscription_updated}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Скрипт остановлен")
    finally:
        _executor.shutdown(wait=True)