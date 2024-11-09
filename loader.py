from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.misc.connection import Database

from utils.misc.edit.video_edit import VideoEdit
from aiogram.bot.api import TelegramAPIServer

from data.config import BOT_TOKEN, DEBUG

# AIOgram
local_server = TelegramAPIServer.from_base('http://localhost:8081')

if DEBUG:
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
else:
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML, server=local_server)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# DB
db = Database()

# Video
vid = VideoEdit()

# Path
BASE_DIR = Path(__file__).parent.resolve()
