import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS numbers (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT UNIQUE, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
cursor.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
conn.commit()

def save_number(number):
    try:
        cursor.execute("INSERT OR IGNORE INTO numbers (number) VALUES (?)", (number,))
        conn.commit()
    except Exception as e:
        print("DB error:", e)

def save_chat(user_id, message):
    try:
        cursor.execute("INSERT INTO chats (user_id, message) VALUES (?, ?)", (str(user_id), message))
        conn.commit()
    except Exception as e:
        print("Chat DB error:", e)

def get_all_numbers():
    cursor.execute("SELECT number, timestamp FROM numbers ORDER BY timestamp DESC")
    return cursor.fetchall()

def get_all_chats():
    cursor.execute("SELECT user_id, message, timestamp FROM chats ORDER BY timestamp DESC")
    return cursor.fetchall()