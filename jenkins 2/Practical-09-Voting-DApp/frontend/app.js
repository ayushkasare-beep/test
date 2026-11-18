// Paste the address printed by `truffle migrate --reset --network development`.
const ADDRESS = 'PASTE_DEPLOYED_CONTRACT_ADDRESS_HERE';
const ABI = [
  "function candidate1Votes() view returns (uint256)",
  "function candidate2Votes() view returns (uint256)",
  "function voteCandidate1()",
  "function voteCandidate2()"
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

async function refresh() {
  if (!contract) throw Error('Connect first');
  document.getElementById('votes1').textContent = (await contract.candidate1Votes()).toString();
  document.getElementById('votes2').textContent = (await contract.candidate2Votes()).toString();
}
async function vote(candidate) {
  try {
    if (!contract) throw Error('Connect first');
    status('Confirm the transaction in MetaMask');
    const tx = candidate === 1 ? await contract.voteCandidate1() : await contract.voteCandidate2();
    await tx.wait();
    await refresh();
    status('Vote recorded!');
  } catch(e) { status('Error: ' + (e.shortMessage || e.message)); }
}
document.getElementById('vote1').onclick = () => vote(1);
document.getElementById('vote2').onclick = () => vote(2);
document.getElementById('refresh').onclick = () => refresh().catch(e => status(e.message));
