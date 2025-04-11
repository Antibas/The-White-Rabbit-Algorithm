# -*- coding: utf-8 -*-
import numpy as np

from SPARQLWrapper import SPARQLWrapper, JSON
from traceback import print_exc
from sys import exit, argv
from re import fullmatch

from utils.constants import MODEL_PATH
from utils.utils import get_entity_similarity, is_english_only
    


# def get_entity_similarity(wiki2vec, entity1, entity2):
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
#             np.linalg.norm(entity1_vec) * np.linalg.norm(entity2_vec)
#         )
#         return similarity
#     except KeyError as e:
#         print(f"Entity not found: {e}")
#         return None

def get_most_similar_entities(wiki2vec, entity_title, top_k=10):
    """
    Find the most similar entities to a given entity.
    
    Args:
        wiki2vec: Wikipedia2Vec model
        entity_title (str): Target entity title
        top_k (int): Number of similar entities to return
        
    Returns:
        list: List of (entity_title, similarity_score) tuples
    """
    try:
        return wiki2vec.most_similar(wiki2vec.get_entity(entity_title), top_k)
    except KeyError as e:
        print(f"Entity not found: {e}")
        return None

def get_word_entity_similarity(wiki2vec, word, entity_title):
    """
    Calculate similarity between a word and an entity.
    
    Args:
        wiki2vec: Wikipedia2Vec model
        word (str): Input word
        entity_title (str): Entity title
        
    Returns:
        float: Similarity score between 0 and 1
    """
    try:
        word_vec = wiki2vec.get_word_vector(word)
        entity_vec = wiki2vec.get_entity_vector(entity_title)
        
        similarity = np.dot(word_vec, entity_vec) / (
            np.linalg.norm(word_vec) * np.linalg.norm(entity_vec)
        )
        return similarity
    except KeyError as e:
        print(f"Word or entity not found: {e}")
        return None


from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")  # Format: HH:MM:SS
# Set your API key
sstart=0
# Define the query
query = "Explain quantum entanglement in simple terms."
import os
import anthropic



#print("HERE")
#
# response2s = client.chat.completions.create(
#     #model="gpt-4"
#     model="gpt-3.5-turbo",            
#
#
#     messages=[
#         #{"role": "system", "content":query},
#         {"role": "user", "content": query+" " + user_input}])
client = anthropic.Anthropic()

#print(message)


# Make the request
# response = model.generate_content("Write a story about a magic backpack.")
# print(response.text)
import json


from datetime import datetime

# Print the current date and time
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
stra="PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  PREFIX schema: <http://schema.org/> PREFIX yago: <http://yago-knowledge.org/resource/>"

