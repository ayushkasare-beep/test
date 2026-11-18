from chain import Blockchain

def is_anagram(a, b):
    return sorted(a.lower().replace(' ', '')) == sorted(b.lower().replace(' ', ''))

chain = Blockchain()
for a, b in [('undertale', 'deltarune'), ('raj', 'jar'), ('hello', 'world')]:
    chain.add_block({'first': a, 'second': b, 'anagram': is_anagram(a, b)})
chain.show()
print('Chain valid:', chain.is_valid())
