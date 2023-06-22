from aiogram import Bot, executor

from utils.connect_db import con
from utils.db_functions import create_table, create_table_link
from loader import dp, dp2


# Функция, выполняющая создание таблиц при старте бота
async def on_startup(dispatcher):
    await create_table()
    await create_table_link()


# Функция, которая закрывает базу данных после остановки бота
async def on_shutdown(dispatcher):
    con.close()

# Debugger - подключение бота
if __name__ == '__main__':
    from handlers.admins import admin_panel
    from handlers.users import user_panel
    print("                                                      ████ \n ░░███                                               ░░███ \n ███████   █████ ███ █████  ██████  ████████   █████  ░███ \n░░░███░   ░░███ ░███░░███  ███░░███░░███░░███ ███░░   ░███ \n  ░███     ░███ ░███ ░███ ░███████  ░███ ░░░ ░░█████  ░███ \n  ░███ ███ ░░███████████  ░███░░░   ░███      ░░░░███ ░███ \n  ░░█████   ░░████░████   ░░██████  ░███████  ██████  █████\n   ░░░░░     ░░░░ ░░░░     ░░░░░░  ░░░░░     ░░░░░░  ░░░░░ \n                                                           \n                                                           \n                                                           \nBot started successfully")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    # executor.start_polling(dp2, on_startup=on_startup, on_shutdown=on_shutdown)
    print("Bot stopped")

