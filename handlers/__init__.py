from aiogram import Bot
from aiogram.types import BotCommand

async def set_my_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="status", description="Информация о пользователе"),
        BotCommand(command="load", description="Загрузить профили Codewars"),
        BotCommand(command="getres", description="Получить результаты по задачам"),
    ]
    await bot.set_my_commands(commands)