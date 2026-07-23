"""Unit tests for the SQLAlchemy models, independent of the HTTP layer."""
from datetime import date

import pytest

from app.models import Transaction, User


def test_transaction_date_defaults_to_today(db):
    user = User(username="alice", email="alice@example.com", password_hash="hash")
    db.session.add(user)
    db.session.commit()

    transaction = Transaction(amount=10, category="food", type="expense", user_id=user.id)
    db.session.add(transaction)
    db.session.commit()

    assert transaction.transaction_date == date.today()


def test_transaction_belongs_to_user(db):
    user = User(username="alice", email="alice@example.com", password_hash="hash")
    db.session.add(user)
    db.session.commit()

    transaction = Transaction(amount=10, category="food", type="expense", user_id=user.id)
    db.session.add(transaction)
    db.session.commit()

    assert transaction.user is user
    assert list(user.transactions) == [transaction]


def test_user_username_must_be_unique(db):
    db.session.add(User(username="alice", email="a1@example.com", password_hash="hash"))
    db.session.commit()

    db.session.add(User(username="alice", email="a2@example.com", password_hash="hash"))
    with pytest.raises(Exception):
        db.session.commit()