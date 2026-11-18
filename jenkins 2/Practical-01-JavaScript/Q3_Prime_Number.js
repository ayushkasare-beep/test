// Practical 1, Q3: store prime checks in blockchain
const { Blockchain } = require('./blockchain');
function isPrime(n) {
  if (!Number.isInteger(n) || n < 2) return false;
  for (let i = 2; i * i <= n; i++) if (n % i === 0) return false;
  return true;
}
const chain = new Blockchain();
for (const n of [17, 4, 29]) chain.addBlock({ number: n, prime: isPrime(n) });
console.log(chain.chain);
console.log('Valid blockchain:', chain.isValid());
