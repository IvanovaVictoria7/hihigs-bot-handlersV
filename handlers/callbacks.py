from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "button_pressed")
async def handle_button_press(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Подтверждаем нажатие
    await callback_query.message.edit_text("Вы нажали кнопку!")
