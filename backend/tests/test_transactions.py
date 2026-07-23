"""Integration tests for /api/transactions endpoints, including coverage of
the income/expense/net summary calculation returned alongside the list.

NOTE: there is no update (PUT/PATCH) endpoint for transactions anywhere in
the backend, frontend API client, or README, so this suite only covers
create / fetch / delete, per the existing API surface.
"""
import pytest


def create_transaction(client, **overrides):
    payload = {
        "amount": 25.5,
        "category": "groceries",
        "type": "expense",
        "note": "weekly shop",
    }
    payload.update(overrides)
    return client.post("/api/transactions", json=payload)


# ---- create ----------------------------------------------------------


def test_create_transaction_success(auth_client):
    response = create_transaction(auth_client, amount=42.5, category="food", type="expense", note="lunch")

    assert response.status_code == 201
    body = response.get_json()
    assert body["amount"] == 42.5
    assert body["category"] == "food"
    assert body["type"] == "expense"
    assert body["note"] == "lunch"
    assert "id" in body
    assert "transaction_date" in body


def test_create_transaction_defaults_date_to_today(auth_client):
    import datetime

    response = create_transaction(auth_client)

    assert response.status_code == 201
    assert response.get_json()["transaction_date"] == datetime.date.today().isoformat()


def test_create_transaction_with_explicit_date(auth_client):
    response = create_transaction(auth_client, transaction_date="2026-01-15")

    assert response.status_code == 201
    assert response.get_json()["transaction_date"] == "2026-01-15"


def test_create_transaction_requires_auth(client):
    response = create_transaction(client)

    assert response.status_code == 401


@pytest.mark.parametrize("missing_field", ["amount", "category", "type"])
def test_create_transaction_missing_required_field(auth_client, missing_field):
    payload = {"amount": 10, "category": "food", "type": "expense"}
    del payload[missing_field]

    response = auth_client.post("/api/transactions", json=payload)

    assert response.status_code == 400
    assert response.get_json()["error"] == "amount, category, and type are required"


def test_create_transaction_invalid_type(auth_client):
    response = create_transaction(auth_client, type="savings")

    assert response.status_code == 400
    assert response.get_json()["error"] == "type must be 'income' or 'expense'"


def test_create_transaction_invalid_date_format(auth_client):
    response = create_transaction(auth_client, transaction_date="15-01-2026")

    assert response.status_code == 400
    assert response.get_json()["error"] == "transaction_date must be YYYY-MM-DD"


def test_create_transaction_zero_amount_is_rejected(auth_client):
    """Flagged bug: `if not amount` treats amount=0 as missing (0 is falsy
    in Python), so a legitimate zero-amount transaction is rejected with
    the same error as an actually-missing amount. Documented, not fixed."""
    response = create_transaction(auth_client, amount=0)

    assert response.status_code == 400
    assert response.get_json()["error"] == "amount, category, and type are required"


def test_create_transaction_non_string_date_raises_unhandled_error(auth_client):
    """Flagged bug: a non-string transaction_date bypasses the ValueError
    guard around strptime and raises an unhandled TypeError (500 in
    production) instead of the intended 400 response. Documented, not
    fixed. TESTING=True propagates the exception to the test client."""
    with pytest.raises(TypeError):
        create_transaction(auth_client, transaction_date=12345)


# ---- fetch / summary ---------------------------------------------------


def test_get_transactions_empty(auth_client):
    response = auth_client.get("/api/transactions")

    assert response.status_code == 200
    body = response.get_json()
    assert body["transactions"] == []
    assert body["summary"] == {"income": 0, "expenses": 0, "net": 0}


def test_get_transactions_requires_auth(client):
    response = client.get("/api/transactions")

    assert response.status_code == 401


def test_get_transactions_returns_only_own_transactions(auth_client, second_auth_client):
    create_transaction(auth_client, category="mine")
    create_transaction(second_auth_client, category="theirs")

    response = auth_client.get("/api/transactions")

    body = response.get_json()
    assert len(body["transactions"]) == 1
    assert body["transactions"][0]["category"] == "mine"


def test_get_transactions_ordered_by_date_descending(auth_client):
    create_transaction(auth_client, category="oldest", transaction_date="2026-01-01")
    create_transaction(auth_client, category="newest", transaction_date="2026-03-01")
    create_transaction(auth_client, category="middle", transaction_date="2026-02-01")

    body = auth_client.get("/api/transactions").get_json()

    categories = [t["category"] for t in body["transactions"]]
    assert categories == ["newest", "middle", "oldest"]


def test_summary_calculation_income_and_expenses(auth_client):
    create_transaction(auth_client, amount=1000, type="income", category="salary")
    create_transaction(auth_client, amount=200, type="expense", category="rent")
    create_transaction(auth_client, amount=50.25, type="expense", category="food")

    summary = auth_client.get("/api/transactions").get_json()["summary"]

    assert summary["income"] == 1000
    assert summary["expenses"] == 250.25
    assert summary["net"] == 749.75


def test_summary_calculation_income_only(auth_client):
    create_transaction(auth_client, amount=500, type="income", category="salary")
    create_transaction(auth_client, amount=300, type="income", category="freelance")

    summary = auth_client.get("/api/transactions").get_json()["summary"]

    assert summary["income"] == 800
    assert summary["expenses"] == 0
    assert summary["net"] == 800


def test_summary_calculation_expenses_only(auth_client):
    create_transaction(auth_client, amount=60, type="expense", category="utilities")
    create_transaction(auth_client, amount=40, type="expense", category="internet")

    summary = auth_client.get("/api/transactions").get_json()["summary"]

    assert summary["income"] == 0
    assert summary["expenses"] == 100
    assert summary["net"] == -100


def test_summary_calculation_net_can_be_negative(auth_client):
    create_transaction(auth_client, amount=100, type="income", category="salary")
    create_transaction(auth_client, amount=250, type="expense", category="rent")

    summary = auth_client.get("/api/transactions").get_json()["summary"]

    assert summary["net"] == -150


def test_summary_calculation_floating_point_amounts(auth_client):
    create_transaction(auth_client, amount=19.99, type="expense", category="food")
    create_transaction(auth_client, amount=5.01, type="expense", category="food")

    summary = auth_client.get("/api/transactions").get_json()["summary"]

    assert summary["expenses"] == pytest.approx(25.0)


# ---- delete -------------------------------------------------------------


def test_delete_transaction_success(auth_client):
    created = create_transaction(auth_client).get_json()

    response = auth_client.delete(f"/api/transactions/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Transaction deleted"

    remaining = auth_client.get("/api/transactions").get_json()["transactions"]
    assert remaining == []


def test_delete_transaction_requires_auth(client):
    response = client.delete("/api/transactions/1")

    assert response.status_code == 401


def test_delete_transaction_not_found(auth_client):
    response = auth_client.delete("/api/transactions/99999")

    assert response.status_code == 404


def test_delete_transaction_not_owned_by_user(auth_client, second_auth_client):
    created = create_transaction(second_auth_client).get_json()

    response = auth_client.delete(f"/api/transactions/{created['id']}")

    assert response.status_code == 404

    # the other user's transaction should be untouched
    remaining = second_auth_client.get("/api/transactions").get_json()["transactions"]
    assert len(remaining) == 1