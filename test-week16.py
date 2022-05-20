
import re

import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher 
from spacy.tokens import Span
import pandas as pd

import re
import pandas as pd
import bs4
import requests
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

from spacy.matcher import Matcher 
from spacy.tokens import Span 

import networkx as nx

import matplotlib.pyplot as plt
from tqdm import tqdm

pd.set_option('display.max_colwidth', 200)


def get_entities(sent):
  ## chunk 1
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""

  #############################################################
  
  for tok in nlp(sent):
    ## chunk 2
    # if token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":
      # check: token is a compound word or not
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      ## chunk 3
      if tok.dep_.find("subj") and tok.pos_ == "NOUN" and ( not tok.is_stop):
        ent1 = modifier +" "+ prefix + " "+ tok.text
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      ## chunk 4
      if tok.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ tok.text
        
      ## chunk 5  
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text
  #############################################################

  return [ent1.strip(), ent2.strip()]

def get_relation(sent):

    doc = nlp(sent)

    # Matcher class object 
    matcher = Matcher(nlp.vocab)

    #define the pattern 
    pattern = [{'DEP':'ROOT', 'POS': 'AUX'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}] 


    matcher.add("matching_1", [pattern]) 

    matches = matcher(doc)
    if len(matches) == 0:
        return ""
    k = len(matches) - 1
    span = doc[matches[k][1]:matches[k][2]]

    return(span.text)


def match_patterns(text):
    patterns = [
        r"[A-Z].*?(is|are) called (a|an|the).*?\.", 
        r"\..*? defined as .*?\.",
        r"[Aa]n? [a-zA-Z]{0,20} [a-zA-Z]{0,20} [a-zA-Z]{0,20} is an? .*?\.",
        r"[Aa]n? [a-zA-Z]{0,20} [a-zA-Z]{0,20} is an? .*?\.",
        r"[Aa]n? [a-zA-Z]{0,20} is an? .*?\.",
        r"[Aa]n? [a-zA-Z]{0,20} is an? .*?\.",
        r"[[A-Z]{0,20} is an? .*?\."
                ]
    for pattern in patterns:
        if re.search(pattern, text):
            return True
from collections import Counter     

def clean_text(text):
    # if text.startswith("//"):
    #     return ""
    if "//" in text:
        return ""
    text = text.strip().lower()
    text = text.replace("•", "")
    text = " ".join(text.split(' '))
    return text

def sentence_selection():
    texts = []
    with open("data/QG-CS241/CS241_textbook_clean.txt") as f:
        for line in f:
            text = clean_text(line)
            if text != "":
                texts.append(text)

    matched_sentences = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "DET", "OP":"?"}, {"POS": "NOUN", "OP": "+"}, {"POS": "AUX"}, {"POS": "DET"}]
    matcher.add("definition", [pattern])
    sources = [] # concept spans
    start_indexes = []
    
    matched_concepts = Counter()
    for line in texts:
        if line[0].isdigit():
            continue
        sentences = [i.text for i in nlp(line).sents]
        for sent in sentences:
            if match_patterns(sent):
                # print(sent)
                s = nlp(sent)
                matches = matcher(s)
                if len(matches) == 0:
                    break
                noun_spans = []
                max_noun_span_len = 0
                for match_id, start, end in matches:
                    # string_id = nlp.vocab.strings[match_id]  # Get string representation
                    # span = s[start:end]  # The matched span
                    # print(span.text)
                    if end - start > max_noun_span_len:
                        max_noun_span_len = end - start
                        noun_span = s[start:end-2].text
                noun_spans.append(noun_span)
                matched_concepts[noun_span] += 1

                for pt in noun_spans:
                    start = sent.find(pt)
                    if start==-1:
                        continue
                    sources.append(noun_span)
                    matched_sentences.append(sent)
                    start_indexes.append(start)
                    break
    for k,v in matched_concepts.most_common():
        print(k,v)
    with open("week16/extracted_sentences.txt",'w') as f:
        f.write("sentence\tsource\tstart\n")
        for i in range(len(sources)):
            f.write(f"{matched_sentences[i]}\t{sources[i]}\t{start_indexes[i]}\n")

# sentence_selection()

def convert_dataset():
    fr = open("week16/extracted_sentences.txt", 'r')
    lines = fr.readlines()[1:]
    fr.close()

    fw = open("week16/cs241_tb_for_e2e_qg.source", 'w')

    for line in lines:
        arr = line.strip().split('\t')
        start = int(arr[2])
        end = int(arr[2]) + len(arr[1])
        # text = f"generate question: {arr[0][:start]} <hl> {arr[1]} <hl> {arr[0][end:]}\n"
        text = arr[0] + '\n'
        fw.write(text)
    fw.close()
# convert_dataset()


def match_captions():
    fr = open("week16/extracted_sentences.txt", 'r')
    lines = fr.readlines()[1:]
    fr.close()
    concepts = [line.split('\t')[1] for line in lines]
    concepts = set(concepts)
    print(len(concepts))
    # load caption corpus
    texts = []
    with open("week12/combined_captions_CS_241.csv", 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            text = clean_text(arr[5])
            texts.append(text)
    # # match occurences
    # contexts = []
    # for line in texts:
    #     for c in concepts:
    #         if c in line:
    #             start = line.find(c)
    #             contexts.append(line)
    #             break

    # with open("week16/cs241_ct_for_e2e_qg.source",'w') as f:
    #     for line in contexts:
    #         f.write(f"{line}\n")

    # print(len(contexts))

    # contexts = []
    # for line in texts:
    #     for c in concepts:
    #         if c in line:
    #             start = line.find(c)
    #             contexts.append([line, c, start])

    # with open("week16/extracted_sentences_captions.txt",'w') as f:
    #     f.write("sentence\tsource\tstart\n")
    #     for arr in contexts:
    #         f.write(f"{arr[0]}\t{arr[1]}\t{arr[2]}\n")
    # print(len(contexts))
match_captions()


def expand_contexts():
    fr = open("week16/extracted_sentences.txt", 'r')
    lines = fr.readlines()[1:]
    fr.close()
    concepts = [line.split('\t')[1] for line in lines]
    concepts = set(concepts)
    
    # load textbook corpus
    texts = []
    with open("data/QG-CS241/CS241_textbook_clean.txt") as f:
        for line in f:
            text = clean_text(line)
            if text != "":
                texts.append(text)
    

    # match occurences
    contexts = []
    for line in texts:
        for c in concepts:
            if c in line:
                start = line.find(c)
                contexts.append([line, c, start])

    with open("week16/extracted_sentences_expanded.txt",'w') as f:
        f.write("sentence\tsource\tstart\n")
        for arr in contexts:
            f.write(f"{arr[0]}\t{arr[1]}\t{arr[2]}\n")

    print(len(contexts))

# expand_contexts()
    