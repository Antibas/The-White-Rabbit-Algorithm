from time import time
from SPARQLWrapper import SPARQLWrapper, JSON
from traceback import print_exc
from sys import exit, argv
from datetime import datetime
from json import loads
from anthropic import Anthropic

from utils.constants import SPARQL_RESOURCE_URL, SPARQL_URL
from utils.utils import find_path_between_nodes, get_entity_similarity, is_english_only

# def find_path_between_nodes(start_node, target_node, endpoint):
#     sparql = SPARQLWrapper(endpoint)
#     visited = set()
#     # Track visited nodes
#     sstart=0
#     queue = [([start_node,0.0], []),([start_node,0.0], [])]  # Queue of (current_node, path_so_far)


#     while queue:
#         lis=[]
#         it=0
#         for a in queue:
#             c,p=a
#             if it<=10:
#                 print(" --------------------------AEK "+c[0]+" "+str(c[1]))
#             it=it+1
#             lis.append(c[0]+" "+str(c[1]))
#         current_node, path = queue.pop(0)
        
#         result2 = current_node[0].split("resource/")[-1]

#         if current_node[0] in visited:
#             continue
#         print(" ---------------> "+current_node[0])
#         visited.add(current_node[0])
#         value=0
#         # stringass=" from your knowledge if "+current_node[0]+" ταυτιζεται απολυτα με "+target_node+"  return single number 1 else return 0 , comma an explanation for your choice"
#         # #stringas="Select  at most the 7 nodes from the list "+str(lista)+" that could best lead to  "+target_node+" than the others return them without any other words  sort them with the most relevant to target node last return a comma seperated string next to the node write a relevance score for 0 to 1 more score more relevant to target seperate tuples with #"
#         # #response = model.generate_content(stringas)
#         #
#         # # response2s = client.chat.completions.create(
#         # # model="gpt-3.5-turbo",
#         # # messages=[{"role": "user", "content": stringass}])
#         # #
#         # #
#         # # re = response2s.choices[0].message.content
#         # client = Anthropic()
#         # message = client.messages.create(
#         #     model="claude-3-5-sonnet-20241022",
#         #     max_tokens=1000,
#         #     temperature=0,
#         #     system="You are a DBPEDIA GENIOUS",messages=[
#         #     {
#         #         "role": "user",
#         #         "content": [
#         #             {
#         #                 "type": "text",
#         #                 "text": stringass
#         #             }
#         #         ]
#         #     }
#         # ]
#         # )
#         # re=message.content[0].text
#         # print("REEEEEEEEEEEEEEEEEEEEEEEE "+re)
#         # re=re.replace("\n",",")
#         # re=re.replace("\n",',') 
#         # re=re.replace(".",',')
#         # re=re.replace('\n','')
#         print("PATH SO FAR "+str(path))
#         now2 = datetime.now()
#         current_time2 = now2.strftime("%H:%M:%S")
#         print(current_time)
#         print(current_time2)
#         ilen=0
#         for step2 in path:
#             ilen=ilen+1

#         #ral=re.split(',')
#         #print("RRRRWWWW "+ral[1])
#         # Check if we reached the target node
#         if current_node[0] == target_node:
#             print(path)
#             path=path + [(current_node, "reached", target_node)]
#             for step in path:
#                 print(f"{step[0]} --{step[1]}--> {step[2]}")
#             now2 = datetime.now()
#             current_time2 = now2.strftime("%H:%M:%S")
#             print(current_time)
#             print(current_time2)
#             return ilen,path
#             #return path + [(current_node, "reached", target_node)]

#         # Query outgoing links from the current node
        
#         stoa=f""" {stra} 
#         SELECT ?next_node ?predicate WHERE {{
#              <{current_node[0]}> ?predicate ?next_node .
#                ?next_node rdfs:label ?label .
#                                FILTER (?predicate != <http://dbpedia.org/ontology/wikiPageWikiLink>)

#                FILTER (lang(?label) = "en").
              
#          }}
#         """
#         # stoa=f""" {stra} 
#         # SELECT ?next_node ?predicate WHERE {{
#         #     <{current_node[0]}> ?predicate ?next_node .
#         #       ?next_node rdfs:label ?label .
#         #       FILTER (lang(?label) = "en").
#         # }}
#         # """
#         sparql.setQuery(stoa)
        
        
#         print("SPAROS")
#         print(stoa)
#         #print(f""" {stra} 
#         #SELECT ?next_node ?predicate WHERE {{
#         #   <{current_node[0]}> ?predicate ?next_node .
#         #}}
#         #""")
        
