# DECENTRACHEQUE


**DecentraCheque** is a decentralized smart cheque validation system that tackles key challenges in traditional processing such as OCR inaccuracies, fraud, and lack of transparency. By integrating machine learning for signature verification and blockchain for tamper-proof record-keeping, it ensures secure, accurate, and transparent cheque processing.

**Software Requirements**
![image](https://github.com/user-attachments/assets/7a4c1a88-bf57-40a7-8e35-7c4a7f3c1795)

**System Workflow**
![image](https://github.com/user-attachments/assets/3ecf7cb2-0c06-463a-8570-51bab35f99ad)

**Required installations**
**IPFS**
Used to store encrypted cheque and signature images in a decentralized, immutable way.

**Ganache**
A personal Ethereum blockchain for smart contract development and testing.

**MetaMask (Extension)**
Browser extension for managing Ethereum accounts and interacting with deployed smart contracts.

**Running Frontend**
Setup a server and run the command:
python -m http.server 8000

**Running Django Backend**
python manage.py runserver 

**Commands related to running smartcontracts**
npm install -g truffle
truffle init
truffle compile
truffle migrate –network development




