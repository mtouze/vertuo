def corpusCleaning(
        corpus,
        lower_case = True,
        remove_accents = True,
        remove_digits = True,
        remove_punctuations = True):
    
    import string
    
    if lower_case:
        corpus = corpus.str.lower()
    
    if remove_punctuations:
        listPunc = string.punctuation + "’–"
        punctDict = {ord(listPunc[i]): " " for i in range(0, len(listPunc))}
        corpus = corpus.str.translate(punctDict)
        
    if remove_digits:
        digitsDict = {ord(string.digits[i]): "" for i in range(0, len(string.digits))}
        corpus = corpus.str.translate(digitsDict)
        
    if remove_accents:
        eList = "éèêë"
        aList = "àâä"
        eDict = {ord(eList[i]): "e" for i in range(0, len(eList))}
        aDict = {ord(aList[i]): "a" for i in range(0, len(aList))}
        corpus = corpus.str.translate(eDict).str.translate(aDict)
        
    return corpus


def DictMostFrequentStemWord(corpus):

    from collections import Counter
    from nltk.stem.snowball import FrenchStemmer
    
    wordsCount= Counter()
    for article in corpus:
        wordsCount.update(article.split())
        
    stemmer = FrenchStemmer()
    stemDict = dict()
    for word in wordsCount.keys():
        stemWord = stemmer.stem(word)
        if stemWord not in stemDict.keys():
            stemDict[stemWord] = [(word, wordsCount[word])]
        else:
            stemDict[stemWord].append((word, wordsCount[word]))
            
    stemDictClean = dict()
    for stemWord in stemDict.keys():
        maxCount = 0
        for e in stemDict[stemWord]:
            if e[1] > maxCount:
                stemDictClean[stemWord] = e[0]
                maxCount = e[1]
            elif e[1] == maxCount:
                if e[0] < stemDictClean[stemWord]:
                    stemDictClean[stemWord] = e[0]
                    maxCount = e[1]

    return stemDictClean