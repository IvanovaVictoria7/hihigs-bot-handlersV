import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message,CallbackQuery
from aiogram import Router

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
    router = Router()
    return router

@pytest.fixture
def mock_handlers_router():
    """Mock router"""
    router = Router()
    return router

@pytest.fixture
def mock_callbacks_router():
    """Mock router"""
    router = Router()
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

@pytest.fixture
def mock_bot():
    '''Mock бот'''
    with patch("main.Bot") as mock_bot_cls:
        mock_bot_instance = AsyncMock()
        mock_bot_cls.return_value = mock_bot_instance
        yield mock_bot_instance

@pytest.fixture()
def mock_set_my_commands():
    '''Mock создание меню'''
    with patch("main.set_my_commands", new_callable = AsyncMock) as mock:
        yield mock_set_my_commands

@pytest.fixture()
def mock_setup_logger():
    '''Mock логгер'''
    with patch("main.setup_logger", new_callable = AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_dispatcher():
    '''Mock диспетчер'''
    with patch("main.Dispatcher") as mock_dispatcher_cls:
        mock_dispatcher_instance = AsyncMock()
        mock_dispatcher_instance.start_polling = AsyncMock()
        mock_dispatcher_instance.include_router = AsyncMock()
        mock_dispatcher_cls.return_value = mock_dispatcher_instance
        yield mock_dispatcher_instance