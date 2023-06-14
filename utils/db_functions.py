from utils.connect_db import con, cursor_obj


# Table users
async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL,
    username TEXT,
    subscribers INT,
    id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


async def add_users(user_id, username):
    cursor_obj.execute("INSERT INTO users (user_id, username) VALUES (%s, %s)", (user_id, username))
    con.commit()


async def get_users():
    cursor_obj.execute("""SELECT user_id, username, subscribers FROM users""")
    return cursor_obj.fetchall()

