import asyncio
import os
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import inline_buttons
from utils.misc import cyrillic_checker
from states.reg import RegOneChild
from loader import dp, vid, db, bot, BASE_DIR


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
    m_names = {
        'Саша': 'Александр',
        'Сашенька': 'Александр',
        'Шура': 'Александр',
        'Шурочка': 'Александр',
        'Валя': 'Валентин',
        'Валечка': 'Валентин',
        'Валюша': 'Валентин',
        'Вася': 'Василий',
        'Женя': 'Евгений',
        'Женечка': 'Евгений'
    }

    f_names = {
        'Саша': 'Александра',
        'Сашенька': 'Александра',
        'Шура': 'Александра',
        'Шурочка': 'Александра',
        'Валя': 'Валентина',
        'Валечка': 'Валентина',
        'Валюша': 'Валентина',
        'Вася': 'Василиса',
        'Женя': 'Евгения',
        'Женечка': 'Евгения'
    }

    async with state.proxy() as data:
        data['gender'] = c.data

        if c.data == 'male':
            data['name'] = m_names[data['name']]

        else:
            data['name'] = f_names[data['name']]

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


async def show_process(c: types.CallbackQuery):
    for i in range(11):
        msg = await c.message.edit_text(
            "Минуточку, Дедушка Мороз записывает видеопоздравление.\n"
            f"{('🟦' * i) + ('◻️' * (10 - i))}"
        )
        await asyncio.sleep(0.5)

    await msg.delete()
    return msg   
    
@dp.callback_query_handler(state=RegOneChild.step5)
async def process_get_wishes(c: types.CallbackQuery, state: FSMContext):
    task = asyncio.create_task(show_process(c))

    async with state.proxy() as data:
        name = data.get('name')
        gender = data.get('gender')
        age = data.get('age')
        hobbies = data.get('hobbies')
        wishes = data.get('wishes')

        if not gender:
            gender = 'male' if name in vid.name_m.keys() else 'female'

    bot_info = await bot.get_me()
    response = db.get_concat_one(name, gender, age, hobbies, wishes, bot_info.username)
    
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
        vid.generate_video_for_one_child(BASE_DIR, user_id, name, gender, age, hobbies, wishes)

        if await task:
            with open(f'{BASE_DIR}/staticfiles/videos/final/{user_id}.mp4', 'rb') as video:
                sended = await c.message.answer_video(
                    video = video,
                    caption =  f"Поздравление для {name}\n"
                                "Скорее запускайте и смотрите!\n\n"

                                "Поделиться новогодним чудом с друзьями:"
                )

            os.remove(f'{BASE_DIR}/staticfiles/videos/final/{user_id}.mp4')

            db.reg_new_concat(
                user_id = user_id,
                type = 'one',
                wishes = wishes,
                file_id = sended.video.file_id,
                bot_name = bot_info.username,
                name = name,
                age = age,
                hobbies = hobbies,
                gender = gender
            )

            await state.finish()
