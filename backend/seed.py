# PART 3: The Seed File (seed.py) — Stocking the Fridge
# This script is only run once manually to load test data.
from datetime import datetime, date, timedelta
from app import app, db
from models import Account, Note

ACCOUNTS = [
    {"name": "Marcus Johnson",     "balance": 1240.50, "days_past_due": 45,  "status": "delinquent",  "phone": "555-201-0001", "email": "marcus.j@email.com"},
    {"name": "Tanya Williams",     "balance": 3870.00, "days_past_due": 120, "status": "charged_off", "phone": "555-201-0002", "email": "tanya.w@email.com"},
    {"name": "DeShawn Carter",     "balance": 540.75,  "days_past_due": 0,   "status": "current",     "phone": "555-201-0003", "email": "deshawn.c@email.com"},
    {"name": "Priya Patel",        "balance": 2100.00, "days_past_due": 62,  "status": "delinquent",  "phone": "555-201-0004", "email": "priya.p@email.com"},
    {"name": "Carlos Rivera",      "balance": 890.25,  "days_past_due": 0,   "status": "current",     "phone": "555-201-0005", "email": "carlos.r@email.com"},
    {"name": "Latoya Brooks",      "balance": 5500.00, "days_past_due": 180, "status": "charged_off", "phone": "555-201-0006", "email": "latoya.b@email.com"},
    {"name": "James O'Brien",      "balance": 320.00,  "days_past_due": 30,  "status": "delinquent",  "phone": "555-201-0007", "email": "james.ob@email.com"},
    {"name": "Angela Nguyen",      "balance": 760.00,  "days_past_due": 0,   "status": "current",     "phone": "555-201-0008", "email": "angela.n@email.com"},
    {"name": "Robert Thompson",    "balance": 4200.00, "days_past_due": 90,  "status": "delinquent",  "phone": "555-201-0009", "email": "robert.t@email.com"},
    {"name": "Simone Davis",       "balance": 1850.00, "days_past_due": 200, "status": "charged_off", "phone": "555-201-0010", "email": "simone.d@email.com"},
    {"name": "Kevin Park",         "balance": 430.00,  "days_past_due": 0,   "status": "current",     "phone": "555-201-0011", "email": "kevin.p@email.com"},
    {"name": "Maria Gonzalez",     "balance": 975.50,  "days_past_due": 55,  "status": "delinquent",  "phone": "555-201-0012", "email": "maria.g@email.com"},
    {"name": "Tyrone Washington",  "balance": 2300.00, "days_past_due": 0,   "status": "current",     "phone": "555-201-0013", "email": "tyrone.w@email.com"},
    {"name": "Sandra Lee",         "balance": 6100.00, "days_past_due": 150, "status": "charged_off", "phone": "555-201-0014", "email": "sandra.l@email.com"},
    {"name": "Ahmed Hassan",       "balance": 780.00,  "days_past_due": 38,  "status": "delinquent",  "phone": "555-201-0015", "email": "ahmed.h@email.com"},
]

# Sample call-log entries, keyed by the account's name so they attach to the
# right record regardless of insertion order. Mirrors a real collector's log:
# a mix of no-answers, promises, refusals, and a completed payment.
NOW = datetime.utcnow()

NOTES_BY_NAME = {
    "Marcus Johnson": [
        {"contact_date": NOW - timedelta(days=6), "outcome": "no_answer",
         "note_text": "Called cell, no answer, no voicemail box set up."},
        {"contact_date": NOW - timedelta(days=2), "outcome": "promise_to_pay",
         "note_text": "Spoke with Marcus directly. Says he gets paid Friday and will pay the full balance.",
         "promise_amount": 1240.50, "promise_date": (date.today() + timedelta(days=5))},
    ],
    "Priya Patel": [
        {"contact_date": NOW - timedelta(days=10), "outcome": "left_message",
         "note_text": "Left voicemail requesting a callback regarding the account."},
        {"contact_date": NOW - timedelta(days=3), "outcome": "promise_to_pay",
         "note_text": "Priya called back. Can only pay half now, rest next month.",
         "promise_amount": 1050.00, "promise_date": (date.today() + timedelta(days=10))},
    ],
    "James O'Brien": [
        {"contact_date": NOW - timedelta(days=4), "outcome": "refused_to_pay",
         "note_text": "James states he disputes the balance and will not pay until it's reviewed."},
        {"contact_date": NOW - timedelta(days=1), "outcome": "disputed",
         "note_text": "Sent dispute paperwork to compliance for review per his request."},
    ],
    "Robert Thompson": [
        {"contact_date": NOW - timedelta(days=1), "outcome": "promise_to_pay",
         "note_text": "Robert committed to a partial payment plan, first installment this week.",
         "promise_amount": 500.00, "promise_date": (date.today() + timedelta(days=3))},
    ],
    "Ahmed Hassan": [
        {"contact_date": NOW - timedelta(days=8), "outcome": "promise_to_pay",
         "note_text": "Promised payment by end of week.",
         "promise_amount": 780.00, "promise_date": (date.today() - timedelta(days=1))},
        {"contact_date": NOW - timedelta(hours=6), "outcome": "payment_made",
         "note_text": "Payment received in full over the phone. Confirmation #88213.",
         },
    ],
}

with app.app_context():
    db.drop_all()  # Drops all tables (like emptying the fridge)
    db.create_all()  # Rebuilds the tables based on your models (like stocking the fridge)
    accounts_by_name = {}
    for data in ACCOUNTS:
        account = Account(**data)  # **data unpacks the dictionary into keyword arguments
        db.session.add(account)
        accounts_by_name[data["name"]] = account
    db.session.flush()  # assigns IDs without committing yet, so notes can reference them

    note_count = 0
    for name, notes in NOTES_BY_NAME.items():
        account = accounts_by_name[name]
        for note_data in notes:
            db.session.add(Note(account_id=account.id, **note_data))
            note_count += 1

    db.session.commit()  # Commits all the changes to the database
    print(f"seeded {len(ACCOUNTS)} accounts and {note_count} notes")