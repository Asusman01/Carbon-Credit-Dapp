// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";
//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.9.0/contracts/token/ERC20/IERC20.sol";



contract CarbonCredit {
    IERC20 public oniToken;

    constructor(address _oniToken) {
        oniToken = IERC20(_oniToken);
    }

    struct Credit {
        uint256 amount; // Amount of carbon offset (e.g., in tons)
        address creator; // Company that created the credit
        address owner;   // Current owner of the credit
        bool expired;    // Expiry flag
        uint256 price;   // Price in ONI tokens
        bool forSale;    // Is the credit available for sale?
        uint8 requestStatus;
        uint numOfAuditors;
        uint auditFees;
        int auditScore;
        address[] auditorsList;
        mapping(address => bool) AuditInfo;
    }

    error CreditNotForSale();
    error PriceNotMet();
    error OnlyOwnerCanSell();
    error OnlyOwnerCanRemove();
    error CreditDoesntExist();
    error OnlyCreatorCanExpire();
    error MinAuditFees();
    error CreditNotAudited();
    error AlreadyAudited();
    error AuditRequestedAlready();
    error CreatorCantAudit();
    error FeeTransactionFailed();
    error CreditFailedAudit();

    mapping(uint256 => Credit) public credits;
    uint256 nextCreditId;

    // Generate a new carbon credit
    function generateCredit(uint256 amount, uint256 price) external {
        Credit storage newCredit = credits[nextCreditId];
        newCredit.amount = amount;
        newCredit.creator = msg.sender;
        newCredit.owner = msg.sender;
        newCredit.price = price;
        newCredit.numOfAuditors = (amount / 500) * 2 + 3;

        nextCreditId++;
    }

    // Buy a carbon credit listed for sale
    function buyCredit(uint256 creditId) external {
        Credit storage credit = credits[creditId];
        if (!credit.forSale) revert CreditNotForSale();

        uint256 price = credit.price;

        // Transfer ONI tokens from buyer to contract
        require(oniToken.transferFrom(msg.sender, address(this), price), "Token transfer failed");

        uint256 creator_share = (price * 10) / 100;
        uint256 owner_share = price - creator_share;

        require(oniToken.transfer(credit.creator, creator_share), "Creator payment failed");
        require(oniToken.transfer(credit.owner, owner_share), "Owner payment failed");

        credit.owner = msg.sender;
        credit.forSale = false;
    }

    // List a carbon credit for sale
    function sellCredit(uint256 creditId, uint256 price) external {
        Credit storage credit = credits[creditId];

        if (credit.owner == address(0)) revert CreditDoesntExist();
        if (msg.sender != credit.owner) revert OnlyOwnerCanSell();
        if (credits[creditId].requestStatus != 2) revert CreditNotAudited();
        if (credits[creditId].auditScore <= 0) revert CreditFailedAudit();

        credit.price = price;
        credit.forSale = true;
    }

    // Remove a credit from sale
    function removeFromSale(uint256 creditId) external {
        Credit storage credit = credits[creditId];
        if (msg.sender != credit.owner) revert OnlyOwnerCanRemove();
        credit.forSale = false;
    }

    // Expire the credit (can only be done by creator)
    function expire(uint256 creditId) external {
        if (msg.sender != credits[creditId].creator) revert OnlyCreatorCanExpire();
        credits[creditId].expired = true;
    }

    // Request audit by locking ONI tokens
    function requestAudit(uint256 creditId, uint256 feeAmount) external {
        if (credits[creditId].requestStatus != 0) revert AuditRequestedAlready();
        if (feeAmount < (1e14 * credits[creditId].amount)) revert MinAuditFees();

        require(oniToken.transferFrom(msg.sender, address(this), feeAmount), "Fee transfer failed");

        credits[creditId].requestStatus = 1;
        credits[creditId].auditFees = feeAmount;
    }

    // Audit credit (reward in ONI tokens)
    function auditCredit(uint256 creditId, bool vote) external {
        Credit storage credit = credits[creditId];

        if (msg.sender == credit.creator) revert CreatorCantAudit();
        if (credit.requestStatus != 1) revert AlreadyAudited();

        for (uint i = 0; i < credit.auditorsList.length; i++) {
            if (credit.auditorsList[i] == msg.sender) {
                revert AlreadyAudited();
            }
        }

        credit.AuditInfo[msg.sender] = vote;
        credit.auditorsList.push(msg.sender);

        if (vote) {
            credit.auditScore++;
        } else {
            credit.auditScore--;
        }

        if (credit.auditorsList.length == credit.numOfAuditors) {
            credit.requestStatus = 2;
        }

        // Reward auditor with a share of the audit fees
        require(oniToken.transfer(msg.sender, credit.auditFees / 3), "Audit reward failed");
    }

    // --- View Functions ---
    function isExpired(uint256 creditId) external view returns (bool) {
        return credits[creditId].expired;
    }

    function getOwner(uint256 creditId) external view returns (address) {
        return credits[creditId].owner;
    }

    function getCreator(uint256 creditId) external view returns (address) {
        return credits[creditId].creator;
    }

    function getNextCreditId() external view returns (uint256) {
        return nextCreditId;
    }

    function getPrice(uint256 creditId) external view returns (uint256) {
        return credits[creditId].price;
    }

    function getAuditorVote(uint creditId, address auditor) external view returns (bool) {
        return credits[creditId].AuditInfo[auditor];
    }

    function getAuditorList(uint creditId) external view returns (address[] memory) {
        return credits[creditId].auditorsList;
    }

    function getContractBalance() external view returns (uint256) {
        return oniToken.balanceOf(address(this));
    }
}
