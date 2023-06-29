import os
import subprocess
import speech_recognition as sr
from io import BytesIO

from gtts import gTTS

from src.loader import bot


# Список каналов, на которых нужно подписаться
subscriptions = {
    'channel2': "@dsfgbmnjmlhj"
}


# Функция, проверяющая подписку пользователя
async def is_user_subscribed(user_id: int, chat_id: str) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.is_chat_member() or member.is_chat_owner() or member.is_chat_admin() or member.is_chat_creator()


# Функция, которая конвертирует текст в голосовое сообщение
async def converter_text_to_voice(text: str) -> BytesIO:
    bytes_file = BytesIO()
    audio = gTTS(text=text, lang="ru")
    audio.write_to_fp(bytes_file)
    bytes_file.seek(0)
    return bytes_file


# Функция, которая конвертирует текст, который написан на английском языке в голосовое сообщение
async def converter_text_to_voice_en(text: str) -> BytesIO:
    bytes_file = BytesIO()
    audio = gTTS(text=text, lang="en")
    audio.write_to_fp(bytes_file)
    bytes_file.seek(0)
    return bytes_file

# Создайте каталог, если он не существует
os.makedirs("temp", exist_ok=True)

# Если не работает предыдущий код, то попробуйте этот
audio_file_path = "temp/audio.ogg"
if not os.path.exists(audio_file_path):
    with open(audio_file_path, "wb") as file:
        pass


# Функция для удаления после распознавания и окончания конвертации
def remove_audio_files():
    if os.path.exists("temp/audio.ogg"):
        os.remove("temp/audio.ogg")
    if os.path.exists("temp/audio.wav"):
        os.remove("temp/audio.wav")


# Функция конвертации голосового сообщения в текст
def audio_to_text(audio_data, language: str = 'ru-RU'):
    audio_data_bytes = audio_data.read()  # Convert `_io.BytesIO` to bytes
    with open("temp/audio.ogg", "wb") as file:
        file.write(audio_data_bytes)

    # Конвертация в WAV
    process = subprocess.run(["ffmpeg", "-i", "temp/audio.ogg", "temp/audio.wav"])
    if process.returncode != 0:
        raise Exception("Something went wrong")

    with sr.AudioFile("temp/audio.wav") as source:
        r = sr.Recognizer()
        audio = r.record(source)
        audio_text = r.recognize_google(audio)
        response = audio_text
        remove_audio_files()
        return response
        # except:
        #     response = "Слова не распознаны. Попробуйте еще раз!💔"
