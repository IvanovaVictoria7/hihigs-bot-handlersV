import pytest
from unittest.mock import AsyncMock
from fixtures import mock_message,mock_router,mock_callback_query
from handlers.handlers import help_handler, start_handler
from handlers.callbacks import handle_button_press
from aiogram.types import ReplyKeyboardMarkup
# Когда тест помечен @pytest.mark.asyncio, он становится сопрограммой (coroutine), вместе с ключевым словом await в теле
# pytest выполнит функцию теста как задачу asyncio, используя цикл событий, предоставляемый фикстурой event_loop
# https://habr.com/ru/companies/otus/articles/337108/

@pytest.mark.asyncio
async def test_command_start_handler(mock_router,mock_message):
    # # Вызываем хендлер
    await start_handler(mock_message)
    # # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"
    # параметрами которыми был вызыван хендлер
    called_args,called_kwargs = mock_message.answer.call_args
    print(called_args)
    assert called_args[0] == f"Привет, {mock_message.from_user.full_name}!\nТвой ID: {mock_message.from_user.id}"
    # # Проверяем, что mock_ был вызван один раз с ожидаемым результатом
    #mock_message.answer.assert_called_once_with(text="Привет,{message.from_user.full_name}!\n Твой ID: {message.from_user.id}")

@pytest.mark.asyncio
async def test_command_help_handler(mock_router, mock_message):
    # Вызываем хендлер
    await help_handler(mock_message)
    # Проверка, что mock_message.answer был вызван
    assert mock_message.answer.called, "message.answer не был вызван"
    # Параметры, с которыми был вызван хэндлер
    called_args, called_kwargs = mock_message.answer.call_args
    assert called_kwargs["text"] == "Доступные команды:\n/start - Начать\n/help - Справка\n/status - Статус"

@pytest.mark.asyncio
async def test_callbacks_handler(mock_router, mock_callback_query):
    # Устанавливаем тестовые данные коллбека
    mock_callback_query.data = "button_pressed"

    # Вызываем хендлер
    await handle_button_press(mock_callback_query)

    # Проверка, что callback_query.answer был вызван (подтверждение нажатия)
    assert mock_callback_query.answer.called, "callbacks_query.answer не был вызван"

    # Проверка, что callback_query.message.edit_text был вызван
    assert mock_callback_query.message.edit_text.called, "message.edit_text не был вызван"

    # Параметры, с которыми был вызван message.edit_text
    called_args, called_kwargs = mock_callback_query.message.edit_text.call_args
    assert called_args[0] == "Вы нажали кнопку!"


    #TODO - техдолг: переделать тесты



