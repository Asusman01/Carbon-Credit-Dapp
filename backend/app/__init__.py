from dotenv import load_dotenv

# Load .env file before using os.getenv
load_dotenv()

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config
from .utilis.redis import init_redis
from web3 import Web3
import os
import json
from dotenv import load_dotenv

load_dotenv()


db = SQLAlchemy(engine_options=Config.SQLALCHEMY_ENGINE_OPTIONS)
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(Config)

    # Redis optional
    try:
        init_redis(app)
    except Exception as e:
        print(f"⚠️ Redis not available: {e}")

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.NGO_routes import NGO_bp
    from .routes.buyer_routes import buyer_bp
    from .routes.auditor_routes import auditor_bp
    from .routes.health_routes import health_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(NGO_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(auditor_bp)
    app.register_blueprint(health_bp)

    # 🔹 Blockchain route
    w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL", "http://127.0.0.1:8545")))
    contract_address = os.getenv("CONTRACT_ADDRESS")

    # ✅ Correct ABI path (backend/CarbonCreditABI.json)
    ABI_PATH = os.path.join(os.path.dirname(__file__), "..", "CarbonCreditABI.json")
    with open(ABI_PATH) as f:
        contract_json = json.load(f)

        # Handle both artifact (dict with "abi") and raw ABI (list)
        if isinstance(contract_json, list):
            contract_abi = contract_json
        else:
            contract_abi = contract_json.get("abi", [])

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    @app.route("/blockchain/credits", methods=["GET"])
    def get_credits():
        try:
            total = contract.functions.getNextCreditId().call()
            credits = []
            for i in range(total):
                credit = contract.functions.credits(i).call()
                credits.append({
                    "id": i,
                    "owner": credit[0],
                    "creator": credit[1],
                    "amount": credit[2],
                    "price": credit[3],
                    "forSale": credit[4],
                    "expired": credit[5]
                })
            return jsonify(credits), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/blockchain/mint", methods=["POST"])
    def mint_credit():
        try:
            data = request.json
            private_key = os.getenv("PRIVATE_KEY")
            account = w3.eth.account.from_key(private_key).address

            tx = contract.functions.generateCredit(
                int(data["amount"]), int(data["price"])
            ).build_transaction({
                "from": account,
                "nonce": w3.eth.get_transaction_count(account),
                "gas": 3000000,
                "gasPrice": w3.to_wei("20", "gwei")
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return jsonify({"txHash": tx_hash.hex()}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    with app.app_context():
        db.create_all()
        print("✅ Backend connected with Blockchain & Postgres")

    return app
