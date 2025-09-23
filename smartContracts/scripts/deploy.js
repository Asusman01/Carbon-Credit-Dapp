import pkg from "hardhat";
import dotenv from "dotenv";
const { ethers } = pkg;

dotenv.config();

async function main() {
  const ONINO_TOKEN_ADDRESS = process.env.ONINO_TOKEN_ADDRESS;

  if (!ONINO_TOKEN_ADDRESS) {
    throw new Error("❌ Please set ONINO_TOKEN_ADDRESS in your .env file!");
  }

  const CarbonCredit = await ethers.getContractFactory("CarbonCredit");
  const carbonCredit = await CarbonCredit.deploy(ONINO_TOKEN_ADDRESS);

  await carbonCredit.waitForDeployment();
  console.log("✅ CarbonCredit deployed to:", await carbonCredit.getAddress());
  console.log("🔗 Using ONINO token at:", ONINO_TOKEN_ADDRESS);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
