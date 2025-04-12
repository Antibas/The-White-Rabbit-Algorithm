from csv import writer
from algorithms.dbpedia import join, embedding, llm

PAIRS = [
    ('Battle_of_Dunkirk', 'Unix'),
    ('Battle_of_France', 'Amstrad')
]

with open("measurements/dbpedia.csv", "a", newline="") as csv:
    csv_writer = writer(csv, delimiter=",")
    for pair in PAIRS:
        csv_writer.writerow([pair[0], pair[1], *join(*pair), *embedding(*pair), *llm(*pair)])