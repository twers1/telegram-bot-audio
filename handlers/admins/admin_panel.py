import json
import os

from handlers.users.user_panel import send_welcome
from keyboards.inline.choice_buttons import admin_panel, quit_button
from loader import dp, bot
from aiogram import types


ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


@dp.message_handler(text="Админ-панель")
async def contacts(message: types.Message):
    print("Бот запущен(админ-панель)")
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(message.from_user.id, f'Вы вошли в админ-панель', reply_markup=admin_panel)


@dp.message_handler(text="👱‍♂️Посмотреть статистику")
async def statistics(message: types.Message):
    await bot.send_message(message.chat.id, f'Статистика бота: ')
    await bot.send_message(message.chat.id, f'Количество пользователей, которые на start: \n\n'
                                            f'Количество пользователей, которые пользовались функционалом отправки голосовых сообщений: \n\n'
                                            f'Количество пользователей, которые выключили бота: \n\n'
                                            f'Количество пользователей, которые удалились из телеграмма: ', reply_markup=quit_button)


@dp.message_handler(text="Выйти")
async def quit_to_lobby(message: types.Message):
    await send_welcome(message)






