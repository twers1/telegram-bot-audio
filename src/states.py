from aiogram.dispatcher.filters.state import StatesGroup, State


# Класс, содержащий состояние для ссылок, чтобы их записывать в БД
class Links(StatesGroup):
    link = State()


# Класс, содержащий состояние для голосовых сообщений, чтобы распознавать их
class VoiceRecognitionStates(StatesGroup):
    WaitingForVoiceMessage = State()