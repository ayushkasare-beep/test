# Blockchain practicals — exam revision

This folder organizes the exercises from the **95-page uploaded blockchain practical PDF**. It is for **practice and permitted open-book revision**, not a substitute for understanding and running the code yourself.

## Index

| PDF practical | Folder | Questions | Setup |
|---|---|---:|---|
| 1 | `Practical-01-JavaScript` | 3: Addition, Happy number, Prime number | Node.js |
| 2 | `Practical-02-Python` | 3: Armstrong, Anagram, Bank transactions | Python |
| 3 | `Practical-03-Solidity-Basics` | 5: Hello World, Arithmetic, Student, Employee, Palindrome | Remix |
| 4 | `Practical-04-Solidity-Programs` | 3: Bank, Perfect number, Voting | Remix |
| 5 | **Not in the uploaded PDF** | — | — |
| 6 | `Practical-06-Inheritance` | 3: Quiz, Single inheritance, Multiple inheritance | Remix |
| 7 | `Practical-07-Addition-DApp` | 1: Addition with Truffle/Ganache/MetaMask | Truffle + Ganache |
| 8 | `Practical-08-Prime-DApp` | 1: Prime check DApp | Truffle + Ganache |
| 9 | `Practical-09-Voting-DApp` | 1: 2-candidate voting DApp | Truffle + Ganache |
| 10 | `Practical-10-Smart-Contracts` | 2: Online store, Course registration | Remix |
| 11 | `Practical-11-Advanced-Contracts` | 2: Vehicle rental overriding, Crowdfunding | Remix |
| 12 | `Practical-12-Hardhat` | 1: Addition DApp | Hardhat + MetaMask |

**Total:** 11 numbered practicals, 25 questions. Read each folder's `README.md` for commands, expected results and steps.

## Fast exam-style preparation
1. For JS/Python, run the numbered Q files from the folder: `node Q1_Addition.js` or `python Q1_Armstrong.py`.
2. For regular Solidity `.sol` code, use [Remix](https://remix.ethereum.org/) → create file → paste code → Solidity Compiler → Deploy & Run → call public function.
3. For DApps, run Ganache/Hardhat first. Deploy locally and **replace the contract address**; PDF's old addresses cannot be reused.
4. When a transaction function changes state, it uses **Transact**. `pure` / `view` functions use **Call**.
5. Need help remembering? Review `QUICK-REVISION.md` then explain each function's purpose aloud.

## Differences and fixes compared with the PDF
- PDF practical 5 is absent. Nothing was invented.
- Fixed Python chain validation (must verify all block hashes and links, not return success early).
- Reworked DApp JS to use one consistent **ethers 6** API and user-generated deployment addresses.
- Fixed Truffle Prime migration's contract-name mismatch.
- Vehicle rental now implements constructor + event required by the stated question.
- Bank example checks account owner before withdrawal (PDF sample omitted this).
- Course registration uses the supplied code's structure/mapping, which differs from the stated inheritance requirement.
- Hardhat practical uses Hardhat **2** syntax because its setup is easier to reproduce in a compact teaching pack; the uploaded PDF uses Hardhat 3.
- Source document contains someone's identifying information, wallet screenshot and sample secrets. **None of those are included here.** Use only throwaway local test keys.

## Requirements
- Node.js 18+ for JavaScript/Truffle, Python 3.10+ for Python exercises.
- Internet access on first `npm install` / Remix compiler fetch and to load JS dependencies in the frontend.
- For Truffle DApps: a local Ganache node at port 7545 and MetaMask browser extension.
- For Hardhat: a local node at port 8545 and MetaMask browser extension.
- Never push `node_modules`, `.env`, real keys, or wallet phrases into GitHub.

All programs are educational examples, not audited smart contracts. Remix, Hardhat and Truffle commands may vary with the tooling installed in your lab.
