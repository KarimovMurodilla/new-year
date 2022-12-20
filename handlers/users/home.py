import os
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import inline_buttons
from keyboards.default import keyboard_buttons

from loader import dp, bot, db


@dp.message_handler(state="*", text = 'Отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Отменено!", reply_markup=keyboard_buttons.main_menu())


@dp.message_handler(state="*", content_types=types.ContentTypes.VIDEO)
async def photo(message: types.Message):
    pass