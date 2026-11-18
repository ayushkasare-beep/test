# Practical 6 — Quiz and inheritance (3 questions)
**Source:** PDF pp. 60–64. **Tool:** Remix IDE.

| Q | File | Try |
|---|---|---|
| 1 | `Q1_Quiz.sol` | Deploy Quiz → `add("2+2?","4")` → `ansQ(0,"4")` → `correctCount()` = 1 |
| 2 | `Q2_SingleInheritance.sol` | Select **Bike**, deploy with `"Two-wheeler", "Bike", "Honda", "Red"`, call `disp` and `dispB` |
| 3 | `Q3_MultipleInheritance.sol` | Select **Child**, deploy with `"Parent A", "Parent B", "Child C"`, call `disp()` |

**Exam memory:** `contract Child is Parent1, Parent2`, constructor chaining, events via `emit`, compare strings using `keccak256(bytes(a)) == keccak256(bytes(b))`.
