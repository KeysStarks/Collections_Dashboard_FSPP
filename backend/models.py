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

    # One account can have many notes. cascade="all, delete-orphan" means: if an
    # account gets deleted, its notes get deleted too — no orphaned rows left behind.
    notes = db.relationship(
        "Note",
        backref="account",
        cascade="all, delete-orphan",
        order_by="Note.contact_date.desc()",
    )

    # to_dict() is a method (a function that belongs to the class) that converts one Account object into a plain Python dictionary.
    def to_dict(self):
        # Pull the most recent note (if any) so the table can show "last contacted"
        # and whether there's an open payment promise without a second API call.
        latest_note = self.notes[0] if self.notes else None

        return {
        'id': self.id,
        'name': self.name,
        'balance': self.balance,
        'days_past_due': self.days_past_due,
        'status': self.status,
        'phone': self.phone,
        'email': self.email,
        'created_at': self.created_at.isoformat() if self.created_at else None,
        'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        'notes_count': len(self.notes),
        'last_contact_date': latest_note.contact_date.isoformat() if latest_note else None,
        'last_contact_outcome': latest_note.outcome if latest_note else None,
        'open_promise_amount': latest_note.promise_amount if latest_note and latest_note.outcome == "promise_to_pay" else None,
        'open_promise_date': latest_note.promise_date.isoformat() if latest_note and latest_note.outcome == "promise_to_pay" and latest_note.promise_date else None,
    }


# Every entry in a collector's call log: what happened, when, and whether the
# person promised to pay. OUTCOMES lists the values the frontend dropdown uses.
OUTCOMES = [
    "no_answer",
    "left_message",
    "promise_to_pay",
    "payment_made",
    "refused_to_pay",
    "disputed",
    "wrong_number",
    "other",
]


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    contact_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    outcome = db.Column(db.String(30), nullable=False, default="other")
    note_text = db.Column(db.Text, nullable=False)
    # Only meaningful when outcome == "promise_to_pay" — how much and by when.
    promise_amount = db.Column(db.Float, nullable=True)
    promise_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'contact_date': self.contact_date.isoformat() if self.contact_date else None,
            'outcome': self.outcome,
            'note_text': self.note_text,
            'promise_amount': self.promise_amount,
            'promise_date': self.promise_date.isoformat() if self.promise_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

