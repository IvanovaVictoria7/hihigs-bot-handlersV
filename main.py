import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

bot = Bot(token="Your Token")
dp = Dispatcher()


@dp.message(Command('/start'))
async def process_start_command(message):
    await message.answer("Привет!")


@dp.message()
async def echo_message(message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())