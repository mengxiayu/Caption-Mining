'''
1. match caption concepts with ocr concepts

week 10: use OCR "phrases"
week 11: use OCR "title"
'''
import json

import pandas


# load caption concepts list
# fr = open("week09/CS_410_concepts.txt", 'r', encoding='utf-8')
# caption_concepts = []
# for line in fr:
#     caption_concepts.append(" ".join(line.strip().split()[:-1]))
# fr.close()
# print(caption_concepts)

# a caption id to video id mapping
df = pandas.read_csv("data/transcriptions2courses_CS_241.txt", sep='\t')
transcript2video = {}
video2transcript = {}
for idx, row in df.iterrows():
    tid = row["transcriptionid"]
    vid = row["videoid"]
    transcript2video[tid] = vid
    video2transcript[vid] = tid


from nltk.corpus import stopwords
stops = set(stopwords.words('english'))
stops |= {"zhai", "chengxiang", "illinois","university","science", "every", "per", "x", "k", "p", "v", "n", "et", "al", "many"}
import spacy
nlp = spacy.load("en_core_web_sm")

def n_grams(tokens, n):
    ngrams = []
    for i in range(len(tokens)-n+1):
        _tokens = tokens[i:i+n]
        texts = [t.lemma_ for t in _tokens]
        tt = " ".join(texts)
        if not tt[0].isalpha() or not tt[-1].isalpha() or any(p in tt for p in ",./?';+:()\"=]["):
            continue
        if not set(texts) & stops and _tokens[-1].pos_ in ["PROPN","NOUN"] and _tokens[0].pos_ not in ["VERB"] :
            ngrams.append(tt)
    return ngrams

def clean_ocr_phrases(text_list):
    text = " , ".join(text_list)
    text = text.replace("-", ",")
    tokens = nlp(text)
    bigrams = n_grams(tokens, 2)
    trigrams = n_grams(tokens, 3)
    return set(bigrams + trigrams)


def read_ocr_data():
    df = pandas.read_csv("data/CS410-OCRdata-2021-11-18.csv")
    vid2phrases = {}
    for idx, row in df.iterrows():
        scene_data = json.loads(row['SceneData'])
        # print(len(scene_data["Scenes"]))
        # print(scene_data["Scenes"][0].keys()) # dict_keys(['frame_start', 'frame_end', 'start', 'end', 'img_file', 'raw_text', 'phrases', 'title'])
        phrases = []
        for scene in scene_data["Scenes"]:
            # phrases.extend([x.lower() for x in scene["phrases"]])
            phrases.append(scene["title"].lower())
        phrases = clean_ocr_phrases(phrases)
        vid2phrases[row["Id"]] = phrases
    return vid2phrases

# load caption contexts
def read_caption_data(fn):
    fr = open(fn, 'r', encoding='utf-8')
    data = json.loads(fr.read())
    fr.close()
    tid2phrases = {}
    phrases2contexts = {}
    for line in data:
        concept = line["text"]
        contexts = line["contexts"]
        phrases2contexts[concept] = contexts
        for context in contexts:
            tid = context["transcription"]
            if tid not in tid2phrases:
                tid2phrases[tid] = set()
            tid2phrases[tid].add(concept)
            # vid = transcript2video[tid]
            # if vid in vid2phrases:
            #     print("in video:", vid2phrases[vid])
            #     print("in caption:", concept)

    return tid2phrases, phrases2contexts

def lecture_statistics():
    vid2phrases = read_ocr_data()
    tid2phrases, phrases2contexts = read_caption_data("week11/contexts_CS_241.json")
    fw = open("week11/lecture_concepts_CS_241.csv", 'w', encoding='utf-8')
    fw.write(f"transcriptionid\tvideoid\tphrases_both\tphrases_caption\tphrases_video\n")
    for tid, tphrases in tid2phrases.items():
        if tid in transcript2video:
            vid = transcript2video[tid]
            # print("=== in video ===")
            # print(vid2phrases[vid])
            # print("=== in caption ===")
            # print(tphrases)
            vphrases = vid2phrases[vid] if vid in vid2phrases else set()
            phrases_in_both = vphrases & tphrases
            phrases_in_caption = tphrases - vphrases
            phrases_in_video = vphrases - tphrases
            phrases_in_both = ", ".join(list(phrases_in_both))
            phrases_in_caption = ", ".join(list(phrases_in_caption))
            phrases_in_video = ", ".join(list(phrases_in_video))
            fw.write(f"{tid}\t{vid}\t{phrases_in_both}\t{phrases_in_caption}\t{phrases_in_video}\n")
        else:
            print("video not exist")

lecture_statistics()


