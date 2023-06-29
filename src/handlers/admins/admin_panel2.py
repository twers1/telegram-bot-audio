import json
import os
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram import types

from src.keyboards.inline.choice_buttons import admin_panel, quit_button
from src.loader import bot2, dp2
from src.states import Links
from src.utils.db_functions import get_users_count, get_inactive_users_count, get_live_users, get_users_current_time, \
    add_link_to_db

# Загружает данные с env переменной в json
ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


# Стартовое меню. Проверка админ или нет
@dp2.message_handler(commands='start')
async def cmd_start(message: types.Message):
    print('Мы во втором боте')
    if message.from_user.id in ADMIN_ID:
        await bot2.send_message(message.from_user.id, f'Вы успешно зашли в админ-панель', reply_markup=admin_panel)


# Функция, показывающая сколько живых, мертвых, суммарно проверенных и сколько на текущий момент в боте человек
@dp2.message_handler(text="👱‍♂️Посмотреть статистику")
async def statistics(message: types.Message):
    users_count = await get_users_count()
    inactive_users_count = await get_inactive_users_count()
    get_users_live = await get_live_users()
    get_users_cur_time = await get_users_current_time()
    await bot2.send_message(message.chat.id, f'На момент последней проверки: *{datetime.now()}* в боте:\n'
                                             f'Живые: {get_users_live}\n'
                                             f'Мертвые: {inactive_users_count}\n'
                                             f'Суммарно проверено: {users_count}\n'
                                             f'На текущий момент, в боте: *{get_users_cur_time}*',
                            reply_markup=quit_button,
                            parse_mode='Markdown')


# Функция для выхода из статистики
@dp2.message_handler(text="Выйти")
async def quit_to_lobby(message: types.Message):
    await cmd_start(message)


# Функция добавления ссылок в базу данных
@dp2.message_handler(text="🔗Добавить ссылку")
async def add_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot2.send_message(message.from_user.id, "<b>Скиньте ссылку на канал</b>")

    await state.reset_state()
    await Links.first()


# Продолжение добавления ссылки в базу данных
@dp2.message_handler(state=Links.link)
async def get_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["link"] = message.text

    state_data = await state.get_data()
    link = state_data["link"]

    await message.answer("<b>Ссылка успешно добавлена!</b>")

    await add_link_to_db(link)
    await state.reset_state()
