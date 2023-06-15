import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
admin_id = os.getenv("ADMIN_ID")
DB_URI = os.getenv('DB_URI')
BOT_NICKNAME = "audio_26kadr_bot"

