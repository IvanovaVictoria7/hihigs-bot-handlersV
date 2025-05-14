from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Статичная клавиатура ReplyKeyboardMarkup https://docs.aiogram.dev/en/v3.15.0/api/types/reply_keyboard_markup.html
# Динамически генерируемая клавиатура Keyboard builder https://docs.aiogram.dev/en/v3.15.0/utils/keyboard.html
# Примеры создания клавиатуры ReplyKeyboardMarkup https://habr.com/ru/articles/820733/#:~:text=%D0%98%D0%BC%D0%BF%D0%BE%D1%80%D1%82%D1%8B%20%D0%B2%20all_kb.py%3A
# Примеры создания клавиатуры Keyboard builder https://mastergroosha.github.io/aiogram-3-guide/buttons/

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

keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[
        [button_student,button_tutor ]
    ])