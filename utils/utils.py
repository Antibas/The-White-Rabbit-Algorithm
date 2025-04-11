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

def is_english_only(s):
    return bool(fullmatch(r"[A-Za-z0-9 /\-()_:/.]+", s))