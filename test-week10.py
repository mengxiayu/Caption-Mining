'''
1. match caption concepts with ocr concepts
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
df = pandas.read_csv("data/transcriptions2courses-410.txt", sep='\t')
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
            phrases.extend([x.lower() for x in scene["phrases"]])
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

def relabel_contexts():
    vid2phrases = read_ocr_data()
    tid2phrases, phrases2contexts = read_caption_data("week09/contexts_CS_410.json")
    new_data = []
    for phrase, contexts in phrases2contexts.items():
        for cxt in contexts:
            tid = cxt["transcription"]
            vid = transcript2video[tid]
            lecture_name_str = cxt["lecture"].lower().replace("  ", " ")
            if phrase in vid2phrases[vid] or phrase in lecture_name_str:
                print(cxt["context"])
                cxt["label"] = "intro"
            else:
                cxt["label"] = "use"     

        new_data.append({
            "text":phrase,
            "contexts":contexts
        })
    new_data_str = json.dumps(new_data, indent=2)
    with open ("week10/contexts_CS_410.json", 'w', encoding='utf-8') as f:
        f.write(new_data_str)

# relabel_contexts()  

def lecture_statistics():
    vid2phrases = read_ocr_data()
    tid2phrases, phrases2contexts = read_caption_data()
    fw = open("week10/lecture_concepts.csv", 'w', encoding='utf-8')
    fw.write(f"transcriptionid\tvideoid\tphrases_both\tphrases_caption\tphrases_video\n")
    for tid, tphrases in tid2phrases.items():
        if tid in transcript2video:
            vid = transcript2video[tid]
            # print("=== in video ===")
            # print(vid2phrases[vid])
            # print("=== in caption ===")
            # print(tphrases)
            phrases_in_both = vid2phrases[vid] & tphrases
            phrases_in_caption = tphrases - vid2phrases[vid]
            phrases_in_video = vid2phrases[vid] - tphrases
            phrases_in_both = ", ".join(list(phrases_in_both))
            phrases_in_caption = ", ".join(list(phrases_in_caption))
            phrases_in_video = ", ".join(list(phrases_in_video))
            fw.write(f"{tid}\t{vid}\t{phrases_in_both}\t{phrases_in_caption}\t{phrases_in_video}\n")
        else:
            print("video not exist")

lecture_statistics()

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
def draw_phrases_heatmap():
    tid2phrases, phrases2contexts = read_caption_data("week10/contexts_CS_410.json")
    tid2lect = {}
    for phrase, contexts in phrases2contexts.items():
        for cxt in contexts:
            tid2lect[cxt['transcription']] = cxt['lecture_num']
    n_lectures = max(tid2lect.values())
    n_phrases = len(phrases2contexts)
    print(n_lectures,n_phrases)
    map = np.zeros((n_phrases, n_lectures))
    ylabels = []
    xlabels = [f'L{x}' for x in range(1,n_lectures+1)]
    for idx,(phrase, contexts) in enumerate(phrases2contexts.items()):
        ylabels.append(phrase)
        for ctx in contexts:
            if ctx["label"] == "intro":
                map[idx, ctx["lecture_num"]-1] = 2
            else:
                map[idx, ctx["lecture_num"]-1] = 1
    # plt.imshow(map, cmap='hot', interpolation='nearest')
    
    ax = sns.heatmap(map, linewidth=0.1, xticklabels=xlabels, yticklabels=ylabels, cmap="YlGnBu")
    plt.show()
# draw_phrases_heatmap()