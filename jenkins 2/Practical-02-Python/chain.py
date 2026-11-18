"""Simple educational SHA-256 hash-linked blockchain (not a cryptocurrency)."""
import hashlib
import json
from datetime import datetime, timezone

class Block:
    def __init__(self, number, data, previous_hash='0'):
        self.number = number
        self.time = datetime.now(timezone.utc).isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        text = json.dumps([self.number, self.time, self.data, self.previous_hash], sort_keys=True)
        return hashlib.sha256(text.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, {'name': 'Genesis'})]

    def add_block(self, data):
        previous = self.chain[-1]
        self.chain.append(Block(len(self.chain), data, previous.hash))

    def is_valid(self):
        for i, block in enumerate(self.chain):
            if block.hash != block.calculate_hash():
                return False
            if i > 0 and block.previous_hash != self.chain[i - 1].hash:
                return False
        return True

    def show(self):
        for block in self.chain:
            print(f'Block {block.number}: {block.data}')
            print(f'  Current hash: {block.hash}')
            print(f'  Previous hash: {block.previous_hash}')
