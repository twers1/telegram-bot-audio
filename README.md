
<div align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/docker-support-grey">
<img alt="GitHub" src="https://img.shields.io/github/license/twers1/telegram-bot-audio">
<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/twers1/telegram-bot-audio">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/twers1/telegram-bot-audio">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/aiogram?logo=aiogram&label=aiogram">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/twers1/telegram-bot-audio">


<p>A bot that converts text into a voice message</p>
</div>

## How to install and start? 

```
python3 pip install -r requirements.txt

python3 main.py 

python3 admin.py
```

## Functions 

- converting text into a voice message 
- converting a voica message to text 
- channel subscription verification 
- viewing statistics 
- language selection (Russian, English)

## Stack

- Python. Aiogram
- PostgreSQL
- Docker

## Demo

User panel: 

Text-to-speech

![](https://github.com/twers1/telegram-bot-audio/blob/main/readfiles/demov1.gif)

Speech-to-text

![](https://github.com/twers1/telegram-bot-audio/blob/main/readfiles/gif2.gif)


If you are not subscribed: 

<img src="readfiles/img_2.png" width="300px">


Admin panel: 

<img src="readfiles/img.png" width="300px">
<img src="readfiles/img_1.png" width="300px">

## Docker

```
docker build -t bot .

docker run -e TOKEN= -e TOKEN2=  -e ADMIN_ID= -e DB_URI= bot

docker-compose up
```

## Support 

If you want to support me, click "🌟" on this project😊

### Further ideas

Add a "Settings" button with language selection, so that there is a translation of buttons, functions, etc.

# Бот, занимающийся конвертацией текста в голосовое сообщение

## Как установить и запустить бота?

```commandline
python3 pip install -r requirements.txt

python3 main.py 

python3 admin.py
```

## Функции 

- конвертация текста в голосовое сообщение 
- конвертация голосового сообщения в текст
- проверка подписки на канал 
- просмотр статистики 
- выборка языка(русский, английский)

## Технологии

- Python. Aiogram
- PostreSQL
- Docker

## Демонстрация 

Панель пользователя: 

Text-to-speech

![](https://github.com/twers1/telegram-bot-audio/blob/main/readfiles/demov1.gif)

Speech-to-text

![](https://github.com/twers1/telegram-bot-audio/blob/main/readfiles/gif2.gif)

Если не подписан: 

<img src="readfiles/img_2.png" width="300px">

Панель администратора:

<img src="readfiles/img.png" width="300px">
<img src="readfiles/img_1.png" width="300px">

## Docker 

```commandline
docker build -t bot .

docker run -e TOKEN= -e TOKEN2=  -e ADMIN_ID= -e DB_URI= bot

docker-compose up
```

## Поддержка

Если хотите поддержать меня, то нажмите "🌟" на этот проект😊

### Дальнейшие идеи

Добавить кнопку "Настройки" с выбором языка, чтобы был перевод кнопок, функций и тому подобное
