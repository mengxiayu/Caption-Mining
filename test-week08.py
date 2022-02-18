# dependency of lectures based on concepts 
from collections import Counter
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))
import spacy
nlp = spacy.load("en_core_web_sm")
import re

def n_grams(tokens, n):
    ngrams = []
    for i in range(len(tokens)-n+1):
        _tokens = tokens[i:i+n]
        texts = [t.text for t in _tokens]
        if not set(texts) & stops and _tokens[-1].pos_ in ["PROPN","NOUN"]:
            tt = " ".join(texts)
            if not any(p in tt for p in ",./?';:"):
                ngrams.append(tt)
    return ngrams


def extract_ngrams():
    cn = "CS_410"
    script2course = {}
    fr = open("data/transcriptions2courses-410-c5.txt", 'r', encoding='utf-8')
    for line in fr:
        arr = line.strip().split('\t')
        script2course[arr[2]] = arr
    fr.close()
    print(len(script2course))

    fr = open("week04/corpus_corrected_410.txt", 'r', encoding='utf-8')
    cnt = 0
    bigramCounter = Counter()
    trigramCounter = Counter()
    for line in fr:
        cid, scriptid, text = line.strip().split('\t')
        if scriptid not in script2course:
            continue
        # extract concepts
        
        tokens = nlp(text.lower())
        bigrams = n_grams(tokens, 2)
        trigrams = n_grams(tokens, 3)
        bigramCounter.update(bigrams)
        trigramCounter.update(trigrams) 
        cnt += 1
    fr.close()
    print(cnt)
    print(len(bigramCounter))
    print(len(trigramCounter))
    print(" === bigram examples: ===")
    for k,v in bigramCounter.most_common(10):
        print(k,v)
    print(" === trigram examples: ===")
    for k,v in trigramCounter.most_common(10):
        print(k,v)

extract_ngrams()




def find_contexts(text, target, window=200):
    matches = re.finditer(target, text)
    matches_positions = [match.start() for match in matches]
    contexts = []
    for p in matches_positions:
        cstart = p-int(window/2) if p-int(window/2)>0 else 0
        cend = p+len(target)+int(window/2) if p+len(target)+int(window/2)<len(text) else len(text) 
        contexts.append(text[cstart:cend])
    return contexts

import json
def extract_occurences(target):
    cn = "CS_410"
    script2course = {}
    fr = open("data/transcriptions2courses-410-c5.txt", 'r', encoding='utf-8')
    for line in fr:
        arr = line.strip().split('\t')
        script2course[arr[2]] = arr
    fr.close()
    print(len(script2course))

    fr = open("week04/corpus_corrected_410.txt", 'r', encoding='utf-8')
    cnt = 0
    bigramCounter = Counter()
    trigramCounter = Counter()
    occurence = {
        "text": target,
        "contexts": [],
    }
    ctxs = []
    for line in fr:
        cid, scriptid, text = line.strip().split('\t')
        if scriptid not in script2course:
            continue
        text = text.lower()
        # extract concepts
        if target in text:
            contexts = find_contexts(text, target)
            for c in contexts:
                tmp_ctx = {
                    "course": cid, # '410' FIXME should be 'CS_410'
                    "transcription": scriptid,
                    "lecture": script2course[scriptid][6],
                    "lecture_num": int(script2course[scriptid][6].split()[1]),
                    "context": c,
                    "label": "Intro" if "called" in c else "Use",
                }    
                ctxs.append(tmp_ctx)
    occurence["contexts"] = sorted(ctxs, key=lambda x: x["lecture_num"])
    json.dump(occurence, open(f"week08/contexts_CS410_{target.replace(' ', '-')}.json", 'w'), indent=2)
extract_occurences("maximum likelihood")

from pyvis.network import Network
def visualize():
    net = Network(height='1000px', width='2000px', layout=True)
    concepts = ["conditional entropy", "word distribution","maximum likelihood"]
    data = []
    for c in concepts:
        data.append(json.load(open(f"week08/contexts_CS410_{c.replace(' ', '-')}.json", 'r')))
    
    for occur in data:
        # cnt_node = 0

        net.add_node(occur["text"], level=2, size=10)
        # lectures = set([x["lecture_num"] for x in occur["contexts"]])
        # lectures = sorted(list(lectures))

        # net.add_nodes(lectures, label=[f'Lecture {n}' for n in lectures], color=['#00ff1e'] * len(lectures), level=[2]*len(lectures))
        for ctx in occur["contexts"]:
            lecture = f'{ctx["course"]}_{ctx["lecture_num"]}'
            net.add_node(lecture, level=1,color='#00ff1e', size=10)
            # if ctx["course"] not in net:
            net.add_node(ctx["course"], level=0, color='red', size=10)
            net.add_edge(lecture, occur["text"], title=f"<plaintext style='word-break:break-all;'> {ctx['context']} </plaintext>")
            net.add_edge(ctx["course"], lecture)
    net.show("week08/example.html")

# visualize()