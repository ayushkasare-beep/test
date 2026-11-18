# Practical 8 — Prime DApp DApp
**Source:** PDF practical 8. **Tools:** Node.js, Ganache, Truffle, MetaMask, browser.

1. Start **Ganache** locally at `http://127.0.0.1:7545` (check Ganache's actual RPC endpoint).
2. From this folder, run:
```powershell
npm install -g truffle
truffle compile
truffle migrate --reset --network development
```
3. Copy the **deployed contract address** from `truffle migrate` output into `frontend/app.js` at `PASTE_DEPLOYED_CONTRACT_ADDRESS_HERE`.
4. In MetaMask, add/select the **Ganache network** with the same RPC URL and chain ID shown by Ganache. Use a **Ganache-only test wallet**, never a real wallet or a private key committed to GitHub.
5. Start a local web server:
```powershell
cd frontend
python -m http.server 5500
```
6. Open `http://localhost:5500`, connect MetaMask and try the actions.

**If it fails:** check Ganache is running; MetaMask is on the same chain as the deployment; check the contract address and `truffle compile`/migration output. The PDF's sample contract addresses are from other local sessions and will not work on your machine.
