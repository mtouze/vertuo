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