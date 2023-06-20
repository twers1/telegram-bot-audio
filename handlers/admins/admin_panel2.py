import json
import os
from datetime import datetime

from aiogram.dispatcher import FSMContext

from handlers.users.user_panel import send_welcome
from keyboards.inline.choice_buttons import admin_panel, quit_button
from loader import bot2, dp2
from aiogram import types

from states import Links
from utils.db_functions import get_users_count, get_inactive_users_count, add_link_to_db

ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


@dp2.message_handler(commands='start')
async def cmd_start(message: types.Message):
    print('Мы во втором боте')
    if message.from_user.id in ADMIN_ID:
        await bot2.send_message(message.from_user.id, f'Вы успешно зашли в админ-панель', reply_markup=admin_panel)


@dp2.message_handler(text="👱‍♂️Посмотреть статистику")
async def statistics(message: types.Message):
    users_count = await get_users_count()
    inactive_users_count = await get_inactive_users_count()
    await bot2.send_message(message.chat.id, f'На момент последней проверки: *{datetime.now()}* в боте:\n'
                                            f'Живые: {users_count}\n'
                                            f'Мертвые: {inactive_users_count}\n'
                                            f'Суммарно проверено: \n'
                                            f'На текущий момент, в боте: *пока не знаю*', reply_markup=quit_button,
                                            parse_mode='Markdown')


@dp2.message_handler(text="Выйти")
async def quit_to_lobby(message: types.Message):
    await cmd_start(message)


@dp2.message_handler(text="🔗Добавить ссылку")
async def add_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot2.send_message(message.from_user.id, "<b>Скиньте ссылку на канал</b>")

    await state.reset_state()
    await Links.first()


@dp2.message_handler(state=Links.link)
async def get_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["link"] = message.text

    state_data = await state.get_data()
    link = state_data["link"]

    await message.answer("<b>Ссылка успешно добавлена!</b>")

    await add_link_to_db(link)
    await state.reset_state()
