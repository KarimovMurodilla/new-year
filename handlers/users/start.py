from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.deep_linking import get_start_link

from loader import dp, db, bot, user_bot
from keyboards.default import keyboard_buttons
from keyboards.inline import inline_buttons


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    db.reg_user(message.from_user.id, message.from_user.username)
    await message.answer_photo(
        photo='AgACAgIAAxkBAAIRJWOI1HdIcGdS6NyIzoJAezhfc6w-AALGwTEb1bpJSE3yifLli9mpAQADAgADdwADKwQ',
        caption  =  "Сотворите Новогоднее чудо для ребёнка. "
                    "Я помогу за пару секунд создать именное поздравление от Дедушки Мороза и это как в сказке – абсолютно БЕСПЛАТНО! "
                    "Только расскажи немного про адресата, чтобы пожелания попали в самое сердечко ❤",
                        reply_markup=inline_buttons.create_congrats()
    )