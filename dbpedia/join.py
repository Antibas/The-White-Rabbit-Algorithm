from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime
from sys import argv

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

# def get_entity_similarity(wiki2vec: Wikipedia2Vec, entity1: str, entity2: str):
#     """
#     Calculate similarity between two Wikipedia entities.
    
#     Args:
#         wiki2vec: Wikipedia2Vec model
#         entity1 (str): First entity title
#         entity2 (str): Second entity title
        
#     Returns:
#         float: Similarity score between 0 and 1
#     """
#     try:
#         # Get entity embeddings
#         entity1_vec = wiki2vec.get_entity_vector(entity1)
#         entity2_vec = wiki2vec.get_entity_vector(entity2)
        
#         # Calculate cosine similarity
#         similarity = np.dot(entity1_vec, entity2_vec) / (
#         np.linalg.norm(entity1_vec) * np.linalg.norm(entity2_vec)
#         )
#         return similarity
#     except KeyError as e:
#         print(f"Entity not found: {e}")
#         return None

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
    print("PO "+query)
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
    return None

def join(entity1: str, entity2: str):
    now = datetime.now()
    d,results = find_path(entity1, entity2)
    if not results:
        return
    
    # print(f"Paths found: {results}")
    now2 = datetime.now()
    triples = []
    data=results
    # first_p_key = next(key for key in data[0].keys() if key.startswith('p'))

    # Find the last 'p' key (e.g., p5, p10, etc.)
    # last_p_key = next(key for key in reversed(data[0].keys()) if key.startswith('p'))
    
    # Find the first 'x' key (e.g., x1)
    first_x_key = next(key for key in data[0].keys() if key.startswith('x'))
    
    # Find the last 'x' key (e.g., x5, x7, etc.)
    last_x_key = next(key for key in reversed(data[0].keys()) if key.startswith('x'))
    
    # Extract the corresponding values for first and last 'p' and 'x' keys
    # first_p_value = data[0][first_p_key]['value']
    # last_p_value = data[0][last_p_key]['value']
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
    now2 = datetime.now()

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
    # print(str(totale))

    # print(f"\nSimilarity between {entity1} and {xa2}: {word_entity_similarity}")
    for triple in triples:
        print(f"({triple[0]}, {triple[1]}, {triple[2]})")
        #time.sleep(1)
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
        # print(f"\nSimilarity between {xa0} and {xa2}: {word_entity_similarity}")

    #time.sleep(1)

    xa0= last_x_value.rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")
    #xa2= triple[0].rsplit('/', 1)[-1]
    # xa4= entity2.rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")

    word_entity_similarity = get_entity_similarity(xa0, entity2)

    if word_entity_similarity is None:
        totalp+=0
    else:
        totalp+= word_entity_similarity
    #time.sleep(1)

    word_entity_similarity2 = get_entity_similarity(xa0, entity2)
    if word_entity_similarity2 is None:
        totale+=0
    else:
        totale+= word_entity_similarity2
    # print(f"\nSimilarity between {xa0} and {entity2}: {word_entity_similarity}")
    # print("TOTAL P "+str(totalp/(float(d)))+ " TOTAL E "+str(totale/(float(d))))
    nn = str(totalp/(float(d)))
    nt = str(totale/(float(d)))
    current_time = now.strftime("%H:%M:%S")  #
    current_time2 = now2.strftime("%H:%M:%S")  #
    # print(current_time)
    # print(current_time2)
    return nn, nt, current_time, current_time2

if __name__ == "__main__":
    args = argv[1:]  # Exclude script name
    print("2 Received Arguments:", args)
    now = datetime.now()
    #entity1 = input("Enter the first entity (e.g., Albert_Einstein): ").strip()
    #entity2 = input("Enter the second entity (e.g., Italy): ").strip()
    entity1="California"
    entity1="Albert_Camus"
    entity1="Adolf_Hitler"
    entity1="Warner_Bros"
    entity1="Chania"
    start_node = "http://yago-knowledge.org/resource/The_Beatles"
    entity1="The_Beatles"
    entity1='Lamia'
    entity1="Boris_Yeltsin"
    entity1="Heraklion"
    entity1="Boris_Yeltsin"
    entity1="New_York"
    entity1="Morocco"
    entity1="Vikings"
    entity1="Barack_Obama"
    entity1="Boris_Yeltsin"
    entity1='Lamia'

    #entity2="Adolf_Hitler"
    entity2="Heraklion"
    #entity2="John_Lennon"
    #entity2="Jimmy_Carter"
    entity2="China"
    entity2="Nigeria"
    entity2="Izmir"
    entity2="Bavaria"
    entity2="The_Flintstones"
    entity2="Moscow"
    entity2="Heraklion"
    entity2="Nigeria"

    entity2="Moscow"
    entity2="Montevideo"
    entity2="Hawaii"
    entity2="Hanoi"
    
    entity2="Edessa"
    entity2="Pella"
    entity2="NATO"
    entity2="Hawaii"
    entity2="Moscow"
    args=['Athens','Moscow']
    entity1=args[0]
    entity2=args[1]
    d,results = find_path(entity1, entity2)
    if results:

        print("Paths found:")
        for result in results:
            print(result)
        now2 = datetime.now()
        triples = []
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
        #d=d+1
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
        now2 = datetime.now()

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
        print(str(totale))
   
        print(f"\nSimilarity between {entity1} and {xa2}: {word_entity_similarity}")
        for triple in triples:
            print(f"({triple[0]}, {triple[1]}, {triple[2]})")
            #time.sleep(1)
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

        #time.sleep(1)

        xa0= last_x_value.rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")
        #xa2= triple[0].rsplit('/', 1)[-1]
        xa4= entity2.rsplit('/', 1)[-1].replace("_"," ").replace("-"," ")

        word_entity_similarity = get_entity_similarity(xa0, entity2)

        if word_entity_similarity is None:
            totalp+=0
        else:
            totalp+= word_entity_similarity
        #time.sleep(1)

        word_entity_similarity2 = get_entity_similarity(xa0, entity2)
        if word_entity_similarity2 is None:
            totale+=0
        else:
            totale+= word_entity_similarity2
        print(f"\nSimilarity between {xa0} and {entity2}: {word_entity_similarity}")
        print("TOTAL P "+str(totalp/(float(d)))+ " TOTAL E "+str(totale/(float(d))))
        
        # data=results
        # # Filter out 'p0' and extract valid keys
        # valid_keys = [k for k in data.keys() if k != 'p0']
        #
        # # Sort keys numerically (ignoring p0)
        # sorted_keys = sorted(valid_keys, key=lambda k: int(re.findall(r'\d+', k)[0]))
        #
        # # Generate triples dynamically
        # triples = []
        # for i in range(0, len(sorted_keys) - 2, 2):  # Step by 2 (xN → pN → xN+1)
        #     subj = data[sorted_keys[i]]['value']     # xN
        #     pred = data[sorted_keys[i + 1]]['value'] # pN
        #     obj = data[sorted_keys[i + 2]]['value']  # xN+1
        #
        #     triples.append((subj, pred, obj))
        #
        # # Print RDF triples
        # for subj, pred, obj in triples:
        #     #file.write(f"<{subj}> <{pred}> <{obj}> \n")
        #     print(f"<{subj}> <{pred}> <{obj}> .")
        current_time = now.strftime("%H:%M:%S")  #
        current_time2 = now2.strftime("%H:%M:%S")  #
        print(current_time)
        print(current_time2)

    else:
        print("No paths found between the entities.")