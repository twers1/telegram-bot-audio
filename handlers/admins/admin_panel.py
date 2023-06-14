import json
import os

from keyboards.inline.choice_buttons import admin_panel
from loader import dp, bot
from aiogram import types

from utils.db_functions import get_users

ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


@dp.message_handler(text="Админ-панель")
async def contacts(message: types.Message):
    print("Бот запущен(админ-панель)")
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(message.from_user.id, f'Вы вошли в админ-панель', reply_markup=admin_panel)


@dp.message_handler(text="👱‍♂️Посмотреть статистику")
async def statistics(message: types.Message):
    await bot.send_message(message.chat.id, f'Статистика бота: ')


