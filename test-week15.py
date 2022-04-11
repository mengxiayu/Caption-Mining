'''
TODO clean data for CS241 question generation
- textbook data
- quiz data
'''
def organize_cs241_question_data():
    fn = ""
    # with open(fn, 'r', encoding='utf-8') as f:
        # TODO for mx


def clean_textbook():
    fn_textbook = "data/QG-CS241/CS241_textbook.txt"
    with open(fn_textbook, 'r', encoding='utf-8') as f:
        all_lines = [x.strip() for x in f.readlines()]
    print("original lines number", len(all_lines))
    # concatenate lines which should be continuous. blank lines reserved.
    # TODO should replace some characters, such as \u2019
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
        if not tmp_line.strip().endswith(('.','?',"!")):
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

