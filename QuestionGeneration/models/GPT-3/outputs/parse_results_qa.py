import os
import json

def main():
    results = []
    with open("generated_answers.txt", "r") as f:
        for line in f:
            # line = "Q:" + line
            results.append(line.strip())

    dicts = []
    with open("test_generations.jsonl", "w") as f1:
        with open("../data/CS241/cs241tb_q.json", "r") as f2:
            for idx, line in enumerate(f2):
                data = json.loads(line)
                data["answer_GPT3"] = results[idx]
                dicts.append(data)
        for d in dicts:
            json.dump(d, f1)
            f1.write('\n')
    


if __name__ == "__main__":
    main()