import asyncio
from pyrogram import Client


API_ID = 3795764
API_HASH = 'd2958e4859ac9e36be37f086785543e3'
# app = Client(os.path.join(path, "session.session"), api_id, api_hash)


async def main():
    async with Client("my_account.session", API_ID, API_HASH) as app:
        # res = await app.get_chat(875587704)
        # await app.send_message(875587704, "Yo, man")
        # await app.get_chat('https://t.me/thecooldevv')
        res = await app.get_chat('@thecooldevv')
        # vid = await app.send_video(
        #     chat_id = 875587704, 
        #     video = f'staticfiles/videos/final/875587704.mp4'
        # )
        print(res)


if __name__ == '__main__':
    asyncio.run(main())