import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    flask_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret",
    })

    yield flask_app

    with flask_app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, username="alice", email="alice@example.com", password="password123"):
    return client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": password},
    )


@pytest.fixture
def auth_client(client):
    """A test client that is registered and logged in as a default user."""
    response = register(client)
    assert response.status_code == 201
    return client


@pytest.fixture
def second_auth_client(app):
    """A second, independently-authenticated client for cross-user ownership tests."""
    other_client = app.test_client()
    response = register(other_client, username="bob", email="bob@example.com", password="password123")
    assert response.status_code == 201
    return other_client