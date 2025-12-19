from flask import Blueprint, session, render_template, redirect, url_for, request
from app.auth.utils import is_logged_in
from app.database.utils import get_db, get_cursor, get_user_id, retrieve_all_summaries, create_summaries_table
from datetime import date as date_md
from .utils import error
home_bp = Blueprint('home', __name__, static_folder= 'static', template_folder='templates')


@home_bp.route("/")
def home():
    if not is_logged_in():
        return redirect(url_for('auth.login'))
    return render_template("home.html")


@home_bp.route("/summaries")
def summaries():

    if not is_logged_in():
        return redirect(url_for("auth.login"))

    user = session.get('username')

    if not user:
        return error()

    return render_template("summaries.html", summaries=retrieve_all_summaries(user))

@home_bp.route("/new-summary", methods=["POST"])
def new_summary():
    if not is_logged_in():
        return redirect(url_for("auth.login"))
    
    user = session["username"]
    title = request.form.get("summary_title") 
    date = request.form.get("summary_date")
    summary = request.form.get("summary_doc")

    if not user:
        return error()

    if not title:
        title = "untitled_summary"

    if not date:
        date = date_md.today()

    with get_db() as conn:
        user_id = get_user_id(conn, user)

        if not user_id:
            return error(title='Creation Failed', message='Creation of summary was unsuccessful')


        create_summaries_table(conn)
        with get_cursor(conn) as cur:
            cur.execute("""INSERT INTO summaries (user_id, title, date, summary) VALUES (?, ?, ?, ?)""",
                        (user_id, title, date, summary))

        conn.commit()

    return redirect(url_for("home.summaries"))    

@home_bp.route("/del-summary", methods=["POST"])
def del_summary():
    if not is_logged_in():
        return redirect(url_for("auth.login"))
    
    summary_id = request.form.get("summary_id")

    if not summary_id:
        return error()
    with get_db() as conn:
        create_summaries_table(conn)

        with get_cursor(conn) as cur:
            cur.execute("DELETE FROM summaries WHERE id = ?", (summary_id,))

        conn.commit()

    return redirect(url_for("home.summaries"))

@home_bp.route("/update-summary", methods=["POST"])
def update_summary():
    """ Backend for updating a summary"""
    if not is_logged_in():
        return redirect(url_for("auth.login"))
    
    summary_id = request.form.get("section_summary_id")
    new_title = request.form.get("section_title")
    new_date = request.form.get("section_date")
    new_summary = request.form.get("section_input")

    if not new_title:
        new_title = 'untitled_summary'
    if not new_date:
        new_date = date_md.today()

    if not summary_id:
        return redirect(url_for('home.summaries'))

    with get_db() as conn:
        create_summaries_table(conn)
        with get_cursor(conn) as cur:
            user_id = get_user_id(conn, session['username'])
            cur.execute("""UPDATE summaries SET title = ?, date = ?, summary = ? WHERE id = ? AND user_id = ?""",
                         (new_title, new_date, new_summary, summary_id, user_id))
            
        conn.commit()

    return redirect(url_for("home.summaries"))

@home_bp.route("/about")
def about():
    if not is_logged_in():
        return redirect(url_for("auth.login"))
    return render_template("about.html")