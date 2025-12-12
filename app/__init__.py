from datetime import timedelta
from flask import Flask
from .extensions import bcrypt
import secrets
import os

database = os.path.join(os.path.dirname(__file__), "database.db")

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

    bcrypt.init_app(app)

    from .auth.routes import auth
    from .home.routes import home_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(home_bp)

    return app
