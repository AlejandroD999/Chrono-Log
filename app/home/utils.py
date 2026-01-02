from flask import render_template

def error(title='Oops...', message='A problem has occurred'):
    """ Function to manage error pop-up"""
    if not title or not message:
        return
    return render_template('error.html', error_title=title, error_message=message)