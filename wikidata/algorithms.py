from SPARQLWrapper import JSON, SPARQLWrapper
from time import time

from utils.constants import AGENT, WIKIDATA_URL
from utils.enums import ResourceType
from utils.utils import find_path, find_path_between_nodes, find_path_between_nodes_emb_wiki, get_entity_label, get_entity_similarity, get_wikidata_uri

def join(entity1: str, entity2: str):
    now = time()
    entity1=get_wikidata_uri(entity1)
    entity2=get_wikidata_uri(entity2)
    depth,results = find_path(entity1, entity2, agent=True, resource_type=ResourceType.WIKIDATA)

    if not results:
        return time()-now, 0, 0, 0
    triples = []
    data=results
    # Find the first 'x' key (e.g., x1)
    first_x_key = next(key for key in data[0].keys() if key.startswith('x'))
    
    # Find the last 'x' key (e.g., x5, x7, etc.)
    last_x_key = next(key for key in reversed(data[0].keys()) if key.startswith('x'))
    
    # Extract the corresponding values for first and last 'p' and 'x' keys
    first_x_value = data[0][first_x_key]['value']
    last_x_value = data[0][last_x_key]['value']
    
    for entry in data:
        # Iterate over the 'x' and 'p' pairs and form the desired triples
        for i in range(1, len(entry)//2):  # Skip p0
            x_key = f"x{i}"
            p_key = f"p{i}"
    
            # Get the values
            subject = entry[x_key]['value']
            predicate = entry[p_key]['value']
            object_ = entry[f"x{i+1}"]['value'] if f"x{i+1}" in entry else None
            
            if object_:
                triples.append((subject, predicate, object_))
    
    # Print the triples
    totalp=0.0
    totale=0.0
    now2 = time()

    xa0=get_entity_label(entity1, agent=True, resource_type=ResourceType.WIKIDATA).replace("_"," ").replace("-"," ")
    xa1=get_entity_label(first_x_value, agent=True, resource_type=ResourceType.WIKIDATA).replace("_"," ").replace("-"," ")

    word_entity_similarity = get_entity_similarity(xa0, xa1)
    if word_entity_similarity is None:
        totalp+=0
    else:
        totalp+= word_entity_similarity
    

    print(f"\nSimilarity between {xa0} and {xa1}: {word_entity_similarity}")
    for triple in triples:
        print(f"({triple[0]}, {triple[1]}, {triple[2]})")
        xa0=get_entity_label(triple[0], agent=True, resource_type=ResourceType.WIKIDATA).replace("_"," ").replace("-"," ")
        xa1=get_entity_label(triple[2], agent=True, resource_type=ResourceType.WIKIDATA).replace("_"," ").replace("-"," ")
        word_entity_similarity = get_entity_similarity(xa0, xa1)
        if word_entity_similarity is None:
            totalp+=0
        else:
            totalp+= word_entity_similarity
        xa2=get_entity_label(entity2, agent=True, resource_type=ResourceType.WIKIDATA).replace("_"," ").replace("-"," ")
    
        word_entity_similarity2 = get_entity_similarity(xa0, xa2)
        if word_entity_similarity2 is None:
            totale+=0
        else:
            totale+= word_entity_similarity2
        print(f"\nSimilarity between {get_entity_label(triple[0], agent=True, resource_type=ResourceType.WIKIDATA)} and {get_entity_label(triple[2], agent=True, resource_type=ResourceType.WIKIDATA)}: {word_entity_similarity}")
    xa3=get_entity_label(last_x_value, agent=True, resource_type=ResourceType.WIKIDATA).replace("_"," ").replace("-"," ")
    xa4=get_entity_label(entity2, agent=True, resource_type=ResourceType.WIKIDATA).replace("_"," ").replace("-"," ")

    word_entity_similarity = get_entity_similarity(xa3, xa4)
    if word_entity_similarity is None:
        totalp+=0
    else:
        totalp+= word_entity_similarity

    word_entity_similarity2 = get_entity_similarity(xa3,xa4)
    if word_entity_similarity2 is None:
        totale+=0
    else:
        totale+= word_entity_similarity2
    print(f"\nSimilarity between {xa3} and {xa4}: {word_entity_similarity}   {word_entity_similarity2}")
    nn = totalp/(float(depth))
    nt = totale/(float(depth))
    return now2-now, depth, nn, nt

def embedding(entity1: str, entity2: str):
    now = time()
    # start_node=get_wikidata_uri(entity1)
    # target_node=get_wikidata_uri(entity2)

    word_entity_sim = get_entity_similarity(entity1, entity2)
    print(f"\nSimilarity between {entity1} and {entity2}: {word_entity_sim}")
    depth,path = find_path_between_nodes_emb_wiki(entity1, entity2)#, resource_type=ResourceType.WIKIDATA, agent=True, emb=True)
    if not path:
        return time()-now, 0, 0, 0
    
    totalp=0
    totale=0
    now2 = time()
    lana=len(path)
    ida=1
    for triple in path:
        print(f"({triple[0]}, {triple[1]}, {triple[2]})")
        xa0= triple[0][0].rsplit('/', 1)[-1]
        xa2= triple[2][0].rsplit('/', 1)[-1]
        xa0=get_entity_label(triple[0][0], agent=True, resource_type=ResourceType.WIKIDATA)
        xa2=get_entity_label(triple[2][0], agent=True, resource_type=ResourceType.WIKIDATA)
        
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

def llm(entity1: str, entity2: str):
    pass