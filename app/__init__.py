from datetime import timedelta
from flask import Flask
from .extensions import bcrypt
import secrets


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping (
        SECRET_KEY = secrets.token_hex(22),
        PERMANENT_SESSION_LIFETIME = timedelta(days=3)
    )

    bcrypt.init_app(app)

    from .auth.routes import auth
    from .home.routes import home_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(home_bp)

    return app
