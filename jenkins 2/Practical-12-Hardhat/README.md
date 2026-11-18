# Practical 12 — Hardhat addition DApp
**Source:** PDF pp. 1–10. Uses **Hardhat 2** with ethers 6 for a stable CommonJS classroom setup (the PDF uses Hardhat 3 prompts).

## Run on Windows PowerShell
In this folder:
```powershell
npm install
npx hardhat compile
```
Terminal 1 (leave running):
```powershell
npx hardhat node
```
Terminal 2:
```powershell
npx hardhat run scripts/deploy.js --network localhost
```
Expected output includes `10 + 20 = 30`. The script also writes the new contract address to `frontend/config.js`.
Terminal 3:
```powershell
cd frontend
python -m http.server 5500
```
Open `http://localhost:5500`. In MetaMask, add/select local Hardhat network: RPC `http://127.0.0.1:8545`, Chain ID `31337`. If test transactions need gas, import **only an ephemeral account printed by the local Hardhat test node**; never expose or commit real wallet credentials.

**Important:** After restarting `npx hardhat node`, deploy again: local chain state and contract addresses reset.
**Learn:** Compile → run local node → deploy → connect wallet → call `addition`.
