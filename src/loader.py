from aiogram import Bot, Dispatcher, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src import config

# Покдлючение переменных из файла config
bot = Bot(config.TOKEN, parse_mode=types.ParseMode.HTML)
bot2 = Bot(config.TOKEN2, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp2 = Dispatcher(bot2, storage=storage)