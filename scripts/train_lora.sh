#!/usr/bin/env bash
set -e
export $(grep -v '^#' .env | xargs)

python -m src.train.lora_runner \
  --base_model "$BASE_MODEL" \
  --data ./datasets/bible_qa.jsonl \
  --output_dir "$OUTPUT_DIR" \
  --run_name "$RUN_NAME" \
  --epochs ${EPOCHS:-2} \
  --batch_size ${BATCH_SIZE:-2} \
  --lr ${LR:-2e-4} \
  --save_steps ${SAVE_STEPS:-200} \
  --save_total ${SAVE_TOTAL:-3} \
  --max_seq_len ${MAX_SEQ_LEN:-1024}