from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.misc.connection import Database

from utils.misc.edit.video_edit import VideoEdit
from aiogram.bot.api import TelegramAPIServer

# AIOgram
local_server = TelegramAPIServer.from_base('http://localhost:8081')
bot = Bot(token='API_TOKEN', server=local_server, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# DB
db = Database()


# Video
vid = VideoEdit()