def find_path_between_nodes(start_node, target_node, endpoint):
    sparql = SPARQLWrapper(endpoint)
    visited = set()
      # Track visited nodes
    sstart=0
    #startnode[0]=start_node    
    queue = [([start_node,0.0], []),([start_node,0.0], [])]  # Queue of (current_node, path_so_far)


    while queue:
        lis=[]
        it=0
        for a in queue:
            c,p=a
            if it<=10:
                print(" --------------------------AEK "+c[0]+" "+str(c[1]))
            it=it+1
            lis.append(c[0]+" "+str(c[1]))
        current_node, path = queue.pop(0)
        
        result2 = current_node[0].split("resource/")[-1]
     

        if current_node[0] in visited:
            continue
        print(" ---------------> "+current_node[0])
        visited.add(current_node[0])
        value=0
        # stringass=" from your knowledge if "+current_node[0]+" ταυτιζεται απολυτα με "+target_node+"  return single number 1 else return 0 , comma an explanation for your choice"
        # #stringas="Select  at most the 7 nodes from the list "+str(lista)+" that could best lead to  "+target_node+" than the others return them without any other words  sort them with the most relevant to target node last return a comma seperated string next to the node write a relevance score for 0 to 1 more score more relevant to target seperate tuples with #"
        # #response = model.generate_content(stringas)
        #
        # # response2s = client.chat.completions.create(
        # # model="gpt-3.5-turbo",
        # # messages=[{"role": "user", "content": stringass}])
        # #
        # #
        # # re = response2s.choices[0].message.content
        # client = anthropic.Anthropic()
        # message = client.messages.create(
        #     model="claude-3-5-sonnet-20241022",
        #     max_tokens=1000,
        #     temperature=0,
        #     system="You are a DBPEDIA GENIOUS",messages=[
        #     {
        #         "role": "user",
        #         "content": [
        #             {
        #                 "type": "text",
        #                 "text": stringass
        #             }
        #         ]
        #     }
        # ]
        # )
        # re=message.content[0].text
        # print("REEEEEEEEEEEEEEEEEEEEEEEE "+re)
        # re=re.replace("\n",",")
        # re=re.replace("\n",',') 
        # re=re.replace(".",',')
        # re=re.replace('\n','')
        print("PATH SO FAR "+str(path))
        now2 = datetime.now()
        current_time2 = now2.strftime("%H:%M:%S")
        print(current_time)
        print(current_time2)
        ilen=0
        for step2 in path:
            ilen=ilen+1

        #ral=re.split(',')
        #print("RRRRWWWW "+ral[1])
        # Check if we reached the target node
        if current_node[0] == target_node or result2 in target_node:
            print(path)
            path=path + [(current_node, "reached", target_node)]
            for step in path:
                print(f"{step[0]} --{step[1]}--> {step[2]}")
            now2 = datetime.now()
            current_time2 = now2.strftime("%H:%M:%S")
            print(current_time)
            print(current_time2)
            return ilen,path
            #return path + [(current_node, "reached", target_node)]

        # Query outgoing links from the current node
        
        stoa=f""" {stra} 
        SELECT  distinct ?next_node ?predicate WHERE {{
             <{current_node[0]}> ?predicate ?next_node .
               ?next_node rdfs:label ?label .
                               FILTER (?predicate != <http://dbpedia.org/ontology/wikiPageWikiLink>)

               FILTER (lang(?label) = "en").
              
         }}
        """
        # stoa=f""" {stra} 
        # SELECT ?next_node ?predicate WHERE {{
        #     <{current_node[0]}> ?predicate ?next_node .
        #       ?next_node rdfs:label ?label .
        #       FILTER (lang(?label) = "en").
        # }}
        # """
        sparql.setQuery(stoa)
        
        
        print("SPAROS")
        print(stoa)
        #print(f""" {stra} 
        #SELECT ?next_node ?predicate WHERE {{
        #   <{current_node[0]}> ?predicate ?next_node .
        #}}
        #""")
        
        sparql.setReturnFormat(JSON)

        try:
            print("HE1")

            results = sparql.query().convert()
            print("HE")
            if isinstance(results, bytes):  # Decode if necessary
                results = json.loads(results.decode("utf-8"))
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
                    
                    #queue.append((next_node, path + [(current_node, predicate, next_node)]))
        #print('LISTA EINAI '+str(lis))      
              
        aa=queue[0]
        an,ass=aa
        
        print("LISTA")
        print(str(lista))
        
        if lista.__len__()>1:
            epel=3
            toyl=lista.__len__()
            if toyl>6 and toyl<=12:
                epel=11
            elif toyl>12:
                epel=toyl-1
            else:
                epel=toyl-1
            print("EPEL "+str(epel))
            #print("ANE "+an[0])
            si=target_node
            si1=si.rsplit('/', 1)[-1]
            si1=si1.replace("_"," ")
            oka=""
            llasta=[]
            prf = "http://dbpedia.org/resource/"    
                          
            coa=0
            loa=[]
            for l in lista:
                last_part = l.rsplit('/', 1)[-1]
                last_part2=last_part.replace("_"," ")
                word_entity_sim = get_entity_similarity(si1, last_part2)
                print(f"\nSimilarity between {si1} and {last_part2}: {word_entity_sim}")
                print(last_part)  # Output: Heraklion
                if word_entity_sim is not None:
                    oka=oka+prf+last_part+","+str(word_entity_sim)+"#"
                    lss=[prf+last_part,float(word_entity_sim)]
                    print("KA")
                    print(lss)
                    loa.append(lss)
                    
            print(loa)
         
            oka=''
            apa=0
            # Sort in descending order based on the second element (similarity score)
            sorted_data = sorted(loa, key=lambda x: x[1], reverse=True)
            
            # Print sorted list
            for item in sorted_data:
                print(item)
                a1=item[0]
                a2=item[1]
                oka=oka+a1+","+str(a2)+"#"
                if apa==epel:
                    break
                apa=apa+1

            #stringas="Select  at most the 4 nodes from the list "+str(lista)+" that could best as meaning lead to  "+target_node+" than the others. Return them  as string of entities. An entity is node comma score. Score is from 0.0 for irrelevant to 1.0 high relevant. If target node is exacly found in list give it score 5.0. Final string is entity#entity#entity etc mean seperate entities with # Return plain string"
           
            oka=oka.rstrip()
            # stringas=" do not insert δικους σου nodes αλλα επελεξε ακριβως "+str(epel)+" αν ειναι διαθεσιμoi απο την "+str(lista)+" αυτους που πλησιαζουν πιο πολυ  α΄΄΄΄λλα και αλλους που θα μπορουσαν πιο πιθανα να οδηγησουν στον κομβο  "+target_node+" επελεξε συνολικα +"+str(epel)+"και δωσε τους ενα σκορ εγγυτητας. εαν δεν πλησιαζει πολυ δωσε σκορ κατω απο 0.4. Αν πλησιζει πολυ δωσε πανω απο 0.7. Επελεξε τους κομβους με τα μεγαλυτερα σκορ. Επισης μην επιλεξεις nodes που αναφερονται σε γενικες κατηγοριες αλλα μονο σε υπαρκτα entities. Return them  as string of entities. An entity is node comma score. Score is from 0.0 for irrelevant to target to 1 .if the node includes the word of the target, return as a score 1.0 .Do not comment scores.If target node is exacly found in list give it score 500.0. Final string is entity#entity#entity etc mean seperate entities with without headers # Return plain string.Αν δεν ειναι διαθεσιμοι 6 κομβοι δεν πειραζει και ΜΗΝ ΔΗΜΙΟΥΡΓΗΣΕΙΣ ΚΟΜΒΟΥΣ ΑΠΟ ΤΗΝ ΔΙΚΗ ΣΟΥ ΓΝΩΣΗ που δεν υπαρχουν στην λιστα. ΑΚΟΜΑ ΚΑΙ ΕΝΑΣ ΝΑ ΕΙΝΑΙ Ο ΚΟΜΒΟΣ ΕΠΕΣΤΡΕΨΕ ΤΟΝ"
            #
            # #stringas="Select  at most the 7 nodes from the list "+str(lista)+" that could best lead to  "+target_node+" than the others return them without any other words  sort them with the most relevant to target node last return a comma seperated string next to the node write a relevance score for 0 to 1 more score more relevant to target seperate tuples with #"
            # #response = model.generate_content(stringas)
            #
            # # response2 = client.chat.completions.create(
            # # model="gpt-3.5-turbo",
            # # messages=[{"role": "user", "content": stringas}])
            # message = client.messages.create(
            # model="claude-3-5-sonnet-20241022",
            # max_tokens=1000,
            # temperature=0,
            # system="You are a DBPEDIA SPECIALIST",
            # messages=[
            #         {
            #             "role": "user",
            #             "content": [
            #                 {
            #                     "type": "text",
            #                     "text": stringas
            #                 }
            #             ]
            #         }
            #     ]
            # )
            # response=message.content[0].text
    
            #response = response2.choices[0].message.content
            #print("l2 "+str(lista2))
            #print()
            #int("STRINGAS "+stringas)
            #print()
            # /ra=response.text
            print("RA1")
            response=oka
            ra=response
            print(ra)
            #ra=ra.strip()
            ra=ra.replace('\n','')
    
            
            tups=ra.split('#')
            
            #for t in tups:
             #   sta=t.split(',')
                
            
            #print("RAA "+ra)
            # fruit_list = ra.split(',')
            print("TUPS "+str(tups))
            
            if lista:
                for ft in tups:
                    #print("FT "+ft)
                    try:
                        sco=ft.split(',')
                        sco[0]=sco[0].replace(' ','')
                        sco[0]=sco[0].replace('\'','')
                        sco[1]=sco[1].replace('\'','')
                        print("SCO +"+str(sco))
        
                        #print("LENA "+str(len(queue)))
                        # if start==0:
                        #     #print("SALOS")
                        #     queue = [([start_node,0.0], [])]   
                                         
                        #print("LENA2 "+str(len(queue)))
                        #print("TUPS "+str(len(tups)))
                        position=-1
                        if sstart==0:
                            
                            position=0
                            sstart=1
                            queue.insert(position,(sco, path + [(current_node, dicta[sco[0]], sco)]))
        
                            #print("STARTER")    
                        else:          
                            i=0  
                            
                            while True:
                                if i>=queue.__len__():
                                    print("BROKE")
                                    break
                                #print("OKL")
                                #print("AI "+str(i))
                                a,b=queue[i]
                                #print("QYA "+a[0])
                                # print("A! "+str(a[1])+" "+str(float(sco[1])))
                                try:
                                    if  float(a[1])<float(sco[1]):
                                            #print("KO")
                                            position=i
                                            #print("AD "+sco[0])
                                            start=1
                                            break
                                    
                                    
                                except Exception as e:
                                    print(f"aAn error occurred: {e}")
                                    
                                    print_exc() 
                                    break
                                    
                                i=i+1 
                            if i>=len(queue):
                                print("XAATZIBRETAS")
                                position=len(queue)-1
                            else:
                                print("")
                                #print("MANTOS "+str(len(queue))+"POS "+str(position))  
                                
                            if position==-1:
                                print("HELLO DOLLY")
                            else:
                                #print('thmuios')     
                                #if (float(sco[1])>0):
                                if (True):
        
                                    #print("TJU2")
                                    queue.insert(position,(sco, path + [(current_node, dicta[sco[0]], sco)]))
        
                        #queue.insert(0,(f, path + [(current_node, dicta[f], f)]))
                        
                        # if sco[0]==target_node:
                        #     print("DOUNF")
                        #     for step in path:
                        #         print(f"{step[0]} --{step[1]}--> {step[2]}")
                        #     return
                        # print("AD "+sco[0])
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        print_exc() 
                        
    # If queue exhausts without finding target
    return None
