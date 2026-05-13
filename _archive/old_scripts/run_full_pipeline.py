"""Run the full downstream pipeline after llm_label_abc.py completes.

Steps:
  1. extract_features.py        (12 features on LLM-labeled A class)
  2. match_y1_v2_piie.py         (per-post Y1 outcome)
  3. event_study_y2.py           (CAR around each post)
  4. episode_clustering.py       (group same-topic posts)
  5. match_episodes_to_outcomes.py (per-episode Y1)
  6. cox_model.py                (Cox PH on episodes)
  7. feature_analysis.py         (correlation, PCA, distributions)
  8. unsupervised_explore.py     (UMAP + HDBSCAN)
  9. build_app_data.py           (data.json for web app)
"""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

STEPS = [
    "extract_features.py",
    "match_y1_v2_piie.py",
    "event_study_y2.py",
    "episode_clustering.py",
    "match_episodes_to_outcomes.py",
    "cox_model.py",
    "feature_analysis.py",
    "unsupervised_explore.py",
    "build_app_data.py",
]

def main():
    log_path = ROOT / "data" / "processed" / "full_pipeline.log"
    with open(log_path, "w") as log:
        for step in STEPS:
            t0 = time.time()
            print(f"\n{'=' * 50}\n[run] {step}\n{'=' * 50}", flush=True)
            log.write(f"\n=== {step} ===\n"); log.flush()
            try:
                r = subprocess.run(
                    [sys.executable, str(SRC / step)],
                    cwd=ROOT, capture_output=True, text=True, timeout=900,
                )
                log.write(r.stdout); log.write(r.stderr); log.flush()
                if r.returncode != 0:
                    print(f"  FAILED (exit {r.returncode})")
                    print(r.stderr[-1500:])
                else:
                    print(f"  OK ({time.time() - t0:.1f}s)")
            except subprocess.TimeoutExpired:
                print(f"  TIMEOUT after 900s")
                log.write(f"TIMEOUT\n")
            except Exception as e:
                print(f"  ERROR: {e}")
                log.write(f"ERROR: {e}\n")
    print(f"\n[done] full log → {log_path}")

if __name__ == "__main__":
    main()
