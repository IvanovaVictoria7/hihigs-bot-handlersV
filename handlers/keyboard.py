from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,  InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 О нас"), KeyboardButton(text="👤 Профиль")]
        ],
        resize_keyboard=True,  # Автоматически подстраивает размер под экран
        one_time_keyboard=False  # Клавиатура остаётся после нажатия (можно сделать True, чтобы исчезала)
    )
    return keyboard

button_continue = InlineKeyboardButton(text="Далее", callback_data="button_continue")
button_tutor = InlineKeyboardButton(text="Слушатель", callback_data="button_student")
button_student = InlineKeyboardButton(text="Преподаватель", callback_data="button_tutor")

keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[
    [button_continue]
])
keyboard_start = InlineKeyboardMarkup(inline_keyboard=[
    [button_student, button_tutor]
])