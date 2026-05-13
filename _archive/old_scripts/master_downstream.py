"""Master downstream pipeline (runs after rich features complete).

Steps:
  1. Episode clustering with bge-large embedding (consensus A only)
  2. Match episodes to PIIE outcomes
  3. Event study CAR (re-compute on consensus A)
  4. Cox PH with bootstrap CI
  5. Update web app data
"""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

STEPS = [
    # We've changed sources of A class — need to wire the new pipeline.
    # episode_clustering reads threats_with_outcomes_v2 by default.
    # We need to make it read consensus_a + features_aggregated.
    "make_consensus_features_ready.py",   # wrapper to create the right input parquet
    "episode_clustering_v2.py",
    "match_episodes_v2.py",
    "event_study_v2.py",
    "cox_with_bootstrap.py",
    "build_app_data_v2.py",
]


def main():
    log_path = ROOT / "data" / "processed" / "master_downstream.log"
    with open(log_path, "w") as log:
        for step in STEPS:
            t0 = time.time()
            print(f"\n{'=' * 60}\n[run] {step}\n{'=' * 60}", flush=True)
            log.write(f"\n=== {step} ===\n"); log.flush()
            step_fp = SRC / step
            if not step_fp.exists():
                print(f"  [skip] {step} not yet written")
                log.write("(not yet written, skipping)\n")
                continue
            try:
                r = subprocess.run(
                    [sys.executable, str(step_fp)],
                    cwd=ROOT, capture_output=True, text=True, timeout=1200,
                )
                log.write(r.stdout); log.write(r.stderr); log.flush()
                if r.returncode != 0:
                    print(f"  FAILED exit {r.returncode}")
                    print(r.stderr[-1500:])
                else:
                    print(f"  OK ({time.time() - t0:.1f}s)")
            except Exception as e:
                print(f"  ERROR: {e}")
                log.write(f"ERROR: {e}\n")
    print(f"\n[done] full log → {log_path}")

if __name__ == "__main__":
    main()
