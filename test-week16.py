
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
    # doc = nlp(sent)

    # # Matcher class object 
    # matcher = Matcher(nlp.vocab)
    # pattern = [
    #     {"IS_ALPHA": True, "POS": "NOUN"},
    #     {"POS":"AUX",}
    # ] 


    # matcher.add("matching_1", [pattern]) 

    # matches = matcher(doc)
    # k = len(matches) - 1
    # span = doc[matches[k][1]:matches[k][2]]
from collections import Counter     

entity_pairs = []
relations = []
def sentence_selection():
    texts = []
    with open("data/QG-CS241/CS241_textbook_clean.txt") as f:
        for line in f:
            texts.append(line.strip().lower())

    # word2freq = Counter()
    # noun2freq = Counter()
    # for line in texts:
    #     doc = nlp(line)
    #     words = [token.text
    #             for token in doc
    #             if not token.is_stop and not token.is_punct]
    #     nouns = [token.text
    #             for token in doc
    #             if (not token.is_stop and
    #                 not token.is_punct and
    #                 token.pos_ == "NOUN")]
    #     word2freq.update(words)
    #     noun2freq.update(nouns)
    # with open("week16/cs241_textbook_wordfreq.txt", 'w') as f:
    #     for k,v in word2freq.most_common():
    #         f.write(f"{k} {v}\n")
    # with open("week16/cs241_textbook_nounfreq.txt", 'w') as f:
    #     for k,v in noun2freq.most_common():
    #         f.write(f"{k} {v}\n")
    matched_sentences = []

    sources = []
    start_indexes = []
    for line in texts:
        if line[0].isdigit():
            continue
        sentences = [i.text for i in nlp(line).sents]
        for sent in sentences:
            if match_patterns(sent):
                for pt in ["is an", "is a"]:
                    
                    start = sent.find(pt)
                    if start==-1:
                        continue
                    front_text = sent[:start]
                    if front_text.split()[-1] in ["this", "that", "here", "here", "it","there","where","below"]:
                        continue
                    sources.append(front_text)
                    matched_sentences.append(sent)
                    start_indexes.append(start)
                    break
        
    with open("week16/extracted_sentences_1.txt",'w') as f:
        f.write("sentence\tsource\tstart\n")
        for i in range(len(sources)):
            f.write(f"{matched_sentences[i]}\t{sources[i]}\t{start_indexes[i]}\n")


                # rel = get_relation(sent)
                # ent1, ent2 = get_entities(sent)
                # if rel != "" and ent1 !="" and ent2 != "":
                #     entity_pairs.append([ent1, ent2])
                #     relations.append(rel)
                #     matched_sentences.append(sent)

    # print(len(matched_sentences))
    # # for s in matched_sentences:
    # #     print(s)

    # source = [i[0] for i in entity_pairs]
    # # extract object
    # target = [i[1] for i in entity_pairs]
    # with open("week16/extracted_sentences.txt",'w') as f:
    #     f.write("sentence\tsource\target\trelation\n")
    #     for i in range(len(source)):
    #         f.write(f"{matched_sentences[i]}\t{source[i]}\t{target[i]}\t{relations[i]}\n")

    # kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})

    # # create a directed-graph from a dataframe
    # G=nx.from_pandas_edgelist(
    #         kg_df[kg_df['edge']=="is"], "source", "target", 
    #         edge_attr=True, create_using=nx.MultiDiGraph())
    # plt.figure(figsize=(12,12))

    # pos = nx.spring_layout(G, k=0.5)
    # nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
    # plt.show()


sentence_selection()




# with open("data/transcriptions2courses_CS_241.txt") as f:
#     videos = set()
#     captionids = set()
#     for line in f:
#         arr = line.strip().split('\t')
#         if arr[1] not in videos:    
#             videos.add(arr[1])
#             captionids.add(arr[0])
#     print(len(videos))

# with open("data/allcaptions_CS_241.csv") as f:
#     for line in f:
#         arr = line.strip()
        
