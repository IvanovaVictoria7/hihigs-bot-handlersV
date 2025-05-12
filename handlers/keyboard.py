from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 О нас"), KeyboardButton(text="👤 Профиль")]
        ],
        resize_keyboard=True,  # Автоматически подстраивает размер под экран
        one_time_keyboard=False  # Клавиатура остаётся после нажатия (можно сделать True, чтобы исчезала)
    )
    return keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def get_continue_keyboard():
    button_continue = InlineKeyboardButton(text="Далее", callback_data="button_continue")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_continue]
        ]
    )
    return keyboard

def get_role_selection_keyboard():
    button_tutor = InlineKeyboardButton(text="Преподаватель", callback_data="button_tutor")
    button_student = InlineKeyboardButton(text="Ученик", callback_data="button_student")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_student, button_tutor]
        ]
    )
    return keyboard