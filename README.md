## CARBON CREDIT MARKETPLACE


This is a decentralized Carbon Credit Marketplace for managing, trading and auditing carbon credits with transparency and trust.
Built with React.js (frontend) and the backend with Python, Flask (backend API) and Ethereum Smart Contracts deployed on ONINO Blockchain, 
This project enables NGOs, Auditors and Buyers to interact in a secure and efficient carbon credit marketplace.

##  Features
## Roles

## NGOs

1. Create and submit carbon reduction projects.

2. Upload supporting documents (PDFs).

3. Request audits to verify carbon credits.

## Auditors

1. Review project submissions from NGOs.

2. Approve or reject credits after verification.

3. Earn audit fees for their service.

## Buyers 

1. Purchase verified carbon credits from NGOs.

2. Use blockchain-backed proof of carbon offset.

## Core Functionalities

1. Tokenization of carbon credits using smart contracts.

2. Audit process workflow with fees.

3. Secure transactions and record-keeping on Ethereum.

4. Role-based dashboards (NGO, Auditor, Buyer).

5. File upload & project documentation.

## Tech Stack

## Frontend

** React.js (UI)

** TailwindCSS (styling)

** Axios (API calls)

** Web3.js / Ethers.js (Ethereum interaction)

## Backend

** Python + Flask

** Postgres database

** JWT Authentication


## Blockchain

** Solidity Smart Contracts

** Hardhat for development & testing

** ONINO Blockchain  Testnet 

## Installation & Setup

1. Clone the repository

git clone https://github.com/Asusman01/Carbon-Credit-Dapp.git
cd Carbon-Credit-Dapp

2. Backend Setup
cd backend
npm install


Create .env file:

PORT=5000
postgres_URI=your-postgresdb-connection-string
JWT_SECRET=your-secret


Start backend:

npm start

3. Frontend Setup
cd ../client
npm install
npm start


Frontend runs on: http://localhost:3000
Backend runs on: http://localhost:5000

4. Smart Contracts
cd smartContracts
npm install
npx hardhat compile
npx hardhat test


Deploy contract to testnet:

npx hardhat run scripts/deploy.js --network sepolia


Update frontend with deployed contract address & ABI.

##  Usage

Login / Signup as NGO, Auditor or Buyer.

1. NGOs → Create project → Upload PDF → Request Audit.

2. Auditors → Review project → Approve/Reject.

3. Buyers → Purchase credits from verified NGOs.




## Security

JWT authentication for API access.

Role-based access control.

All transactions recorded immutably on-chain.

## Contributors

Asusman01

## Licensecd

This project is licensed under the MIT License.