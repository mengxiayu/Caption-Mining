# Question Genration
The code is modified from https://github.com/huggingface/transformers/tree/v4.17.0/examples/pytorch/question-answering

# Requirements
(Other versions might work)
```
transformers==4.17
python==3.7
rouge_score
```


# Data format
The data files are in JSON lines format. File extention should be .json.

Each line is a JSON dictionary same as SQuAD. Let's see an example
```python
{'id': '5733be284776f41900661182', 'title': 'University_of_Notre_Dame', 'context': 'Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend "Venite Ad Me Omnes". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.', 'question': 'To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?', 'answers': {'text': ['Saint Bernadette Soubirous'], 'answer_start': [515]}}
{'id': '5733be284776f4190066117f', 'title': 'University_of_Notre_Dame', 'context': 'Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend "Venite Ad Me Omnes". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.', 'question': 'What is in front of the Notre Dame Main Building?', 'answers': {'text': ['a copper statue of Christ'], 'answer_start': [188]}}
```

Mainly we use these fields: **'id', 'context', 'question', 'answer'**. Other fields can be empty but in format.

# Run

1. Activate your conda environment.
2. Use the following script to test the running.
```sh
data_dir=QuestionGeneration/data/squad

python run_seq2seq_qg.py \
  --model_name_or_path t5-base \
  --train_file ${data_dir}/squad_train.json \
  --validation_file ${data_dir}/squad_val.json \
  --context_column context \
  --question_column question \
  --answer_column answers \
  --do_train \
  --do_eval \
  --evaluation_strategy epoch \
  --per_device_train_batch_size 4 \
  --gradient_accumulation_steps 4 \
  --learning_rate 3e-5 \
  --num_train_epochs 2 \
  --max_seq_length 384 \
  --max_answer_length 64 \
  --generation_max_length 64 \
  --output_dir tmp/debug_seq2seq_squad \
  --overwrite_output_dir \
  --overwrite_cache \
  --save_strategy epoch \
  --save_total_limit 2 \
  --predict_with_generate \
  --max_train_samples 200 \
  --max_eval_samples 200 \

```
**Training Arguments**
For training arguments setting, please refer to https://huggingface.co/docs/transformers/v4.17.0/en/main_classes/trainer#transformers.TrainingArguments.evaluation_strategy

**Model selection**
You can choose from the following models for the `--model_name_or_path` argument.
- t5-base 
    - The pretrained Google T5 model.
    - Hasn't been trained with any QG data.
- mrm8488/t5-base-finetuned-question-generation-ap [model-card](https://huggingface.co/mrm8488/t5-base-finetuned-question-generation-ap)
    - You need to `pip install transformers[sentencepiece]` and `pip install protobuf==3.20` for this one.
    - Trained with SQuAD QG data.
