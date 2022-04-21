# process captions with timestamps
# get a subset of allcaptions of cs241
import json
import re
from datetime import timedelta
from datetime import datetime
from tqdm import tqdm
import spacy
# import datetime
import pandas as pd


def extract_course_allcaptions():
    df = pd.read_csv("data/transcriptions2courses_CS_241.txt", sep='\t')
    all_tid = df["transcriptionid"].tolist()
    print(f"all: {len(all_tid)}, unique: {len(set(all_tid))}")
    course_tid = set(all_tid)

    course_data = []
    with open("data/allcaptions-2021-09-24.csv", 'r', encoding='utf-8') as f:
        for line in f:
            arr = line.split('\t')
            if arr[0] in course_tid:
                # check if the same caption is the same as the last one (for CS241)
                if len(course_data) > 0 and (course_data[-1]).split('\t')[2] == arr[2]:
                    course_data[-1] = line
                else:
                    course_data.append(line)
    print(f"course data size: {len(course_data)}")
    with open("data/allcaptions_241-c5.csv", 'w', encoding='utf-8') as f:
        for line in course_data:
            f.write(line)

    print("course data written.")

# extract_course_allcaptions()


nlp = spacy.load("en_core_web_sm")


def combine_captions():
    def str2date(s):
        y, m, d = [int(x) for x in s.split('-')]
        return datetime.date(y, m, d)
    tid2segid2data = {}
    with open("data/allcaptions_241-c5.csv", 'r', encoding='utf-8') as f:
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
                    # adopt the later version
                    tid2segid2data[tid][seg_idx] = arr

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

            # print(data)
            # print(tmp_data)
            # assert False

            # continuous in time or continuous in text
            # total length not to exceed 20 words
            if ((data[3].split('.')[0] == tmp_data[4].split('.')[0])
                or (tmp_data[5][-1] not in ['.', '?'] and data[5][0].islower())):
                if (len(tmp_data[5].split(' ')) + len(data[5].split(' '))) <= 20:
                    tmp_data = combine_continuous_data(tmp_data, data)
                    continue
                # else:
                #     print("total length exceeds 20 words")
            tmp_new_all_data.append(tmp_data)
            tmp_data = data
        new_all_data.extend(tmp_new_all_data)
        print("new data size", len(tmp_new_all_data))
    with open("week12/combined_captions_241_c5.csv", 'w', encoding='utf-8') as f:
        print("lemmatizing combined captions...")
        for data in tqdm(new_all_data):
            text = data[5]
            lemmatized_text = " ".join([t.lemma_ for t in nlp(text)])
            data.append(lemmatized_text)
            f.write("\t".join(data)+'\n')


# combine_captions()


def data2time(arr):
    return datetime.strptime(arr[4].split('.')[0], "%H:%M:%S")


def analyse_information_flow():
    # duration 1 min
    # slide 30 sec
    all_phrases = set()
    # with open("week09/CS_410_concepts_all.txt", 'r') as f:
    with open("week09/CS_241_concepts.txt", 'r', encoding='utf-8') as f:
        for line in f:
            phrase = line.strip().split(' ')[:-1]
            phrase = ' '.join(phrase)
            all_phrases.add(phrase)
    print("all phrase size", len(all_phrases))
    tid2data = {}
    with open("week12/combined_captions_241_c5.csv", 'r', encoding='utf-8') as f:
        for line in f:
            arr = line.strip().split('\t')
            tid = arr[0]
            if tid not in tid2data:
                tid2data[tid] = []
            tid2data[tid].append(arr)
    print("all lecture size", len(tid2data))

    tid2phraseswindow = {}  # show phrases density via sliding window
    tid2textwindow = {}
    for tid, data in tid2data.items():
        # if tid == '7466bd20-538e-4aeb-b004-1fa8fb518f9f':
        #     print(data)
        window_end = datetime.strptime("00:01:00", "%H:%M:%S")
        # delta = timedelta(seconds=30)
        delta = timedelta(seconds=60)
        text_windows = []
        current_window = []
        for arr in data:
            if current_window == []:
                current_window.append(arr)
                continue
            if data2time(current_window[-1]) < window_end:
                current_window.append(arr)
                continue
            alltext = " ".join([x[6].lower() for x in current_window])
            text_windows.append(alltext)
            window_end += delta
            current_window = []
        tid2textwindow[tid] = text_windows
        # print("analysing lecure", tid)
        phrases_windows = []
        for window in text_windows:
            tmp_phrases = []
            for phrase in all_phrases:
                # if len(re.findall(phrase, window)) >= 2:
                if len(re.findall(phrase, window)) >= 1:
                    tmp_phrases.append(phrase)
            phrases_windows.append(tmp_phrases)
        # todo: add ocr phrases, and both

        tid2phraseswindow[tid] = phrases_windows
    with open("week12/CS410/tid2textwindow.json", 'w', encoding='utf-8') as f:
        json.dump(tid2textwindow, f, indent=2)
    with open("week12/CS410/tid2phrasewindow.json", 'w', encoding='utf-8') as f:
        json.dump(tid2phraseswindow, f, indent=2)

analyse_information_flow()


def phrase_density():
    tid2lect = {}
    # with open("data/transcriptions2courses-241-c5.txt", 'r', encoding='utf8') as f:
    with open("data/transcriptions2courses_CS_241.txt", 'r', encoding='utf8') as f:
        for line in f:
            arr = line.strip().split('\t')
            # tid2lect[arr[2]] = arr[6]
            tid2lect[arr[0]] = arr[4]
    tid2textwindow = json.load(open("week12/CS410/tid2textwindow.json", 'r'))
    tid2phraseswindow = json.load(
        open("week12/CS410/tid2phrasewindow.json", 'r'))
    fw = open("week12/CS410/phrase_flow_nonzero.txt", 'w')
    all_phrases = set()
    for tid, pwindows in tid2phraseswindow.items():
        for w in pwindows:
            for p in w:
                all_phrases.add(p)
    for tid, text_windows in sorted(tid2textwindow.items(), key=lambda x: int(tid2lect[x[0]].split(' ')[1])):
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
# phrase_density()
