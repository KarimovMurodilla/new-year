import asyncio
import os
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import inline_buttons
from states.reg import RegManyChild
from loader import dp, vid, db, bot, BASE_DIR


@dp.callback_query_handler(text_contains = 'many_child', state="*")
async def cancel_handler(c: types.CallbackQuery, state: FSMContext):
    await c.answer()
    await c.message.edit_text("Пожелание:", reply_markup=inline_buttons.choose_wishes())
    await RegManyChild.step1.set()


@dp.callback_query_handler(state=RegManyChild.step1)
async def process_get_wishes(c: types.CallbackQuery, state: FSMContext):
    await c.answer()

    async with state.proxy() as data:
        data['wishes'] = c.data

    await c.message.edit_text("Регистрация завершена, нажмите на кнопку чтобы продолжить:", reply_markup=inline_buttons.get_congrats())
    await RegManyChild.next()


@dp.callback_query_handler(state=RegManyChild.step2)
async def process_get_wishes(c: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        wishes = data.get('wishes')

    for i in range(11):
        msg = await c.message.edit_text(
            "Минуточку, Дедушка Мороз записывает видеопоздравление.\n"
            f"{('🟦' * i) + ('◻️' * (10 - i))}"
        )
        await asyncio.sleep(0.5)

    bot_name = await bot.get_me()
    response = db.get_concat_many(wishes, bot_name.username)
    print("Response:", response)

    if response:
        return await c.message.answer_video(
            video = response.file_id, 
            caption= "Поздравление от Дедушки Мороза\n"
                    "В словарном запасе Дедушки мороза не было имени, которое вы назвали. Но он всё равно записал новогоднее поздравление. Нажмите на видео, чтобы посмотреть.\n\n"

                    "Поделиться новогодним чудом с друзьями:"
        )

    vid.generate_video_for_many_child(BASE_DIR, wishes, c.from_user.id)

    await msg.edit_text("Отправляем...")
    with open(f"{BASE_DIR}/staticfiles/videos/final/{c.from_user.id}.mp4", 'rb') as video:
        await msg.delete()
        result = await c.message.answer_video(
            video = video, 
            caption= "Поздравление от Дедушки Мороза\n"
                    "В словарном запасе Дедушки мороза не было имени, которое вы назвали. Но он всё равно записал новогоднее поздравление. Нажмите на видео, чтобы посмотреть.\n\n"

                    "Поделиться новогодним чудом с друзьями:"
        )

    os.remove(f'{BASE_DIR}/staticfiles/videos/final/{c.from_user.id}.mp4')

    db.reg_new_concat(
        user_id=c.from_user.id,
        type = 'many',
        file_id = result.video.file_id,
        wishes = wishes,
        bot_name = bot_name.username
    )