from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_keyboard_list = [
        [KeyboardButton(text="Статус"),]

main_keyboard = ReplyKeyboardMarkup(keyboard=main_keyboard_list, resize_keyboard=True, one_time_keyboard=True)