#         sparql.setReturnFormat(JSON)

#         try:
#             print("HE1")

#             results = sparql.query().convert()
#             print("HE")
#             if isinstance(results, bytes):  # Decode if necessary
#                 results = loads(results.decode("utf-8"))
#         except Exception as e:
#             print(f"Error querying SPARQL endpoint: {e}")
#             print_exc() 
#             continue
#         lista=[]
#         lista2=[]
#         dicta={}
#         # Process each outgoing link and add it to the queue if not visited
#         if results.get("results") and results["results"].get("bindings"):
#             for result in results["results"]["bindings"]:
#                 next_node = result["next_node"]["value"]
#                 predicate = result["predicate"]["value"]
#                 dicta[next_node]=predicate
                
#                 # Append to the path and add to the queue
                
#                 if is_english_only(next_node) and next_node not in visited and "resource" in next_node and 'Category' not in next_node and 'Template' not in next_node:
#                     lista.append(next_node)
#                     lista2.append(predicate+" "+next_node)
                    
#                     #queue.append((next_node, path + [(current_node, predicate, next_node)]))
#         #print('LISTA EINAI '+str(lis))      
              
#         aa=queue[0]
#         an,ass=aa
        
#         print("LISTA")
#         print(str(lista))
        
#         if lista.__len__()>1:
#             epel=3
#             toyl=lista.__len__()
#             if toyl>6 and toyl<=12:
#                 epel=11
#             elif toyl>12:
#                 epel=11
#             else:
#                 epel=toyl-1
#             print("EPEL "+str(epel))
#             #print("ANE "+an[0])
#             #stringas="Select  at most the 4 nodes from the list "+str(lista)+" that could best as meaning lead to  "+target_node+" than the others. Return them  as string of entities. An entity is node comma score. Score is from 0.0 for irrelevant to 1.0 high relevant. If target node is exacly found in list give it score 5.0. Final string is entity#entity#entity etc mean seperate entities with # Return plain string"
#             stringas=" do not insert δικους σου nodes αλλα επελεξε ακριβως "+str(epel)+" αν ειναι διαθεσιμoi απο την "+str(lista)+" αυτους που πλησιαζουν πιο πολυ  α΄΄΄΄λλα και αλλους που θα μπορουσαν πιο πιθανα να οδηγησουν στον κομβο  "+target_node+" επελεξε συνολικα +"+str(epel)+"και δωσε τους ενα σκορ εγγυτητας με τρια δεκαδικα. εαν δεν πλησιαζει πολυ δωσε σκορ κατω απο 0.4. Αν πλησιζει πολυ δωσε πανω απο 0.7. Επελεξε τους κομβους με τα μεγαλυτερα σκορ. Επισης μην επιλεξεις nodes που αναφερονται σε γενικες κατηγοριες αλλα μονο σε υπαρκτα entities. Return them  as string of entities. An entity is node comma score. Score is from 0.0 for irrelevant to target to 1 .if the node includes the word of the target, return as a score 1.0 .Do not comment scores.If target node is exacly found in list give it score 500.0. Final string is entity#entity#entity etc mean seperate entities with without headers # Return plain string.Αν δεν ειναι διαθεσιμοι 6 κομβοι δεν πειραζει και ΜΗΝ ΔΗΜΙΟΥΡΓΗΣΕΙΣ ΚΟΜΒΟΥΣ ΑΠΟ ΤΗΝ ΔΙΚΗ ΣΟΥ ΓΝΩΣΗ που δεν υπαρχουν στην λιστα. ΑΚΟΜΑ ΚΑΙ ΕΝΑΣ ΝΑ ΕΙΝΑΙ Ο ΚΟΜΒΟΣ ΕΠΕΣΤΡΕΨΕ ΤΟΝ"
    
#             #stringas="Select  at most the 7 nodes from the list "+str(lista)+" that could best lead to  "+target_node+" than the others return them without any other words  sort them with the most relevant to target node last return a comma seperated string next to the node write a relevance score for 0 to 1 more score more relevant to target seperate tuples with #"
#             #response = model.generate_content(stringas)
            
#             # response2 = client.chat.completions.create(
#             # model="gpt-3.5-turbo",
#             # messages=[{"role": "user", "content": stringas}])
#             message = client.messages.create(
#             model="claude-3-5-sonnet-20241022",
#             max_tokens=1000,
#             temperature=0,
#             system="You are a DBPEDIA SPECIALIST",
#             messages=[
#                     {
#                         "role": "user",
#                         "content": [
#                             {
#                                 "type": "text",
#                                 "text": stringas
#                             }
#                         ]
#                     }
#                 ]
#             )
#             response=message.content[0].text
    
