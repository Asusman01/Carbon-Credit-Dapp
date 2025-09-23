from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models.credit import Credit
from app.models.request import Request
from app.models.transaction import PurchasedCredit, Transactions
from app.models.user import User
from app.utilis.redis import get_redis
import random
import json

NGO_bp = Blueprint('NGO', __name__)
redis_client = get_redis()

def get_current_user():
    try:
        return json.loads(get_jwt_identity())
    except json.JSONDecodeError:
        return None

def numberOfAuditors(k) -> int:
    """Return number of auditors required based on carbon amount."""
    return int((k // 500) * 2 + 3)


# ✅ 1. Check auditors availability
@NGO_bp.route('/api/NGO/audit-req', methods=['GET'])
@jwt_required()
def check_audit_request():
    try:
        auditors = User.query.filter_by(role='auditor').all()
        num_auditors = len(auditors)

        carbon_amount = request.args.get('amount')
        if not carbon_amount:
            return jsonify({"message": "Missing 'amount' parameter"}), 400

        try:
            carbon_amount = int(carbon_amount)
        except ValueError:
            return jsonify({"message": "'amount' must be an integer"}), 400

        req_auditors = numberOfAuditors(carbon_amount)

        if num_auditors < req_auditors:
            return jsonify({
                "message": f"Not Enough Auditors for {carbon_amount} tons of carbon. Maybe split the credit!",
                "available_auditors": num_auditors,
                "required_auditors": req_auditors
            }), 503

        return jsonify({
            "message": "Enough auditors for the credit",
            "available_auditors": num_auditors,
            "required_auditors": req_auditors
        }), 200
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500


# ✅ 2. Create a new credit
@NGO_bp.route('/api/NGO/credits', methods=['POST'])
@jwt_required()
def create_credit():
    current_user = get_current_user()
    if not current_user or current_user.get("role") != "NGO":
        return jsonify({"message": "Unauthorized"}), 403

    username = current_user.get("username")
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    if not data:
        return jsonify({"message": "Missing request body"}), 400

    try:
        # auditor selection
        auditors = User.query.filter_by(role="auditor").all()
        auditor_ids = [auditor.id for auditor in auditors]
        required = numberOfAuditors(int(data["amount"]))

        try:
            selected_auditor_ids = random.sample(auditor_ids, required)
        except ValueError:
            return jsonify({"message": "Not enough auditors"}), 503

        # create credit
        new_credit = Credit(
            id=data["creditId"],
            name=data["name"],
            amount=data["amount"],
            price=data["price"],
            creator_id=user.id,
            docu_url=data["secure_url"],
            auditors=selected_auditor_ids,
            req_status=1
        )
        db.session.add(new_credit)

        # create request
        new_request = Request(
            credit_id=data["creditId"],
            creator_id=user.id,
            auditors=selected_auditor_ids
        )
        db.session.add(new_request)

        # clear redis cache if exists
        if redis_client:
            try:
                key = username + "_credits"
                redis_client.delete(key)
            except Exception as e:
                print(f"Redis delete error: {e}")

        db.session.commit()
        return jsonify({"message": "Credit created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Server error: {str(e)}"}), 500


# ✅ 3. Expire a credit
@NGO_bp.route('/api/NGO/credits/expire/<int:credit_id>', methods=['PATCH'])
@jwt_required()
def expire_credit(credit_id):
    current_user = get_current_user()
    if current_user.get('role') != 'NGO':
        return jsonify({"message": "Unauthorized"}), 403

    user = User.query.filter_by(username=current_user.get('username')).first()
    credit = Credit.query.get(credit_id)
    pc = PurchasedCredit.query.filter_by(credit_id=credit.id).first()

    if not credit:
        return jsonify({"message": "Credit not found"}), 404
    if not pc:
        return jsonify({"message": f"Credit can't be expired as it has not been sold yet, credit with B_ID {credit_id} is not found"}), 400
    if credit.creator_id != user.id:
        return jsonify({"message": "You do not have permission to expire this credit"}), 403

    credit.is_active = False
    credit.is_expired = True
    pc.is_expired = True
    db.session.commit()
    return jsonify({"message": "Credit expired successfully"}), 200


# ✅ 4. Get transactions
@NGO_bp.route('/api/NGO/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    current_user = get_current_user()
    if current_user.get('role') != 'NGO':
        return jsonify({"message": "Unauthorized"}), 403
    key = current_user.get('username') + "trans"

    if redis_client:
        try:
            cached_txns = redis_client.get(key)
            if cached_txns:
                print("Cache hit")
                return jsonify(json.loads(cached_txns)), 200
            else:
                print("Cache miss")
        except Exception as e:
            print(f"redis get client error: {e}")

    transactions = Transactions.query.order_by(Transactions.timestamp.desc()).all()
    transaction_list = []
    for t in transactions:
        transaction_list.append({
            "id": t.id,
            "buyer": t.buyer_id,
            "credit": t.credit_id,
            "amount": t.amount,
            "total_price": t.total_price,
            "timestamp": t.timestamp.isoformat(),
            "txn_hash": t.txn_hash
        })
    if redis_client:
        redis_client.set(key, json.dumps(transaction_list), ex=1)
    return jsonify(transaction_list)


# ✅ 5. Verify NGO before expire
@NGO_bp.route('/api/NGO/expire-req', methods=['POST'])
@jwt_required()
def check_expire_request():
    data = request.json
    current_user = get_current_user()
    if current_user.get('role') != 'NGO':
        return jsonify({"message": "Unauthorized"}), 403

    username = current_user.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "User verified successfully! can proceed to expire credit"}), 200
    return jsonify({"message": "Invalid credentials"}), 401
