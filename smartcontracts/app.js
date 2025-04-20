// Connect to the local blockchain via Web3
console.log("Connecting to the blockchain...");
const web3 = new Web3("http://127.0.0.1:7545");

// Replace with your contract's address and ABI
const contractAddress = "0x92CCbDC0c10BfD745E4736E59129A86e022DA933";
const contractABI = [
  {
    "inputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "name": "cheques",
      "outputs": [
        {
          "internalType": "string",
          "name": "chequeNumber",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "dateOfIssue",
          "type": "string"
        },
        {
          "internalType": "bool",
          "name": "isValid",
          "type": "bool"
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
          "name": "chequeNumber",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "dateOfIssue",
          "type": "string"
        }
      ],
      "name": "validateCheque",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "chequeNumber",
          "type": "string"
        }
      ],
      "name": "getCheque",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "chequeNumber",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "amount",
              "type": "uint256"
            },
            {
              "internalType": "string",
              "name": "dateOfIssue",
              "type": "string"
            },
            {
              "internalType": "bool",
              "name": "isValid",
              "type": "bool"
            }
          ],
          "internalType": "struct ChequeValidation.Cheque",
          "name": "",
          "type": "tuple"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": true
    }
];

// Instantiate the contract
console.log("Instantiating the contract...");
const chequeValidation = new web3.eth.Contract(contractABI, contractAddress);
console.log("Contract instantiated with address:", contractAddress);

// Get the accounts from MetaMask
let accounts;
console.log("Requesting MetaMask accounts...");
if (typeof window.ethereum !== "undefined") {
  window.ethereum.request({ method: "eth_requestAccounts" })
    .then((acc) => {
      accounts = acc;
      console.log("Connected accounts:", accounts);
    })
    .catch((error) => {
      console.error("Error fetching accounts from MetaMask:", error.message);
      alert("Error connecting to MetaMask: " + error.message);
    });
} else {
  console.error("MetaMask is not installed.");
  alert("MetaMask is not installed. Please install MetaMask to proceed.");
}

// Add event listener for "Validate Cheque"
document.getElementById("validateCheque").addEventListener("click", async () => {
  const chequeNumber = document.getElementById("chequeNumber").value.trim();
  const amount = document.getElementById("amount").value.trim();
  const dateOfIssue = document.getElementById("dateOfIssue").value.trim();

  console.log("Validate Cheque clicked.");
  console.log("Cheque Number:", chequeNumber);
  console.log("Amount:", amount);
  console.log("Date of Issue:", dateOfIssue);

  if (!chequeNumber || !amount || !dateOfIssue) {
    console.error("All input fields must be filled.");
    alert("Please fill all the input fields before submitting.");
    return;
  }

  try {
    console.log("Sending transaction to validate cheque...");
    await chequeValidation.methods
      .validateCheque(chequeNumber, parseInt(amount), dateOfIssue)
      .send({ from: accounts[0], gas: 5000000 }); 

    console.log("Transaction successful! Cheque validated.");
    document.getElementById("output").innerText = "Cheque validated successfully!";
  } catch (error) {
    console.error("Error during transaction:", error.message);
    document.getElementById("output").innerText = `Error: ${error.message}`;
  }
});

// Add event listener for "Get Cheque Details"
document.getElementById("getCheque").addEventListener("click", async () => {
  const chequeNumber = document.getElementById("retrieveChequeNumber").value.trim();

  console.log("Get Cheque Details clicked.");
  console.log("Retrieving details for Cheque Number:", chequeNumber);

  if (!chequeNumber) {
    console.error("Cheque number is required to fetch details.");
    alert("Please enter a cheque number to retrieve details.");
    return;
  }

  try {
    console.log("Fetching cheque details from the contract...");
    const cheque = await chequeValidation.methods.getCheque(chequeNumber).call();
    console.log("Cheque details retrieved:", cheque);

    document.getElementById("output").innerHTML = `
      <p><strong>Cheque Number:</strong> ${cheque.chequeNumber}</p>
      <p><strong>Amount:</strong> ${cheque.amount}</p>
      <p><strong>Date of Issue:</strong> ${cheque.dateOfIssue}</p>
      <p><strong>Is Valid:</strong> ${cheque.isValid}</p>
    `;
  } catch (error) {
    console.error("Error fetching cheque details:", error.message);
    document.getElementById("output").innerText = `Error: ${error.message}`;
  }
});