args = argv[1:]  # Exclude script name
print("Received Arguments:", args)
# Example usage
endpoint = "https://yago-knowledge.org/sparql/query"
endpoint = "http://localhost:8890/sparql"
endpoint = "https://dbpedia.org/sparql/query"

#start_node = "http://yago-knowledge.org/resource/The_Beatles"
#target_node = "http://yago-knowledge.org/resource/Heraklion"
start_node = "http://yago-knowledge.org/resource/Chania"
start_node = "http://dbpedia.org/resource/Chania"
start_node = "http://dbpedia.org/resource/Lamia"
start_node = "http://dbpedia.org/resource/Boris_Yeltsin"
start_node = "http://dbpedia.org/resource/Heraklion"
start_node = "http://dbpedia.org/resource/Boris_Yeltsin"
start_node = "http://dbpedia.org/resource/Morocco"


start_node = "http://dbpedia.org/resource/The_Beatles"
start_node = "http://dbpedia.org/resource/Vikings"
start_node = "http://dbpedia.org/resource/Barack_Obama" #to aristotle failure
start_node = "http://dbpedia.org/resource/The_Beatles"

start_node="http://dbpedia.org/resource/Albert_Einstein"
start_node="http://dbpedia.org/resource/Barack_Obama"
start_node="http://dbpedia.org/resource/Paris"
start_node="http://dbpedia.org/resource/Apple_Inc."
start_node="http://dbpedia.org/resource/Mona_Lisa"
start_node="http://dbpedia.org/resource/Google"
start_node="http://dbpedia.org/resource/United_States"
start_node="http://dbpedia.org/resource/World_War_II"
start_node="http://dbpedia.org/resource/Shakespeare"
start_node="http://dbpedia.org/resource/Microsoft"
start_node="http://dbpedia.org/resource/New_York_City"
start_node="http://dbpedia.org/resource/Leonardo_da_Vinci"
start_node="http://dbpedia.org/resource/Elon_Musk"
start_node="http://dbpedia.org/resource/China"
start_node="http://dbpedia.org/resource/India"
start_node="http://dbpedia.org/resource/Java_(programming_language)"
start_node="http://dbpedia.org/resource/Internet"
start_node="http://dbpedia.org/resource/Artificial_intelligence"
start_node="http://dbpedia.org/resource/Earth"
start_node="http://dbpedia.org/resource/Star_Wars"
start_node="http://dbpedia.org/resource/Apple_Inc."
start_node="http://dbpedia.org/resource/Microsoft"
start_node="http://dbpedia.org/resource/Elon_Musk"
start_node="http://dbpedia.org/resource/Hanoi"
start_node="http://dbpedia.org/resource/Boris_Yeltsin"

