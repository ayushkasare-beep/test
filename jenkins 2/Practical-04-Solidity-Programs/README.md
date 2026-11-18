# Practical 4 — Solidity applications (3 questions)
**Source:** PDF pp. 65–70. **Tool:** Remix IDE. Use Remix VM and compiler 0.8.x.

| Q | File | Try |
|---|---|---|
| 1 | `Q1_Bank.sol` | `createAccount(101,"Asha")`, set **VALUE = 1 ether**, call `deposit(101)`, `getBalance(101)` → 1000000000000000000 wei; `withdraw(101,500000000000000000)` |
| 2 | `Q2_PerfectNumber.sol` | `check(6)` → Perfect, `check(28)` → Perfect, `check(12)` → Not Perfect |
| 3 | `Q3_Voting.sol` | Deploy constructor `["Asha","Ravi"]`; call `vote("Asha")`, then `winner()` → Asha |

For Q3, use a different **Remix VM account** to vote again because the contract allows each address to vote once.
**Exam memory:** `msg.sender` = caller; `msg.value` = ETH sent; `payable` = accepts ETH; `require` = validation.
**Safety improvement:** The supplied PDF's bank lets anyone withdraw from any account number; this version checks account ownership.
