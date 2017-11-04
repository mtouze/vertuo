def corpusCleaning(
        corpus,
        lower_case = True,
        remove_accents = True,
        remove_digits = True,
        remove_punctuations = True,
        remove_blanks = True):
    
    import string
    import unidecode
    import re
    
    ans = corpus.copy()
    
    if lower_case:
        ans = ans.str.lower()
    
    if remove_punctuations:
        listPunc = string.punctuation.replace("-","") + "’…–>«»"
        punctDict = {ord(listPunc[i]): " " for i in range(0, len(listPunc))}
        ans = ans.str.translate(punctDict)
        
    if remove_digits:
        digitsDict = {ord(string.digits[i]): "" for i in range(0, len(string.digits))}
        ans = ans.str.translate(digitsDict)
        
    if remove_accents:
        for i, article in enumerate(ans):
            ans[i] = unidecode.unidecode(article)
            
    if remove_blanks:
        for i, article in enumerate(ans):
            ans[i] = re.sub(" +", " ", article)
        
    return ans


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
                
    cleanDict = dict()
    for word in wordsCount.keys():
        stemWord = stemmer.stem(word)
        cleanDict[" " + word + " "] = " " + stemDictClean[stemWord] + " "
        
    return cleanDict