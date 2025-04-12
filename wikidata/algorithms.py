from SPARQLWrapper import JSON, SPARQLWrapper

from utils.constants import AGENT

def get_wikidata_uri(label):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql",agent=AGENT)
    
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
    else:
        return None