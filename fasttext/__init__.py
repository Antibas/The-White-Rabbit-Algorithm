import os
from gensim.models import KeyedVectors
from gensim.downloader import base_dir


def load_data():
    path = os.path.join(base_dir, 'fasttext-wiki-news-subwords-300', "fasttext-wiki-news-subwords-300.gz")
    model = KeyedVectors.load_word2vec_format(path, binary=False)
    return model
