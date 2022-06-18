data_dir=/afs/crc.nd.edu/group/dmsquare/vol2/myu2/Caption-Mining/QuestionGeneration/data/squad

CUDA_VISIBLE_DEVICES=0 python run_seq2seq_qg.py \
  --model_name_or_path mrm8488/t5-base-finetuned-question-generation-ap \
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