from aiogram.dispatcher.filters.state import StatesGroup, State


class Links(StatesGroup):
    link = State()


class Language(StatesGroup):
    lang = State()
    text = State()
