from csv import writer
from algorithms.dbpedia import join, embedding

def llm(entity1: str, entity2: str):
    return 0,0,0,0

PAIRS = []
with open("config/pairs.conf") as pairs:
    for pair in pairs.readlines():
        if pair.startswith("#"):
            continue
        pair_sp = pair.split(",")
        PAIRS.append((pair_sp[0].strip(), pair_sp[1].strip()))
for pair in PAIRS:
    with open("measurements/dbpedia.csv", "a", newline="") as csv:
        csv_writer = writer(csv, delimiter=",")
        csv_writer.writerow([pair[0], pair[1], *join(*pair), *embedding(*pair), *llm(*pair)])