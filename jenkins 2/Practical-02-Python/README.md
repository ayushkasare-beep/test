# Practical 2 — Python blockchain
**Source:** PDF pp. 79–89. **Tool:** Python 3.10+ (standard library only).

| Question | File | Example |
|---|---|---|
| 1 | `Q1_Armstrong.py` | 153 is Armstrong |
| 2 | `Q2_Anagram.py` | `raj` and `jar` are anagrams |
| 3 | `Q3_Bank_Transactions.py` | Deposit and withdraw; final balance 7100 |

Run:
```powershell
python Q1_Armstrong.py
python Q2_Anagram.py
python Q3_Bank_Transactions.py
```
Shared `chain.py` implements SHA-256 hash chaining. Unlike the PDF's Armstrong validity loop, this version checks *every block* and *both* conditions using `!=` and returns `False` for tampering.
**Exam memory:** `hashlib.sha256(text.encode()).hexdigest()`; previous hash = last block's hash.
