# dependency of lectures based on concepts 
from collections import Counter
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

stops |= {"one", "many", "little", "different", "thing", "two", "theta" , "get",}
# print(stops)
import spacy
nlp = spacy.load("en_core_web_sm")
import re

def n_grams(tokens, n):
    ngrams = []
    for i in range(len(tokens)-n+1):
        _tokens = tokens[i:i+n]

        texts = [t.lemma_ for t in _tokens]
        tt = " ".join(texts)
        if tt[0]=="-" or any(p in tt for p in ",./?';:\""):
            continue
        if not set(texts) & stops and _tokens[-1].pos_ in ["PROPN","NOUN"]:
            ngrams.append(tt)
    return ngrams


def extract_ngrams():
    cn = "CS_410"
    script2course = {}
    fr = open("data/transcriptions2courses-410-c5.txt", 'r', encoding='utf-8')
    # fr = open(f"data/transcriptions2courses_{cn}.txt", 'r', encoding='utf-8')
    for line in fr:
        arr = line.strip().split('\t')
        # script2course[arr[0]] = arr
        script2course[arr[2]] = arr
    fr.close()
    print(len(script2course))

    fr = open("week04/corpus_corrected_410.txt", 'r', encoding='utf-8')
    # fr = open(f"data/course_captions/{cn}", 'r', encoding='utf-8')
    cnt = 0
    bigramCounter = Counter()
    trigramCounter = Counter()
    for line in fr:
        cid, scriptid, text = line.strip().split('\t')
        # scriptid, text = line.strip().split('\t')

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
    concept_list = []

    print(" === bigram examples: ===")
    for k,v in bigramCounter.most_common(100):
        if v > 5:
            concept_list.append([k,v])
        print(k,v)
    print(" === trigram examples: ===")
    for k,v in trigramCounter.most_common(100):
        if v > 10:
            concept_list.append([k,v])
        print(k,v)
    with open(f"week09/{cn}_concepts.txt", 'w', encoding='utf-8') as f:
        for k,v in concept_list:
            f.write(f"{k} {v}\n")
            
extract_ngrams()


def find_contexts(text, target, window=300):
    matches = re.finditer(target, text)
    matches_positions = [match.start() for match in matches]
    contexts = []
    for p in matches_positions:
        cstart = p-int(window/2) if p-int(window/2)>0 else 0
        cend = p+len(target)+int(window/2) if p+len(target)+int(window/2)<len(text) else len(text) 
        contexts.append(text[cstart:cend])
    return contexts


def curate_meta_data_for_course():
    dept = "CS"
    cn = "241"
    fr = open("data/transcriptions2courses-2021-09-24.csv", 'r', encoding='utf-8')
    data = []
    for line in fr:
        arr = line.strip().split('\t')
        if arr[6] == dept and arr[7] == cn and arr[4].startswith("CS241-Lec"): # only for CS 241
            data.append(line)
    fr.close()
    fw = open(f"data/transcriptions2courses_{dept}_{cn}.txt", 'w', encoding='utf-8')
    for line in data:
        fw.write(line)
    fw.close()
# curate_meta_data_for_course()


import json
def extract_occurences(cn):
    fr = open(f"week09/{cn}_concepts.txt", 'r', encoding='utf-8')
    concept_list = [" ".join(line.split()[:-1]) for line in fr]
    fr.close()
    script2course = {}
    # fr = open("data/transcriptions2courses-410-c5.txt", 'r', encoding='utf-8')
    fr = open(f"data/transcriptions2courses_{cn}.txt", 'r', encoding='utf-8')
    for line in fr:
        arr = line.strip().split('\t')
        script2course[arr[0]] = arr
    fr.close()
    print("script2course size", len(script2course))

    fr = open(f"data/course_captions/{cn}", 'r', encoding='utf-8')
    occr_list = []
    script_data = fr.readlines()
    fr.close()
    for target in concept_list:
        cnt = 0
        bigramCounter = Counter()
        trigramCounter = Counter()
        occurence = {
            "text": target,
            "contexts": [],
        }
        ctxs = []
        
        for line in script_data:
            scriptid, text = line.strip().split('\t') # NOT FOR CS 410
            if scriptid not in script2course:
                # print("啊？")
                continue
            text = text.lower() # filtering
            # extract concepts
            if target in text:
                contexts = find_contexts(text, target)
                for c in contexts:
                    tmp_ctx = {
                        "course": cn, 
                        "transcription": scriptid,
                        "lecture": script2course[scriptid][6],
                        # "lecture_num": int(script2course[scriptid][6].split()[1]),
                        "lecture_num": int(script2course[scriptid][4].split('-')[1][-2:]), # only for CS 
                        "context": c,
                        "label": "",
                    }    
                    ctxs.append(tmp_ctx)
        print(target, len(ctxs))
        occurence["contexts"] = sorted(ctxs, key=lambda x: x["lecture_num"])
        occr_list.append(occurence)
    fw = open(f"week09/contexts_{cn}.json", 'w')
    tmp = json.dumps(occr_list, indent=2)
    fw.write(tmp)
    fw.close()

# extract_occurences("CS_241")



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