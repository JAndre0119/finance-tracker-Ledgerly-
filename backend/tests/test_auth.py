"""Integration tests for /api/auth/* endpoints."""


def test_register_success(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "password123"},
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["username"] == "alice"
    assert body["email"] == "alice@example.com"
    assert "id" in body
    assert "password" not in body
    assert "password_hash" not in body


def test_register_missing_fields(client):
    response = client.post("/api/auth/register", json={"username": "alice"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "All fields required"


def test_register_duplicate_username(client):
    client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "different@example.com", "password": "password123"},
    )

    assert response.status_code == 409
    assert response.get_json()["error"] == "Username already taken"


def test_register_duplicate_email(client):
    client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "password123"},
    )
    response = client.post(
        "/api/auth/register",
        json={"username": "different", "email": "alice@example.com", "password": "password123"},
    )

    assert response.status_code == 409
    assert response.get_json()["error"] == "Email already registered"


def test_register_logs_user_in(client):
    client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "password123"},
    )
    response = client.get("/api/auth/me")

    assert response.status_code == 200
    assert response.get_json()["username"] == "alice"


def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "password123"},
    )
    client.post("/api/auth/logout")

    response = client.post(
        "/api/auth/login", json={"username": "alice", "password": "password123"}
    )

    assert response.status_code == 200
    assert response.get_json()["username"] == "alice"


def test_login_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "password123"},
    )
    client.post("/api/auth/logout")

    response = client.post(
        "/api/auth/login", json={"username": "alice", "password": "wrong-password"}
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"


def test_login_unknown_username(client):
    response = client.post(
        "/api/auth/login", json={"username": "nobody", "password": "password123"}
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"


def test_logout_requires_login(client):
    response = client.post("/api/auth/logout")

    assert response.status_code == 401


def test_logout_success(auth_client):
    response = auth_client.post("/api/auth/logout")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Logged out"

    # session should no longer be authenticated
    me_response = auth_client.get("/api/auth/me")
    assert me_response.status_code == 401


def test_me_unauthenticated(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Not authenticated"


def test_me_authenticated(auth_client):
    response = auth_client.get("/api/auth/me")

    assert response.status_code == 200
    body = response.get_json()
    assert body["username"] == "alice"
    assert body["email"] == "alice@example.com"