#start_node = "http://dbpedia.org/resource/The_Beatles"

#start_node = "http://dbpedia.org/resource/California"
#start_node = "http://dbpedia.org/resource/Adolf_Hitler"
start_node = "http://dbpedia.org/resource/Lamia"

target_node = "http://yago-knowledge.org/resource/Heraklion"
target_node = "http://dbpedia.org/resource/China"
target_node = "http://dbpedia.org/resource/Nigeria"
target_node = "http://dbpedia.org/resource/Australia"
target_node = "http://dbpedia.org/resource/Bavaria"
target_node = "http://dbpedia.org/The_Flintstones"
target_node = "http://dbpedia.org/resource/Moscow"
target_node = "http://dbpedia.org/resource/Montevideo"
target_node = "http://dbpedia.org/resource/Hawaii"
target_node = "http://dbpedia.org/resource/Hanoi"
target_node = "http://dbpedia.org/resource/Heraklion"
target_node = "http://dbpedia.org/resource/Edessa"
target_node = "http://dbpedia.org/resource/Pella"
target_node = "http://dbpedia.org/resource/Aristotle"
target_node = "http://dbpedia.org/resource/NATO"
target_node = "http://dbpedia.org/resource/Herne_Bay_High_School"

target_node="http://dbpedia.org/resource/Isaac_Newton"
target_node="http://dbpedia.org/resource/Stephen_Hawking"
target_node="http://dbpedia.org/resource/Nikola_Tesla"
target_node="http://dbpedia.org/resource/Vincent_van_Gogh"
target_node="http://dbpedia.org/resource/Ludwig_van_Beethoven"
target_node="http://dbpedia.org/resource/Marie_Curie"
target_node="http://dbpedia.org/resource/Charles_Darwin"
target_node="http://dbpedia.org/resource/Adolf_Hitler"
target_node="http://dbpedia.org/resource/Julius_Caesar"
target_node="http://dbpedia.org/resource/Alexander_the_Great"
target_node="http://dbpedia.org/resource/Napoleon"
target_node="http://dbpedia.org/resource/Winston_Churchill"
target_node="http://dbpedia.org/resource/Martin_Luther_King_Jr."
target_node="http://dbpedia.org/resource/Mahatma_Gandhi"
target_node="http://dbpedia.org/resource/Nelson_Mandela"
target_node="http://dbpedia.org/resource/Plato"
target_node="http://dbpedia.org/resource/Aristotle"
target_node="http://dbpedia.org/resource/William_Shakespeare"
target_node="http://dbpedia.org/resource/Christopher_Columbus"
target_node="http://dbpedia.org/resource/Java_(programming_language)"
target_node="http://dbpedia.org/resource/Christopher_Columbus"

