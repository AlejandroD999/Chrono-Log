from . import *
from flask import Blueprint
from .utils import check_valid_password, create_bcrypt, get_db

users = Blueprint('users',__name__, static_folder="static", template_folder="templates")

@users.route("/login", methods=["GET", "POST"])
def login():

    bcrypt = create_bcrypt()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # TODO Close database cursor and do try & except
        
        db = get_db()
        cur = db.cursor()
        # Get users When username, and password match
        cur.execute("SELECT * FROM users WHERE username == ?", (username,))
        user_info = cur.fetchone()
        db.commit()


        # If password does not match or user doesn't exist
        if not user_info or not bcrypt.check_password_hash(user_info["password"], password):
            flash("Invalid username or password")
            return redirect("/login")


        session["username"] = user_info["username"]
        session["logged_in"] = True
        session.permanent = True

        return redirect(url_for("home"))

    else:
        return render_template("auth/login.html")
    
@users.route("/signup", methods=["GET", "POST"])
def signup():
    """ Get username and password then insert into database """

    # TODO Add username, and password limitations

    bcrypt = create_bcrypt()

    if request.method == "POST":
        # TODO Make input more secure from user
        
        name = request.form.get("username")
        # Hash password  
        password = request.form.get("password")

        if not check_valid_password(password):
            flash("Password must include 6 or more characters")
            return redirect(url_for("signup"))
        
        if not name or not password:
            flash("Input must be valid")
            return redirect(url_for('signup'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        


        try:

            db = get_db()
            cur = db.cursor()

            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                        (name, hashed_password))
            
            db.commit()
            db.close()

        except sqlite3.IntegrityError:
            flash("User Already Exists")
            return redirect("/signup")


        return redirect("/login")

    return render_template("auth/signup.html")