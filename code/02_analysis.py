import pandas as pd
import numpy as np
import re

link = "https://raw.githubusercontent.com/mtouze/vertuo/master/data/articles.csv"
df = pd.read_csv(link, quoting = 1, encoding = "utf-8")
print(df.head())

# Title 
df["title"] = df["link"].str.extract(re.compile("/portfolio/(.*?)/")).str.replace("-", " ")

# Clean corpus

## Common cleaning process
corpus = df["article"]
corpus = corpusCleaning(
        corpus,
        lower_case = True,
        remove_digits = True,
        remove_punctuations = True,
        remove_accents = True)

## Remove NA articles
df.dropna(inplace = True)

# Stemming

## Stem Dictionnary
stemDict = DictMostFrequentStemWord(corpus)

## Replace Stem word / most frequent word
corpus = corpus.str.translate(stemDict)


# Lemmatisation
"""
import treetaggerwrapper as ttw

tagger = ttw.TreeTagger (TAGLANG = 'fr')
tags = tagger.tag_text (df ["article"].iloc[4])

lem_article = ""
for word in range (0, len (tags)):
    new_word = tags [word].split("\t")[-1]
    print (new_word)
    lem_article += " " + new_word
"""


#
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.corpus import stopwords
from stop_words import get_stop_words

stopWords = stopwords.words("french") + get_stop_words("french")
maxFeatures = 100

nbArticles = len(corpus)
CV = CountVectorizer(
        encoding = "utf-8",
        decode_error = "ignore", 
        stop_words = stopWords,
        lowercase = True,
        max_df = nbArticles*0.5,
        min_df = nbArticles*0.1,
        max_features = maxFeatures)
articlesCV = CV.fit_transform (corpus)

"""
TfidfV = TfidfVectorizer(
        encoding = "utf-8", 
        decode_error = "ignore", 
        strip_accents = "ascii",
        stop_words = stopWords,
        max_features = maxFeatures,
        use_idf = True)
articlesTfidfV = TfidfV.fit_transform(stemArticles)
"""

# cosine similiarity
from sklearn.metrics.pairwise import cosine_similarity
dist = cosine_similarity(articlesCV.T)

# Adjacency matrix
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

nodeLabels = CV.get_feature_names()
for row in range(0, len(nodeLabels)):
    G.add_edge(nodeLabels[row], nodeLabels[dist[row,:].argsort()[-2]])
    G.add_edge(nodeLabels[row], nodeLabels[dist[row,:].argsort()[-3]])

d = G.degree()
nodeColor = []
for e in d.keys():
    cmap = plt.get_cmap("Blues")
    color = d[e]/max(d.values())
    nodeColor.append(cmap(color))

nx.draw(
        G,
        pos = nx.spring_layout(G),
        with_labels = True, 
        node_color = nodeColor,
        node_size = [n * 100 for n in d.values()])
plt.show()
