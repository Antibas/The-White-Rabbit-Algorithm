from re import fullmatch
from SPARQLWrapper import JSON, SPARQLWrapper
import numpy as np
from utils.constants import AGENT, BASE_URLS, WIKI2VEC, WIKIDATA_URL
from utils.enums import ResourceType
from utils.logger import LOGGER

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
        LOGGER.exception(f"Error executing query: {e}")
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
    LOGGER.debug(query)
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
        # Get entity embeddings
        entity1_vec = WIKI2VEC.get_entity_vector(entity1)
        entity2_vec = WIKI2VEC.get_entity_vector(entity2)
        
        # Calculate cosine similarity
        similarity = np.dot(entity1_vec, entity2_vec) / (
        np.linalg.norm(entity1_vec) * np.linalg.norm(entity2_vec)
        )
        return similarity
    except KeyError as e:
        LOGGER.exception(f"Entity not found: {e}")
        return None

def get_most_similar_entities(entity_title, top_k=10):
    """
    Find the most similar entities to a given entity.
    
    Args:
        entity_title (str): Target entity title
        top_k (int): Number of similar entities to return
        
    Returns:
        list: List of (entity_title, similarity_score) tuples
    """
    try:
        return WIKI2VEC.most_similar(WIKI2VEC.get_entity(entity_title), top_k)
    except KeyError as e:
        LOGGER.exception(f"Entity not found: {e}")
        return None

def get_word_entity_similarity(word, entity_title):
    """
    Calculate similarity between a word and an entity.
    
    Args:
        word (str): Input word
        entity_title (str): Entity title
        
    Returns:
        float: Similarity score between 0 and 1
    """
    try:
        word_vec = WIKI2VEC.get_word_vector(word)
        entity_vec = WIKI2VEC.get_entity_vector(entity_title)
        
        similarity = np.dot(word_vec, entity_vec) / (
            np.linalg.norm(word_vec) * np.linalg.norm(entity_vec)
        )
        return similarity
    except KeyError as e:
        LOGGER.exception(f"Word or entity not found: {e}")
        return None

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
