

const Web3 = require('web3').default; 
const contractABI = require('./build/contracts/ModelCIDStorage.json'); // Ensure ABI is correct
const contractAddress = "0x5b4862896e6a36030a721446AC10e5a0F03205B3"; // Update this after deploying
const web3 = new Web3("http://127.0.0.1:7545"); // Update RPC if using testnet

const account = "0xf5a9C47edC1e713BBD4e97b23486841663e8D9EC"; // Update with your account

async function storeCID() {
    const contract = new web3.eth.Contract(contractABI.abi, contractAddress);
    const cid = "Qmbbfu1FvUXzAKKZQ9HmWHvfRo6sMuDpRKWiJJQ7xbaecW"; // Replace with your actual CID

    await contract.methods.storeCID(cid).send({ from: account, gas: 3000000 });
    console.log("✅ Model CID stored successfully!");
}

async function retrieveCID() {
    const contract = new web3.eth.Contract(contractABI.abi, contractAddress);
    const cid = await contract.methods.getCID(account).call();
    console.log("🔍 Retrieved Model CID:", cid);
}

// Run both functions sequentially
storeCID().then(retrieveCID);
