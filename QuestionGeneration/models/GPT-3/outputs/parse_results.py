import os
import json

def main():
    results = []
    with open("test_generations.txt", "r") as f:
        for line in f:
            # line = "Q:" + line
            results.append(line.strip().split("Q:"))

    with open("test_generations.jsonl", "w") as f:
        for l in results:
            json.dump(l, f)
            f.write('\n')
    


if __name__ == "__main__":
    main()