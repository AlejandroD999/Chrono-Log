from flask import Flask, after_this_request, flash, render_template, redirect, request, session, url_for
from flask_bcrypt import Bcrypt
from datetime import timedelta
from users.utils import *
import secrets
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(22)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=3)

@app.route("/")
def home():
    if is_logged_in():
        return render_template("home/home.html")
    else:
        return redirect(url_for('login'))

@app.route("/about")
def about():
    if is_logged_in():
        return render_template("home/about.html")
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)