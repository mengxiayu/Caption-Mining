# CODE FROM https://github.com/HazyResearch/fm_data_tasks
import argparse
import json
import logging
from pathlib import Path

import numpy as np
from tqdm.auto import tqdm

from utils import setup_logger, read_data_infer
from openai_client import Client


logger = logging.getLogger(__name__)

client = Client()

def parse_args() -> argparse.Namespace:
    """Generate args."""
    parser = argparse.ArgumentParser(description="Simple calculator")
    parser.add_argument(
        "--data_dir",
        type=str,
        help="Which data directory to run.",
        required=True,
    )
    parser.add_argument(
        "--output_dir", type=str, help="Output directory.", default="outputs"
    )
    parser.add_argument(
        "--k", type=int, help="Number examples in prompt", default=1)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument(
        "--sep_tok",
        type=str,
        help="Separate for attr: val pairs in row. Default is '.'.",
        default=".",
    )
    parser.add_argument(
        "--nan_tok",
        type=str,
        help="Token to represent nan entries. Default is 'nan'.",
        default="nan",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        help="Which OpenAI model to use.",
        default="text-davinci-002",
        choices=[
            "text-davinci-002",
            "text-curie-001",
            "text-babbage-001",
            "text-ada-001",
        ],
    )
    parser.add_argument(
        "--num_examples",
        type=int,
        help="Number examples to run through model.",
        default=2,
    )
    parser.add_argument(
        "--num_trials",
        type=int,
        help="Number trials to run. Results will be averaged with variance reported.",
        default=1,
    )
    parser.add_argument(
        "--num_print",
        type=int,
        help="Number example prompts to print.",
        default=10,
    )
    parser.add_argument(
        "--add_task_instruction",
        help="Add task instruction to the prompt before examples.",
        action="store_true",
    )
    parser.add_argument(
        "--dry_run", help="Dry run. Do not actually ping model.", action="store_true"
    )

    # Open AI args
    parser.add_argument("--temperature", type=float,
                        help="Temperature.", default=0.5)
    parser.add_argument(
        "--max_tokens", type=int, help="Max tokens to generate.", default=256
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.num_trials < 1:
        raise ValueError("num_trials must be greater than 0.")

    # Get absolute path
    args.data_dir = str(Path(args.data_dir).resolve())
    setup_logger(args.output_dir)
    logger.info(json.dumps(vars(args), indent=4))
    np.random.seed(args.seed)

    # Load data
    logger.info("Loading data...")

    # Read datasets
    contexts = read_data_infer(
        data_dir=args.data_dir,
        sep_tok=args.sep_tok,
        nan_tok=args.nan_tok,
    )
    contexts = contexts[: args.num_examples]

    # construct prompts
    # Q + A
    task_instruction = """
    I am a highly intelligent question 
    generation bot. If you give a context text, 
    I will generate several questions as if I were the teacher. 
    I will ask questions along with potential answers. 
    """
    inputs = []
    for i, context in enumerate(contexts):
        # if args.add_task_instruction:
        input = "Task Instruction: " + task_instruction + "\n" +\
        "Context: \n" + context + "\n" +\
        "Generated Questions: \nQ: "
        inputs.append(input)
    # print(inputs[0], inputs[1])

    # Q + A with few-shot examples
    # todo
    



    # query model
    logger.info("Querying model...")
    results = []
    for input in tqdm(inputs):
        if not args.dry_run:
            response = client.query(
                engine=args.model_name,
                prompt=input,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
                # overwrite_cache=args.overwrite_cache,
            )
            # parse response
            result = response["choices"][0]["text"]
            result = result.replace("\n", "")
            results.append(result)
    # print(results)

    # dump results to file
    with open(args.output_dir + "/test_generations.txt", "w") as f:
        for result in results:
            f.write(result + "\n")

    # assert False, "Not implemented"
    

if __name__ == "__main__":
    main()
