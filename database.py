import sqlite3
from config import Config

DB_NAME = Config.DB_NAME


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance REAL DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_balance(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result["balance"] if result else None


def update_balance(username, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE username = ?",
        (amount, username)
    )
    conn.commit()
    conn.close()


def transfer_money(sender, receiver, amount):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # verify receiver
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (receiver,))
        if cursor.fetchone() is None:
            conn.close()
            return "Receiver not found"

        cursor.execute("BEGIN")

        # deduct sender
        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE username = ? AND balance >= ?",
            (amount, sender, amount)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            conn.close()
            return "Insufficient balance or sender not found"

        # add receiver
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE username = ?",
            (amount, receiver)
        )

        # ledger record
        cursor.execute(
            "INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)",
            (sender, receiver, amount)
        )

        conn.commit()
        conn.close()
        return "Success"

    except Exception:
        conn.rollback()
        conn.close()
        return "Transfer failed"


def get_transactions(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sender, receiver, amount, timestamp
        FROM transactions
        WHERE sender = ? OR receiver = ?
        ORDER BY timestamp DESC
    """, (username, username))

    data = cursor.fetchall()
    conn.close()
    return data