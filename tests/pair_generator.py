from itertools import permutations
from random import choices

EXISTING = {
    ('Athens', 'Moscow'),
    ('Hanoi', 'The_Beatles'),
    ('Hanoi', 'Barcelona'),
    ('Heraklion', 'Montevideo'),
    ('Albtert_Einstein', 'Moscow'),
    ('Microsoft', 'Crete'),
    ('Marie_Curie', 'Nigeria'),
    ('Adolf_Hitler', 'Nicaragua'),
    ('Battle_of_Dunkirk', 'Unix'),
    ('Battle_of_France', 'Amstrad')
}

with open("config/nodes.conf") as f:
    nodes = set(node.strip() for node in f.readlines())
    print(nodes)
    print(len(nodes))
    perms = list(permutations(nodes, 2))# - EXISTING
    print(len(perms))

    pairs = choices(perms, k=20)
    print(pairs)
    with open("config/pairs.conf", "w") as fp:
        fp.writelines([f"{pair[0]}, {pair[1]}\n" for pair in pairs])
