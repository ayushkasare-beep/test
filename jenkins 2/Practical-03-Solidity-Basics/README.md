# Practical 3 — Solidity basics (5 questions)
**Source:** PDF pp. 71–78. **Tool:** [Remix IDE](https://remix.ethereum.org/).

Open `contracts/Q...sol` in Remix. Compile using Solidity **0.8.21 or newer 0.8.x**, then **Deploy & Run Transactions → Remix VM**. Select the named contract, click Deploy and call these functions:

| Q | Contract file | Test function and expected result |
|---|---|---|
| 1 | `Q1_HelloWorld.sol` | `print()` → `Hello World!` |
| 2 | `Q2_Arithmetic.sol` | `add(4,6)` → 10, `div(9,2)` → 4 |
| 3 | `Q3_Student.sol` | `addStud(1,"Asha","Pune")`, `getS(1)` → student record |
| 4 | `Q4_Employee.sol` | `addempD(1,"Asha",20000,"Dev")`, `updatesal(1,25000)`, `getE(1)` |
| 5 | `Q5_Palindrome.sol` | `check(121)` → `Palindrome`; `check(123)` → `Not Palindrome` |

**Recall:** `pure` = no state; `view` = read state; `mapping` = key/value; `struct` = group fields.
