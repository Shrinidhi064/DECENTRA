// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ChequeMetadata {
    struct Cheque {
        uint id;
        string payeeName;
        string amountInNumber;
        string amountInWords;
        string bankName;
        string branch;
        string ifscCode;
        string date;
        string micrCode;
        string accountNumber;
        string chequeImageUrl; // ✅ Image URL instead of just name
    }

    mapping(uint => Cheque) public cheques;
    uint[] private chequeIds;
    address public owner;

    event ChequeStored(uint id, string chequeImageUrl);

    constructor() {
        owner = msg.sender;
    }

    function storeCheque(
        uint id,
        string memory payeeName,
        string memory amountInNumber,
        string memory amountInWords,
        string memory bankName,
        string memory branch,
        string memory ifscCode,
        string memory date,
        string memory micrCode,
        string memory accountNumber,
        string memory chequeImageUrl // ✅ Store full URL
    ) public {
        require(cheques[id].id == 0, "Cheque with this ID already exists.");
        
        cheques[id] = Cheque(
            id,
            payeeName,
            amountInNumber,
            amountInWords,
            bankName,
            branch,
            ifscCode,
            date,
            micrCode,
            accountNumber,
            chequeImageUrl
        );
        
        chequeIds.push(id);
        emit ChequeStored(id, chequeImageUrl);
    }

    function getCheque(uint id) public view returns (uint, string memory, string memory) {
        require(cheques[id].id != 0, "Cheque with this ID does not exist.");
        return (cheques[id].id, cheques[id].date, cheques[id].chequeImageUrl);
    }

    function getChequeIds() public view returns (uint[] memory) {
        return chequeIds;
    }

    function getAllCheques() public view returns (uint[] memory, string[] memory, string[] memory) {
        uint length = chequeIds.length;
        uint[] memory ids = new uint[](length);
        string[] memory dates = new string[](length);
        string[] memory chequeImageUrls = new string[](length);

        for (uint i = 0; i < length; i++) {
            uint chequeId = chequeIds[i];
            ids[i] = chequeId;
            dates[i] = cheques[chequeId].date;
            chequeImageUrls[i] = cheques[chequeId].chequeImageUrl;
        }

        return (ids, dates, chequeImageUrls);
    }
}
