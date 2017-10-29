import pandas as pd
import numpy as np

link = "https://raw.githubusercontent.com/mtouze/vertuo/master/data/articles.csv"
df = pd.read_csv(link, quoting = 1, encoding = "utf-8")
print(df.head())


# Punctations & others
import string

## Lower case
df["article"] = df["article"].str.lower()

## Remove punctuations
punctDict = {ord(string.punctuation[i]): " " for i in range(0, len(string.punctuation))}
df["article"] = df["article"].str.translate(punctDict)

## Remove digits
digitsDict = {ord(string.digits[i]): "" for i in range(0, len(string.digits))}
df["article"] = df["article"].str.translate(digitsDict)

## Remove accent
eList = "éèêë"
aList = "àâä"
eDict = {ord(eList[i]): "e" for i in range(0, len(eList))}
aDict = {ord(aList[i]): "a" for i in range(0, len(aList))}

df["article"] = df["article"].str.translate(eDict).str.translate(aDict)

## Remove NA articles
df.dropna(inplace = True)


stemDict = DictMostFrequentStemWord(df["article"])


# Stemming

df["stemArticle"] = np.nan
for i, article in enumerate(articles):
    stemArticle = ""
    for word in article.split():
        stemWord = stemmer.stem(word)
        stemArticle = stemArticle + " " + stemDictClean[stemWord]
    df["stemArticle"].iloc[i] = stemArticle

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
stemArticles = df["stemArticle"]
maxFeatures = 100

CV = CountVectorizer(
        encoding = "utf-8",
        decode_error = "ignore", 
        stop_words = stopWords,
        lowercase = True,
        max_features = maxFeatures)
articlesCV = CV.fit_transform (stemArticles)


TfidfV = TfidfVectorizer(
        encoding = "utf-8", 
        decode_error = "ignore", 
        strip_accents = "ascii",
        stop_words = stopWords,
        max_features = maxFeatures,
        use_idf = True)
articlesTfidfV = TfidfV.fit_transform(stemArticles)


# cosine similiarity
from sklearn.metrics.pairwise import cosine_similarity
dist = cosine_similarity (articlesCV)

# Adjacency matrix
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

#nodeLabels = CV.get_feature_names()
import re
df["title"] = df["link"].str.extract(re.compile("/portfolio/(.*?)/")).str.replace("-", " ")
nodeLabels = [title for title in df["title"]]
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
