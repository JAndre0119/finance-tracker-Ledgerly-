# Holds the app factory and that app is a package 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv
import os

# Global db object, doesn't connect to anything yet (called extension initialization)
db = SQLAlchemy()

# Creates, configures, and returns a Flask app
# Better than app = Flask(__name__) at top level and scales cleanly
def create_app():
    # Reads your .env file and loads, without it, os.getenv() would return None
    load_dotenv()

    app = Flask(__name__)
    # Used for sessions, cookies, and CSRF protection
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    # Tells SQLAlchemy which db to connect to
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ledgerly.db"
    # Disables an unncecessary feature to reduce memory usage and silence warnings 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Attaches SQLAlchemy to this specific Flask app, now models can talk to the DB
    # What actually connects your db object to the app
    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app