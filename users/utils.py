from . import Bcrypt, sqlite3, session

def get_db():
    conn = sqlite3.connect("data/users.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_bcrypt(app):
    return Bcrypt(app)

def check_valid_password(password):

    if len(password) < 6:
        return False
    
def is_logged_in():
    if 'logged_in' in session and session["logged_in"]:
        return True
    return False