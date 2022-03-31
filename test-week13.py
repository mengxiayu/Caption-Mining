
            

import json

def organize_bus_question_data():
    fn = "week13/bus_questions.txt"
    with open (fn, 'r', encoding='utf-8') as f:
        lines = []
        for line in f:
            if line.strip() == "":
                continue
            lines.append(line.strip())
    # print(len(lines))
    # for line in lines[:20]:
    #     print(line)

    # split into chapters
    chapter_questions = []
    chapter_data = []
    for line in lines:
        if line.startswith("Ch"):
            chapter_questions.append(chapter_data)
            chapter_data = []
        chapter_data.append(line)
    print("# chapter", len(chapter_questions))

    all_question_data = []
    for data_lines in chapter_questions:
        isquestion = True
        chapter = ""
        id2questions = {}
        question_data = {}
        for line in data_lines:
            if line.startswith("Ch"):
                chapter = line
                continue
            if line.startswith("Indicate"):
                continue 
            if line.startswith("Answer"):
                id2questions[question_data["index"]] = question_data
                question_data = []
                isquestion = False
                continue

            tmp = line.split('.')
            if len(tmp) < 2:
                print("false line", line)

            idx = tmp[0]
            text = ".".join(tmp[1:])
            for i in range(len(text)):
                if text[i].isalnum():
                    text = text[i:]
                    break
            if isquestion:
                if idx.isnumeric(): # initialize a new question
                    if question_data != {}:
                        id2questions[question_data["index"]] = question_data
                        # print(question_data)
                        question_data = {}
                    question_data["chapter"] = chapter
                    question_data["index"] = idx
                    question_data["question"] = text
                    question_data["candidates"] = []
                    question_data["answers"] = []
                    continue
                if idx.isalpha():
                    question_data["candidates"].append(line.replace('\t', ''))
                    continue
            else:
                assert idx.isnumeric() and text.isalpha()
                for c in id2questions[idx]["candidates"]:
                    if c.startswith(text):
                        id2questions[idx]["answers"].append(c)
                assert len(id2questions[idx]["answers"]) == 1

        for idx, data in id2questions.items():
            all_question_data.append(data)
                
                
    print(len(all_question_data))
    print(all_question_data[-1])
    print(all_question_data[0])
                
    print("# avg chapter quesitons", len(all_question_data)/len(chapter_questions))


    data_str = json.dumps(all_question_data, indent=2)
    with open("data/BUS_Chapter_Review_Questions.json", 'w', encoding='utf-8') as f:
        f.write(data_str)

def bus_data_analysis():
    with open("data/BUS_Chapter_Review_Questions.json", 'r', encoding='utf-8') as f:
        data_str = f.read()
    all_question_data = json.loads(data_str)

    # avg question words
    num_words = []
    for data in all_question_data:
        cnt = data["question"].count(' ')
        num_words.append(cnt)
    avg_words = sum(num_words)/len(num_words)
    print(num_words)
    print("avg words in quesiton", avg_words)


    num_words = []
    for data in all_question_data:
        for c in data["candidates"]:
            cnt = c.count(' ')
            num_words.append(cnt)
    avg_words = sum(num_words)/len(num_words)
    print(num_words)
    print("avg words in answer candidates", avg_words)

bus_data_analysis()