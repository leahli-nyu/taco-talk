#!/bin/bash
# Run the full downstream pipeline after llm_label_abc.py completes.
# Each step's output is appended to data/processed/post_label_pipeline.log.

set -e
cd "$(dirname "$0")/.."

LOG="data/processed/post_label_pipeline.log"
echo "===== Pipeline start: $(date) =====" | tee -a "$LOG"

steps=(
  "extract_features.py"
  "match_y1_v2_piie.py"
  "event_study_y2.py"
  "episode_clustering.py"
  "match_episodes_to_outcomes.py"
  "cox_model.py"
  "feature_analysis.py"
  "unsupervised_explore.py"
  "contrastive_ngrams.py"
  "build_app_data.py"
)

for s in "${steps[@]}"; do
  echo "" | tee -a "$LOG"
  echo "----- $s -----" | tee -a "$LOG"
  t0=$(date +%s)
  if python3 -u "src/$s" >>"$LOG" 2>&1; then
    t1=$(date +%s)
    echo "  OK ($((t1 - t0))s)" | tee -a "$LOG"
  else
    echo "  FAILED — check $LOG" | tee -a "$LOG"
    # Don't exit — continue with other steps
  fi
done

echo "" | tee -a "$LOG"
echo "===== Pipeline done: $(date) =====" | tee -a "$LOG"
