import urllib
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


#==============================================================================
# initialisation des paramètre
#==============================================================================
explored = dict ()
frontier = []
vertuo = "http://www.vertuoconseil.com/portfolio/"


#==============================================================================
# # URL du site internet Vertuo
#==============================================================================
url = "http://www.vertuoconseil.com/vertuo-conseil/"
req = urllib.request.Request (url, headers = {"User-agent": "Mozilla/5.0"})
html_page = urllib.request.urlopen (req)
html_text = html_page.read ()


#==============================================================================
# # Lecture du code HTML de l'URL
#==============================================================================
code_html = BeautifulSoup (html_text, "lxml")

for link in code_html.find_all (href = True):
    if not link ["href"] in frontier + list (explored.keys()) and len (link["href"]) != 0:
        if link ["href"][:len (vertuo)] == vertuo:
            if link ["href"][-4:] not in [".jpg", ".png"] and link ["href"][0] != "/":
                frontier.append (link ["href"])
explored [url] = True


#==============================================================================
# # Récupération de l'ensemble des liens HTML
#==============================================================================
while frontier:

    url =  frontier.pop ()
    
    req = urllib.request.Request (url, headers = {"User-agent": "Mozilla/5.0"})
    html_page = urllib.request.urlopen (req)
    html_text = html_page.read ()
    code_html = BeautifulSoup (html_text, "lxml")

    for link in code_html.find_all (href = True):
        if not link ["href"] in frontier + list (explored.keys()) and len (link["href"]) != 0:
            if link ["href"][:len (vertuo)] == vertuo:
                if link ["href"][-4:] not in [".jpg", ".png"] and link ["href"][0] != "/":
                    frontier.append (link ["href"])
                    
    explored [url] = True
    


# Suppressions des liens en doublon
d_articles = explored.copy ()
for link in explored.keys ():
    if "?" in link or "feed" in link:
        del d_articles [link]


             
#==============================================================================
# Import des articles
#==============================================================================
df = pd.DataFrame (columns = ["link", "title", "article"])

for link in d_articles.keys ():
    
    req = urllib.request.Request (link, headers = {"User-agent": "Mozilla/5.0"})
    html_page = urllib.request.urlopen (req)
    html_text = html_page.read ()
    code_html = BeautifulSoup (html_text, "lxml")
    
    if code_html.find_all ("div", 
                           class_ = "project-description post-content"):
        
        text = code_html.find_all ("div", 
                                   class_ = "project-description post-content")[0].get_text()
        
        text_short = code_html.find_all ("span",
                                         class_ = "entry-title")[0].get_text ()

        article = text[text.find ("Project Description") + len ("Project Description"):text.lower ().find (".fusion-button.button-1")].replace("\n", "").replace (u"\xa0", "")
        title = text_short.replace ("\n", "").replace ("\t", "")

        # Alimentation de la table
        if title and article:
            df = df.append (pd.DataFrame ([[link, title, article]],
                                     columns = ["link", "title", "article"]),
                            ignore_index = True)


#==============================================================================
# Sauvegarde de la table
#==============================================================================
df.index.names = ["ID"]
df.to_csv ("articles.csv",
           sep = ";")
