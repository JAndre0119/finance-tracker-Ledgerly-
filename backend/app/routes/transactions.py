from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import date

from app.extensions import db
from app.models import Transaction

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/transactions", methods=["GET"])
@login_required
def get_transactions():
    transactions = (
        Transaction.query
        .filter_by(user_id=current_user.id)
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

    income = sum(t.amount for t in transactions if t.type == "income")
    expenses = sum(t.amount for t in transactions if t.type == "expense")
    net = income - expenses

    return jsonify({
        "transactions": [
            {
                "id": t.id,
                "amount": t.amount,
                "category": t.category,
                "type": t.type,
                "note": t.note,
                "transaction_date": t.transaction_date.isoformat(),
            }
            for t in transactions
        ],
        "summary": {
            "income": income,
            "expenses": expenses,
            "net": net,
        },
    })


@transactions_bp.route("/transactions", methods=["POST"])
@login_required
def add_transaction():
    data = request.get_json()
    amount = data.get("amount")
    category = data.get("category")
    type_ = data.get("type")
    note = data.get("note")

    if not amount or not category or not type_:
        return jsonify({"error": "amount, category, and type are required"}), 400

    if type_ not in ("income", "expense"):
        return jsonify({"error": "type must be 'income' or 'expense'"}), 400

    transaction = Transaction(
        amount=float(amount),
        category=category,
        type=type_,
        note=note,
        transaction_date=date.today(),
        user_id=current_user.id,
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "id": transaction.id,
        "amount": transaction.amount,
        "category": transaction.category,
        "type": transaction.type,
        "note": transaction.note,
        "transaction_date": transaction.transaction_date.isoformat(),
    }), 201


@transactions_bp.route("/transactions/<int:transaction_id>", methods=["DELETE"])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(
        id=transaction_id, user_id=current_user.id
    ).first_or_404()

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted"})
