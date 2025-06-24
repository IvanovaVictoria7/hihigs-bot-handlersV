from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

#  Главное меню (reply-кнопки)
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=" О нас"), KeyboardButton(text=" Профиль")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

#  Inline-кнопки для выбора роли
button_teacher = InlineKeyboardButton(text=" Преподаватель", callback_data="button_tutor")
button_student = InlineKeyboardButton(text=" Студент", callback_data="button_student")

keyboard_start = InlineKeyboardMarkup(inline_keyboard=[
    [button_teacher, button_student]
])

#  Кнопка "Далее" (пока не используется)
button_continue = InlineKeyboardButton(text="Далее", callback_data="button_continue")

keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[
    [button_continue]
])