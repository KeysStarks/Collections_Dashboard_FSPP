# PART 2: Flask (app.py) — The Kitchen That Listens
# Importing Tools (Ingredients
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Account 

# Ceate Application (Kitchen)
app = Flask(__name__)
CORS(app)

# This tells Flask where the database file lives. 
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'collections.db')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Silence the deprecation warning

# db.init_app(app) connects your database object to your Flask app. db.create_all() reads your models and creates the actual database tables if they don't exist yet. The with app.app_context() block is required because Flask needs to know which app is "active" when doing setup work outside of a request.
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # The Routes - This is Where the Action Happens
    @app.route("/")
    def health():
        return jsonify({"status": "ok", "message": "Collections API is running!"})
    
    
    
    @app.route("/accounts", methods=["GET"])
    def get_accounts():
        status = request.args.get("status")
        query = Account.query
        if status:
            query = query.filter_by(status=status)
        accounts = query.order_by(Account.days_past_due.desc()).all()
        return jsonify([a.to_dict() for a in accounts])
    
    
    @app.route("/accounts/stats", methods=["GET"])
    def get_stats():
        # GET /accounts/stats — summary numbers for the dashboard header.
        total  = Account.query.count()
        delinquent = Account.query.filter_by(status="delinquent").all()
        charged_off = Account.query.filter_by(status="charged_off").all()
        current = Account.query.filter_by(status="current").count()
        
        delinquent_balance = sum(a.balance for a in delinquent)
        charged_off_balance = sum(a.balance for a in charged_off)
        
        
        return jsonify({
            "total_accounts": total,
            "current_count": current,
            "delinquent_count": len(delinquent),
            "charged_off_count": len(charged_off),
            "total_delinquent_balance": round(delinquent_balance, 2),
            "total_charged_off_balance": round(charged_off_balance, 2),
        })
        
    @app.route("/accounts/<int:account_id>", methods=["GET"])
    def get_account(account_id):
        account = Account.query.get_or_404(account_id)
        return jsonify(account.to_dict())
    
    
    
    # POST is for creating. request.get_json() reads the JSON body that React sent.   
    @app.route("/accounts", methods=["POST"])
    def create_account():
        data = request.get_json()
        if not data or not data.get("name"):
            return jsonify({"error": "Name is required"}), 400
        
        allowed_statuses = ["current", "delinquent", "charged_off"]
        status = data.get("status", "current")
        if status not in allowed_statuses:
            return jsonify({"error": f"Status must be one of {allowed_statuses}"}), 400
        
            
        account = Account(
            name=data["name"],
            balance=float(data.get("balance", 0)),
            days_past_due=int(data.get("days_past_due", 0)),
            status=status,
            phone=data.get("phone"),
            email=data.get("email"),
        )
        
        # Account(...) creates a new Python object using your blueprint. db.session.add(account) stages it — like putting something in your cart. db.session.commit() actually saves it to the database. 201 is HTTP status for "Created." You always return the new object so React knows the ID that was assigned.
        db.session.add(account)
        db.session.commit()
        return jsonify(account.to_dict())
            
        #  <int:account_id> in the route is a URL parameter. The URL /accounts/3 means account_id = 3. Flask passes it into the function automatically. get_or_404 finds the account or returns a 404 error if it doesn't exist. The if "name" in data pattern means: only update fields that were actually sent — if you only want to change the status, you shouldn't have to re-send the name.
    @app.route("/accounts/<int:account_id>", methods=["PUT"])
    def update_account(account_id):
        account = Account.query.get_or_404(account_id)
        data = request.get_json()
        
        if "name" in data:
            account.name = data["name"]
        if "balance" in data:
            account.balance = float(data["balance"])
        if "days_past_due" in data:
            account.days_past_due = int(data["days_past_due"])
        if "status" in data:
            allowed = ["current", "delinquent", "charged_off"]
            if data["status"] not in allowed:
                return jsonify({"error": f"Status must be one of {allowed}"}), 400
            account.status = data["status"]
        if "phone" in data:
            account.phone = data["phone"]
        if "email" in data:
            account.email = data["email"]
        
        db.session.commit()
        return jsonify(account.to_dict())
    
    @app.route("/accounts/<int:account_id>", methods=["DELETE"])
    def delete_account(account_id):
        account = Account.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        return jsonify({"message": f"Account {account_id} deleted."}), 200
    
    
    
    if __name__ == "__main__":
        app.run(debug=True, port=5000)
            