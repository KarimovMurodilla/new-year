import asyncio
import os
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import inline_buttons
from keyboards.default import keyboard_buttons
from utils.misc import cyrillic_checker
from utils.misc.payment import YooKassa
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

    m_names = list(vid.name_m.keys())
    w_names = list(vid.name_w.keys())
    m_names.extend(w_names)
    all_names = m_names

    if not cyrillic_checker.all_ru(message.text):
        await message.answer("Только кириллицей!")

    else:
        async with state.proxy() as data:
            data['name'] = message.text.title()

        if message.text.title() in u_names or message.text.title() not in all_names:
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
            data['name'] = m_names.get(data['name'])

        else:
            data['name'] = f_names.get(data['name'])

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
    await c.message.delete()

    async with state.proxy() as data:
        data['wishes'] = c.data
        
    await c.message.answer(
        "Отлично! Для оформления заявки, "
        "нажимай кнопку - отправить контакт. "
        "На	него я вышлю видеопоздравление.", 
            reply_markup=keyboard_buttons.send_contact()
    )
    await RegOneChild.next()

@dp.message_handler(content_types="contact", state=RegOneChild.step5)
async def process_get_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number

    msg = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()
    
    await message.answer(
        "Регистрация завершена, нажмите на кнопку чтобы продолжить:",
        reply_markup=inline_buttons.get_congrats()
    )
    await RegOneChild.next()

@dp.callback_query_handler(state=RegOneChild.step6)
async def process_show_paytypes(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete()

    kassa = YooKassa()
    payment_details = kassa.payment_create(value=1, description="For video generation")
    payment_url = payment_details['confirmation']['confirmation_url']
    payment_id = payment_details['id']

    await c.message.answer(
        "У вас есть промокод? "	
        "(промокод расположен на тыльной "
        "стороне конверта)",
            reply_markup=inline_buttons.show_paytypes(url=payment_url)
    )

    task = asyncio.create_task(kassa.check_payment(payment_id))

    async with state.proxy() as data:
        data['payment_url'] = payment_url

    await RegOneChild.next()

    if await task:
        await process_send_result(c.message, state)


@dp.callback_query_handler(lambda c: c.data == 'promo', state=RegOneChild.step7)
async def process_promocode(c: types.CallbackQuery, state: FSMContext):
    await c.answer()

    await c.message.answer("Отправьте промокод")
    await RegOneChild.next()


async def cancel_task(task):
    print("Cancelling the task...")
    task.cancel()
    try:
        await task  # Wait for the task to handle cancellation
    except asyncio.CancelledError:
        print("Task has been cancelled successfully.")


@dp.message_handler(state=RegOneChild.step8)
async def process_get_promocode(message: types.Message, state: FSMContext):
    promo = db.get_promocode_status(message.text)

    if promo and not promo.status:
        await process_send_result(message, state)
        db.update_promo_to_expired(message.text, message.from_user.id)

    else:
        data = await state.get_data()
        await message.answer(
            "Промокод недействителен. "
            "Пожалуйста, проверьте его и "
            "попробуйте	снова!",
            reply_markup=inline_buttons.show_paytypes(url=data['payment_url'])
        )
        await state.set_state(RegOneChild.step7)
 

async def show_process(message: types.Message):
    for i in range(11):
        msg = await message.edit_text(
            "Минуточку, Дедушка Мороз записывает видеопоздравление.\n"
            f"{('🟦' * i) + ('◻️' * (10 - i))}"
        )
        await asyncio.sleep(0.5)

    await msg.delete()
    return msg

# @dp.callback_query_handler(state=RegOneChild.step7)
async def process_send_result(message: types.Message, state: FSMContext):
    msg = await message.answer("Минуточку, Дедушка Мороз записывает видеопоздравление.")
    task = asyncio.create_task(show_process(msg))

    async with state.proxy() as data:
        name = data.get('name') if data.get('name') else 'no_name'
        gender = data.get('gender')
        age = data.get('age')
        hobbies = data.get('hobbies')
        wishes = data.get('wishes')
        phone_number = data.get("phone_number")

        if not gender:
            gender = 'male' if name in vid.name_m.keys() else 'female'

    db.reg_user(message.from_user.id, message.from_user.username, phone_number)
    bot_info = await bot.get_me()
    response = db.get_concat_one(name, gender, age, hobbies, wishes, bot_info.username)
    
    if name == 'no_name':
        caption = "Поздравление от Дедушки Мороза\n" \
                "В словарном запасе Дедушки мороза не было имени, которое вы назвали. " \
                "Но он всё равно записал новогоднее поздравление. Нажмите на видео, чтобы посмотреть.\n\n"
    else:
        caption = f"Поздравление для {name}\n" \
                    "Скорее запускайте и смотрите!\n\n"
        
    if response:            
        await message.answer_video(
            video = response.file_id,
            caption= caption
        )
        await state.finish()

    else:
        user_id = message.from_user.id
        video_url = vid.generate_video_for_one_child(BASE_DIR, user_id, name, gender, age, hobbies, wishes)

        if await task:
            with open(video_url, 'rb') as video:
                sended = await message.answer_video(
                    video = video,
                    caption = caption
                )

            os.remove(video_url)

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
