from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.misc.connection import Database

from utils.misc.edit.video_edit import VideoEdit
from utils.userbot.large_file_sender import UserBot


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# DB
db = Database()


# Video
vid = VideoEdit()


# User Bot
user_bot = UserBot()
