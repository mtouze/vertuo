import Fonctions
from Fonctions import RecupMostFreq
from Fonctions import FichierMostFreq
from Fonctions import CreationWordle
import codecs
import os

nb_articles=(len(os.listdir("Articles")))

for i in range (1, nb_articles):
    #Ouverture du fichier 
    text=codecs.open('Articles\Article_%d.txt'%i)#Article12
    #Lecture du fichier 
    contenu=text.read()
    text.close()
    fdist=RecupMostFreq(contenu)
    
       
    FichierMostFreq(fdist,i)
    
    text=codecs.open('Most_Freq\MostFreq_%d.txt' %i)
    nuage=text.read()
    text.close()
    if len(nuage)>0:
        CreationWordle(nuage,i)
   
    
    