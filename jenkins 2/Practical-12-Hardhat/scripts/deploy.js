const hre = require('hardhat');
const fs = require('fs');
const path = require('path');
async function main() {
  const factory = await hre.ethers.getContractFactory('Add');
  const contract = await factory.deploy();
  await contract.waitForDeployment();
  const address = await contract.getAddress();
  console.log('Deployed contract:', address);
  console.log('10 + 20 =', (await contract.addition(10, 20)).toString());
  const configPath = path.join(__dirname, '..', 'frontend', 'config.js');
  fs.writeFileSync(configPath, 'window.ADDRESS = ' + JSON.stringify(address) + ';\n');
  console.log('Updated frontend/config.js');
}
main().catch(e => { console.error(e); process.exitCode = 1; });
