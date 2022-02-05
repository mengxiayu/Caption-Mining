
# discover noun multi-grams
def _read_voab():
    fr = open("week07/vocab.txt", 'r', encoding='utf-8')
    word2freq = {}
    word2df = {}
    for line in fr:
        arr = line.strip().split('\t')
        word2freq[arr[0]] = int(arr[1])
        word2df[arr[0]] = int(arr[2])
    fr.close()
    return word2freq, word2df

def discover_noun_multi_grams(tokens, word2freq):
    # tokens is a list of parsed token
    rlt = []
    i = 0
    tmp = ""
    last = ""
    while i < len(tokens):
        _token = tokens[i].split('::')
        # print(_token)
        if len(_token) != 9:
            i += 1
            continue
        if _token[1] not in word2freq or word2freq[_token[1]] < 3:
            i += 1
            continue
        if _token[2] in ["PROPN","NOUN"] and _token[1] != last: # avoid "vector vector"
            tmp += ' ' + _token[1]
            last = _token[1]
        else:
            if tmp.count(' ') > 1: # only need multi-grams
                multigram = tmp.strip().lower()
                rlt.append(multigram)
            tmp = ""
            last = ""
        i += 1
    return rlt

def _load_wiki_set():
    fr = open("week07/wiki_all.txt", 'r', encoding='utf-8')
    terms = [line.strip() for line in fr]
    fr.close()
    return set(terms)
from collections import Counter

import os
def discover_concepts(cn):
    fr = open("data/course_captions_parsed/"+cn, 'r', encoding='utf-8')
    all_noun_multi_grams = set()
    multigram2freq = Counter()
    all_lectures = []
    wiki_set = _load_wiki_set()
    word2freq, word2df =  _read_voab()
    trancripid2lectid = {}
    # write lecture files
    for line in fr:
        arr = line.strip().split('\t')
        trancripid2lectid[arr[0]] = f"{cn}-{len(trancripid2lectid)}"
        all_lectures.append(trancripid2lectid[arr[0]])
        tokens = arr[1].split(' ')
        noun_multi_grams = discover_noun_multi_grams(tokens, word2freq)
        multigram2freq.update(noun_multi_grams)
        noun_multi_grams_set = set(noun_multi_grams)
        # all_noun_multi_grams |= noun_multi_grams_set
        tgt_dir = "week07/course_concepts/"+cn+'/'
        if not os.path.exists(tgt_dir):
            os.makedirs(tgt_dir)
        fw = open(tgt_dir+trancripid2lectid[arr[0]]+".md", 'w', encoding='utf-8')
        fw.write(f"#{cn}\n")
        fw.write("#lecture\n")
        for noun in noun_multi_grams_set:
            fw.write("[[" + noun + "]]\n") # create a link
        fw.close()
    fr.close()
    fw = open("week07/course_concepts/"+cn+"/statistics.txt",'w',encoding='utf-8')
    for k,v in multigram2freq.most_common():
        fw.write(f"{k}\t{v}\n")
    fw.close()
    # write concept files
    for noun, freq in multigram2freq.items():
        if '/' not in noun and freq > 2: # frequency filtering
        # if noun in wiki_set: # wiki filtering
            concept_fn = "week07/course_concepts/concepts/"+noun+".md"
            if os.path.exists(concept_fn):
                continue
            fw = open(concept_fn, 'w', encoding='utf-8')
            fw.write("#concept\n")
            fw.close()
    '''
    '''
    # wirte course files
    fw = open("week07/course_concepts/"+cn+".md", 'w', encoding='utf-8')
    fw.write("#course\n")
    for lect in all_lectures:
        fw.write("[["+lect+"]]\n")
    for noun, freq in multigram2freq.items():
        if '/' not in noun and freq > 2: # frequency filtering
            fw.write("[["+noun+"]]\n")

    fw.close()

# discover_concepts("CS_410")
# discover_concepts("CS_447")
# discover_concepts("ECE_448")
# discover_concepts("CS_361")
# discover_concepts("STAT_432")
discover_concepts("CS_446")


# discover_concepts("CS_357")



