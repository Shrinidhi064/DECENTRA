const Web3 = require('web3').default;
const fetch = require('node-fetch'); // Add this if using Node.js

// Initialize Web3 provider (Ganache local blockchain)
const web3 = new Web3("http://127.0.0.1:7545");

// Contract ABI and Address
const CONTRACT_ABI = [
    {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
          }
        ],
        "name": "personAddresses",
        "outputs": [
          {
            "internalType": "address",
            "name": "",
            "type": "address"
          }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": true
      },
      {
        "inputs": [
          {
            "internalType": "address",
            "name": "",
            "type": "address"
          }
        ],
        "name": "persons",
        "outputs": [
          {
            "internalType": "string",
            "name": "name",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "ipfsHash",
            "type": "string"
          }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": true
      },
      {
        "inputs": [
          {
            "internalType": "string",
            "name": "_name",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "_ipfsHash",
            "type": "string"
          }
        ],
        "name": "addPerson",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "address",
            "name": "_person",
            "type": "address"
          }
        ],
        "name": "getPerson",
        "outputs": [
          {
            "internalType": "string",
            "name": "",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "",
            "type": "string"
          }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": true
      },
      {
        "inputs": [],
        "name": "getAllPersons",
        "outputs": [
          {
            "internalType": "address[]",
            "name": "",
            "type": "address[]"
          },
          {
            "internalType": "string[]",
            "name": "",
            "type": "string[]"
          },
          {
            "internalType": "string[]",
            "name": "",
            "type": "string[]"
          }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": true
      }
];

const CONTRACT_ADDRESS = "0xc1295154C2CB1CB79e0994f548035e5eda4191fD"; // Add your deployed contract address here

// Initialize contract instance
const contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);

// Function to add a person's name and IPFS hash
async function addPerson(name, ipfsHash) {
    try {
        const accounts = await web3.eth.getAccounts();
        if (!accounts.length) {
            throw new Error("No accounts found. Ensure Ganache is running.");
        }

        await contract.methods.addPerson(name, ipfsHash).send({ 
            from: accounts[3], 
            gas: 3000000 
        });
        console.log(accounts)
        console.log(`✅ Person added: ${name} with IPFS Hash: ${ipfsHash}`);
    } catch (error) {
        console.error(`❌ Error adding person: ${error.message}`);
    }
}

// Function to retrieve a person's data
async function getPerson(address) {
    try {
        const result = await contract.methods.getPerson(address).call();

        if (result && result[0] && result[1]) {
            const ipfsHash = result[1];

            const gateways = [
                `https://ipfs.io/ipfs/${ipfsHash}`,
                `https://cloudflare-ipfs.com/ipfs/${ipfsHash}`,
                `https://gateway.pinata.cloud/ipfs/${ipfsHash}`
            ];

            let validImageUrl = null;
            for (const url of gateways) {
                try {
                    const response = await fetch(url, { method: 'HEAD' });
                    if (response.ok) {
                        validImageUrl = url;
                        break;
                    }
                } catch (error) {
                    console.warn(`❌ Failed to load image from: ${url}`);
                }
            }

            if (validImageUrl) {
                console.log(`✅ Image available at: ${validImageUrl}`);
                console.log(`👤 Name: ${result[0]}`);
                console.log(`🖼️ Signature URL: ${validImageUrl}`);
            } else {
                console.log(`❌ Image not found on any gateway.`);
            }
        } else {
            console.log(`❌ No data found for address: ${address}`);
        }
    } catch (error) {
        console.error(`❌ Error retrieving data: ${error.message}`);
    }
}

async function getAllPersons() {
    try {
        const result = await contract.methods.getAllPersons().call();

        if (result && result[0]?.length > 0) {
            const persons = result[0].map((_, index) => ({
                walletAddress: result[0][index],
                name: result[1][index],
                ipfsHash: result[2][index]
            }));

            persons.forEach(person => {
                console.log(`👤 Name: ${person.name}`);
                console.log(`🏠 Wallet Address: ${person.walletAddress}`);
                console.log(`🖼️ IPFS Hash: ${person.ipfsHash}`);
                console.log('-----------------------------------');
            });
        } else {
            console.log("❌ No records found.");
        }
    } catch (error) {
        console.error(`❌ Error retrieving all persons: ${error.message}`);
    }
}


// Example Usage
(async () => {
    await addPerson("Shiva Kumar", "bafkreifttxirx4pslg47zpkfvybyyo7egetjhcrgyswyickejqsltx4oni");
    
    await getPerson("0xe1e0Be27514E0A2BcEd756e1Bf0Ff56E327eB1b5");
    await getPerson("0xf5a9C47edC1e713BBD4e97b23486841663e8D9EC");
    await getPerson("0xF422fca01F03D0FA96596466A40Cf743cd4d92cf");
    //await getAllPersons();
})();