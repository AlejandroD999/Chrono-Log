import sqlite3
from contextlib import contextmanager
from . import database
@contextmanager
def get_db():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_cursor(conn):
    cur = conn.cursor()
    try:
        yield cur
    finally:
        cur.close()

@contextmanager
def create_users_table(conn):
    table_query = """
            CREATE TABLE IF NOT EXISTS "users" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL); 
                """
    with get_cursor(conn) as cur:
        cur.execute(table_query)
        
        conn.commit()