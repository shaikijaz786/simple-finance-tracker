import sqlite3
import pandas as pd

DB_NAME = "finance.db"

def init_db():
    """Creates the database and table if they don't exist yet."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction_to_db(title, amount, type_trans, category):
    """Inserts a new transaction row into the table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (title, amount, type, category) VALUES (?, ?, ?, ?)",
        (title, amount, type_trans, category)
    )
    conn.commit()
    conn.close()

def get_all_transactions():
    """Fetches all rows and returns them directly as a Pandas DataFrame."""
    conn = sqlite3.connect(DB_NAME)
    # Pandas can read SQL queries directly into a DataFrame!
    df = pd.read_sql_query("SELECT title AS Name, amount AS Amount, type AS Type, category AS Category FROM transactions", conn)
    conn.close()
    return df

def clear_db():
    """Deletes all records from the table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()