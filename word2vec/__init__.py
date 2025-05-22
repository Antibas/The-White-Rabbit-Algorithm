import os
from gensim.models import KeyedVectors

def load_data():
    path = os.path.join('word2vec', "word2vec-google-news-300.gz")
    model = KeyedVectors.load_word2vec_format(path, binary=True)
    return model
