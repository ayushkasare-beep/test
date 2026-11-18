from chain import Blockchain

def is_armstrong(n):
    if n < 0:
        return False
    digits = str(n)
    return sum(int(d) ** len(digits) for d in digits) == n

chain = Blockchain()
for n in [12, 153, 1652]:
    chain.add_block({'number': n, 'armstrong': is_armstrong(n)})
chain.show()
print('Chain valid:', chain.is_valid())
