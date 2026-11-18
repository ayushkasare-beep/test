const ABI = ['function addition(uint256 a, uint256 b) view returns (uint256)'];
let contract;
const result = document.getElementById('result');
document.getElementById('connect').onclick = async () => {
  try {
    if (!window.ethereum) throw Error('Install MetaMask');
    if (!ethers.isAddress(window.ADDRESS)) throw Error('Run deployment first');
    const provider = new ethers.BrowserProvider(window.ethereum);
    await provider.send('eth_requestAccounts', []);
    const signer = await provider.getSigner();
    if (await provider.getCode(window.ADDRESS) === '0x') throw Error('Select Hardhat local network');
    contract = new ethers.Contract(window.ADDRESS, ABI, signer);
    document.getElementById('account').textContent = 'Connected: ' + await signer.getAddress();
  } catch (e) { result.textContent = e.shortMessage || e.message; }
};
document.getElementById('add').onclick = async () => {
  try {
    if (!contract) throw Error('Connect first');
    const a = document.getElementById('a').value;
    const b = document.getElementById('b').value;
    if (!/^\d+$/.test(a) || !/^\d+$/.test(b)) throw Error('Enter nonnegative integers');
    result.textContent = 'Result: ' + (await contract.addition(BigInt(a), BigInt(b))).toString();
  } catch (e) { result.textContent = e.shortMessage || e.message; }
};
