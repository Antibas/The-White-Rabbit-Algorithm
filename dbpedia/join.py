from SPARQLWrapper import SPARQLWrapper, JSON
from time import time

from utils.constants import SPARQL_RESOURCE_URL, SPARQL_URL
from utils.utils import get_entity_similarity

def get_entity_label(entity_id: str):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
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
        print(f"Error executing query: {e}")
        return None

def construct_query(entity1: str, entity2: str, depth: int):
    """
    Δημιουργεί ένα SPARQL query για την εύρεση μονοπατιού μεταξύ δύο οντοτήτων.
    Εξαιρεί τριπλέτες με predicate `http://dbpedia.org/ontology/wikiPageWikiLink`.
    """
    
    if depth==1:
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
        for i in range(1, depth-1):
            query += f"?x{i} ?p{i} ?x{i+1} .\n"
            query += f"FILTER (?p{i} != <http://dbpedia.org/ontology/wikiPageWikiLink>)\n"

       
        query += f"?x{depth-1} ?p{depth-1} <{entity2}> .\n"
        query += f"FILTER (?p{depth-1} != <http://dbpedia.org/ontology/wikiPageWikiLink>)\n"

    query += "} limit 1"
    return query

def find_path(entity1: str, entity2: str, max_depth: int=15):
    """
    Βρίσκει μονοπάτι μεταξύ δύο οντοτήτων στο DBpedia μέσω SPARQL queries.
    """
    sparql = SPARQLWrapper(SPARQL_URL)

    # Μετατροπή οντοτήτων σε πλήρη URIs εάν δεν έχουν ήδη.
    if not entity1.startswith("http"):
        entity1 = f"{SPARQL_RESOURCE_URL}{entity1}"
    if not entity2.startswith("http"):
        entity2 = f"{SPARQL_RESOURCE_URL}{entity2}"

    # Επαναληπτική εκτέλεση queries μέχρι το μέγιστο βάθος
    for depth in range(1, max_depth + 1):
        print(f"Executing query with depth {depth}...")
        query = construct_query(entity1, entity2, depth)

        results = execute_query(sparql, query)

        if results and results["results"]["bindings"]:
            print(f"Path found at depth {depth}!")
            return depth, results["results"]["bindings"]

    print("No path found within the given depth.")
    return None, None

def join(entity1: str, entity2: str):
    now = time()
    depth, results = find_path(entity1, entity2)
    if not results:
        return
    
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
    
    totalp=0.0
    totale=0.0
    now2 = time()

    xa2= first_x_value.rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")
    entity1=entity1.replace("_"," ").replace("-"," ")
    entity2= entity2.replace("_"," ").replace("-"," ")

    word_entity_similarity = get_entity_similarity(entity1, xa2)
    if word_entity_similarity is None:
        totalp+=0
    else:
        totalp+= word_entity_similarity
    word_entity_similarity2 = get_entity_similarity(entity1, entity2)
    if word_entity_similarity2 is None:
        totale+=0
    else:
        totale+= word_entity_similarity2

    print(f"\nSimilarity between {entity1} and {xa2}: {word_entity_similarity}")
    for triple in triples:
        print(f"({triple[0]}, {triple[1]}, {triple[2]})")
        xa0= triple[0].rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")
        xa2= triple[2].rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")

        word_entity_similarity = get_entity_similarity(xa0, xa2)
        if word_entity_similarity is None:
            totalp+=0
        else:
            totalp+= word_entity_similarity

        word_entity_similarity2 = get_entity_similarity(xa0, entity2)
        if word_entity_similarity2 is None:
            totale+=0
        else:
            totale+= word_entity_similarity2
        print(f"\nSimilarity between {xa0} and {xa2}: {word_entity_similarity}")

    xa0= last_x_value.rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")
    word_entity_similarity = get_entity_similarity(xa0, entity2)

    if word_entity_similarity is None:
        totalp+=0
    else:
        totalp+= word_entity_similarity

    word_entity_similarity2 = get_entity_similarity(xa0, entity2)
    if word_entity_similarity2 is None:
        totale+=0
    else:
        totale+= word_entity_similarity2
    print(f"\nSimilarity between {xa0} and {entity2}: {word_entity_similarity}")
    nn = totalp/(float(depth))
    nt = totale/(float(depth))
    return now2-now, depth, nn, nt