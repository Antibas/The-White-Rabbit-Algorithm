from enum import Enum, IntEnum, auto


class ResourceType(Enum):
    DBPEDIA="dbpedia"
    WIKIDATA="wikidata"
    YAGOS="yagos"

class EmbeddingType(IntEnum):
    WIKI2VEC=auto()
    WORD2VEC=auto()
    SBERT=auto()
    FASTTEXT=auto()