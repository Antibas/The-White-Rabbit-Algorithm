# The White Rabbit

This code is part of paper **"White Rabbit: Escaping the Online KG Rabbit Hole Using Embeddings"**

## Abstract
The proliferation of Knowledge Graphs (KGs) in recent years has resulted in the generation of massive datasets now available online. Exploring these graphs to identify meaningful connections between entities is a valuable, yet challenging task. This is mainly due to the large size, the complexity, and the limited interfaces (i.e., SPARQL endpoints) they offer for their online exploration. In this paper, we focus on discovering high-quality paths between two entities in online KGs, using embeddings. First, we introduce the problem of context-aware path finding, which results into coherent paths including highly relevant entities.  Then, we introduce the White Rabbit, an approach that involves scoring entity neighbors using embeddings, prioritizing exploration through a queue-based mechanism, and iteratively refining the search process. We compare our approach with baselines including structural methods, various pretrained embedding methods, and a large language model oracle, showing the benefits of our approach in optimizing both the efficiency of the task and the quality of the retrieved paths.

## Instructions
1. Download [enwiki_20180420_100d.pkl.bz2](http://wikipedia2vec.s3.amazonaws.com/models/en/2018-04-20/enwiki_20180420_100d.pkl.bz2)
2. TODO