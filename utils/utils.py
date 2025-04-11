from re import fullmatch
import numpy as np
from utils.constants import WIKI2VEC

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