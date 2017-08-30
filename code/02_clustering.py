import pandas as pd
import numpy as np

import os
os.chdir ("C:/Users/micha/Documents/Python Scripts")
df = pd.read_csv ("articles.csv", sep = ";", encoding = "latin-1")
print (df.head())

df.set_index ("ID", inplace = True)


# Features
corpus = df ["article"]


# Punctations & others
import string

df ["article"] = df ["article"].str.lower()

d_punctuation = {ord (string.punctuation [i]): " " for i in range (0, len (string.punctuation))}
df ["article"] = df ["article"].str.translate (d_punctuation)

d_digits = {ord (string.digits [i]): None for i in range (0, len (string.digits))}
df ["article"] = df ["article"].str.translate (d_digits)

print (df.head())

        
# Stemming
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer ()
for word in df ["article"].iloc[4].split (" "):
    print (stemmer.stem (word))


# Lemmatisation
import treetaggerwrapper as ttw

tagger = ttw.TreeTagger (TAGLANG = 'fr')
tags = tagger.tag_text (df ["article"].iloc[4])

lem_article = ""
for word in range (0, len (tags)):
    new_word = tags [word].split("\t")[-1]
    print (new_word)
    lem_article += " " + new_word



#
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.corpus import stopwords

cv = CountVectorizer
x = cv().fit_transform (df ["article"])

stopWords = stopwords.words ("french")
max_features = 100

tfidf_vectorizer = TfidfVectorizer (encoding = "Latin-1", 
                                    decode_error = "ignore", 
                                    stop_words = stopWords,
                                    max_df = 1.,
                                    min_df = 0.,
                                    max_features = max_features,
                                    use_idf = True)

tfidf = tfidf_vectorizer.fit_transform (df ["article"])
print (tfidf)


from sklearn.metrics.pairwise import cosine_similarity
dist = cosine_similarity (tfidf)
print (dist)


# Adjacency matrix
adj_dict = {}
label_dict = {}
dist_diag = (dist < 0.99) * dist.T

for row in range (0, len (dist_diag)-1):
    node = np.argpartition (dist_diag [row,:], -1)[-1:]
    edge = dist_diag [row, np.argpartition (dist_diag [row,:], -1)[-1:]]
    adj_dict [row] = {node [0]: {'weight': edge [0]}}
    #label_dict [row] = np.array (tfidf_vectorizer.get_feature_names ())[row]
    label_dict [row] = np.array (df ["title"])[row]


# Graph
import networkx as nx
import matplotlib as plt

labels = np.array (tfidf_vectorizer.get_feature_names ())

G = nx.from_dict_of_dicts (adj_dict)
nx.relabel_nodes (G, mapping=label_dict, copy=False)
nx.draw (G, pos=nx.spring_layout (G), with_labels=True)

