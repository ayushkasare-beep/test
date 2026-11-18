# Practical 11 — Overriding and crowdfunding (2 questions)
**Source:** PDF pp. 11–16. **Tool:** Remix IDE.

| Q | File | Demo steps |
|---|---|---|
| 1 | `Q1_VehicleRental.sol` | Select **CarRental**, deploy with `"Demo Agency"`; `calculateRent(3)` → 30000; `rent(3)` emits event. For **BikeRental**, 3 days → 9000 |
| 2 | `Q2_Crowdfunding.sol` | Select **Contribution**; deploy with goal `100` wei and duration `60` seconds; set **VALUE=100 wei**, `contribute()`, then `totalFunds()` = 100 and `withdraw()` owner can withdraw. |

To test a failed-campaign refund, deploy a **new** Contribution contract (goal 100 wei, duration 10 seconds), contribute 20 wei, wait until deadline, switch back to contributor account and call `refund()`.
**Recall:** `virtual` = may be changed by child, `override` = replaces parent implementation, `event` = log.
**Correction:** Source vehicle rental exercise requests constructor + event, but its sample code omits them. This version includes both.
