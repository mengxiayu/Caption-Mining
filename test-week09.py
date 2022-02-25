# process syllabus data
# each txt file is a course

from collections import Counter
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

stops |= {"one", "many", "little", "different", "thing", "two", "theta" , "get", "semester","hour","class","week","textbook","students","student","mask","part","office","hour","assignments","syllabus","exam","grade","homework", "university", "short", "long", "test", "tests", "quiz", "rubric", "course", "previous", "e", "assignment", "exams", "due","policy"}
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
    output_dir = "syllabus/syllabus/course_concepts/"
    # files = glob.glob(data_dir + '/**/*.txt', recursive=True)
    depts = os.listdir(data_dir)
    for dept in depts:
        if dept.startswith('.'):
            continue
        files = os.listdir(data_dir+dept)
        print("# files:", len(files))
        for fn in files:
            if fn.startswith('.'):
                continue
            bigramCounter = Counter()
            trigramCounter = Counter()
            fr = open(data_dir+dept+'/'+fn, 'r', encoding='utf-8')
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
                    # print(k,v)
            print(" === trigram examples: ===")
            for k,v in trigramCounter.most_common(100):
                if v > 1:
                    concept_list.append([k,v])
                    # print(k,v)
            course_name = fn.split("Syllabus")[0]
            fw = open(output_dir+dept+'/'+course_name+'.md', 'w', encoding='utf-8')
            fw.write("#course\n")
            fw.write(f"#{dept}\n")
            for c,v in concept_list:
                fw.write(f"[[{c}]]\n")
            fw.close()
extract_ngrams()