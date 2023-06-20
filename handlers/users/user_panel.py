import json
import os
from io import BytesIO

from aiogram import types
from aiogram.types import CallbackQuery

from gtts import gTTS

from keyboards.inline.choice_buttons import main, keyboard_open, language, main_admin
from loader import bot, dp
from utils.db_functions import add_users, add_users_func, get_links

from datetime import datetime

subscriptions = {
    'channel2': "@dsfgbmnjmlhj"
}


async def is_user_subscribed(user_id: int, chat_id: str) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.is_chat_member() or member.is_chat_owner() or member.is_chat_admin() or member.is_chat_creator()


async def converter_text_to_voice(text: str) -> BytesIO:
    bytes_file = BytesIO()
    audio = gTTS(text=text, lang="ru")
    audio.write_to_fp(bytes_file)
    bytes_file.seek(0)
    return bytes_file


async def converter_text_to_voice_en(text: str) -> BytesIO:
    bytes_file = BytesIO()
    audio = gTTS(text=text, lang="en")
    audio.write_to_fp(bytes_file)
    bytes_file.seek(0)
    return bytes_file


ADMIN_ID = json.loads(os.getenv('ADMIN_ID'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    start_time = datetime.now()

    await add_users(user_id, username, start_time)

    await message.reply("👋🏻 Привет!\n\n🖥 С помощью этого бота вы можете конвертировать текст в голосовое сообщение\n", reply_markup=main)

    if message.from_user.id in ADMIN_ID:
        await message.answer(f'Вы авторизовались как администратор', reply_markup=main_admin)


@dp.message_handler(text="🗣Хочу голосовое сообщение!")
async def convert_to(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    await add_users_func(user_id, username, used_voice=True)
    await bot.send_message(message.chat.id, 'Выберите язык для конвертации', reply_markup=language)

    @dp.message_handler()
    async def get_text(message: types.Message):
        if message.text == 'ru':
            await bot.send_message(message.chat.id, 'Введите любой текст, а я конвертирую его в голосовое сообщение')
            voice = await converter_text_to_voice(message.text)
            print('Начинаю конвертировать...')
            await bot.send_message(message.chat.id, 'Начинаю конвертировать...')
            await bot.send_voice(message.from_user.id, voice)
        elif message.text == 'en':
            await bot.send_message(message.chat.id, 'Type any text and I will convert it into a voice message')
            print('Starting convert en...')
            await bot.send_message(message.chat.id, 'Starting convert...')
            voice = converter_text_to_voice_en(message.text)
            await bot.send_voice(message.from_user.id, voice)

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

        # await message.answer("Перейти к конвертации: ", reply_markup=language)


@dp.callback_query_handler(lambda query: query.data == 'rules')
async def process_rules(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Здесь будут простые правила")


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
