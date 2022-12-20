import asyncio

from aiogram import types, executor
from pyrogram import Client

from loader import dp
from data.config import API_ID, API_HASH


client = Client("my_account", API_ID, API_HASH)

def send_large(file_name='875587704', bot_name='teeessstbot'):
    with client as app:
        vid = app.send_video(
            chat_id = f'@{bot_name}', 
            video = f'staticfiles/videos/final/{file_name}.mp4'
        )
    return vid


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm TestBot!")


@dp.message_handler()
async def echo(message: types.Message):
    res = send_large(875587704, 'teeessstbot')
    print(res)


if __name__ == '__main__':
    executor.start_polling(dp)