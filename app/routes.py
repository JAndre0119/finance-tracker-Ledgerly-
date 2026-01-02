from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date
from app import db
from app.models import Transaction

main = Blueprint("main", __name__)


@main.route("/")
def dashboard():
    transactions = Transaction.query.order_by(
        Transaction.transaction_date.desc()
    ).all()

    income = sum(t.amount for t in transactions if t.type == "income")
    expenses = sum(t.amount for t in transactions if t.type == "expense")
    net = income - expenses

    return render_template(
        "dashboard.html",
        transactions=transactions,
        income=income,
        expenses=expenses,
        net=net
    )


@main.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        type_ = request.form["type"]
        note = request.form.get("note")

        transaction = Transaction(
            amount=amount,
            category=category,
            type=type_,
            note=note,
            transaction_date=date.today()
        )

        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for("main.dashboard"))

    return render_template("add_transaction.html")

@main.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)

    db.session.delete(transaction)
    db.session.commit()

    return redirect(url_for("main.dashboard"))

