__all__ = [
    'set_my_commands'
]
from aiogram import Bot
from aiogram.types import BotCommand

async def set_my_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="status", description="Информация о пользователе"),
    ]
    await bot.set_my_commands(commands)

