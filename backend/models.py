# PART 1: The Model (models.py) — Designing the Fridge Shelf
# Defines database tables:
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# SQLAlchemy is a library (pre-built tool) that lets you talk to databases using Python instead of raw SQL.
db = SQLAlchemy()

# Each db.Column(...) is one column in the table — like a column in a spreadsheet.
class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    days_past_due = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="current")
    # current | delinquent | charged-off
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # to_dict() is a method (a function that belongs to the class) that converts one Account object into a plain Python dictionary.     
    def to_dict(self):
        return {
        'id': self.id,
        'name': self.name,
        'balance': self.balance,
        'days_past_due': self.days_past_due,
        'status': self.status,
        'phone': self.phone,
        'email': self.email,
        'created_at': self.created_at.isoformat() if self.created_at else None,
        'updated_at': self.updated_at.isoformat() if self.updated_at else None
    }

