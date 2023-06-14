from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('🗣Хочу голосовое сообщение!'))

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add(KeyboardButton('🗣Хочу голосовое сообщение!'), KeyboardButton('Админ-панель'))

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add(KeyboardButton('👱‍♂️Посмотреть статистику'))

subscribe_to_channels0 = InlineKeyboardButton("Правила", callback_data="rules")
subscribe_to_channels1 = InlineKeyboardButton("Наш канал", url="https://t.me/dsfgbmnjmlhj")
subscribe_to_channels3 = InlineKeyboardButton("Проверка подписки✅", callback_data="check_subbed")

keyboard_open = InlineKeyboardMarkup().add(subscribe_to_channels0).add(subscribe_to_channels1).add(subscribe_to_channels3)

language = ReplyKeyboardMarkup(resize_keyboard=True)
language.add(KeyboardButton(text='ru'), KeyboardButton(text='en'))
