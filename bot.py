from aiogram import Bot
from config_reader import config


TOKEN = config.bot_token.get_secret_value()
bot = Bot(token=TOKEN)


def get_bot():
    return bot