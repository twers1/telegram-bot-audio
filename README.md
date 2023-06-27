# A bot that converts text into a voice message

## How to install and start? 

```
python3 pip install -r requirements.txt

python3 main.py 
```

## Functions 

- converting text into a voice message 
- channel subscription verification 
- viewing statistics 
- language selection (Russian, English)

## Stack

- Python. Aiogram
- PostgreSQL

## Demo

User panel: 

![](https://github.com/twers1/telegram-bot-audio/blob/main/readfiles/demov1.gif)

Admin panel: 

<img src="readfiles/img.png" width="300px">
<img src="readfiles/img_1.png" width="300px">

## Docker

```
docker build -t bot .

docker run -e TOKEN= -e TOKEN2=  -e ADMIN_ID= -e DB_URI= bot

docker-compose up
```



# Бот, занимающийся конвертацией текста в голосовое сообщение

## Как установить и запустить бота?

```commandline
python3 pip install -r requirements.txt

python3 main.py 
```

## Функции 

- конвертация текста в голосовое сообщение 
- проверка подписки на канал 
- просмотр статистики 
- выборка языка(русский, английский)

## Технологии

- Python. Aiogram
- PostreSQL


## Демонстрация 

Панель пользователя: 

![](https://github.com/twers1/telegram-bot-audio/blob/main/readfiles/demov1.gif)

Панель администратора:

<img src="readfiles/img.png" width="300px">
<img src="readfiles/img_1.png" width="300px">

## Docker 

```commandline
docker build -t bot .

docker run -e TOKEN= -e TOKEN2=  -e ADMIN_ID= -e DB_URI= bot

docker-compose up
```
