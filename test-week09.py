# process syllabus data
# each txt file is a course

from collections import Counter
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

stops |= {"one", "many", "little", "different", "thing", "two", "theta" , "get", "semester","hour","class","week","textbook","students","mask","part","office","hour","assignments"}
# print(stops)
import spacy
nlp = spacy.load("en_core_web_sm")
import re

def n_grams(tokens, n):
    ngrams = []
    for i in range(len(tokens)-n+1):
        _tokens = tokens[i:i+n]

        texts = [t.text for t in _tokens]
        tt = " ".join(texts)
        if not tt[0].isalpha() or any(p in tt for p in ",./?';:()\""):
            continue
        if not set(texts) & stops and _tokens[-1].pos_ in ["PROPN","NOUN"] and _tokens[0].pos_ not in ["VERB"] :
            ngrams.append(tt)
    return ngrams

import glob
import os
def extract_ngrams():
    data_dir = "syllabus/data/syllabus/Fall2021/txt/"
    files = glob.glob(data_dir + '/**/*.txt', recursive=True)
    print("# files:", len(files))
    for fn in files:
        bigramCounter = Counter()
        trigramCounter = Counter()
        fr = open(fn, 'r', encoding='utf-8')
        lines = fr.readlines()
        fr.close()
        for line in lines:
            t = line.strip()
            if t == "":
                continue
            tokens = nlp(t.lower())
            bigrams = n_grams(tokens, 2)
            trigrams = n_grams(tokens, 3)
            bigramCounter.update(bigrams)
            trigramCounter.update(trigrams)
        concept_list = []

        print(" === bigram examples: ===")
        for k,v in bigramCounter.most_common(100):
            if v > 1:
                concept_list.append([k,v])
                print(k,v)
        print(" === trigram examples: ===")
        for k,v in trigramCounter.most_common(100):
            if v > 1:
                concept_list.append([k,v])
                print(k,v)
extract_ngrams()