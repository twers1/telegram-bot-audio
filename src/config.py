import os
from dotenv import load_dotenv

# Библиотека для загрузки данных из файла ENV
load_dotenv()

# Подключение переменных из файла ENV
TOKEN = os.getenv("TOKEN")
TOKEN2 = os.getenv("TOKEN2")
admin_id = os.getenv("ADMIN_ID")
DB_URI = os.getenv('DB_URI')
BOT_NICKNAME = "audio_26kadr_bot"