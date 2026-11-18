// Paste the address printed by `truffle migrate --reset --network development`.
const ADDRESS = 'PASTE_DEPLOYED_CONTRACT_ADDRESS_HERE';
const ABI = [
  "function isPrime(uint256 n) view returns (bool)"
];
let contract;
function status(message) { document.getElementById('result').textContent = message; }
async function connect() {
  try {
    if (!window.ethereum) throw Error('Install MetaMask');
    if (!ethers.isAddress(ADDRESS)) throw Error('Paste your own deployed contract address into app.js');
    const provider = new ethers.BrowserProvider(window.ethereum);
    await provider.send('eth_requestAccounts', []);
    const signer = await provider.getSigner();
    const bytecode = await provider.getCode(ADDRESS);
    if (bytecode === '0x') throw Error('No contract at this address on the selected network');
    contract = new ethers.Contract(ADDRESS, ABI, signer);
    document.getElementById('account').textContent = 'Connected: ' + await signer.getAddress();
    status('Connected!');
  } catch(e) { status('Error: ' + (e.shortMessage || e.message)); }
}
document.getElementById('connect').onclick = connect;

document.getElementById('action').onclick = async () => {
  try {
    if (!contract) throw Error('Connect first');
    const n = document.getElementById('number').value;
    if (!/^\d+$/.test(n)) throw Error('Use a whole non-negative number');
    status(n + (await contract.isPrime(BigInt(n)) ? ' is prime' : ' is not prime'));
  } catch(e) { status('Error: ' + (e.shortMessage || e.message)); }
};
