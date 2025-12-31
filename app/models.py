from app import db
from datetime import date

# This class represents a databse table, Class name -> table name (by default)
class Transaction(db.Model):
    # id uniquely identifies each row
    # primary_key=True means auto-incrementing, indexed, and unique (every table should have one)
    id = db.Column(db.Integer, primary_key=True)
    # Stores money value
    # If you try to save a transaction without amount, the DB will reject it
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    # income or expense
    type = db.Column(db.String(10), nullable=False)
    # Allows comments like "Groceries at Costco"
    note = db.Column(db.String(200))
    # Stores a date, if not provided, automatically uses today's date
    transaction_date = db.Column(db.Date, default=date.today)

'''
What the table looks like when translated into SQL

CREATE TABLE transaction (
  id INTEGER PRIMARY KEY,
  amount FLOAT NOT NULL,
  category VARCHAR(50) NOT NULL,
  type VARCHAR(10) NOT NULL,
  note VARCHAR(200),
  transaction_date DATE
);
'''