import sqlite3
from contextlib import contextmanager
from . import database
@contextmanager
def get_db():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
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

def create_summaries_table(conn):
    summaries_query = """CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                summary TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
    
    with get_cursor(conn) as cur:
        cur.execute(summaries_query)

    conn.commit()

def get_user_id(conn, user_name):
    create_users_table(conn)

    with get_cursor(conn) as cur:
        cur.execute("SELECT id FROM users WHERE username = ?", (user_name,))
        row = cur.fetchone()
    return row["id"] if row else None

def retrieve_all_summaries(user):
    """ returns a dict of all summaries """
    
    with get_db() as conn:
        create_summaries_table(conn)
        create_users_table(conn)
        with get_cursor(conn) as cur:
            cur.execute("""SELECT * FROM users as usr 
                        JOIN summaries as smr 
                        ON usr.id = smr.user_id WHERE usr.username = ?""", (user,))
            summaries = cur.fetchall()

    return summaries

