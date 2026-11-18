from chain import Blockchain

class BankChain:
    def __init__(self):
        self.chain = Blockchain()
        self.balances = {}

    def deposit(self, account, amount):
        if amount <= 0: raise ValueError('Amount must be positive')
        self.balances[account] = self.balances.get(account, 0) + amount
        self.chain.add_block({'account': account, 'type': 'DEPOSIT', 'amount': amount,
                              'balance': self.balances[account]})

    def withdraw(self, account, amount):
        if amount <= 0 or self.balances.get(account, 0) < amount:
            raise ValueError('Invalid amount or insufficient balance')
        self.balances[account] -= amount
        self.chain.add_block({'account': account, 'type': 'WITHDRAW', 'amount': amount,
                              'balance': self.balances[account]})

bank = BankChain()
bank.deposit('Demo', 11000)
bank.deposit('Demo', 5200)
bank.withdraw('Demo', 6700)
bank.withdraw('Demo', 900)
bank.withdraw('Demo', 1500)
bank.chain.show()
print('Final balance:', bank.balances['Demo']) # 7100
print('Chain valid:', bank.chain.is_valid())
