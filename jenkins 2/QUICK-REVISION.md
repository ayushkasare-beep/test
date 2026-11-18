# Quick revision sheet — blockchain practicals

## Must-know one-liners
- **Block:** index + timestamp + data + previous hash + current SHA-256 hash.
- **Genesis block:** the first block, whose previous hash is usually `'0'`.
- **Hash:** `sha256` fingerprint; any data change changes the hash.
- **Blockchain valid if:** each stored hash equals its recalculated hash **and** each block points to previous block hash.
- **Armstrong:** e.g. 153 = 1³ + 5³ + 3³.
- **Anagram:** two words have the same letters when sorted.
- **Happy:** replace number by sum of squared digits; success if it ends at 1.
- **Prime:** n ≥ 2, no divisor from 2 to √n.
- **Pure:** function reads no contract state, **view:** reads but doesn't modify state.
- **Constructor:** executes once on deployment.
- **Mapping:** like a dictionary `mapping(uint => Student)`.
- **Struct:** group of data fields.
- **Payable:** function can receive ether; `msg.value` contains amount in wei.
- **require:** validates condition; invalid call reverts.
- **Inheritance:** `contract Bike is Vehicle`.
- **Overriding:** parent `virtual`, child `override`.
- **Events:** `event ...` then `emit ...`.
- **Truffle:** `truffle compile` then `truffle migrate --reset --network development`.
- **Hardhat:** `npx hardhat compile`, `npx hardhat node`, then deployment in another terminal.
- **MetaMask:** connect to the same local RPC + chain ID used to deploy.

## Commands by tool
```powershell
node --version
python --version
node Q1_Addition.js
python Q1_Armstrong.py
truffle compile
truffle migrate --reset --network development
npx hardhat compile
npx hardhat node
npx hardhat run scripts/deploy.js --network localhost
python -m http.server 5500
```

## Typical oral exam questions
1. What is SHA-256? A cryptographic hash function producing a 256-bit digest.
2. Why previous hash? It links each block to the prior block for tamper detection.
3. Is this proof-of-work or a real decentralized blockchain? No. These are single-process hash-linked demos.
4. Why doesn't my DApp find the contract? Wrong RPC/chain ID or old deployment address.
5. `call()` versus transaction? View/pure calls read; transactions change blockchain state and cost local test gas.
6. What is the difference between Ganache and Remix VM? Both are local simulated Ethereum environments; Ganache is a separately running local node, Remix VM is in-browser.
