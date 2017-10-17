#Pour un article
import nltk
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import SpaceTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import codecs
from wordcloud import WordCloud
import matplotlib.pyplot as plt



def RecupMostFreq (article):
    #Supression de la ponctuation
    ponctuation = [";","!",",",".","?","'","[","]","(",")","{","}","»","«","–",":","’","%","&"]
    for i in article :
        if i in ponctuation :
            article=article.replace(i,' ')
    #On mets tous les mots en minsucules pour éviter les doublons 
    #entre La et la par exemple
    article=article.lower()
    #On récupère les mots en supprimant les espaces dans le texte 
    token=WhitespaceTokenizer().tokenize(article)
    """
    Si besoin de télécharger le package stopwords
    nltk.download("stopwords")
    """
    # Fréquence des mots 
    fdist = FreqDist((token))
         
    #On supprime ceux qui sont dans la liste issue de stopwords
    for sw in stopwords.words("french"):
         if sw in fdist:
              fdist.pop(sw)
              
    #Supression des mots inutiles issue du fichier 000.txt
    text=codecs.open('000.txt', encoding='utf-8')
    inutile=text.read()
    text.close()
    #On repasse par un token pour isoler les mots
    token_inutile=WhitespaceTokenizer().tokenize(inutile)
    for supp in token_inutile:
         if supp in fdist:
              fdist.pop(supp)
             
    #Supression des chiffres inutiles issue du fichier 000.txt
    text=codecs.open('chiffre.txt')
    inutile=text.read()
    #On repasse par un token pour isoler les mots
    token_chiffre=WhitespaceTokenizer().tokenize(inutile)
    for supp in token_chiffre:
         if supp in fdist:
              fdist.pop(supp)
              
    #↨print (fdist.items())
    #print (fdist.most_common(100))
    return fdist
    
def FichierMostFreq (fdist,i):
   # NbTotal=fdist.N()
   # fichier = open("Most_Freq\MostFreq_%d.txt" %i, "a")
   # for i in fdist.keys():
   #     if int(fdist.freq(i)*NbTotal)>2 :
   #         for j in range(1,int(fdist.freq(i)*NbTotal)):
   #             fichier.write(i)
   #             fichier.write(" ")
   # fichier.close() 
   
    mc=fdist.most_common(100)
    for j in range(1,len(mc)) :
        if fdist.most_common(100)[j][1] <= 2 :
            mc.pop()
    
    fichier = open("Most_Freq\MostFreq_%d.txt" %i, "a")
    for j in range(0,len(mc)):
        fichier.write(mc[j][0])
        fichier.write(" ")
    fichier.close()
    
def CreationWordle (article, i):
    # Generate a word cloud image
    wc = WordCloud(background_color="white")
    wc.generate(article)
    
    fig = plt.figure()
    fig.set_figwidth(10)
    fig.set_figheight(14)
    title = 'Most frequent words Article %d' %i
    fontcolor='#000000'
    plt.imshow(wc, interpolation='bilinear')
    plt.title(title, color=fontcolor, size=20, y=1.01)
    plt.axis('off')
    #☺plt.show()
    fig.savefig('wordle\wc_article_%d' %i)
    
    return wc
