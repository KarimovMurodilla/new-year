from environs import Env

env = Env()
env.read_env()

# Telegram Bot
DEBUG = env.bool("DEBUG")  # Забираем значение типа booldd
BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список админов

SHOP_ID=env.str("SHOP_ID")
SHOP_API_TOKEN=env.str("SHOP_API_TOKEN")
