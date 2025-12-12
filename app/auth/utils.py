from flask import session

def check_valid_password(password):
    if len(password) >= 5:
        return True
    return False

    
def is_logged_in():
    if 'logged_in' in session and session["logged_in"]:
        return True
    return False