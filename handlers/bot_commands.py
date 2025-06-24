__all__ = ["set_my_commands"]

from aiogram import Bot
from aiogram.types import BotCommand

async def set_my_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="status", description="Показать ваш статус"),
        BotCommand(command="load", description="Загрузить профили Codewars"),
        BotCommand(command="getres", description="Показать выполненные задачи"),
    ]
    await bot.set_my_commands(commands)