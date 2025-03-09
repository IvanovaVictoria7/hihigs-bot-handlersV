import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def process_start_command(message):
    await message.answer("Привет!")


@dp.message()
async def echo_message(message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())