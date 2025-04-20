import json
import os
import ipfshttpclient
import torch
from web3 import Web3

# Connect to IPFS
client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")  # Ensure IPFS daemon is running

# Connect to Blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Ganache RPC URL
contract_address = "0x5b4862896e6a36030a721446AC10e5a0F03205B3"
account = "0xf5a9C47edC1e713BBD4e97b23486841663e8D9EC"  # Ethereum account

# Load Smart Contract ABI
with open("./build/contracts/ModelCIDStorage.json") as f:
    contract_abi = json.load(f)["abi"]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Retrieve CID from Blockchain
model_cid = contract.functions.getCID(account).call()
print(f"🔍 Retrieved Model CID from Blockchain: {model_cid}")

# Check if CID is valid
if not model_cid or not isinstance(model_cid, str):
    raise ValueError("❌ Invalid model CID retrieved from blockchain.")

# Define model save path
model_path = "./logistic_siamese_model.pth"

# Download model file directly from IPFS
try:
    model_data = client.cat(model_cid)  # Fetch entire file directly
    with open(model_path, "wb") as f:
        f.write(model_data)
    print(f"✅ Model successfully downloaded and saved as: {model_path}")

    # Verify Model Integrity
    try:
        model = torch.load(model_path, map_location=torch.device("cpu"))
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")

except Exception as e:
    print(f"❌ Error downloading model from IPFS: {e}")
