import urllib
#from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


#==============================================================================
# initialisation des paramètre
#==============================================================================
# Get articles link
url = "http://www.vertuoconseil.com/vertuo-conseil/"
req = urllib.request.Request(url, headers = {"User-agent": "Mozilla/5.0"})
htmlPage = urllib.request.urlopen(req)
htmlText = htmlPage.read()
htmlText = htmlText.decode("utf-8", "ignore")

pattern = re.compile("http://www.vertuoconseil.com/portfolio/[\w-]{1,}/")
pageList = list(set(re.findall(pattern, htmlText)))
pageDict = dict(zip(pageList, [False] * len(pageList)))
print(pageDict)


# Retrieving articles
def getArtileTag(s):
    articleTag = re.compile("<article[\s\S]*?/article")
    #"<article[\s\S]*?</article>"
    try:
        return re.findall(articleTag, s)[0]
    except:
        return None
    
# Remove tags in html code
def removeTags(s):
    tags = re.compile("<.*?>")
    try:
        return re.sub(tags, "", s)
    except:
        return None

# Remove special car & get article content
def cleanText(s):
    #endArticleRe = re.compile("^.*?Conseil")
    try:
        # Remove mutliple special caracter
        cleanString = re.sub(re.compile("(\s{2,}|&\w*?;)"), " ", s)
        # Remove single special caracter
        cleanString = re.sub(re.compile("\s"), " ", cleanString)
        # Trunc text
        cleanString = re.findall("(^[\w\W]*?onseil) .fusion", cleanString)[0]
        # Remove datetime / title
        cleanString = re.sub(re.compile("^[\s\S]*?Project Description "), "", cleanString)
        return cleanString
    except:
        return None

d_article = {}
for page in pageDict.keys():
    req = urllib.request.Request(page, headers = {"User-agent": "Mozilla/5.0"})
    htmlPage = urllib.request.urlopen(req)
    htmlText = htmlPage.read().decode("utf-8", "ignore")
    
    article = getArtileTag(htmlText)
    article = removeTags(article)
    article = cleanText(article)

    # Stock article in dic
    d_article[page] = article


# Convert dictionnary to dataframe
df = pd.DataFrame(list(d_article.items()), columns = ["link", "article"])
df.set_index("link", inplace = True)

# Save in text file
df.to_csv(
        "C:/Users/micha/Documents/Python Scripts/vertuo/articles.csv",
        sep = ",",
        encoding = "utf-8",
        quoting = 1)
