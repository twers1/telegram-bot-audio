import asyncio
import json
import os, subprocess
import speech_recognition as sr
from google.cloud import speech

from io import BytesIO

from aiogram import types
from aiogram.types import CallbackQuery

from gtts import gTTS

from src.keyboards.inline.choice_buttons import main, main_admin, keyboard_open
from src.loader import bot, dp
from src.utils.db_functions import add_users, add_users_func, get_links

from datetime import datetime

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

# Create the directory if it doesn't exist
os.makedirs("temp", exist_ok=True)

# Create an empty audio file if it doesn't exist
audio_file_path = "temp/audio.ogg"
if not os.path.exists(audio_file_path):
    with open(audio_file_path, "wb") as file:
        pass

def remove_audio_files():
    if os.path.exists("temp/audio.ogg"):
        os.remove("temp/audio.ogg")
    if os.path.exists("temp/audio.wav"):
        os.remove("temp/audio.wav")


def audio_to_text(audio_data):
    LANG = 'ru'
    audio_data_bytes = audio_data.read()  # Convert `_io.BytesIO` to bytes
    with open("temp/audio.ogg", "wb") as file:
        file.write(audio_data_bytes)

    # Converting to WAV
    process = subprocess.run(["ffmpeg", "-i", "temp/audio.ogg", "temp/audio.wav"])
    if process.returncode != 0:
        raise Exception("Something went wrong")

    with sr.AudioFile("temp/audio.wav") as source:
        r = sr.Recognizer()
        audio = r.record(source)
        try:
            # Convert the audio file to text using Google Cloud Speech API
            # Write the heard text to a text variable
            audio_text = r.recognize_google(audio, language=LANG)
            response = audio_text
        except:
            response = "Words not recognized. Please, try again!"

    # Removing files after convertion to text
    remove_audio_files()
    return response

r = sr.Recognizer()

# Загружает данные с env переменной в json
ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


# При нажатии /start - будет выводиться данная функция
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    start_time = datetime.now()

    await add_users(user_id, username, start_time)

    await message.reply("👋🏻 Привет!\n\n🖥 С помощью этого бота вы можете конвертировать текст в голосовое сообщение\n", reply_markup=main)

    if message.from_user.id in ADMIN_ID:
        await message.answer(f'Вы авторизовались как администратор', reply_markup=main_admin)


# Кнопка "Хочу голосовое сообщение". Там проверяется подписан ли человек на каналы и уже присылает голосовые сообщения
@dp.message_handler(text="🗣Хочу голосовое сообщение!")
async def convert_to(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    await add_users_func(user_id, username, used_voice=True)
    await bot.send_message(message.chat.id, 'Погнали получать голосовое сообщение\nВведите любой текст')

    @dp.message_handler()
    async def get_text(message: types.Message):
        print('ку-ку я тут')
        user_text = message.text
        user_id = message.from_user.id
        is_subbed = False
        for group_id in subscriptions.values():
            if await is_user_subscribed(user_id, group_id):
                is_subbed = True
                break

        links = await get_links()
        result = '\n '.join(links)

        if not is_subbed:
            await message.reply(
                f"Для того, чтобы получить голосовое сообщение тебе нужно подписаться на каналы ниже и просмотреть 10 первых постов."
                f" Это наши спонсоры и без них наш проект бы не существовал бесплатно."
                f" Без подписки голосовые сообщения не будут отправлены. Прочитай правила!!!"
                f"\nhttps://t.me/audio_26kadr_bot\nhttps://t.me/audio_26kadr_bot"
                f"\nhttps://t.me/audio_26kadr_bot\n {result}"
                f"Если отписаться, бот может не работать ",
                reply_markup=keyboard_open)
            return
        if message.text == user_text:
            await bot.send_message(message.chat.id, 'Начинаю конвертировать...')
            voice = await converter_text_to_voice(user_text)
            print('Начинаю конвертировать...')
            # старт
            conversion_message = await bot.send_message(message.chat.id, "⏳ Начало конвертации...")

            for i in range(10):
                progress_bar = '🟩' * i + '⬜️' * (10 - i)
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=conversion_message.message_id,
                    text=f"Прогресс конвертации: \n{progress_bar} {i * 10}%"
                )
                await asyncio.sleep(0.5)  # задержка

            voice = await converter_text_to_voice(user_text)

            # окончания
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=conversion_message.message_id,
                text="✅ Конвертация завершена!"
            )

            await bot.send_voice(message.from_user.id, voice)

        # await message.answer("Перейти к конвертации: ", reply_markup=language)


# Кнопка "Правила"
@dp.callback_query_handler(lambda query: query.data == 'rules')
async def process_rules(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Здесь будут простые правила")


# Кнопка "Проверка подписки"
@dp.callback_query_handler(lambda query: query.data == 'check_subbed')
async def check_subscribed(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    is_subbed = True

    # Проверяем, подписан ли пользователь на все каналы и просмотрел ли он первые 10 постов
    for group_id in subscriptions.values():
        if not await is_user_subscribed(user_id, group_id):
            is_subbed = False
            break
        # if not await has_user_viewed_posts(user_id, group_id, 10):
        #     is_subbed = False
        #     break

    if is_subbed:
        await bot.answer_callback_query(callback_query.id, text="Вы подписаны на все каналы и просмотрели первые 10 постов!")
    else:
        await bot.answer_callback_query(callback_query.id, text="Вы еще не подписались на все каналы или не просмотрели первые 10 постов.")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def start_get_text_message(message: types.Message):
    if message.text == '✍️Хочу текстовое сообщение!':
        print('Хочу текстовое сообщение!')
        await message.answer('Пришли голосовое сообщение')

@dp.message_handler(content_types=types.ContentType.VOICE)
async def start_get_voice_message(message: types.Message):
    if message.voice is None:
        await message.reply("Голосовое сообщение не обнаружено.")
        return

    # Download the audio file sent by the user
    file_info = await bot.get_file(message.voice.file_id)
    audio_file = await bot.download_file(file_info.file_path)

    # Converting speech to text
    audio_text = audio_to_text(audio_file)

    # Reply to the user with the converted text
    await message.reply(audio_text)
