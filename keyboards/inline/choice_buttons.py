from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('Запустить'))

subscribe_to_channels1 = InlineKeyboardButton("Канал №1", url="https://t.me/dsfgbmnjmlhj")
subscribe_to_channels3 = InlineKeyboardButton("Проверить подписку", callback_data="check_subbed")

keyboard_open = InlineKeyboardMarkup().add(subscribe_to_channels1).add(subscribe_to_channels3)

language = ReplyKeyboardMarkup(resize_keyboard=True)
language.add(KeyboardButton('ru'), KeyboardButton('en'))
