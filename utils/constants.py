from os import getenv
from SPARQLWrapper import SPARQLWrapper
from wikipedia2vec import Wikipedia2Vec

from utils.enums import ResourceType

MODEL_PATH = getenv("MODEL_PATH", "enwiki_20180420_100d.pkl")
WIKI2VEC = Wikipedia2Vec.load(MODEL_PATH)
CLAUDE_MODEL = getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
DBPEDIA_URL = "https://dbpedia.org/sparql"
DBPEDIA_RESOURCE_URL = "http://dbpedia.org/resource"
WIKIDATA_URL = "https://query.wikidata.org/sparql"
WIKIDATA_RESOURCE_URL = "http://www.wikidata.org/entity/"
YAGOS_URL = "https://yago-knowledge.org/sparql/query."
YAGOS_RESOURCE_URL="http://yago-knowledge.org/resource"
AGENT=getenv("AGENT", "MyWikidataBotPAATH/2.0 (giannis_vassiliou@yahoo.gr")
SPARQL_PREFIX = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  PREFIX schema: <http://schema.org/> PREFIX yago: <http://yago-knowledge.org/resource/>"
BASE_URLS = {
    ResourceType.DBPEDIA: DBPEDIA_URL,
    ResourceType.WIKIDATA: WIKIDATA_URL,
    ResourceType.YAGOS: YAGOS_URL
}
RESOURCE_URLS = {
    ResourceType.DBPEDIA: DBPEDIA_RESOURCE_URL,
    ResourceType.WIKIDATA: WIKIDATA_RESOURCE_URL,
    ResourceType.YAGOS: YAGOS_RESOURCE_URL
}
ACCEPTANCE_THRESHOLD=.9