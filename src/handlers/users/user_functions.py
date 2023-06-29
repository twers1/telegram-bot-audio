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


def voice_recognizer(language):
    subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])
    r = sr.Recognizer()
    with sr.AudioFile('audio.wav') as source:
        try:
            audio = r.record(source)
            text = r.recognize_google(audio, language=language)
        except:
            text = 'Слова не распознаны. Попробуйте еще раз!💔'
    return text

