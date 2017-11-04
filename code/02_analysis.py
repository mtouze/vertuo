import pandas as pd
import numpy as np
import re


stop_wordsList = "https://raw.githubusercontent.com/mtouze/vertuo/master/data/adverb.csv"
link = "https://raw.githubusercontent.com/mtouze/vertuo/master/data/articles.csv"

df = pd.read_csv(link, quoting = 1, encoding = "utf-8")
df_adverb = pd.read_csv(adverb, encoding = "latin-1")

print(df.head())

# Title
df["title"] = df["link"].str.extract(re.compile("/portfolio/(.*?)/")).str.replace("-", " ")
df.fillna("", inplace = True)
# Clean corpus

## Common cleaning process
corpus = df.reset_index().dropna()["article"]
titles = df.reset_index().dropna()["title"]
corpus = corpusCleaning(corpus, remove_accents = False)

adverb = df_adverb["ADVERB"]
adverb = corpusCleaning(adverb)
# Stemming

## Stem Dictionnary
stemDict = DictMostFrequentStemWord(corpus)
## Replace Stem word / most frequent word
corpus = corpus.replace(stemDict, regex = True)


# Lemmatisation
lemmCorpus = pd.Series([np.nan for i in range(0, len(corpus))])
for i, article in enumerate(corpus):
    lemmArticle = ""
    for word in article.split(" "):
        if word in lemmDict.keys():
            lemmArticle = lemmArticle + " " + str(lemmDict[word])
        else:
            print(word)
            lemmArticle = lemmArticle + " " + str(word)
    lemmCorpus[i] = lemmArticle


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

adverbList = df_adverb["ADVERB"].tolist()
stopWords = stopwords.words("french") + get_stop_words("french") + adverbList
maxFeatures = 100

nbArticles = len(corpus)
CV = CountVectorizer(
        encoding = "utf-8",
        decode_error = "ignore",
        stop_words = stopWords,
        lowercase = True,
        max_df = nbArticles*0.5,
        min_df = nbArticles*0.1,
        max_df = 0.5,
        min_df = 0.1,
        max_features = maxFeatures)
articlesCV = CV.fit_transform(lemmCorpus)

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


# Clustering
from sklearn.cluster import KMeans
KM = KMeans(
        n_clusters = 8)
corpusKM = KM.fit(dist)

wordClusters = list(zip(CV.get_feature_names(), corpusKM.labels_))
clusterDict = dict()
for e in wordClusters:
    if e[1] not in clusterDict.keys():
        clusterDict[e[1]] = e[0]
    else:
        clusterDict[e[1]] = clusterDict[e[1]] + ", " + e[0]
clusterDict

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
cluster = corpusKM.labels_
colorDict = dict(zip(nodeLabels, cluster))
for e in d.keys():
    cmap = plt.get_cmap("Set2")
    color = colorDict[e]/max(colorDict.values())
    #color = 0.5
    nodeColor.append(cmap(color))

nx.draw(
        G,
        pos = nx.spring_layout(G, k = 0.05),
        with_labels = True,
        node_color = nodeColor,
        node_size = [n * 100 for n in d.values()])
plt.show()
