import pytest
from main import main
from fixtures import mock_bot, mock_dispatcher, mock_set_my_commands, mock_handlers_router, mock_callbacks_router, mock_setup_logger

@pytest.mark.asyncio
async def test_main(mock_bot, mock_dispatcher, mock_setup_logger, mock_set_my_commands):
    # вызов функции main
    await main()

    #Проверка
    mock_dispatcher.start_polling.assert_awaited_once_with(mock_bot)

    #TODO - техдолг: доделать вызовы функций
    # mock_dispatcher.include_router.assert_awaited_once_with(mock_handlers_router, mock_callbacks_router)
    # mock_bot.set_my_commands.assert_awaited_once()
    # mock_setup_logger.assert_awaited_once()