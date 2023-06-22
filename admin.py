from aiogram import Bot, executor

from utils.connect_db import con
from utils.db_functions import create_table, create_table_link
from loader import dp2


async def on_startup(dispatcher):
    await create_table()
    await create_table_link()


async def on_shutdown(dispatcher):
    con.close()

# Подключение второго бота. Админ
if __name__ == '__main__':
    from handlers.admins import admin_panel2
    print("                                                      ████ \n ░░███                                               ░░███ \n ███████   █████ ███ █████  ██████  ████████   █████  ░███ \n░░░███░   ░░███ ░███░░███  ███░░███░░███░░███ ███░░   ░███ \n  ░███     ░███ ░███ ░███ ░███████  ░███ ░░░ ░░█████  ░███ \n  ░███ ███ ░░███████████  ░███░░░   ░███      ░░░░███ ░███ \n  ░░█████   ░░████░████   ░░██████  ░███████  ██████  █████\n   ░░░░░     ░░░░ ░░░░     ░░░░░░  ░░░░░     ░░░░░░  ░░░░░ \n                                                           \n                                                           \n                                                           \nBot started successfully")
    executor.start_polling(dp2, on_startup=on_startup, on_shutdown=on_shutdown)
    print("Bot stopped")

