const crypto = require('crypto');

class Block {
  constructor(index, data, previousHash = '0') {
    this.index = index;
    this.timestamp = new Date().toISOString();
    this.data = data;
    this.previousHash = previousHash;
    this.hash = this.calculateHash();
  }
  calculateHash() {
    const text = JSON.stringify([this.index, this.timestamp, this.data, this.previousHash]);
    return crypto.createHash('sha256').update(text).digest('hex');
  }
}

class Blockchain {
  constructor() {
    this.chain = [new Block(0, { name: 'Genesis' })];
  }
  addBlock(data) {
    const previous = this.chain[this.chain.length - 1];
    this.chain.push(new Block(this.chain.length, data, previous.hash));
  }
  isValid() {
    for (let i = 0; i < this.chain.length; i++) {
      const block = this.chain[i];
      if (block.hash !== block.calculateHash()) return false;
      if (i > 0 && block.previousHash !== this.chain[i - 1].hash) return false;
    }
    return true;
  }
}
module.exports = { Block, Blockchain };
