import os
import logging
import random
import string

from io import BytesIO

import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, ChatMemberStatus
from dotenv import load_dotenv
from gtts import gTTS

from keyboards.inline.choice_buttons import main, keyboard_open, language

load_dotenv()
bot = Bot(os.getenv('TOKEN'))

logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

subscriptions = {
    'channel2': "@dsfgbmnjmlhj"
}


async def is_user_subscribed(user_id: int, chat_id: str) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.is_chat_member() or member.is_chat_owner() or member.is_chat_admin() or member.is_chat_creator()


def converter_text_to_voice(text: str) -> BytesIO:
    bytes_file = BytesIO()
    audio = gTTS(text=text, lang="ru")
    audio.write_to_fp(bytes_file)
    bytes_file.seek(0)
    return bytes_file


def converter_text_to_voice_en(text: str) -> BytesIO:
    bytes_file = BytesIO()
    audio = gTTS(text=text, lang="en")
    audio.write_to_fp(bytes_file)
    bytes_file.seek(0)
    return bytes_file


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋🏻 Привет!\n🖥 С помощью этого бота вы можете конвертировать текст в голосовое сообщение\n", reply_markup=main)


@dp.message_handler(text="Запустить")
async def convert_to(message: types.Message):
    user_id = message.from_user.id
    is_subbed = False
    for group_id in subscriptions.values():
        if await is_user_subscribed(user_id, group_id):
            is_subbed = True
            break

    if not is_subbed:
        await message.reply("Для использования функции конвертации сначала подпишитесь на необходимые каналы.",
                            reply_markup=keyboard_open)
        return

    await message.answer("Перейти к конвертации: ", reply_markup=language)


@dp.message_handler(text="ru")
async def convert_to_ru(message: types.Message):
    await message.answer('Введите любой текст, а я конвертирую его в голосовое сообщение')

    @dp.message_handler()
    async def handle_user_text(message: types.Message):
        voice = converter_text_to_voice(message.text)
        await bot.send_voice(message.from_user.id, voice)


@dp.message_handler(text="en")
async def convert_to_en(message: types.Message):
    await message.answer('Type any text and I will convert it into a voice message')

    @dp.message_handler()
    async def handle_user_text(message: types.Message):
        voice = converter_text_to_voice_en(message.text)
        await bot.send_voice(message.from_user.id, voice)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)