#             #response = response2.choices[0].message.content
#             #print("l2 "+str(lista2))
#             #print()
#             #int("STRINGAS "+stringas)
#             #print()
#             # /ra=response.text
            
#             ra=response
#             #ra=ra.strip()
#             ra=ra.replace('\n','')
    
#             tups=ra.split('#')
    
#             #for t in tups:
#              #   sta=t.split(',')
                
            
#             #print("RAA "+ra)
#             # fruit_list = ra.split(',')
#             print("TUPS "+str(tups))
            
#             if lista:
#                 for ft in tups:
#                     #print("FT "+ft)
#                     try:
#                         sco=ft.split(',')
#                         sco[0]=sco[0].replace(' ','')
#                         sco[0]=sco[0].replace('\'','')
#                         sco[1]=sco[1].replace('\'','')
#                         print("SCO +"+str(sco))
        
#                         #print("LENA "+str(len(queue)))
#                         # if start==0:
#                         #     #print("SALOS")
#                         #     queue = [([start_node,0.0], [])]   
                                         
#                         #print("LENA2 "+str(len(queue)))
#                         #print("TUPS "+str(len(tups)))
#                         position=-1
#                         if sstart==0:
                            
#                             position=0
#                             sstart=1
#                             queue.insert(position,(sco, path + [(current_node, dicta[sco[0]], sco)]))
        
#                             #print("STARTER")    
#                         else:          
#                             i=0  
                            
#                             while True:
#                                 if i>=queue.__len__():
#                                     print("BROKE")
#                                     break
#                                 #print("OKL")
#                                 #print("AI "+str(i))
#                                 a,b=queue[i]
#                                 #print("QYA "+a[0])
#                                 # print("A! "+str(a[1])+" "+str(float(sco[1])))
#                                 try:
#                                     if  float(a[1])<float(sco[1]):
#                                             #print("KO")
#                                             position=i
#                                             #print("AD "+sco[0])
#                                             start=1
#                                             break
                                    
                                    
#                                 except Exception as e:
#                                     print(f"aAn error occurred: {e}")
                                    
#                                     print_exc() 
#                                     break
                                    
#                                 i=i+1 
#                             if i>=len(queue):
#                                 print("XAATZIBRETAS")
#                                 position=len(queue)-1
#                             else:
#                                 print("")
#                                 #print("MANTOS "+str(len(queue))+"POS "+str(position))  
                                
#                             if position==-1:
#                                 print("HELLO DOLLY")
#                             else:
#                                 #print('thmuios')     
#                                 #if (float(sco[1])>0):
#                                 if (True):
        
#                                     #print("TJU2")
#                                     queue.insert(position,(sco, path + [(current_node, dicta[sco[0]], sco)]))
        
#                         #queue.insert(0,(f, path + [(current_node, dicta[f], f)]))
                        
#                         # if sco[0]==target_node:
#                         #     print("DOUNF")
#                         #     for step in path:
#                         #         print(f"{step[0]} --{step[1]}--> {step[2]}")
#                         #     return
#                         # print("AD "+sco[0])
#                     except Exception as e:
#                         print(f"An error occurred: {e}")
#                         print_exc() 
                        
#     # If queue exhausts without finding target
#     return None

def llm(entity1: str, entity2: str):
    start_node=f"{SPARQL_RESOURCE_URL}{entity1}"
    target_node=f"{SPARQL_RESOURCE_URL}{entity2}"
    now = time()
    word_entity_sim = get_entity_similarity(entity1, entity2)
    
    print(f"\nSimilarity between {start_node} and {target_node}: {word_entity_sim}")
    depth,path = find_path_between_nodes(start_node, target_node, f"{SPARQL_URL}/query", llm=True)
    if not path:
        return
    for step in path:
        print(f"{step[0]} --{step[1]}--> {step[2]}")
    totalp=0.0
    totale=0.0
    now2 = time()
    
    lana=len(path)
    ida=1
    for triple in path:
        print(f"({triple[0]}, {triple[1]}, {triple[2]})")
        xa0= triple[0][0].rsplit('/', 1)[-1]
        xa2= triple[2][0].rsplit('/', 1)[-1]
        xa0=xa0.replace("_"," ").replace("-",' ')
        xa2=xa2.replace("_"," ").replace("-",' ')
        xa3=entity2
        xa3=xa3.replace("_"," ").replace("-",' ')
    
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
    nn = totalp/(float(depth))
    nt = totale/(float(depth))
    return now2-now, depth, nn, nt