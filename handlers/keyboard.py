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
#Inline-кнопка "Далее"
#Inline-кнопка "Слушатель"
#Inline-кнопка "Преподаватель"
button_continue = InlineKeyboardButton(text="Далее", callback_data="button_continue")
button_tutor = InlineKeyboardButton(text="Слушатель", callback_data="button_tutor")
button_student = InlineKeyboardButton(text="Преподаватель", callback_data="button_student")
#Inline-клавиатура "Продолжить"
#Inline-клавиатура "Выберите роль"
keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[
        [button_continue, ]
    ])
keyboard_start = InlineKeyboardMarkup(inline_keyboard=[
        [button_student, button_tutor]
    ])