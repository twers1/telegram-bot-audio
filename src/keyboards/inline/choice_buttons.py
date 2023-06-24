from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Кнопочки бота
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('🗣Хочу голосовое сообщение!'))

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add(KeyboardButton('🗣Хочу голосовое сообщение!'), KeyboardButton(text='Админ-панель'))

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add(KeyboardButton('👱‍♂️Посмотреть статистику'))
admin_panel.add(KeyboardButton('🔗Добавить ссылку'))

# language = ReplyKeyboardMarkup(resize_keyboard=True)
# language.add(KeyboardButton(text='ru'))

subscribe_to_channels0 = InlineKeyboardButton("Правила", callback_data="rules")
subscribe_to_channels1 = InlineKeyboardButton("Наш канал", url="https://t.me/dsfgbmnjmlhj")
subscribe_to_channels3 = InlineKeyboardButton("Проверка подписки✅", callback_data="check_subbed")

keyboard_open = InlineKeyboardMarkup().add(subscribe_to_channels0).add(subscribe_to_channels1).add(subscribe_to_channels3)

quit_button = ReplyKeyboardMarkup(resize_keyboard=True)
quit_button.add(KeyboardButton('Выйти'))

