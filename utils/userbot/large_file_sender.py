from pyrogram import Client
from data.config import API_ID, API_HASH


class UserBot:
    async def send_large(self, file_name, bot_name):
        async with Client("my_account", API_ID, API_HASH) as app:
            vid = await app.send_video(
                chat_id = f'@{bot_name}', 
                video = f'staticfiles/videos/final/{file_name}.mp4'
            )
        return vid