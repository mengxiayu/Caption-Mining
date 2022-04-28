#!/bin/bash
#$ -M myu2@nd.edu
#$ -m abe
#$ -q gpu@qa-2080ti-007
#$ -pe smp 1
#$ -l gpu=1

CUDA_VISIBLE_DEVICES=0 /afs/crc.nd.edu/user/m/myu2/anaconda2/envs/bart/bin/python3.6 -u finetune.py \
    --data_dir datasets/bus_240 \
    --model_name_or_path t5-small  \
    --output_dir out_bus_240_lr5e-5 \
    --num_train_epochs 20 \
    --max_source_length 512 \
    --max_target_length 150 \
    --val_max_target_length 150 \
    --learning_rate 5e-5 \
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
