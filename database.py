import sqlite3
from config import DB_PATH


# Создание таблицы для белого списка
def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS whitelist (
                user_id INTEGER PRIMARY KEY
            )
        """)
        conn.commit()


# Добавление пользователя в белый список
def add_user_to_whitelist(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO whitelist (user_id)
            VALUES (?)
        """, (user_id,))
        conn.commit()


# Проверка, разрешен ли пользователь (по user_id)
def is_user_allowed(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM whitelist WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None
