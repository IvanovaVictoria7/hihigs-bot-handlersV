import pytest
from unittest.mock import AsyncMock
from aiogram.types import Message,CallbackQuery
from aiogram import Router


# Фикстуры в pytest позволяют выносить в отдельные функции типовые действия
# например: настройка тестового окружения, создание тестовых данных, выполнение завершающие действия
# https://habr.com/ru/articles/731296/

@pytest.fixture
def mock_message():
    """Mock сообщение"""
    mock_msg=AsyncMock(spec=Message)
    mock_msg.answer = AsyncMock()
    mock_msg.from_user = AsyncMock()
    mock_msg.from_user.id = AsyncMock()
    mock_msg.from_user.full_name = AsyncMock()
    return mock_msg

@pytest.fixture
def mock_router():
    """Mock router"""
    router = Router
    return router

@pytest.fixture
def mock_callback_query():
    """Mock коллбек-запрос"""
    mock_cb = AsyncMock(spec=CallbackQuery)
    mock_cb.answer = AsyncMock()
    mock_cb.message = AsyncMock(spec=Message)
    mock_cb.message.answer = AsyncMock()
    mock_cb.message.edit_text = AsyncMock()
    mock_cb.data = ""  # Данные коллбека, можно переопределить в тестах
    return mock_cb
