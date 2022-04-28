'''
ReadMe:
- should run from root directory

'''

import json

# transform BUS dataset
data_fn = "data/BUS-QG/BUS_Chapter_Review_Questions_extracted_contexts.json"
with open(data_fn, 'r', encoding='utf-8') as f:
    data = json.loads(f.read())


sources = []
targets = []
for d in data:
    source = ""
    question = d["question"]
    question = question.replace("_____", "[BLANK]")
    answer = d["answers"][0][3:]
    distractors = []
    for c in d["candidates"]:
        if c != answer:
            distractors.append(c[3:])
    candidates = f"a. {answer} b. {distractors[0]} c. {distractors[1]} d. {distractors[2]}"
    contexts = d["contexts"]
    source = f"Context: {contexts[0]} Answer: {answer}"
    target = f"Question: {question} Candidates: {candidates}"
    
    sources.append(source)
    targets.append(target)

import random
random.seed(7)
tmp = list(zip(sources, targets))
random.shuffle(tmp)
train_src, train_tgt = zip(*tmp[:200])
val_src, val_tgt = zip(*tmp[200:])

new_data_dir = "QuestionGeneration/data/bus_240/"
with open(new_data_dir+"train.source", 'w', encoding='utf-8') as f:
    for line in train_src:
        f.write(line+'\n')
with open(new_data_dir+"train.target", 'w', encoding='utf-8') as f:
    for line in train_tgt:
        f.write(line+'\n')

with open(new_data_dir+"val.source", 'w', encoding='utf-8') as f:
    for line in val_src:
        f.write(line+'\n')
with open(new_data_dir+"val.target", 'w', encoding='utf-8') as f:
    for line in val_tgt:
        f.write(line+'\n')

    