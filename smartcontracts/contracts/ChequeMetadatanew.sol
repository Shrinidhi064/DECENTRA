// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract ChequeMetadatanew {
    struct Cheque {
        uint256 chequeNumber;
        uint256 amount;
        uint256 issueDate;
        address issuerAccount;
        bool isProcessed;
    }

    mapping(uint256 => Cheque) public cheques;
    mapping(address => bool) public validAccounts;

    event ChequeProcessed(uint256 chequeNumber, address issuer, bool isValid, string reason);
    event AccountRegistered(address account);
    event AccountFlagged(address account);

    constructor() {
        // Initialize validAccounts mapping for at least one account (to prevent invalid opcode)
        validAccounts[msg.sender] = true;
        emit AccountRegistered(msg.sender);
    }

    modifier onlyValidAccount(address _issuer) {
        require(validAccounts[_issuer], "Issuer account is not valid");
        _;
    }

    function registerAccount(address _account) external {
        validAccounts[_account] = true;
        emit AccountRegistered(_account);
    }

    function flagAccount(address _account) external {
        validAccounts[_account] = false;
        emit AccountFlagged(_account);
    }

    function processCheque(
        uint256 _chequeNumber,
        uint256 _amount,
        uint256 _issueDate,
        address _issuer
    ) external onlyValidAccount(_issuer) {
        require(_amount > 0, "Amount must be greater than zero");

        // Validate cheque number length (6 to 10 digits)
        require(_chequeNumber >= 100000 && _chequeNumber <= 9999999999, "Invalid cheque number length");

        // Validate date: Issue date must be in the past or today
        require(_issueDate <= block.timestamp, "Invalid issue date: Future date is not allowed");

    

        // Check for duplicate cheque
        if (cheques[_chequeNumber].isProcessed) {
            emit ChequeProcessed(_chequeNumber, _issuer, false, "Duplicate cheque detected");
            return;
        }

        // Store cheque details
        cheques[_chequeNumber] = Cheque(_chequeNumber, _amount, _issueDate, _issuer, true);
        emit ChequeProcessed(_chequeNumber, _issuer, true, "Cheque successfully processed");
    }

    function getCheque(uint256 _chequeNumber) external view returns (Cheque memory) {
        return cheques[_chequeNumber];
    }
}
