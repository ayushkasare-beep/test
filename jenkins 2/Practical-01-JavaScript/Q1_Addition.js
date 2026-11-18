// Practical 1, Q1: addition of two numbers stored in a block
const { Blockchain } = require('./blockchain');
const chain = new Blockchain();
const a = 23, b = 76;
chain.addBlock({ a, b, result: a + b });
console.log(chain.chain);
console.log('Valid blockchain:', chain.isValid()); // true
