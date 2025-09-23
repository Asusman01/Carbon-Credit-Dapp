import "@nomicfoundation/hardhat-toolbox";
import dotenv from "dotenv";

dotenv.config();

const PRIVATE_KEY = process.env.DEPLOYER_PRIVATE_KEY || "";

export default {
  solidity: "0.8.20",
  networks: {
    hardhat: {},
    oninoTestnet: {
      url: process.env.ONINO_TESTNET_RPC || "https://rpctestnet.onino.io",
      chainId: 211223,  // Onino testnet chain ID
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [],
    },
  },
};
