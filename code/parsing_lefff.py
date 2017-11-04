# Parsinf leff
lefff = pd.read_csv("C:/Users/TOUZEM/Documents/Python Scripts/vertuo/lefff.txt", sep = "\t")
lefff.drop(lefff.columns[1], axis = 1, inplace = True)

lefff.head()
lefff["SYNTACTIC_CLASS"].head()

import re
lefff["PREDICAT"] = lefff["SYNTACTIC_CLASS"].str.extract(re.compile("\[pred\=\'(.*?)\_"))
lemmDict = dict(zip(lefff["LEXICON"], lefff["PREDICAT"]))
