from json import loads
from re import fullmatch
from traceback import print_exc
from SPARQLWrapper import JSON, SPARQLWrapper
from anthropic import Anthropic
import numpy as np
from utils.constants import SPARQL_PREFIX, SPARQL_RESOURCE_URL, WIKI2VEC

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
        print(f"Entity not found: {e}")
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
        print(f"Entity not found: {e}")
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
        print(f"Word or entity not found: {e}")
        return None

def is_english_only(s):
    return bool(fullmatch(r"[A-Za-z0-9 /\-()_:/.]+", s))

def find_path_between_nodes(start_node: str, target_node: str, endpoint: str, llm: bool=False):
    sparql = SPARQLWrapper(endpoint)
    visited = set()
    # Track visited nodes
    sstart=0
    queue = [([start_node,0.0], []),([start_node,0.0], [])]  # Queue of (current_node, path_so_far)


    while queue:
        lis=[]
        it=0
        for a in queue:
            c,_=a
            if it<=10:
                print(" -------------------------- "+c[0]+" "+str(c[1]))
            it=it+1
            lis.append(c[0]+" "+str(c[1]))
        current_node, path = queue.pop(0)
        
        result2 = current_node[0].split("resource/")[-1]
     

        if current_node[0] in visited:
            continue
        print(" ---------------> "+current_node[0])
        visited.add(current_node[0])
        print("PATH SO FAR "+str(path))
        ilen=0
        for step2 in path:
            ilen=ilen+1

        # Check if we reached the target node
        if current_node[0] == target_node or (not llm and result2 in target_node):
            print(path)
            path=path + [(current_node, "reached", target_node)]
            for step in path:
                print(f"{step[0]} --{step[1]}--> {step[2]}")
            return ilen,path

        # Query outgoing links from the current node
        
        stoa=f""" {SPARQL_PREFIX} 
        SELECT  {'distinct' if not llm else ""} ?next_node ?predicate WHERE {{
             <{current_node[0]}> ?predicate ?next_node .
               ?next_node rdfs:label ?label .
                               FILTER (?predicate != <http://dbpedia.org/ontology/wikiPageWikiLink>)

               FILTER (lang(?label) = "en").
              
         }}
        """
        sparql.setQuery(stoa)
        print(stoa)
        
        sparql.setReturnFormat(JSON)

        try:
            results = sparql.query().convert()
            if isinstance(results, bytes):  # Decode if necessary
                results = loads(results.decode("utf-8"))
        except Exception as e:
            print(f"Error querying SPARQL endpoint: {e}")
            print_exc() 
            continue
        lista=[]
        lista2=[]
        dicta={}
        # Process each outgoing link and add it to the queue if not visited
        if results.get("results") and results["results"].get("bindings"):
            for result in results["results"]["bindings"]:
                next_node = result["next_node"]["value"]
                predicate = result["predicate"]["value"]
                dicta[next_node]=predicate
                
                # Append to the path and add to the queue
                if is_english_only(next_node) and next_node not in visited and "resource" in next_node and 'Category' not in next_node and 'Template' not in next_node:
                    lista.append(next_node)
                    lista2.append(predicate+" "+next_node)
                    
        aa=queue[0]
        print(str(lista))
        
        if lista.__len__()>1:
            epel=3
            toyl=lista.__len__()
            if toyl>6 and toyl<=12:
                epel=11
            elif toyl>12:
                epel=toyl-1 if not llm else 11
            else:
                epel=toyl-1
            print("EPEL "+str(epel))

            if llm:
                stringas=" do not insert δικους σου nodes αλλα επελεξε ακριβως "+str(epel)+" αν ειναι διαθεσιμoi απο την "+str(lista)+" αυτους που πλησιαζουν πιο πολυ  α΄΄΄΄λλα και αλλους που θα μπορουσαν πιο πιθανα να οδηγησουν στον κομβο  "+target_node+" επελεξε συνολικα +"+str(epel)+"και δωσε τους ενα σκορ εγγυτητας με τρια δεκαδικα. εαν δεν πλησιαζει πολυ δωσε σκορ κατω απο 0.4. Αν πλησιζει πολυ δωσε πανω απο 0.7. Επελεξε τους κομβους με τα μεγαλυτερα σκορ. Επισης μην επιλεξεις nodes που αναφερονται σε γενικες κατηγοριες αλλα μονο σε υπαρκτα entities. Return them  as string of entities. An entity is node comma score. Score is from 0.0 for irrelevant to target to 1 .if the node includes the word of the target, return as a score 1.0 .Do not comment scores.If target node is exacly found in list give it score 500.0. Final string is entity#entity#entity etc mean seperate entities with without headers # Return plain string.Αν δεν ειναι διαθεσιμοι 6 κομβοι δεν πειραζει και ΜΗΝ ΔΗΜΙΟΥΡΓΗΣΕΙΣ ΚΟΜΒΟΥΣ ΑΠΟ ΤΗΝ ΔΙΚΗ ΣΟΥ ΓΝΩΣΗ που δεν υπαρχουν στην λιστα. ΑΚΟΜΑ ΚΑΙ ΕΝΑΣ ΝΑ ΕΙΝΑΙ Ο ΚΟΜΒΟΣ ΕΠΕΣΤΡΕΨΕ ΤΟΝ"
                message = Anthropic().messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0,
                system="You are a DBPEDIA SPECIALIST",
                messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": stringas
                                }
                            ]
                        }
                    ]
                )
                response=message.content[0].text
            else:
                si=target_node
                si1=si.rsplit('/', 1)[-1]
                si1=si1.replace("_"," ")
                oka=""
                prf = f"{SPARQL_RESOURCE_URL}"    
                          
                loa=[]
                for l in lista:
                    last_part = l.rsplit('/', 1)[-1]
                    last_part2=last_part.replace("_"," ")
                    word_entity_sim = get_entity_similarity(si1, last_part2)

                    print(f"\nSimilarity between {si1} and {last_part2}: {word_entity_sim}")
                    if word_entity_sim is not None:
                        oka=oka+prf+last_part+","+str(word_entity_sim)+"#"
                        lss=[prf+last_part,float(word_entity_sim)]
                        loa.append(lss)
                        
                print(loa)
            
                oka=''
                apa=0
                # Sort in descending order based on the second element (similarity score)
                sorted_data = sorted(loa, key=lambda x: x[1], reverse=True)
                
                # Print sorted list
                for item in sorted_data:
                    a1=item[0]
                    a2=item[1]
                    oka=oka+a1+","+str(a2)+"#"
                    if apa==epel:
                        break
                    apa=apa+1

                oka=oka.rstrip()
                response=oka
            ra=response
            ra=ra.replace('\n','')
    
            
            tups=ra.split('#')
            
            print("TUPS "+str(tups))
            
            if lista:
                for ft in tups:
                    try:
                        sco=ft.split(',')
                        sco[0]=sco[0].replace(' ','')
                        sco[0]=sco[0].replace('\'','')
                        sco[1]=sco[1].replace('\'','')
                        print("SCO +"+str(sco))
                        position=-1
                        if sstart==0:
                            
                            position=0
                            sstart=1
                            queue.insert(position,(sco, path + [(current_node, dicta[sco[0]], sco)]))
                        else:          
                            i=0  
                            
                            while True:
                                if i>=queue.__len__():
                                    break
                                a,b=queue[i]
                                try:
                                    if  float(a[1])<float(sco[1]):
                                            position=i
                                            break
                                    
                                    
                                except Exception as e:
                                    print(f"An error occurred: {e}")
                                    print_exc() 
                                    break
                                    
                                i=i+1 
                            if i>=len(queue):
                                position=len(queue)-1
                                
                            if position != -1:
                                queue.insert(position,(sco, path + [(current_node, dicta[sco[0]], sco)]))
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        print_exc() 
                        
    # If queue exhausts without finding target
    return None