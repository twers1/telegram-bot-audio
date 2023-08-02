import asyncio
import json
import os

import speech_recognition as sr

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from src.handlers.users.user_functions import subscriptions, is_user_subscribed, converter_text_to_voice, \
    voice_recognizer, show_loading_animation
from src.keyboards.inline.choice_buttons import main, main_admin, keyboard_open, language_buttons
from src.loader import bot, dp
from src.states import VoiceRecognitionStates
from src.utils.db_functions import add_users, add_users_func, get_links

from datetime import datetime


r = sr.Recognizer()

# Загружает данные с env переменной в json. (для нескольких админов)
ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


# Стартовое меню.
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    start_time = datetime.now()

    await add_users(user_id, username, start_time)

    await message.reply("👋🏻 Привет!\n\n🤖Я бот, который поможет тебе записать голосовое сообщение"
                        "и распознавать голосовых сообщения людей\n", reply_markup=main)

    if message.from_user.id in ADMIN_ID:
        await message.answer(f'У вас есть преимущества! Вы администратор😎', reply_markup=main_admin)


# Функция получения голосового сообщения.
@dp.message_handler(text="🗣Хочу голосовое сообщение!")
async def convert_to(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    await add_users_func(user_id, username, used_voice=True)
    await bot.send_message(message.chat.id, 'Погнали получать голосовое сообщение!\n'
                                            'Для этого напиши любой текст и отправь мне')

    # Функция логики проверки подписки на канал
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
        # Получение ссылок из базы данных
        links = await get_links()
        result = '\n '.join(links)

        if not is_subbed:
            await message.reply(
                f"Для того, чтобы получить голосовое сообщение тебе нужно подписаться на каналы ниже"
                f" и просмотреть 10 первых постов."
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
            # Старт анимации для пользователя
            conversion_message = await bot.send_message(message.chat.id, "⏳ Начало конвертации...")

            for i in range(10):
                progress_bar = '🟩' * i + '⬜️' * (10 - i)
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=conversion_message.message_id,
                    text=f"Прогресс конвертации: \n{progress_bar} {i * 10}%"
                )
                await asyncio.sleep(0.5)  # Задержка на 0.5 секунд

            voice = await converter_text_to_voice(user_text)

            # Окончание анимации
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=conversion_message.message_id,
                text="✅ Конвертация завершена!"
            )

            await bot.send_voice(message.from_user.id, voice)


# Функция для написания правил
@dp.callback_query_handler(lambda query: query.data == 'rules')
async def process_rules(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Здесь будут простые правила")


# Функция для проверки подписки.
@dp.callback_query_handler(lambda query: query.data == 'check_subbed')
async def check_subscribed(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    is_subbed = True

    # Проверяем, подписан ли пользователь на все каналы и просмотрел ли он первые 10 постов
    for group_id in subscriptions.values():
        if not await is_user_subscribed(user_id, group_id):
            is_subbed = False
            break

    if is_subbed:
        await bot.answer_callback_query(callback_query.id, text="Вы подписаны на все каналы"
                                                                " и просмотрели первые 10 постов! Вы лучший❤️")
    else:
        await bot.answer_callback_query(callback_query.id, text="Вы еще не подписались на все каналы"
                                                                " или не просмотрели первые 10 постов! Вы плохой💔")


# Функция для получения распознавания голосового сообщения
@dp.message_handler(content_types=types.ContentType.TEXT, text="✍️Хочу текстовое сообщение!")
async def start_get_text_message(message: types.Message):
    if message.text == '✍️Хочу текстовое сообщение!':
        print('Хочу текстовое сообщение!')
        await message.answer('Пришли голосовое сообщение, а я его распознаю его в речь🗣')

        @dp.message_handler(content_types=types.ContentType.VOICE)
        async def voice_handler(message: types.Message, state: FSMContext):
            file_id = message.voice.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path

            file_size = file_info.file_size
            if int(file_size) >= 715000:
                await message.reply('Слишком большое голосовое сообщение!😔')
            else:
                await file_info.download(destination='audio.ogg')
                await VoiceRecognitionStates.WaitingForVoiceMessage.set()
                await language_buttons(message)


# Функция выборки языка и продолжение конвертации голосового сообщения в текст
@dp.callback_query_handler(lambda call: True, state=VoiceRecognitionStates.WaitingForVoiceMessage)
async def buttons(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    if call.data == 'russian':
        # Показ анимации загрузки перед обработкой голосового сообщения
        await show_loading_animation(call.message)
        # await bot.send_message(call.from_user.id, 'Загрузка завершена☺')
        text = voice_recognizer('ru_RU')
        await bot.send_message(call.from_user.id, text)
        os.remove('audio.wav')
        os.remove('audio.ogg')
    elif call.data == 'english':
        await show_loading_animation(call.message)
        await bot.send_message(call.from_user.id, 'Загрузка завершена☺')
        text = voice_recognizer('en_EN')
        await bot.send_message(call.from_user.id, text)
        os.remove('audio.wav')
        os.remove('audio.ogg')

    await state.finish()