target_node="http://dbpedia.org/resource/Nelson_Mandela"
target_node="http://dbpedia.org/resource/Plato"
target_node="http://dbpedia.org/resource/Nigeria"
target_node="http://dbpedia.org/resource/Hawaii"

#target_node = "http://yago-knowledge.org/resource/John_Lennon"
#target_node = "http://yago-knowledge.org/resource/Spain"
target_node = "http://dbpedia.org/resource/Moscow"
args=['Athens','Moscow']
start_node="http://dbpedia.org/resource/"+args[0]
target_node="http://dbpedia.org/resource/"+args[1]

now = datetime.now()
current_time = now.strftime("%H:%M:%S")  # Format: HH:MM:SS
word_entity_sim = get_entity_similarity(args[0], args[1])
print(f"\nSimilarity between {start_node} and {target_node}: {word_entity_sim}")
la,path = find_path_between_nodes(start_node, target_node, endpoint)
print("MANOS")
if path:
    for step in path:
        print(f"{step[0]} --{step[1]}--> {step[2]}")
    now2 = datetime.now()
    current_time2 = now2.strftime("%H:%M:%S")
    print(current_time)
    print(current_time2)
    print("KENZA")
    totalp=0.0
    totale=0.0
    now2 = datetime.now()
    
    # #file.write(entity1+" ----->  "+first_p_value+" ------> "+first_x_value+'\n')
    # xa2= first_x_value.rsplit('/', 1)[-1]
    #
    # word_entity_similarity = get_entity_similarity(wiki2vec, entity1, xa2)
    # if word_entity_similarity is None:
    #     totalp+=0
    # else:
    #     totalp+= word_entity_similarity
    # word_entity_similarity2 = get_entity_similarity(wiki2vec, entity1, entity2)
    # if word_entity_similarity2 is None:
    #     totale+=0
    # else:
    #     totale+= word_entity_similarity2
    # print(str(totale))
    #
    # print(f"\nSimilarity between {entity1} and {xa2}: {word_entity_similarity}")
    import time
    
    lana=len(path)
    ida=1
    for triple in path:
        print("MENU")
        print(f"({triple[0]}, {triple[1]}, {triple[2]})")
        #time.sleep(1)
        xa0= triple[0][0].rsplit('/', 1)[-1]
        xa2= triple[2][0].rsplit('/', 1)[-1]
        xa0=xa0.replace("_"," ").replace("-",' ')
        xa2=xa2.replace("_"," ").replace("-",' ')
        xa3=args[1]
        xa3=xa3.replace("_"," ").replace("-",' ')
        #xa2=xa2.replace("_"," ").replace("-",' ') 
    
        word_entity_similarity = get_entity_similarity(xa0, xa2)
        if word_entity_similarity is None:
            totalp+=0
        else:
            totalp+= word_entity_similarity
    
        word_entity_similarity2 = get_entity_similarity(xa0, xa3)
        if word_entity_similarity2 is None:
            totale+=0
        else:
            totale+= word_entity_similarity2
        print(f"\nSimilarity between {xa0} and {xa2}: {word_entity_similarity} {word_entity_similarity2} ")
        ida=ida+1
        if ida==lana:
            break
    
        #file.write(f"({triple[0]}, {triple[1]}, {triple[2]})\n")
    #time.sleep(1)
    
    #file.write(last_x_value+" -----> "+last_p_value+' -----> '+entity2+'\n')
    # xa0= last_x_value.rsplit('/', 1)[-1]
    # #xa2= triple[0].rsplit('/', 1)[-1]
    #
    # word_entity_similarity = get_entity_similarity(wiki2vec, xa0, entity2)
    #
    # if word_entity_similarity is None:
    #     totalp+=0
    # else:
    #     totalp+= word_entity_similarity
    # #time.sleep(1)
    #
    # word_entity_similarity2 = get_entity_similarity(wiki2vec,xa0, entity2)
    # if word_entity_similarity2 is None:
    #     totale+=0
    # else:
    #     totale+= word_entity_similarity2
    #print(f"\nSimilarity between {xa0} and {entity2}: {word_entity_similarity}")
    print("TOTAL P "+str(totalp/(float(la)))+ " TOTAL E "+str(totale/(float(la))))    
    
    
    
    
    exit()      # Format: HH:
else:
    print("No path found between the nodes.")
from datetime import datetime

# Print the current date and time
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
