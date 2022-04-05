#!/bin/bash
#$ -M wyu1@nd.edu
#$ -m abe
#$ -q gpu@qa-v100-001
#$ -pe smp 1
#$ -l gpu=0

CUDA_VISIBLE_DEVICES=3 /afs/crc.nd.edu/user/w/wyu1/anaconda3/envs/bart/bin/python -u finetune.py \
    --data_dir cnn_tiny \
    --model_name_or_path t5-small  \
    --output_dir cnn_tiny_out \
    --num_train_epochs 20 \
    --max_source_length 512 \
    --max_target_length 150 \
    --val_max_target_length 150 \
    --learning_rate 1e-4 \
    --fp16 \
    --do_train \
    --do_eval \
    --do_predict \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 8 \
    --predict_with_generate \
    --load_best_model_at_end \
    --overwrite_output_dir
    # --evaluate_during_training \
    # --prediction_loss_only \
    # --n_val 1000 \
    # "$@"
