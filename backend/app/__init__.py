from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.extensions import db, login_manager, bcrypt


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ledgerly.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Allow the Vite dev server to make credentialed requests
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Return JSON 401 instead of redirecting to a login page
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "Authentication required"}), 401

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.transactions import transactions_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(transactions_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
