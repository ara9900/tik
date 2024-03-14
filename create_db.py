import sqlite3

# Connect to the database (create it if it doesn't exist)
conn = sqlite3.connect('bot.db')
c = conn.cursor()

# Create the users table
c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 first_name TEXT,
                 last_name TEXT,
                 telegram_id INTEGER UNIQUE,
                 user_id TEXT UNIQUE,
                 wallet_balance REAL DEFAULT 0)''')

# Create other tables if needed (e.g., orders, subscriptions)
# ...

# Save changes and close the connection
conn.commit()
conn.close()
