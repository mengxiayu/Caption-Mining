#!/bin/bash
#$ -M myu2@nd.edu
#$ -m abe
#$ -q gpu@qa-2080ti-007
#$ -pe smp 1
#$ -l gpu=1

data_dir=/afs/crc.nd.edu/group/dmsquare/vol2/myu2/Caption-Mining/QuestionGeneration/data/RQgen/data_v1
output_dir=/afs/crc.nd.edu/group/dmsquare/vol2/myu2/Caption-Mining/QuestionGeneration/experiments/rq_v1_bart_0923

CUDA_VISIBLE_DEVICES=3 /afs/crc.nd.edu/user/m/myu2/anaconda2/envs/bert/bin/python3.7 -u run_rqgen.py \
  --model_name_or_path facebook/bart-base \
  --train_file ${data_dir}/RQ_v1_train.json \
  --validation_file ${data_dir}/RQ_v1_dev.json \
  --context_column relatedWork \
  --answer_column intro \
  --question_column rq \
  --do_train \
  --do_eval \
  --evaluation_strategy epoch \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 1 \
  --learning_rate 3e-5 \
  --num_train_epochs 20 \
  --max_seq_length 512 \
  --max_answer_length 64 \
  --generation_max_length 64 \
  --output_dir ${output_dir} \
  --overwrite_output_dir \
  --overwrite_cache \
  --save_strategy epoch \
  --save_total_limit 2 \
  --predict_with_generate \
