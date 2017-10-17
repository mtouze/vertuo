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

d_punc = {ord (string.punctuation[i]): " " for i in range (0, len (string.punctuation))}
df["article"] = df["article"].str.translate(d_punc)

d_digits = {ord (string.digits[i]): "" for i in range (0, len (string.digits))}
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

stopWords = stopwords.words("french") + get_stop_words("french")
articles = df["article"]
maxFeatures = 100

CV = CountVectorizer(
        encoding = "utf-8",
        decode_error = "ignore", 
        stop_words = stopWords,
        lowercase = True,
        max_df = 0.75,
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

plt.subplot(111)
nodeLabels = CV.get_feature_names()
for row in range(0, len(nodeLabels)):
    G.add_node(nodeLabels[row], label = nodeLabels[row])
    G.add_edge(nodeLabels[row], nodeLabels[dist[row,:].argsort()[-2]])
    G.add_edge(nodeLabels[row], nodeLabels[dist[row,:].argsort()[-3]])
    
nx.draw(G, with_labels = True)
plt.show()
