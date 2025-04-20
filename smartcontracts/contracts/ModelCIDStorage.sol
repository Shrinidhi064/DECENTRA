// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ModelCIDStorage {
    mapping(address => string) public modelCIDs;

    event CIDStored(address indexed user, string cid);

    function storeCID(string memory _cid) public {
        modelCIDs[msg.sender] = _cid;
        emit CIDStored(msg.sender, _cid);
    }

    function getCID(address user) public view returns (string memory) {
        return modelCIDs[user];
    }
}
