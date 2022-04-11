'''
clean BUSiness data for question generation.
'''

import json

def clean_textbook():
    fn_textbook = "data/BUS-QG/BUSN_textbook.txt"
    with open(fn_textbook, 'r', encoding='utf-8') as f:
        all_lines = [x.strip() for x in f.readlines()]
    print("original lines number", len(all_lines))
    # concatenate lines which should be continuous. blank lines reserved.
    # TODO should replace some characters, such as \u2019
    new_lines = [] # 
    tmp_line = all_lines[0]
    for line in all_lines[1:]:
        if line == "":
            new_lines.append(tmp_line)
            tmp_line = line
            continue
        if tmp_line == "":
            new_lines.append(tmp_line)
            tmp_line = line
            continue
        if line[0].isalpha() and line[0].islower():
            tmp_line += " " + line
            continue
    print("new line number", len(new_lines))
    # remove empty lines
    new_lines = [x for x in new_lines if x!=""]

    print("new line number", len(new_lines))
    with open("data/BUS-QG/BUSN_textbook_clean.txt", 'w', encoding='utf-8') as f:
        for line in new_lines:
            f.write(line+'\n')
    print("clean textbook saved")
    # NOTE after this, I manually seperate the textbook into 4 parts: preface, clean, endnotes, and glossary
# clean_textbook()

import spacy
nlp = spacy.load("en_core_web_sm")
def process_corpus():
    fn_textbook = "data/BUS-QG/BUSN_textbook_clean.txt"
    with open(fn_textbook, 'r', encoding='utf-8') as f:
        all_lines_textbook = [x.strip() for x in f.readlines()]
    def preprocess_corpus(all_lines):
        lines = []
        processed_lines = []
        for line in all_lines:
            if len(line) < 100:
                continue
            line = line.replace("’", "'") # \u2019
            doc = nlp(line)
            lines.append(line)
            processed_lines.append(' '.join([t.text.lower() for t in doc]))
        return lines, processed_lines
    lines, processed_lines = preprocess_corpus(all_lines_textbook)
    
    with open("data/BUS-QG/BUSN_textbook_corpus.tsv", 'w', encoding='utf-8') as f:
        f.write("Line\tProcessed_line\n")
        for line, processed_line in zip(lines, processed_lines):
            f.write(line+'\t'+processed_line+'\n')
    print("corpus saved")
process_corpus()

from rank_bm25 import BM25Okapi
def extract_contexts():
    with open("data/BUS-QG/BUSN_textbook_corpus.tsv", 'r', encoding='utf-8') as f:
        corpus = []
        for line in f:
            arr = line.strip().split('\t')
            corpus.append(arr[1])

    tokenized_corpus = [doc.split() for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)

    with open("data/BUS-QG/BUS_Chapter_Review_Questions.json", 'r', encoding='utf-8') as f:
        question_data = json.loads(f.read())
    queries = []
    for data in question_data:
        answer = data["answers"][0][3:]
        # print(answer)
        doc = nlp(answer)
        query = [t.text.lower() for t in doc]
        contexts = bm25.get_top_n(query, corpus, n=5)
        # print(contexts)
        data["contexts"] = contexts
    with open("data/BUS-QG/BUS_Chapter_Review_Questions_extracted_contexts.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(question_data, indent=2, ensure_ascii=False)) # allow unicode
        print("extracted data dumped")
extract_contexts()