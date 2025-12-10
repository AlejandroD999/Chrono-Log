from flask import Flask, after_this_request, flash, render_template, redirect, request, session, url_for
from flask_bcrypt import Bcrypt
import secrets
from datetime import timedelta
import sqlite3
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping (
        SECRET_KEY = secrets.token_hex(22),
        PERMANENT_SESSION_LIFETIME = timedelta(days=3)
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    else:
         app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .routes import users
    app.register_blueprint(users, url_prexi="/users")

    return app
