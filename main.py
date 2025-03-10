imrort asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

#экземпляр бота
bot = Bot(token="Your Token")
dp = Dispatcher()

#Бот принимает команды, например /start.
# Создадим хендлер - обработчик сообщений, и будет возвращать сообщение
@dp.message(Command('start'))
async def process_start_command(message):
    await message.answer("Привет!")


@dp.message()
async def echo_message(message):
    await message.answer(message.text)

#функция запуска проекта
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())