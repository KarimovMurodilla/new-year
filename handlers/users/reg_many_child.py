import asyncio
import os
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import inline_buttons
from keyboards.default import keyboard_buttons
from utils.misc.payment import YooKassa
from states.reg import RegManyChild
from loader import dp, vid, db, bot, BASE_DIR


@dp.callback_query_handler(text_contains = 'many_child', state="*")
async def cancel_handler(c: types.CallbackQuery, state: FSMContext):
    await c.answer()
    await c.message.edit_text("Пожелание:", reply_markup=inline_buttons.choose_wishes())
    await RegManyChild.step1.set()


@dp.callback_query_handler(state=RegManyChild.step1)
async def process_get_wishes(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete()

    async with state.proxy() as data:
        data['wishes'] = c.data

    await c.message.answer(
        "Отлично! Для оформления заявки, "
        "нажимай кнопку	- отправить контакт. "
        "На него я вышлю видеопоздравление.", 
        reply_markup=keyboard_buttons.send_contact())
    await RegManyChild.next()


@dp.message_handler(content_types="contact", state=RegManyChild.step2)
async def process_get_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
    
    msg = await message.answer(".")
    await msg.delete()

    await message.answer(
        "Регистрация завершена, нажмите на кнопку чтобы продолжить:",
        reply_markup=inline_buttons.get_congrats()
    )
    await RegManyChild.next()


@dp.callback_query_handler(state=RegManyChild.step3)
async def process_show_paytypes_to_many(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete()

    await c.message.answer(
        "У вас есть промокод? "	
        "(промокод расположен на тыльной "
        "стороне конверта)",
            reply_markup=inline_buttons.show_paytypes()
    )

    await RegManyChild.next()


@dp.callback_query_handler(lambda c: c.data == 'promo', state=RegManyChild.step4)
async def process_promocode(c: types.CallbackQuery, state: FSMContext):
    await c.answer()

    await c.message.answer("Отправьте промокод")
    await RegManyChild.next()


@dp.message_handler(state=RegManyChild.step5)
async def process_get_promocode(message: types.Message, state: FSMContext):
    promo = db.get_promocode_status(message.text)

    if promo and not promo.status:
        await process_send_result(message, state)
        db.update_promo_to_expired(message.text)
    
    else:
        await message.answer(
            "Промокод недействителен. "
            "Пожалуйста, проверьте его и "	
            "попробуйте	снова!",
            reply_markup=inline_buttons.show_paytypes()
        )
        await state.set_state(RegManyChild.step3)


@dp.callback_query_handler(lambda c: c.data == 'yookassa', state=RegManyChild.step4)
async def process_promocode(c: types.CallbackQuery, state: FSMContext):
    await c.answer()

    kassa = YooKassa()
    payment_details = kassa.payment_create(value=90, description="For video generation")
    payment_url = payment_details['confirmation']['confirmation_url']
    payment_id = payment_details['id']

    await c.message.answer(
        "Чтобы оплатить, переходите на страницу оплаты по указанной кнопки",
        reply_markup=inline_buttons.show_yookassa_payment(payment_url)
    )

    if await kassa.check_payment(payment_id):
        process_send_result(c, state)
        await state.finish()

    # await RegManyChild.next()


async def show_process(message: types.Message):
    for i in range(11):
        msg = await message.edit_text(
            "Минуточку, Дедушка Мороз записывает видеопоздравление.\n"
            f"{('🟦' * i) + ('◻️' * (10 - i))}"
        )
        await asyncio.sleep(0.5)

    await msg.delete()
    return msg


async def process_send_result(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        wishes = data.get('wishes')
        phone_number = data.get('phone_number')

    msg = await message.answer("Минуточку, Дедушка Мороз записывает видеопоздравление.")
    task = asyncio.create_task(show_process(msg))

    db.reg_user(message.from_user.id, message.from_user.username, phone_number)
    bot_name = await bot.get_me()
    response = db.get_concat_many(wishes, bot_name.username)

    if response:
        return await message.answer_video(
            video = response.file_id, 
            caption= "Дедушка Морозvзаписал видеопоздравление. "
                        "Скорее запускайте и смотрите!"
        )

    video_url = vid.generate_video_for_many_child(BASE_DIR, wishes, message.from_user.id)

    if await task:
        with open(video_url, 'rb') as video:
            result = await message.answer_video(
                video = video, 
                caption= "Дедушка Морозvзаписал видеопоздравление. "
                        "Скорее запускайте и смотрите!"
            )

        os.remove(video_url)

        db.reg_new_concat(
            user_id=message.from_user.id,
            type = 'many',
            file_id = result.video.file_id,
            wishes = wishes,
            bot_name = bot_name.username
        )