from flask import session

def check_valid_password(password):
    if len(password) > 5 and any_upper(password):
        return True
    return False

def any_upper(string):
    return (any(char.isupper() for char in string))
    
def is_logged_in():
    if 'logged_in' in session and session["logged_in"]:
        return True
    return False