from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

# Кнопочки бота
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('🗣Хочу голосовое сообщение!'),
         KeyboardButton('✍️Хочу текстовое сообщение!'))

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add(KeyboardButton('🗣Хочу голосовое сообщение!'),
               KeyboardButton('✍️Хочу текстовое сообщение!'),
               KeyboardButton('Админ-панель'))

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add(KeyboardButton('👱‍♂️Посмотреть статистику'))
admin_panel.add(KeyboardButton('🔗Добавить ссылку'))

subscribe_to_channels0 = InlineKeyboardButton("Правила", callback_data="rules")
subscribe_to_channels1 = InlineKeyboardButton("Наш канал", url="https://t.me/dsfgbmnjmlhj")
subscribe_to_channels3 = InlineKeyboardButton("Проверка подписки✅", callback_data="check_subbed")

keyboard_open = InlineKeyboardMarkup().add(subscribe_to_channels0)\
    .add(subscribe_to_channels1)\
    .add(subscribe_to_channels3)

quit_button = ReplyKeyboardMarkup(resize_keyboard=True)
quit_button.add(KeyboardButton('Выйти'))


# Функция, содержащая две кнопки для конвертации
async def language_buttons(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button_ru = types.InlineKeyboardButton(text='Русский 🇷🇺', callback_data='russian')
    button_eng = types.InlineKeyboardButton(text='Английский 🇺🇸', callback_data='english')
    keyboard.add(button_ru, button_eng)
    await message.reply('Выберите язык для распознавания речи', reply_markup=keyboard)


