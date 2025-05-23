import algorithms.dbpedia as dbpedia
import algorithms.wikidata as wikidata
import algorithms.yago as yago
from utils.enums import EmbeddingType

def main():
    with open("config/nodes.conf") as f:
        nodes = list(node.strip() for node in f.readlines())
        selection = input(f"Select two of the following nodes: {nodes}")
    ds = input("Select one of the following datasets:\n\t1. DBPEDIA\n\t2. WIKIDATA\n\t3. YAGO\n")
    dataset = None
    if(ds.upper() in ["1", "DBPEDIA"]):
        dataset = dbpedia
    elif(ds.upper() in ["2", "WIKIDATA"]):
        dataset = wikidata
    elif(ds.upper() in ["3", "YAGO"]):
        dataset = yago
    else:
        print(f"Invalid dataset: {ds}")
        return
    
    alg = input("Select one of the following algorithms to test:\n\t1. The White Rabbit\n\t2. Query Expansion\n\t" \
                "3. Embeddings\n\t4. LLM\n")
    algorithm = None
    embedding = None
    if(alg.upper() in ["1", "The White Rabbit"]):
        algorithm = dataset.white_rabbit
    elif(alg.upper() in ["2", "Query Expansion"]):
        algorithm = dataset.query_expansion
    elif(alg.upper() in ["3", "Embeddings"]):
        algorithm = dataset.embedding

        emb = input("Select one of the following embeddings:\n\t1. WORD2VEC\n\t2. FASTTEXT\n\t" \
                "3. SBERT\n")
        embedding = EmbeddingType(emb)
        # if(emb.upper() in ["1", "WORD2VEC"]):
        #     embedding = EmbeddingType(emb)
        # elif(emb.upper() in ["2", "FASTTEXT"]):
        #     embedding = EmbeddingType
        # elif(emb.upper() in ["3", "SBERT"]):
        #     embedding = EmbeddingType
        # else:
        #     print(f"Invalid embedding: {ds}")
        #     return
    elif(alg.upper() in ["4", "LLM"]):
        algorithm = dataset.llm
    else:
        print(f"Invalid algorithm: {alg}")
        return
    
    acc = input("(Optional) Select an accuracy threshold between 0 and 0.99: ")
    try:
        accuracy_threshold = float(acc)
    except ValueError:
        accuracy_threshold = 1
    
    tm = input("Now select a timeout in seconds: ")
    try:
        timeout_seconds = int(tm)
    except ValueError:
        print(f"Invalid input: {tm}")
        return
    


if __name__ == "__main__":
    main()