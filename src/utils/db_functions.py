from datetime import datetime, timedelta

from src.utils.connect_db import con, cursor_obj


# Создание таблицы пользователей
async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    referral_id INT,
    username TEXT,
    subscribers INT,
    used_voice BOOLEAN,
    last_activity TIMESTAMP,
    start_time TIMESTAMP,
    id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


# Создание таблицы с ссылками
async def create_table_link():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS links (
    link TEXT,
    id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


# Функция добавление ссылки в базу данных
async def add_link_to_db(link):
    cursor_obj.execute("INSERT INTO links (link) VALUES (%s)", (link,))

    con.commit()


# Функция получения ссылок из базы данных
async def get_links():
    cursor_obj.execute("""SELECT link from links;""")
    links = cursor_obj.fetchall()
    return [link[0] for link in links]


# Функция добавления пользователя
async def add_users(user_id, username, start_time):
    # если пользователя нет в базе данных, добавляем его
    cursor_obj.execute("""
               INSERT INTO users (user_id, username, start_time, last_activity)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (user_id) DO UPDATE
               SET last_activity = EXCLUDED.last_activity;
           """, (user_id, username, start_time, datetime.now()))

    con.commit()


# Функция добавление столбца user_voice (не используется)
async def add_users_func(user_id, username, used_voice=False):
    # проверяем наличие пользователя в базе данных
    cursor_obj.execute("""SELECT * FROM users WHERE user_id = %s""", (user_id,))
    existing_user = cursor_obj.fetchone()

    if not existing_user:
        # если пользователя нет в базе данных, добавляем его
        cursor_obj.execute("INSERT INTO users (user_id, username, used_voice) VALUES (%s, %s, %s)", (user_id, username, used_voice))
        con.commit()
    elif not existing_user[2]:
        # если поле used_voice не установлено, устанавливаем его в true
        cursor_obj.execute("""UPDATE users SET used_voice = TRUE WHERE user_id = %s""", (user_id,))
        con.commit()


# Функция получения всех пользователей
async def get_users():
    cursor_obj.execute("""SELECT user_id, username, subscribers FROM users""")
    return cursor_obj.fetchall()


# Функция получения количества всех пользователей, которые зашли в бота
async def get_users_count():
    cursor_obj.execute("SELECT COUNT(*) FROM users")
    count = cursor_obj.fetchone()[0]
    print(f"Количество пользователей, зашедших в бота: {count}")
    return count


# Функция получения живых пользователей
async def get_live_users():
    # Определяем период времени, в течение которого пользователь должен был быть активным, чтобы считаться активным
    active_period = 1  # дни

    # Выбираем всех пользователей, которые были активны в течение последнего периода времени
    cursor_obj.execute("SELECT user_id FROM users WHERE last_activity >= (NOW() - INTERVAL '%s DAY')", (active_period,))
    active_users = set([row[0] for row in cursor_obj.fetchall()])

    # Считаем количество пользователей, которые были активны в течение предыдущего периода времени
    live_users = len(active_users)
    print(f"Количество пользователей, которые сейчас в боте: {live_users}")
    return live_users


# Функция получения мертвых пользователей
async def get_inactive_users_count():
    # Определяем период времени, в течение которого пользователь должен был быть активным, чтобы считаться активным
    active_period = 1 # дни
    period = timedelta(days=active_period)


    # Выбираем всех пользователей, которые были активны в течение последнего периода времени
    cursor_obj.execute("SELECT user_id FROM users WHERE last_activity >= NOW() - INTERVAL %s", (period,))
    active_users = set([row[0] for row in cursor_obj.fetchall()])

    # Получаем все ID пользователей из базы данных
    cursor_obj.execute("SELECT user_id FROM users")
    all_users = set([row[0] for row in cursor_obj.fetchall()])

    # Считаем количество пользователей, которые были неактивны в течение предыдущего периода времени
    inactive_users = all_users - active_users
    count = len(inactive_users)

    print(f"Количество пользователей, которые выключили вашего бота: {count}")
    return count


# Функция получения текущих пользователей, которые сейчас в боте
async def get_users_current_time():
    # Определяем период времени, в течение которого пользователь должен был быть активным, чтобы считаться активным
    active_period = 15  # минуты

    # Выбираем всех пользователей, которые были активны в течение последнего периода времени
    cursor_obj.execute("SELECT user_id FROM users WHERE last_activity >= (NOW() - INTERVAL '%s MINUTE')", (active_period,))
    active_users = set([row[0] for row in cursor_obj.fetchall()])

    # Считаем количество пользователей, которые были активны в течение последних 15 минут
    current_users = len(active_users)
    print(f"Количество пользователей, которые сейчас в боте(15 min): {current_users}")
    return current_users