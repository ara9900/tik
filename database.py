# database.py

import sqlite3

conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# ایجاد جدول کاربران در صورت عدم وجود
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER PRIMARY KEY,
                   first_name TEXT,
                   last_name TEXT,
                   username TEXT,
                   balance INTEGER DEFAULT 0)''')
conn.commit()
