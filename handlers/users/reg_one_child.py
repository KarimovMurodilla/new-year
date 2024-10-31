import asyncio
import os
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import inline_buttons
from utils.misc import cyrillic_checker
from states.reg import RegOneChild
from loader import dp, vid, db, bot


@dp.callback_query_handler(text_contains = 'one_child', state="*")
async def cancel_handler(c: types.CallbackQuery, state: FSMContext):
    await c.answer()
    await c.message.answer("Напишите ИМЯ ребёнка:")
    await RegOneChild.step1.set()


@dp.message_handler(state=RegOneChild.step1)
async def process_get_name(message: types.Message, state: FSMContext):
    u_names = [
        'Саша', 'Сашенька', 'Шура', 'Шурочка', 'Валя', 'Валечка', 'Валюша', 'Вася', 'Женя', 'Женечка'
    ]

    if not cyrillic_checker.all_ru(message.text):
        await message.answer("Только кириллицей!")

    else:
        async with state.proxy() as data:
            data['name'] = message.text.title()

        if message.text.title() in u_names:
            await message.answer("Уточняю, это мужское или женское имя?", reply_markup=inline_buttons.m_or_w())
            await RegOneChild.additive.set()

        else:
            await message.answer("Введите возраст:")
            await RegOneChild.next()


@dp.callback_query_handler(state=RegOneChild.additive)
async def process_get_wishes(c: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['male'] = c.data

    await c.message.delete()
    await c.message.answer("Введите возраст:")
    await RegOneChild.step2.set()


@dp.message_handler(state=RegOneChild.step2)
async def process_get_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) <= 0:
            await message.answer("О как.) Друг, обращайся когда появишься на свет.")
        
        elif int(message.text) > 14:
            await message.answer("Прости дружок, давай поздравим малышей.)")
        
        else:
            async with state.proxy() as data:
                data['age'] = int(message.text)
            await message.answer("Увлечения:", reply_markup=inline_buttons.choose_hobbies())
            await RegOneChild.next()


@dp.callback_query_handler(state=RegOneChild.step3)
async def process_get_hobbies(c: types.CallbackQuery, state: FSMContext):
    await c.answer()

    async with state.proxy() as data:
        data['hobbies'] = c.data
    await c.message.edit_text("Пожелание:", reply_markup=inline_buttons.choose_wishes())
    await RegOneChild.next()


@dp.callback_query_handler(state=RegOneChild.step4)
async def process_get_wishes(c: types.CallbackQuery, state: FSMContext):
    await c.answer()

    async with state.proxy() as data:
        data['wishes'] = c.data
    await c.message.edit_text("Регистрация завершена, нажмите на кнопку чтобы продолжить:", reply_markup=inline_buttons.get_congrats())
    await RegOneChild.next()


@dp.callback_query_handler(state=RegOneChild.step5)
async def process_get_wishes(c: types.CallbackQuery, state: FSMContext):
    for i in range(11):
        msg = await c.message.edit_text(
            "Минуточку, Дедушка Мороз записывает видеопоздравление.\n"
            f"{('🟦' * i) + ('◻️' * (10 - i))}"
        )
        await asyncio.sleep(0.5)

    async with state.proxy() as data:
        name = data.get('name')
        male = data.get('male')
        age = data.get('age')
        hobbies = data.get('hobbies')
        wishes = data.get('wishes')

        if not male:
            male = 'man' if name in vid.name_m.keys() else 'woman'

    bot_info = await bot.get_me()
    response = db.get_concat_one(name, male, age, hobbies, wishes, bot_info.username)
    
    if response:
        await c.message.answer_video(
            video = response.file_id, 
            caption= "Поздравление от Дедушки Мороза\n"
                    "В словарном запасе Дедушки мороза не было имени, которое вы назвали. Но он всё равно записал новогоднее поздравление. Нажмите на видео, чтобы посмотреть.\n\n"

                    "Поделиться новогодним чудом с друзьями:"
        )
        await state.finish()

    else:
        user_id = c.from_user.id
        vid.name_m.keys
        vid.generate_video_for_one_child(user_id, name, male, age, hobbies, wishes)
        await msg.delete()

        with open(f'staticfiles/videos/final/{user_id}.mp4', 'rb') as video:
            sended = await c.message.answer_video(
                video = video,
                caption = f"Поздравление для {name}\n"
                            "Скорее запускайте и смотрите!\n\n"

                            "Поделиться новогодним чудом с друзьями:"
            )

        os.remove(f'staticfiles/videos/final/{user_id}.mp4')

        db.reg_new_concat(
            user_id = user_id,
            type = 'one',
            wishes = wishes,
            file_id = sended.video.file_id,
            bot_name = bot_info.username,
            name = name,
            age = age,
            hobbies = hobbies,
            male = male
        )

        await state.finish()
