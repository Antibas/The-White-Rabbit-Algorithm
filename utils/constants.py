from os import getenv
from sentence_transformers import SentenceTransformer
from wikipedia2vec import Wikipedia2Vec
from gensim.downloader import load

from utils.enums import ResourceType
from utils.logger import LOGGER

WIKI2VEC_MODEL = getenv("WIKI2VEC_MODEL", "model.pkl")
WORD2VEC_MODEL = getenv('WORD2VEC_MODEL', 'word2vec-google-news-300')
FASTTEXT_MODEL = getenv('FASTTEXT_MODEL', 'fasttext-wiki-news-subwords-300')
SBERT_MODEL = getenv('SBERT_MODEL', 'all-mpnet-base-v2')
# class Models: 
#     instance = None
#     def __new__(cls):
#         if not cls.instance:
#             cls.instance = super(Models, cls).__new__(cls)
#             cls.instance.WIKI2VEC = Wikipedia2Vec.load(WIKI2VEC_MODEL)
#             LOGGER.info("WIKI2VEC loaded...")
#             cls.instance.WORD2VEC = load(getenv('WORD2VEC_MODEL', 'word2vec-google-news-300'))
#             LOGGER.info("WORD2VEC loaded...")
#             cls.instance.FASTTEXT = load(getenv('FASTTEXT_MODEL', 'fasttext-wiki-news-subwords-300'))
#             LOGGER.info("FASTTEXT loaded...")
#             cls.instance.SBERT = SentenceTransformer(getenv('SBERT_MODEL', 'all-mpnet-base-v2'))
#             LOGGER.info("SBERT loaded...")
#         return cls.instance

# MODELS = Models()
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
# CONSTANTS = Constants()