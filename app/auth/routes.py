from flask import Blueprint, flash, render_template, redirect, request, session, url_for
import sqlite3
from .utils import check_valid_password, is_logged_in
from app.database.utils import get_db, create_users_table, get_cursor
from app.extensions import bcrypt

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """ Get username and password then insert into database """

    if is_logged_in():
        return redirect(url_for("home.home"))

    if request.method == "POST":
        
        name = request.form.get("username").strip()
        password = request.form.get("password").strip()
        
        if not name or not password:
            flash("Input must be valid")
            return redirect(url_for('auth.signup'))
        
        if not check_valid_password(password):
            flash("Password must include 6 or more characters and one uppercase letter ")
            return redirect(url_for("auth.signup"))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        with get_db() as conn:
            create_users_table(conn)
            with get_cursor(conn) as cur:
                try:
                    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                            (name, hashed_password))

                except sqlite3.IntegrityError:
                    flash("User Already Exists")
                    return redirect(url_for("auth.signup"))
            conn.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for("home.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with get_db() as conn: 
            # Get users info through username match
            create_users_table(conn)

            with get_cursor(conn) as cur:
                cur.execute("SELECT * FROM users WHERE username = ?", (username,))
                user_info = cur.fetchone()


        # If password does not match or user doesn't exist
        if not user_info or not bcrypt.check_password_hash(user_info["password"], password):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))


        session["username"] = user_info["username"]
        session["logged_in"] = True
        session.permanent = True

        return redirect(url_for("home.home"))
    return render_template("login.html")
    
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))