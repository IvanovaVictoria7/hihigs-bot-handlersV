from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 О нас"), KeyboardButton(text="👤 Профиль")]
        ],
        resize_keyboard=True,  # Автоматически подстраивает размер под экран
        one_time_keyboard=False  # Клавиатура остаётся после нажатия (можно сделать True, чтобы исчезала)
    )
    return keyboard
