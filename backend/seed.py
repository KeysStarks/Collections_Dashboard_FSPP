# PART 3: The Seed File (seed.py) — Stocking the Fridge
# This script is only run once manually to load test data.
from app import app, db
from models import Account

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

with app.app_context():
    db.drop_all()  # Drops all tables (like emptying the fridge)
    db.create_all()  # Rebuilds the tables based on your models (like stocking the fridge)       
    for data in ACCOUNTS:
        db.session.add(Account(**data))  # **data unpacks the dictionary into keyword arguments
    db.session.commit()# Commits all the changes to the database
    print(f"seeded {len(ACCOUNTS)} accounts")