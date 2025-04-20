# DECENTRACHEQUE

**DecentraCheque** is a decentralized smart cheque validation system that tackles key challenges in traditional processing—such as OCR inaccuracies, fraud, and lack of transparency.  
By integrating **machine learning** for signature verification and **blockchain** for tamper-proof record-keeping, it ensures **secure**, **accurate**, and **transparent** cheque processing.

---

### Software Requirements

![Software Requirements](https://github.com/user-attachments/assets/7a4c1a88-bf57-40a7-8e35-7c4a7f3c1795)

---

### System Workflow

![System Workflow](https://github.com/user-attachments/assets/3ecf7cb2-0c06-463a-8570-51bab35f99ad)

---

### Required Installations

1. **IPFS**  
   Used to store encrypted cheque and signature images in a decentralized, immutable way.

2. **Ganache**  
   A personal Ethereum blockchain for smart contract development and testing.

3. **MetaMask (Browser Extension)**  
   Used to manage Ethereum accounts and interact with deployed smart contracts via the browser.

4. **Set up an account in Pinata**
   Uploaded the reference signature imgaes for reference

---

### Running the Application

#### Frontend
To start a simple HTTP server for the frontend:
```
python -m http.server 8000

```

#### Backend

```
python manage.py runserver 

```
### Smart Contract Commands

Make sure **Node.js** and **Truffle** are installed. Then use the following commands to initialize and deploy the smart contracts:

```bash
npm install -g truffle
truffle init
truffle compile
truffle migrate --network development
```

Refer requirements.txt to install python libraries for backend!
