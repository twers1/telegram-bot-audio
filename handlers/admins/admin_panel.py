import json
import os

from loader import dp, bot
from aiogram import types

ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


@dp.message_handler(text="Админ-панель")
async def redirect_to_second_bot(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        url = f"https://t.me/voicetest2_bot?start=admin"
        await bot.send_message(message.chat.id, "Переход на админ панельку", reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Перейти🙄", url=url)))
