from types import ModuleType
import algorithms.dbpedia as dbpedia
import algorithms.wikidata as wikidata
import algorithms.yago as yago
from utils.enums import EmbeddingType
from utils.utils import timeout
from sys import argv

DATASETS = {
    "DBPEDIA": dbpedia,
    "1": dbpedia,
    "WIKIDATA": wikidata,
    "2": wikidata,
    "YAGO": yago,
    "3": yago
}

def usage():
    print("")

def main(arguments: list[str] = []):
    if not arguments:
        print("Welcome to the White Rabbit demo.")
        print("Here you can test our algorithm along with various others to make the comparison.")
        source, target = "", ""
        with open("config/nodes.conf") as f:
            nodes = list(node.strip() for node in f.readlines())
            nodes.sort()
            entities = "\n\t".join(f"{i+1}. {nodes[i]}" for i in range(len(nodes)))
            try:
                sel = input(f"Select two of the following nodes: {entities}\n\nSelect them with their number separated by whitespace: ")
                selections = tuple(sel.split(" "))
                s_i, t_i = int(selections[0]), int(selections[1])
            except IndexError:
                print(f"Invalid input {sel}. You need to type two numbers")
                return
            except ValueError:
                print(f"One of the inputs is invalid: {selections}")
                return
            source, target = nodes[s_i-1], nodes[t_i-1]
        ds = input("Select one of the following datasets:\n\t1. DBPEDIA\n\t2. WIKIDATA\n\t3. YAGO\n\nSelect them with either their number or name: ")
        dataset = None
        try:    
            dataset = DATASETS[ds.upper()]
        # if(ds.upper() in ["1", "DBPEDIA"]):
        #     dataset = dbpedia
        # elif(ds.upper() in ["2", "WIKIDATA"]):
        #     dataset = wikidata
        # elif(ds.upper() in ["3", "YAGO"]):
        #     dataset = yago
        # else:
        except KeyError as e:
            print(f"Invalid input: {e}")
            return
        
        alg = input("Select one of the following algorithms to test:\n\t1. The White Rabbit\n\t2. Query Expansion\n\t" \
                    "3. Embeddings\n\t4. LLM\n\nSelect them with either their number or name: ")
        algorithm = None
        embedding = None
        if(alg.upper() in ["1", "The White Rabbit"]):
            algorithm = dataset.white_rabbit
        elif(alg.upper() in ["2", "Query Expansion"]):
            algorithm = dataset.query_expansion
        elif(alg.upper() in ["3", "Embeddings"]):
            algorithm = dataset.embedding

            emb = input("Select one of the following embeddings:\n\t1. WORD2VEC\n\t2. FASTTEXT\n\t" \
                    "3. SBERT\n\nSelect them with either their number or name:")
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
            if(accuracy_threshold < 0 or accuracy_threshold > 1):
                raise ValueError()
        except ValueError:
            print(f"Invalid input: {acc}. Changing to default threshold (=1)")
            accuracy_threshold = 1
        
        tm = input("Now select a timeout in seconds: ")
        try:
            timeout_seconds = int(tm)
        except ValueError:
            print(f"Invalid input: {tm}. Changing to default timeout (=360 s)")
            timeout_seconds = 360
    else:
        try:
            source = arguments[1]
            target = arguments[2]
            try:    
                dataset = DATASETS[arguments[3].upper()]
            except KeyError as e:
                print(f"Invalid parameter for dataset: {e}")
                return

            alg = arguments[4]
            algorithm = None
            embedding = None
            if(alg.upper() in ["1", "The White Rabbit"]):
                algorithm = dataset.white_rabbit
            elif(alg.upper() in ["2", "Query Expansion"]):
                algorithm = dataset.query_expansion
            elif(alg.upper() in ["3", "Embeddings"]):
                algorithm = dataset.embedding
                embedding = EmbeddingType(arguments[5])
            elif(alg.upper() in ["4", "LLM"]):
                algorithm = dataset.llm
            else:
                print(f"Invalid algorithm: {alg}")
                return
            
        except IndexError:
            usage()
            return
    inputs = (source, target, accuracy_threshold)
    print("Inputs: ")
    print(f"\tSource: {source}")
    print(f"\tTarget: {target}")
    print(f"\tDataset: {dataset.__name__}")
    print(f"\tAlgorithm: {algorithm.__name__}")
    if embedding:
        inputs = (source, target, embedding, accuracy_threshold)
        print(f"\tEmbedding: {embedding}")
    print(f"\tAccuracy Threshold: {accuracy_threshold}")
    print(f"\tTimeout in {timeout_seconds} seconds.")
    print("Starting the algorithm...")
    time, length, pc, ta, path = timeout(algorithm, inputs, embedding_type=embedding or EmbeddingType.WIKI2VEC, timeout=timeout_seconds)
    if not length:
        print("Algorithm timed out and/or no valid path was found. Try increasing the timeout.")
    else:
        print(f"Algorithm finished in {time} seconds.")
        print(f"Path length: {length}")
        print(f"Path Coherence: {pc}")
        print(f"Target Affiliation: {ta}")
        print(f"Path:")
        for p in path:
            print(f"{p[0]} ------> {p[1]} ------> {p[2]}")



if __name__ == "__main__":
    print(len(argv))
    if len(argv) < 2:
        main()
    else:
        main(argv)