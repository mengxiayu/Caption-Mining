'''
clean data for CS241 question generation
- textbook data
- quiz data
'''
import re
def parse_question_data(idx, lines):
    question_data = {}
    question_data["chapter"] = ""
    question_data["idx"] = idx
    question_data["question"] = ""
    question_data["distractors"] = []
    question_data["answers"] = []
    counting_q = False
    counting_a = False
    for line in lines:
        # print(counting_q, counting_a, line)
        if '\\variant' in line:
            counting_q = True
            continue
        if '\\begin{answers}' in line:
            counting_q = False
            counting_a = True
            continue
        if '\\end{answers}' in line:
            break
        if counting_q:
            question_data["question"] += line + '[SEP]'
            continue
        if counting_a:
            if line.startswith('\\correctanswer'):
                question_data["answers"].append(line.strip('\\correctanswer'))
            elif line.startswith('\\answer'):
                question_data["distractors"].append(line.strip('\\answer'))
            else:
                print("unknown start?")
            continue
    return question_data


def organize_cs241_question_data():
    fn = "data/QG-CS241/cs241_quiz.tex"
    # # question size: 218

    with open(fn, 'r', encoding='utf-8') as f:
        question_texts = []
        tmp_question_lines = []
        for x in f:
            line = x.strip()
            if line == "" or line.startswith('%') :
                continue
            if '\\variant' in line:
                question_texts.append(tmp_question_lines)
                tmp_question_lines = []
            tmp_question_lines.append(line)
        tmp_question_lines.append(tmp_question_lines)
    print(len(question_texts))
    print(question_texts[:3])
    
    all_question_data = []
    for idx,lines in enumerate(question_texts[1:]):
        question_data = parse_question_data(idx, lines)
        all_question_data.append(question_data)
    print("data parsed. size of question data", len(all_question_data))

    # statistics
    cnt_verbatim = 0
    for qd in all_question_data:
        if 'verbatim' in qd["question"]:
            cnt_verbatim += 1
    print(cnt_verbatim)




        
# organize_cs241_question_data()
    


def clean_textbook():
    fn_textbook = "data/QG-CS241/CS241_textbook.txt"
    with open(fn_textbook, 'r', encoding='utf-8') as f:
        all_lines = [x.strip() for x in f.readlines()]
    print("original lines number", len(all_lines))
    # concatenate lines which should be continuous. blank lines reserved.
    new_lines = [] # 
    tmp_line = all_lines[0]
    for line in all_lines[1:]:
        if line == "": # if meet empty line, then start a new record
            new_lines.append(tmp_line)
            tmp_line = line
            continue
        if tmp_line == "": # if meet non empty line 
            new_lines.append(tmp_line)
            tmp_line = line
            continue
        if not (re.match(r"[0-9]\.[0-9]", tmp_line) or tmp_line.strip().endswith(('.','?',"!"))):
            tmp_line += " " + line
            continue
        new_lines.append(tmp_line)
        tmp_line = line
        continue   
    print("new line number", len(new_lines))
    # remove '.' lines
    new_lines = [x for x in new_lines if (x!="." and x!="")]

    print("new line number", len(new_lines))
    with open("data/QG-CS241/CS241_textbook_clean.txt", 'w', encoding='utf-8') as f:
        for line in new_lines:
            f.write(line+'\n')
    print("clean textbook saved")
# clean_textbook()

def preprocess_textbook():
    fn_textbook = "data/QG-CS241/CS241_textbook.txt"
    with open(fn_textbook, 'r', encoding='utf-8') as f:
        all_lines = [x.strip() for x in f.readlines()]
    for line in all_lines:
        # remove http
        words = line.split()
        new_line = ""
        for w in words:
            if w.startswith('http'):
                continue
            new_line += f"{w} "
        # split puncuation
        
        

