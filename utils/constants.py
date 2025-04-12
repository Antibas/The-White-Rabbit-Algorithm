from os import getenv
from SPARQLWrapper import SPARQLWrapper
from wikipedia2vec import Wikipedia2Vec

MODEL_PATH = getenv("MODEL_PATH", "enwiki_20180420_100d.pkl")
WIKI2VEC = Wikipedia2Vec.load(MODEL_PATH)
SPARQL_URL = "https://dbpedia.org/sparql"
SPARQL_RESOURCE_URL = "http://dbpedia.org/resource/"
SPARQL_PREFIX = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  PREFIX schema: <http://schema.org/> PREFIX yago: <http://yago-knowledge.org/resource/>"