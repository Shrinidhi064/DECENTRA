// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SignatureRegistry {
    struct Person {
        string name;
        string ipfsHash;
    }

    mapping(address => Person) public persons;
    address[] public personAddresses; // New array to track addresses

    function addPerson(string memory _name, string memory _ipfsHash) public {
        persons[msg.sender] = Person(_name, _ipfsHash);
        personAddresses.push(msg.sender);  // Track new addresses
    }

    function getPerson(address _person) public view returns (string memory, string memory) {
        return (persons[_person].name, persons[_person].ipfsHash);
    }

    // New function to fetch all persons' data
    function getAllPersons() public view returns (address[] memory, string[] memory, string[] memory) {
        uint totalPersons = personAddresses.length;
        string[] memory names = new string[](totalPersons);
        string[] memory ipfsHashes = new string[](totalPersons);

        for (uint i = 0; i < totalPersons; i++) {
            address currentAddress = personAddresses[i];
            names[i] = persons[currentAddress].name;
            ipfsHashes[i] = persons[currentAddress].ipfsHash;
        }

        return (personAddresses, names, ipfsHashes);
    }
}
