from flask import Blueprint, request, jsonify
from .models import db, Transaction 

main = Blueprint("main", __name__)

main = Blueprint("main", __name__)

@main.get("/health")
def health():
    return {"status": "ok"}

@main.get("/")
def home():
    return {"app": "Ledgerly", "message": "Welcome!"}

@main.get("/transactions")
def list_transactions():
    txs = Transaction.query.order_by(Transaction.date.desc()).all()
    return jsonify([t.to_dict() for t in txs])

@main.post("/transactions")
def create_transaction():
    data = request.get_json(silent=True) or {}

    # minimal validation
    required = ["amount", "category", "type"]
    missing = [k for k in required if k not in data]
    if missing:
        return {"error": f"Missing fields: {', '.join(missing)}"}, 400
    
    tx = Transaction(
        amount=float(data["amount"]),
        category=str(data["category"]).strip()
        type=str(data["type"]).strip().lower() # "income" or "expense"
        note=str(data.get("note", "")).strip(),
        date=data.get("date") # optional; can be ISO string if model supports it
    )

    db.session.add(tx)
    db.session.commit()
    return tx.to_dict(), 201

@main.delete("/transactions/<int:tx_id>")
def delete_transaction(tx_id: int):
    tx = Transaction.query.get_or_404(tx_id)
    db.session.delete(tx)
    db.session.commit()
    return {"deleted": tx_id}

