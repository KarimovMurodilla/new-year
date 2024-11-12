from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default import keyboard_buttons
from keyboards.inline import inline_buttons


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    
    await message.answer_photo(
        photo='AgACAgIAAxkBAAIqNWcgpl8L5EP3XYDpAAGUNYiLvF6h6gACOuYxG7ubAAFJ7G4lw5UUVJEBAAMCAAN4AAM2BA',
        caption  =  "Сотворите Новогоднее чудо для ребёнка.\n"
                    "Я помогу за пару секунд создать именное "
                    "поздравление от Дедушки Мороза и это как "
                    "личный	звонок с Северного Полюса!\n"
                    "Только	расскажи немного про адресата, чтобы "
                    "пожелания попали в самое сердечко ❤",
                        reply_markup=inline_buttons.create_congrats()
    )