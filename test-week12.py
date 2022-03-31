# process captions with timestamps
# get a subset of allcaptions of cs410
import pandas as pd

def extract_course_allcaptions():
    df = pd.read_csv("data/transcriptions2courses-410-c5.txt", sep='\t')
    all_tid = df["transcriptionid"].tolist()
    print(f"all: {len(all_tid)}, unique: {len(set(all_tid))}")
    course_tid = set(all_tid)

    course_data = []
    with open ("data/allcaptions-2021-09-24.csv", 'r', encoding='utf-8') as f:
        for line in f:
            arr = line.split('\t')
            if arr[0] in course_tid:
                course_data.append(line)
    print(f"course data size: {len(course_data)}")
    with open("data/allcaptions_410-c5.csv", 'w', encoding='utf-8') as f:
        for line in course_data:
            f.write(line)

    print("course data written.")

# extract_course_allcaptions()


import datetime
import spacy
nlp = spacy.load("en_core_web_sm")
def combine_captions():
    def str2date(s):
        y,m,d = [int(x) for x in s.split('-')] 
        return datetime.date(y,m,d)
    tid2segid2data = {}
    with open ("data/allcaptions_410-c5.csv", 'r', encoding='utf-8') as f:
        for line in f:
            arr = line.strip().split('\t')
            tid = arr[0]
            seg_idx = arr[2]
            if tid not in tid2segid2data:
                tid2segid2data[tid] = {}
            if seg_idx not in tid2segid2data[tid]:
                tid2segid2data[tid][seg_idx] = arr
            else:
                existing_data = tid2segid2data[tid][seg_idx]
                existing_date = str2date(existing_data[1].split(' ')[0])
                current_date = str2date(arr[1].split(' ')[0])
                if existing_date < current_date:
                    tid2segid2data[tid][seg_idx] = arr # adopt the later version
    def combine_continuous_data(d1, d2):
        assert d1[0] == d2[0] and int(d1[2])+1 == int(d2[2])
        new_data = [None] * 6
        new_data[0] = d2[0]
        new_data[1] = d2[1]
        new_data[2] = d2[2]
        new_data[3] = d1[3]
        new_data[4] = d2[4]
        new_data[5] = d1[5] + " " + d2[5]
        return new_data
    new_all_data = []
    for tid, segid2data in tid2segid2data.items():
        print("original data size", len(segid2data))
        tmp_new_all_data = []
        tmp_data = []
        for segid, data in segid2data.items():
            if tmp_data == []:
                tmp_data = data
                continue
            if (data[3].split('.')[0] == tmp_data[4].split('.')[0]) or (tmp_data[5][-1] not in ['.', '?'] and data[5][0].islower()): # continuous in time or continuous in text
                tmp_data = combine_continuous_data(tmp_data, data)
                continue
            tmp_new_all_data.append(tmp_data)
            tmp_data = data
        new_all_data.extend(tmp_new_all_data)
        print("new data size", len(tmp_new_all_data))
    with open("week12/combined_captions_410_c5.csv", 'w', encoding='utf-8') as f:
        for data in new_all_data:
            text = data[5]
            lemmatized_text = " ".join([t.lemma_ for t in nlp(text)])
            data.append(lemmatized_text)
            f.write("\t".join(data)+'\n')

# combine_captions()

from datetime import datetime
from datetime import timedelta
import re
import json
def data2time(arr):
    return datetime.strptime(arr[4].split('.')[0], "%H:%M:%S")

def analyse_information_flow():
    # duration 1 min
    # slide 30 sec   
    all_phrases = set()
    with open("week09/CS_410_concepts_all.txt", 'r') as f:
        for line in f:
            phrase = line.strip().split(' ')[:-1]
            phrase = ' '.join(phrase)
            all_phrases.add(phrase)
    print("all phrase size", len(all_phrases))
    tid2data = {}
    with open("week12/combined_captions_410_c5.csv", 'r', encoding='utf-8') as f:
        for line in f:
            arr = line.strip().split('\t')
            tid = arr[0]
            if tid not in tid2data:
                tid2data[tid] = []
            tid2data[tid].append(arr)
    print("all lecture size", len(tid2data))

    tid2phraseswindow = {} # show phrases density via sliding window
    tid2textwindow = {}   
    for tid, data in tid2data.items():
        window_end = datetime.strptime("00:01:00","%H:%M:%S")
        delta = timedelta(seconds=30)
        text_windows = []
        current_window = []
        for arr in data:
            if current_window == []:
                current_window.append(arr)
                continue
            if data2time(current_window[-1])<window_end:
                current_window.append(arr)
                continue
            alltext = " ".join([x[6].lower() for x in current_window])
            text_windows.append(alltext)
            window_end += delta
            current_window = []
        tid2textwindow[tid] = text_windows
        print("analysing lecure", tid)
        phrases_windows = []
        for window in text_windows:
            tmp_phrases = []
            for phrase in all_phrases:
                if len(re.findall(phrase, window)) >= 2:
                    tmp_phrases.append(phrase)
            phrases_windows.append(tmp_phrases)
        tid2phraseswindow[tid] = phrases_windows
    with open("week12/tid2textwindow.json", 'w', encoding='utf-8') as f:
        json.dump(tid2textwindow, f, indent=2)
    with open("week12/tid2phrasewindow.json", 'w', encoding='utf-8') as f:
        json.dump(tid2phraseswindow, f, indent=2)
    
# analyse_information_flow()

def phrase_density():
    tid2lect = {}
    with open("data/transcriptions2courses-410-c5.txt", 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            tid2lect[arr[2]] = arr[6]
    tid2textwindow = json.load(open("week12/tid2textwindow.json", 'r'))
    tid2phraseswindow = json.load(open("week12/tid2phrasewindow.json", 'r'))
    fw = open("week12/phrase_flow_nonzero.txt", 'w')
    all_phrases = set()
    for tid, pwindows in tid2phraseswindow.items():
        for w in pwindows:
            for p in w:
                all_phrases.add(p)
    for tid, text_windows in sorted(tid2textwindow.items(), key=lambda x:int(tid2lect[x[0]].split(' ')[1])):
        fw.write(f"{tid}\t{tid2lect[tid]}\n")
        pwindows = tid2phraseswindow[tid]
        # Choice 1
        # phrases = set()
        # for w in pwindows:
        #     for p in w:
        #         phrases.add(p)
        # Choice 2
        phrases = all_phrases
        for phrase in phrases:
            phrase_freq_flow = []
            at_least_one = False
            for window in text_windows:
                freq = len(re.findall(phrase, window))
                if freq > 0:
                    at_least_one = True
                phrase_freq_flow.append(str(freq))
            tmp = '\t'.join(phrase_freq_flow)
            if at_least_one:
                fw.write(f"{phrase}\t{tmp}\n")
    fw.close()
phrase_density()
                
            





    
            