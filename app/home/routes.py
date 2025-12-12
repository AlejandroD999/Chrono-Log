from flask import Blueprint, render_template, redirect, url_for
from app.auth.utils import is_logged_in

home_bp = Blueprint('home', __name__, static_folder= 'static', template_folder='templates')

@home_bp.route("/")
def home():
    if is_logged_in():
        return render_template("home.html")
    else:
        return redirect(url_for('auth.login'))

@home_bp.route("/summaries")
def summaries():
    if is_logged_in():
        return render_template("summaries.html")
    else:
        return redirect(url_for("auth.login"))

@home_bp.route("/about")
def about():
    if is_logged_in():
        return render_template("about.html")
    else:
        return redirect(url_for("auth.login"))