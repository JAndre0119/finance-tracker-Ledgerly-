from app.extensions import db
from flask_login import UserMixin
from datetime import date


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    transactions = db.relationship("Transaction", backref="user", lazy=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    # "income" or "expense"
    type = db.Column(db.String(10), nullable=False)
    note = db.Column(db.String(200))
    transaction_date = db.Column(db.Date, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
