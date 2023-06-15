from utils.connect_db import con, cursor_obj


# Table users
async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    referral_id INT,
    username TEXT,
    subscribers INT,
    id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


async def add_users(user_id, username):
    # проверяем наличие пользователя в базе данных
    cursor_obj.execute("""SELECT * FROM users WHERE user_id = %s""", (user_id,))
    existing_user = cursor_obj.fetchone()

    if not existing_user:
        # если пользователя нет в базе данных, добавляем его
        cursor_obj.execute("INSERT INTO users (user_id, username) VALUES (%s, %s)", (user_id, username))
        con.commit()


async def get_users():
    cursor_obj.execute("""SELECT user_id, username, subscribers FROM users""")
    return cursor_obj.fetchall()


async def remove_user_from_db(user_id):
    cursor_obj.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
    con.commit()


async def get_users_count():
    cursor_obj.execute("SELECT COUNT(*) FROM users")
    count = cursor_obj.fetchone()[0]
    print(f"Количество пользователей, зашедших в бота: {count}")
    return count



