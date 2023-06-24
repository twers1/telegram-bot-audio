from aiogram.dispatcher.filters.state import StatesGroup, State


# Класс, содержащий состояние для ссылок, чтобы их записывать в БД
class Links(StatesGroup):
    link = State()

