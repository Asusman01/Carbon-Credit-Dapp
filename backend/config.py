from datetime import timedelta
import os
from dotenv import load_dotenv
from web3 import Web3
import json

load_dotenv()

class Config:
    # Database config
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/local_database"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 240,
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Redis (optional)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Blockchain config
    ONINO_RPC_URL = os.getenv("ONINO_RPC_URL", "https://testnet-rpc.onino.io")
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")

    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(ONINO_RPC_URL))

      # Load ABI from backend/CarbonCreditABI.json
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ABI_PATH = os.path.join(BASE_DIR, "CarbonCreditABI.json")  # 👈 stay inside backend/
        with open(ABI_PATH) as f:
            abi_data = json.load(f)

        # Handle both artifact format and plain ABI
        if isinstance(abi_data, list):
            abi = abi_data
        else:
            abi = abi_data.get("abi", [])

        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    except Exception as e:
        print(f"[Config] Warning: Could not load contract ABI -> {e}")
        contract = None


    # Account
    if PRIVATE_KEY:
        account = w3.eth.account.from_key(PRIVATE_KEY)
    else:
        account = None
