from multiprocessing import Process, Queue
from re import fullmatch
from typing import Callable
from SPARQLWrapper import JSON, SPARQLWrapper
from numpy import dot
from numpy.linalg import norm
from utils.constants import AGENT, BASE_URLS, WIKI2VEC, WIKIDATA_URL
from utils.enums import ResourceType
from utils.logger import LOGGER

def claude_message(epel, lista, target_node):
    return f"do not insert δικους σου nodes αλλα επελεξε ακριβως {epel} αν ειναι διαθεσιμoi απο την {lista} αυτους που πλησιαζουν πιο πολυ  α΄΄΄΄λλα και αλλους που θα μπορουσαν πιο πιθανα να οδηγησουν στον κομβο {target_node} επελεξε συνολικα +{epel} και δωσε τους ενα σκορ εγγυτητας με τρια δεκαδικα. εαν δεν πλησιαζει πολυ δωσε σκορ κατω απο 0.4. Αν πλησιζει πολυ δωσε πανω απο 0.7. Επελεξε τους κομβους με τα μεγαλυτερα σκορ. Επισης μην επιλεξεις nodes που αναφερονται σε γενικες κατηγοριες αλλα μονο σε υπαρκτα entities. Return them  as string of entities. An entity is node comma score. Score is from 0.0 for irrelevant to target to 1 .if the node includes the word of the target, return as a score 1.0 .Do not comment scores.If target node is exacly found in list give it score 500.0. Final string is entity#entity#entity etc mean seperate entities with without headers # Return plain string.Αν δεν ειναι διαθεσιμοι 6 κομβοι δεν πειραζει και ΜΗΝ ΔΗΜΙΟΥΡΓΗΣΕΙΣ ΚΟΜΒΟΥΣ ΑΠΟ ΤΗΝ ΔΙΚΗ ΣΟΥ ΓΝΩΣΗ που δεν υπαρχουν στην λιστα. ΑΚΟΜΑ ΚΑΙ ΕΝΑΣ ΝΑ ΕΙΝΑΙ Ο ΚΟΜΒΟΣ ΕΠΕΣΤΡΕΨΕ ΤΟΝ"

def _wrapper(func: Callable[[str, str], tuple], entity1: str, entity2: str, queue: Queue):
    result = func(entity1, entity2)
    queue.put(result)

def timeout(func: Callable[[str, str], tuple], entity1: str, entity2: str, timeout: int=360):
    queue = Queue()
    process = Process(target=_wrapper, args=(func, entity1, entity2, queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        LOGGER.error(f"Pair {(entity1, entity2)} timed out. Continuing...")
        process.terminate()
        process.join()
    
    return queue.get() if not queue.empty() else (timeout,0,0,0,[])

def read_conf(filename: str):
    with open(filename) as pairs:
        result = list()
        for pair in pairs.readlines():
            if pair.startswith("#"):
                LOGGER.info(f"Skipping {pair}...")
                continue
            pair_sp = pair.split(",")
            result.append((pair_sp[0].strip(), pair_sp[1].strip()))
        return result

def execute_query(sparql: SPARQLWrapper, query: str):
    """
    Εκτελεί το SPARQL query και επιστρέφει τα αποτελέσματα.
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(60)
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        LOGGER.error(f"Error executing query: {e}")
        return None

def construct_query(entity1: str, entity2: str, depth: int, wikidata: bool):
    """
    Δημιουργεί ένα SPARQL query για την εύρεση μονοπατιού μεταξύ δύο οντοτήτων.
    Εξαιρεί τριπλέτες με predicate `http://dbpedia.org/ontology/wikiPageWikiLink`.
    """
    
    if not wikidata and depth==1:
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT * WHERE {{
        <{entity1}> ?p0 <{entity2}> .
        FILTER (?p0 != <http://dbpedia.org/ontology/wikiPageWikiLink>)
        """
    else:
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT * WHERE {{
        <{entity1}> ?p0 ?x1 .
        FILTER (?p0 != <http://dbpedia.org/ontology/wikiPageWikiLink>)
        """
        if not wikidata:
            depth -= 1
        for i in range(1, depth):
            query += f"?x{i} ?p{i} ?x{i+1} .\n"
            query += f"FILTER (?p{i} != <http://dbpedia.org/ontology/wikiPageWikiLink>)\n"

       
        query += f"?x{depth} ?p{depth} <{entity2}> .\n"
        query += f"FILTER (?p{depth} != <http://dbpedia.org/ontology/wikiPageWikiLink>)\n"

    query += "} limit 1"
    # LOGGER.debug(query)
    return query

def get_entity_label(entity_id: str, agent: bool=False, resource_type: ResourceType=ResourceType.DBPEDIA):
    sparql = SPARQLWrapper(BASE_URLS[resource_type], agent=AGENT) if agent else SPARQLWrapper(BASE_URLS[resource_type])

    
    query = f"""
    SELECT ?item ?itemLabel WHERE {{
      BIND(<{entity_id}> AS ?item)
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    # Extract label from the results
    if results["results"]["bindings"]:
        label = results["results"]["bindings"][0]["itemLabel"]["value"]
        return label
    
    return None

def get_entity_similarity(entity1: str, entity2: str):
    """
    Calculate similarity between two Wikipedia entities.
    
    Args:
        entity1 (str): First entity title
        entity2 (str): Second entity title
        
    Returns:
        float: Similarity score between 0 and 1
    """
    try:
        LOGGER.debug(F"{entity1=}")
        LOGGER.debug(F"{entity2=}")
        if not entity1.strip() or not entity2.strip():
            return 0
        # Get entity embeddings
        entity1_vec = WIKI2VEC.get_entity_vector(entity1.strip())
        entity2_vec = WIKI2VEC.get_entity_vector(entity2.strip())
        
        # Calculate cosine similarity
        similarity: float = dot(entity1_vec, entity2_vec) / (
        norm(entity1_vec) * norm(entity2_vec)
        )
        return similarity
    except KeyError as e:
        LOGGER.error(f"Entity not found: {e.__str__()}")
        return 0

def is_english_only(s):
    return bool(fullmatch(r"[A-Za-z0-9 /\-()_:/.]+", s))

def get_wikidata_uri(label: str):
    sparql = SPARQLWrapper(WIKIDATA_URL,agent=AGENT)
    
    query = f"""
    SELECT ?item WHERE {{
      ?item rdfs:label "{label}"@en.
    }}
    LIMIT 1
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]["item"]["value"]
    return None
