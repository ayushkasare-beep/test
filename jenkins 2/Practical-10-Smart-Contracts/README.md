# Practical 10 — Store and course registration (2 questions)
**Source:** PDF pp. 17–23. **Tool:** Remix IDE (0.8.x, Remix VM).

| Q | File | Demo steps |
|---|---|---|
| 1 | `Q1_OnlineStore.sol` | Deploy **OnlineStore** with `1, 10, 2, "Apple"`; set **VALUE = 10 wei** then `purchase()`; `disProduct()` shows stock 1 |
| 2 | `Q2_CourseRegistration.sol` | Deploy with `"Blockchain", 10, 2`; set **VALUE = 10 wei**; call `register("Asha", 101)`; call `registeredCount()` → 1; `seatsLeft()` → 1 |

**Important:** In Remix, contract constructor inputs are entered before Deploy. ETH values must match the constructor price/fee in **wei**; the value control defaults to wei unless changed.
**Note:** The source question describes Person/Student inheritance for Q2, but its supplied code instead defines CourseRegistration with a `Student` struct. This pack follows the supplied implementation and flags that difference.
