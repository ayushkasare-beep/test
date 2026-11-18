# Practical 1 — JavaScript blockchain
**Source:** PDF pp. 90–95. **Tool:** Node.js. No npm packages needed.

| Question | File | What it demonstrates |
|---|---|---|
| 1 | `Q1_Addition.js` | Add two numbers and store result in a hashed block |
| 2 | `Q2_Happy_Number.js` | Only happy numbers enter the chain |
| 3 | `Q3_Prime_Number.js` | Prime-number result stored in a blockchain |

Run each command in this folder:
```powershell
node Q1_Addition.js
node Q2_Happy_Number.js
node Q3_Prime_Number.js
```
Look for `Valid blockchain: true`. The shared `blockchain.js` has the genesis block, SHA-256 and hash-link validation.
**Exam memory:** SHA-256 → previous hash → current hash → chain validity.
