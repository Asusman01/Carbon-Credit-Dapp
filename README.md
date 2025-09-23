Carbon Credit Marketplace
A decentralized platform for creating, auditing, buying, selling, and expiring carbon credits.
 The platform ensures transparency, accountability, and traceability using Flask (backend), React (frontend), Ethereum smart contracts, and Redis caching.

Contents
 Project Overview


 Tech Stack (Frontend + Backend + Smart Contracts + Redis/DB)


 Setup instructions (both frontend and backend)


 Running the project


 User roles (NGO, Buyer, Auditor)


 API Endpoints (brief)


 Features implemented


 Future improvements



 Workflow & Features
 Authentication & Authorization (NGO, Buyer, Auditor roles)


 NGOs can:


Create carbon credits tied to projects


Upload supporting PDF documentation (via Cloudinary)


Assign auditors for verification


Expire credits that are outdated or misused


Track credit transactions


 Buyers can:


View available credits


Purchase credits using Ethereum


Sell previously purchased credits


Generate and download ownership certificates


 Auditors can:


View assigned credits


Verify and approve/reject credits


 Blockchain Integration (Smart Contract) for tokenized carbon credits


Redis caching for speeding up transactions & audit requests


 JWT-based authentication for secure API access



Architecture/ Tech Stack
Frontend
React (with Tailwind + ShadCN UI components)


Axios for API calls


//SweetAlert2 for alerts & confirmations


Lucide-react + React Icons for icons


Backend
Flask (Python) with Blueprints for modular routing


SQLAlchemy ORM with PostgreSQL


Redis for caching requests & transactions


Flask-JWT-Extended for authentication


bcrypt for password hashing


Smart Contracts
Solidity (for Ethereum-based credits)


Web3 / ethers.js integration in frontend


 Installation
1. Clone the repo
git clone https://github.com/your-username/carbon-credit-platform.git
cd carbon-credit-platform

2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  
 # On Windows:
 venv\Scripts\activate
pip install -r requirements.txt

Set up .env file:


SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///carbon.db   # or Postgres/MySQL
JWT_SECRET_KEY=your-jwt-secret
REDIS_URL=redis://localhost:6379
CLOUD_NAME=your-cloudinary-cloud-name

Run Flask:


flask run --host=0.0.0.0 --port=5000

3. Frontend Setup
cd client
npm install

Set up .env:


REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_CLOUD_NAME=your-cloudinary-cloud-name

Run React:


npm start


 Usage
Visit http://localhost:3000 to access the app.


Sign up as:


NGO → create credits


Buyer → purchase credits


Auditor → verify credits



User Roles
NGO Dashboard → manage projects, create credits, upload documents, expire credits


Buyer Dashboard → browse credits, purchase/sell, generate certificates


Auditor Dashboard → review & audit assigned credits


 API Endpoints (Backend)
Auth
POST /api/signup → register new user


POST /api/login → login user


NGO
POST /api/NGO/credits → create credit


GET /api/NGO/credits → fetch NGO’s credits


PATCH /api/NGO/credits/expire/:id → expire a credit


GET /api/NGO/transactions → fetch transactions


Buyer
GET /api/buyer/credits → list all credits


POST /api/buyer/purchase → buy a credit


PATCH /api/buyer/sell → sell a credit


GET /api/buyer/purchased → list purchased credits


GET /api/buyer/generate-certificate/:id → generate certificate


Auditor
GET /api/auditor/credits → list assigned credits


PATCH /api/auditor/audit/:creditId → audit a credit


 Future Improvements
Oracle Integration for Verification: Chainlink, EVM-compatible with ONINO) pulls data from carbon registries like Verra or Gold Standard to verify credits automatically.
ERC721 Tokenization: ERC721 NFTs makes each credit unique, tradable on external platforms (e.g., MEXC), and compatible with ONINO’s RWA tokenization tools.
Compliance with KYC: Using ONINO’s Genesys Chain KYC ensures only verified users mint or trade credits, avoiding legal risks.