def relabel_contexts():
    vid2phrases = read_ocr_data()
    tid2phrases, phrases2contexts = read_caption_data("week09/contexts_CS_241.json")
    new_data = []
    for phrase, contexts in phrases2contexts.items():
        for cxt in contexts:
            tid = cxt["transcription"]
            vid = transcript2video[tid]
            lecture_name_str = cxt["lecture"].lower().replace("  ", " ")
            if vid in vid2phrases:
                if phrase in vid2phrases[vid] or phrase in lecture_name_str:
                    print(cxt["context"])
                    cxt["label"] = "intro"
                else:
                    cxt["label"] = "use"    
            else:
                cxt["label"] = ""

        new_data.append({
            "text":phrase,
            "contexts":contexts
        })
    new_data_str = json.dumps(new_data, indent=2)
    with open ("week11/contexts_CS_241.json", 'w', encoding='utf-8') as f:
        f.write(new_data_str)

# relabel_contexts()  


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


## week 11
def draw_phrases_heatmap():
    tid2phrases, phrases2contexts = read_caption_data("week11/contexts_CS_410.json")
    tid2lect = {}
    for phrase, contexts in phrases2contexts.items():
        for cxt in contexts:
            tid2lect[cxt['transcription']] = cxt['lecture_num']
    df = pandas.read_csv("week11/lecture_concepts.csv", sep='\t', keep_default_na=False)
    df.fillna('')
    n_lectures = max(tid2lect.values())
    phrases2labels = {}
    for idx, row in df.iterrows():
        # print(row)
        lectnum = tid2lect[row["transcriptionid"]]
        # both
        if row["phrases_both"]!="":
            phrases_list =[x.strip() for x in row["phrases_both"].split(",")] 
            for p in phrases_list:
                if p not in phrases2labels:
                    phrases2labels[p] = [0] * n_lectures
                phrases2labels[p][lectnum-1] = 3
        # caption
        if row["phrases_caption"]!="":
            phrases_list =[x.strip() for x in row["phrases_caption"].split(",")] 
            for p in phrases_list:
                if p not in phrases2labels:
                    phrases2labels[p] = [0] * n_lectures
                phrases2labels[p][lectnum-1] = 2
        # video
        if row["phrases_video"]!="":
            phrases_list =[x.strip() for x in row["phrases_video"].split(",")] 
            for p in phrases_list:
                if p not in phrases2labels:
                    phrases2labels[p] = [0] * n_lectures
                phrases2labels[p][lectnum-1] = 1
    # print(phrases2labels)
    n_phrases = len(phrases2labels)
    map = []
    
    ylabels = []
    xlabels = [f'L{x}' for x in range(1,n_lectures+1)]
    for idx, (k,v) in enumerate(phrases2labels.items()):
        map.append(v)
        ylabels.append(k)
    map = np.array(map)
    print(map.shape)
    # print(map)
    # print(len(xlabels),xlabels)
    # print(len(ylabels),ylabels)
    ax = sns.heatmap(map, linewidth=0.1, xticklabels=xlabels, yticklabels=ylabels, cmap="YlGnBu")
    plt.show()

# def draw_phrases_heatmap_legacy():
#     tid2phrases, phrases2contexts = read_caption_data("week11/contexts_CS_410.json")
#     tid2lect = {}
#     for phrase, contexts in phrases2contexts.items():
#         for cxt in contexts:
#             tid2lect[cxt['transcription']] = cxt['lecture_num']
#     n_lectures = max(tid2lect.values())
#     n_phrases = len(phrases2contexts)
#     print(n_lectures,n_phrases)
#     map = np.zeros((n_phrases, n_lectures))read_ocr_data
#     ylabels = []
#     xlabels = [f'L{x}' for x in range(1,n_lectures+1)]
#     for idx,(phrase, contexts) in enumerate(phrases2contexts.items()):
#         ylabels.append(phrase)
#         for ctx in contexts:
#             if ctx["label"] == "intro":
#                 map[idx, ctx["lecture_num"]-1] = 2
#             else:
#                 map[idx, ctx["lecture_num"]-1] = 1
#     # plt.imshow(map, cmap='hot', interpolation='nearest')
#     ax = sns.heatmap(map, linewidth=0.1, xticklabels=xlabels, yticklabels=ylabels, cmap="YlGnBu")
#     plt.show()
# draw_phrases_heatmap()

def get_ocr_vocab():
    vid2phrases = read_ocr_data()
    all_phrases = set()
    for vid, phrases in vid2phrases.items():
        all_phrases |= phrases
    with open("week11/CS410_ocr_concepts.txt", 'w', encoding='utf-8') as f:
        for p in all_phrases:
            f.write(p+'\n')
# get_ocr_vocab()
