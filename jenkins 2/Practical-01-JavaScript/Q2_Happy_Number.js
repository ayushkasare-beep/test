// Practical 1, Q2: add only happy numbers to blockchain
const { Blockchain } = require('./blockchain');
function isHappy(n) {
  if (!Number.isInteger(n) || n <= 0) return false;
  const seen = new Set();
  while (n !== 1 && !seen.has(n)) {
    seen.add(n);
    n = String(n).split('').reduce((sum, d) => sum + Number(d) ** 2, 0);
  }
  return n === 1;
}
const chain = new Blockchain();
for (const n of [19, 20, 7]) {
  if (isHappy(n)) chain.addBlock({ number: n, happy: true });
}
console.log(chain.chain);
console.log('Valid blockchain:', chain.isValid());
