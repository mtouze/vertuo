import pandas as pd
import numpy as np

link = "https://raw.githubusercontent.com/mtouze/vertuo/master/data/articles.csv"
df = pd.read_csv(
        link, 
        quoting = 1, 
        encoding = "utf-8")
print (df.head())


# Punctations & others
import string

df["article"] = df["article"].str.lower()

d_punc = {ord (string.punctuation[i]): " " for i in range(0, len(string.punctuation))}
df["article"] = df["article"].str.translate(d_punc)

d_digits = {ord (string.digits[i]): "" for i in range(0, len(string.digits))}
df["article"] = df["article"].str.translate(d_digits)

df.dropna(inplace = True)
        
# Stemming
"""
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer ()
for word in df ["article"].iloc[4].split (" "):
    print (stemmer.stem (word))
"""

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

stopWords = list(set(stopwords.words("french") + get_stop_words("french")))
articles = df["article"]
maxFeatures = 100

CV = CountVectorizer(
        encoding = "utf-8",
        decode_error = "ignore", 
        stop_words = stopWords,
        lowercase = True,
        max_df = 2/3,
        max_features = maxFeatures)
articlesCV = CV.fit_transform (articles)


TfidfV = TfidfVectorizer(
        encoding = "utf-8", 
        decode_error = "ignore", 
        strip_accents = "ascii",
        stop_words = stopWords,
        max_features = maxFeatures,
        use_idf = True)
articlesTfidfV = TfidfV.fit_transform(articles)


# cosine similiarity
from sklearn.metrics.pairwise import cosine_similarity
dist = cosine_similarity (articlesCV.T)

# Adjacency matrix
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

nodeLabels = CV.get_feature_names()
for row in range(0, len(nodeLabels)):
    print(dist[row,:dist[row,:].argsort()[-2]])
    G.add_edge(nodeLabels[row], nodeLabels[dist[row,:].argsort()[-2]], weight = dist[row, dist[row,:].argsort()[-2]])
    G.add_edge(nodeLabels[row], nodeLabels[dist[row,:].argsort()[-3]], weight = dist[row, dist[row,:].argsort()[-3]])

edgeWidth = [G[u][v]["weight"] * 2 for u, v in G.edges()]

d = G.degree()
nodeColor = []
for e in d.keys():
    cmap = plt.get_cmap("Blues")
    color = d[e]/max(d.values())
    nodeColor.append(cmap(color))

pos= nx.spring_layout(G, k = 0.15, iterations = 20)
nx.draw(
        G,
        pos = pos,
        with_labels = True, 
        node_color = nodeColor,
        node_size = [n * 100 for n in d.values()],
        width = edgeWidth)
plt.show()
