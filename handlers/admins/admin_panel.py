import json
import os
from datetime import datetime

from handlers.users.user_panel import send_welcome
from keyboards.inline.choice_buttons import admin_panel, quit_button
from loader import dp, bot
from aiogram import types

from utils.db_functions import get_users_count, get_inactive_users_count

ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


# @dp.message_handler(text="Админ-панель")
# async def contacts(message: types.Message):
#     print("Бот запущен(админ-панель)")
#     if message.from_user.id in ADMIN_ID:
#         await bot.send_message(message.from_user.id, f'Вы вошли в админ-панель', reply_markup=admin_panel)

@dp.message_handler(text="Админ-панель")
async def redirect_to_second_bot(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        url = f"https://t.me/voicetest2_bot?start=admin"
        await bot.send_message(message.chat.id, "Переход на админ панельку", reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Перейти🙄", url=url)))


@dp.message_handler(commands='start')
async def handle_start_command(message: types.Message):
    if message.from_user.id in ADMIN_ID and message.get_args() == "admin":
        await bot.send_message(message.from_user.id, f'Вы успешно зашли в админ-панель', reply_markup=admin_panel)


@dp.message_handler(text="👱‍♂️Посмотреть статистику")
async def statistics(message: types.Message):
    users_count = await get_users_count()
    inactive_users_count = await get_inactive_users_count()
    await bot.send_message(message.chat.id, f'На момент последней проверки: *{datetime.now()}* в боте:\n'
                                            f'Живые: {users_count}\n'
                                            f'Мертвые: {inactive_users_count}\n'
                                            f'Суммарно проверено: \n'
                                            f'На текущий момент, в боте: *пока не знаю*', reply_markup=quit_button, parse_mode='Markdown')


@dp.message_handler(text="Выйти")
async def quit_to_lobby(message: types.Message):
    await send_welcome(message)






