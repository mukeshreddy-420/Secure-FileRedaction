
import sqlite3
import os

# Use environment variable for database path, default to app.db
DB_PATH = os.environ.get("DATABASE_PATH", "app.db")
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 email TEXT UNIQUE,
 password TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS downloads (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_email TEXT,
 filename TEXT,
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)''')

conn.commit()

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
