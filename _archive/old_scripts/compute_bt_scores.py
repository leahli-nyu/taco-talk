"""Compute Bradley-Terry ranking scores from pairwise comparisons.

For each feature, fit P(i beats j) = sigmoid(s_i - s_j) by MLE.
Ties counted as 0.5 wins for each side.

Output: data/processed/episodes_bt_scores.parquet
  episode_id, bt__{feature} columns
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
PAIRS_FP = ROOT / "data" / "processed" / "pairwise_bt_raw.parquet"
EP_FP = ROOT / "data" / "processed" / "episodes_v2.parquet"
OUT_FP = ROOT / "data" / "processed" / "episodes_bt_scores.parquet"


def fit_bt(items: list, wins: list[tuple[int, int, float]]) -> dict:
    """Fit BT model. items = list of episode_ids. wins = list of (winner_idx, loser_idx, weight).
    Weight 1.0 for clean win, 0.5 each direction for ties.
    """
    n = len(items)
    idx = {it: i for i, it in enumerate(items)}

    def neg_loglik(s):
        s = np.concatenate([[0.0], s])  # fix s_0 = 0 for identifiability
        ll = 0.0
        for w, l, wt in wins:
            diff = s[w] - s[l]
            # numerically stable log-sigmoid
            if diff > 0:
                ll += wt * (-np.log1p(np.exp(-diff)))
            else:
                ll += wt * (diff - np.log1p(np.exp(diff)))
        return -ll

    x0 = np.zeros(n - 1)
    res = minimize(neg_loglik, x0, method="L-BFGS-B", options={"maxiter": 500})
    s = np.concatenate([[0.0], res.x])
    return {it: float(s[i]) for it, i in idx.items()}


def main():
    pairs = pd.read_parquet(PAIRS_FP)
    eps = pd.read_parquet(EP_FP)[["episode_id"]]
    all_ids = sorted(set(pairs["ep_a"]).union(pairs["ep_b"]))
    print(f"[load] {len(pairs)} pair-feature rows over {len(all_ids)} unique episodes")

    feats = pairs["feature"].unique().tolist()
    print(f"[features] {feats}")

    score_dfs = []
    for feat in feats:
        sub = pairs[pairs["feature"] == feat]
        wins = []
        for _, r in sub.iterrows():
            a, b = r["ep_a"], r["ep_b"]
            v = r["winner"]
            if v == "A":
                wins.append((all_ids.index(a), all_ids.index(b), 1.0))
            elif v == "B":
                wins.append((all_ids.index(b), all_ids.index(a), 1.0))
            else:  # tie
                wins.append((all_ids.index(a), all_ids.index(b), 0.5))
                wins.append((all_ids.index(b), all_ids.index(a), 0.5))
        scores = fit_bt(all_ids, wins)
        s_arr = np.array([scores[i] for i in all_ids])
        # z-standardize for downstream Cox
        s_z = (s_arr - s_arr.mean()) / (s_arr.std() + 1e-9)
        score_dfs.append(pd.DataFrame({
            "episode_id": all_ids,
            f"bt__{feat}": s_arr,
            f"btz__{feat}": s_z,
        }))
        print(f"  {feat:25s}  mean={s_arr.mean():+.2f}  std={s_arr.std():.2f}  "
              f"range=[{s_arr.min():+.2f},{s_arr.max():+.2f}]")

    out = score_dfs[0]
    for d in score_dfs[1:]:
        out = out.merge(d, on="episode_id")
    # merge to episode list (in case some episodes weren't sampled)
    full = eps.merge(out, on="episode_id", how="left")
    full.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}  rows={len(full)}, with-bt={full[f'bt__{feats[0]}'].notna().sum()}")

    # Sanity: correlate with the old 0-10 scores
    af = pd.read_parquet(ROOT / "data" / "processed" / "all_features.parquet")
    merged = af.merge(full, on="episode_id", how="left") if "episode_id" in af.columns else None
    if merged is None:
        # Try via first_post link via posts table
        pass


if __name__ == "__main__":
    main()
