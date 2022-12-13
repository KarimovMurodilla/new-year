from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import inline_buttons
from loader import dp


@dp.callback_query_handler(text_contains = 'create', state="*")
async def cancel_handler(c: types.CallbackQuery, state: FSMContext):
    await c.answer()
    await c.message.answer("Выберите, кого желаете поздравить:", reply_markup=inline_buttons.choose_type())