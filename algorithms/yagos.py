from time import time
from utils.constants import YAGOS_RESOURCE_URL, YAGOS_URL
from utils.enums import ResourceType
from utils.logger import LOGGER
from utils.pathfinder import find_path, find_path_between_nodes
from utils.utils import get_entity_similarity


def join(entity1: str, entity2: str):
    now = time()
    paths: list[tuple[str, str, str]] = []
    depth, results = find_path(entity1, entity2, agent=True, resource_type=ResourceType.YAGOS)
    if not results:
        return round(time()-now), 0, 0, 0, []
    triples: list[tuple[str, str, str]] = []
    data=results
    first_p_key = next(key for key in data[0].keys() if key.startswith('p'))

    # Find the last 'p' key (e.g., p5, p10, etc.)
    last_p_key = next(key for key in reversed(data[0].keys()) if key.startswith('p'))
    
    # Find the first 'x' key (e.g., x1)
    first_x_key = next(key for key in data[0].keys() if key.startswith('x'))
    
    # Find the last 'x' key (e.g., x5, x7, etc.)
    last_x_key = next(key for key in reversed(data[0].keys()) if key.startswith('x'))
    
    # Extract the corresponding values for first and last 'p' and 'x' keys
    first_p_value = data[0][first_p_key]['value']
    last_p_value = data[0][last_p_key]['value']
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
    
    totalp=0.0
    totale=0.0
    now2 = time()

    paths.append((entity1, first_p_value, first_x_value))
    xa2= first_x_value.rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")
    entity1=entity1.replace("_"," ").replace("-"," ")
    entity2= entity2.replace("_"," ").replace("-"," ")

    word_entity_similarity = get_entity_similarity(entity1, xa2)
    totalp+= word_entity_similarity
    word_entity_similarity2 = get_entity_similarity(entity1, entity2)
    totale+= word_entity_similarity2

    LOGGER.info(f"Similarity between {entity1} and {xa2}: {word_entity_similarity}")
    for triple in triples:
        # LOGGER.info(f"({triple[0]}, {triple[1]}, {triple[2]})")
        xa0= triple[0].rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")
        xa2= triple[2].rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")

        word_entity_similarity = get_entity_similarity(xa0, xa2)
        totalp+= word_entity_similarity

        word_entity_similarity2 = get_entity_similarity(xa0, entity2)
        totale+= word_entity_similarity2
        LOGGER.info(f"Similarity between {xa0} and {xa2}: {word_entity_similarity}")
        
        paths.append(triple)

    paths.append((last_x_value, last_p_value, entity2))
    xa0= last_x_value.rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")
    word_entity_similarity = get_entity_similarity(xa0, entity2)

    totalp+= word_entity_similarity

    word_entity_similarity2 = get_entity_similarity(xa0, entity2)
    totale+= word_entity_similarity2
    LOGGER.info(f"Similarity between {xa0} and {entity2}: {word_entity_similarity}")
    nn = totalp/(float(depth))
    nt = totale/(float(depth))
    return round(now2-now), depth, round(nn, 2), round(nt, 2), paths

def embedding(entity1: str, entity2: str):
    start_node=f"{YAGOS_RESOURCE_URL}/{entity1}"
    target_node=f"{YAGOS_RESOURCE_URL}/{entity2}"
    now = time()
    word_entity_sim = get_entity_similarity(entity1, entity2)
    
    LOGGER.info(f"Similarity between {start_node} and {target_node}: {word_entity_sim}")
    depth,path = find_path_between_nodes(start_node, target_node, YAGOS_URL, resource_type=ResourceType.YAGOS)
    if not path:
        return round(time()-now), 0, 0, 0, []
    
    # for step in path:
    #     LOGGER.info(f"{step[0]} --{step[1]}--> {step[2]}")
    totalp=0.0
    totale=0.0
    now2 = time()
    
    lana=len(path)
    ida=1
    for triple in path:
        # LOGGER.info(f"({triple[0]}, {triple[1]}, {triple[2]})")
        xa0= triple[0][0].rsplit('/', 1)[-1]
        xa2= triple[2][0].rsplit('/', 1)[-1]
        xa0=xa0.replace("_"," ").replace("-",' ')
        xa2=xa2.replace("_"," ").replace("-",' ')
        xa3=entity2
        xa3=xa3.replace("_"," ").replace("-",' ')
    
        word_entity_similarity = get_entity_similarity(xa0, xa2)
        totalp+= word_entity_similarity
    
        word_entity_similarity2 = get_entity_similarity(xa0, xa3)
        totale+= word_entity_similarity2
        LOGGER.info(f"Similarity between {xa0} and {xa2}: {word_entity_similarity} {word_entity_similarity2} ")
        ida=ida+1
        if ida==lana:
            break
    nn = totalp/(float(depth))
    nt = totale/(float(depth))
    return round(now2-now), depth, round(nn, 2), round(nt, 2), path

def llm(entity1: str, entity2: str):
    start_node=f"{YAGOS_RESOURCE_URL}/{entity1}"
    target_node=f"{YAGOS_RESOURCE_URL}/{entity2}"
    now = time()
    word_entity_sim = get_entity_similarity(entity1, entity2)
    
    LOGGER.info(f"Similarity between {start_node} and {target_node}: {word_entity_sim}")
    depth,path = find_path_between_nodes(start_node, target_node, YAGOS_URL, resource_type=ResourceType.YAGOS, llm=True)
    if not path:
        return round(time()-now), 0, 0, 0, []
    
    # for step in path:
    #     LOGGER.info(f"{step[0]} --{step[1]}--> {step[2]}")
    totalp=0.0
    totale=0.0
    now2 = time()
    
    lana=len(path)
    ida=1
    for triple in path:
        # LOGGER.info(f"({triple[0]}, {triple[1]}, {triple[2]})")
        xa0= triple[0][0].rsplit('/', 1)[-1]
        xa2= triple[2][0].rsplit('/', 1)[-1]
        xa0=xa0.replace("_"," ").replace("-",' ')
        xa2=xa2.replace("_"," ").replace("-",' ')
        xa3=entity2
        xa3=xa3.replace("_"," ").replace("-",' ')
    
        word_entity_similarity = get_entity_similarity(xa0, xa2)
        totalp+= word_entity_similarity
    
        word_entity_similarity2 = get_entity_similarity(xa0, xa3)
        totale+= word_entity_similarity2
        LOGGER.info(f"Similarity between {xa0} and {xa2}: {word_entity_similarity} {word_entity_similarity2} ")
        ida=ida+1
        if ida==lana:
            break
    nn = totalp/(float(depth))
    nt = totale/(float(depth))
    return round(now2-now), depth, round(nn, 2), round(nt, 2), path