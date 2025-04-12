from time import time
from anthropic import Anthropic

from utils.constants import SPARQL_RESOURCE_URL, SPARQL_URL
from utils.utils import find_path_between_nodes, get_entity_similarity
client = Anthropic()

def embedding(entity1: str, entity2: str):
    start_node=f"{SPARQL_RESOURCE_URL}{entity1}"
    target_node=f"{SPARQL_RESOURCE_URL}{entity2}"
    now = time()
    word_entity_sim = get_entity_similarity(entity1, entity2)
    
    print(f"\nSimilarity between {start_node} and {target_node}: {word_entity_sim}")
    depth,path = find_path_between_nodes(start_node, target_node, f"{SPARQL_URL}/query")
    if not path:
        return
    for step in path:
        print(f"{step[0]} --{step[1]}--> {step[2]}")
    totalp=0.0
    totale=0.0
    now2 = time()
    
    lana=len(path)
    ida=1
    for triple in path:
        print(f"({triple[0]}, {triple[1]}, {triple[2]})")
        xa0= triple[0][0].rsplit('/', 1)[-1]
        xa2= triple[2][0].rsplit('/', 1)[-1]
        xa0=xa0.replace("_"," ").replace("-",' ')
        xa2=xa2.replace("_"," ").replace("-",' ')
        xa3=entity2
        xa3=xa3.replace("_"," ").replace("-",' ')
    
        word_entity_similarity = get_entity_similarity(xa0, xa2)
        if word_entity_similarity is None:
            totalp+=0
        else:
            totalp+= word_entity_similarity
    
        word_entity_similarity2 = get_entity_similarity(xa0, xa3)
        if word_entity_similarity2 is None:
            totale+=0
        else:
            totale+= word_entity_similarity2
        print(f"\nSimilarity between {xa0} and {xa2}: {word_entity_similarity} {word_entity_similarity2} ")
        ida=ida+1
        if ida==lana:
            break
    nn = totalp/(float(depth))
    nt = totale/(float(depth))
    return now2-now, depth, nn, nt