"""Compute BT scores from v2 pairwise (1-7 scale, Claude AND GPT, anonymized).

Cross-LLM BT agreement check: do Claude and GPT BT scores correlate?

Outputs:
  data/processed/episodes_bt_v2_scores.parquet  (Claude + GPT separate, plus consensus average)
  Console: cross-LLM correlation per feature
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
PC_FP = ROOT / "data" / "processed" / "pairwise_bt_v2_claude.parquet"
PG_FP = ROOT / "data" / "processed" / "pairwise_bt_v2_gpt.parquet"
EPS_FP = ROOT / "data" / "processed" / "episodes_v2_narrow.parquet"
OUT_FP = ROOT / "data" / "processed" / "episodes_bt_v2_scores.parquet"

FEATURES = ["commitment_strength", "hedging_level", "specificity", "audience_cost"]


def score_to_weights(score: int) -> tuple[float, float]:
    """Convert 1-7 score to (weight_for_A_wins, weight_for_B_wins).
    1=A definitely much higher -> A_weight=1.0, B_weight=0.0
    4=tie -> A_weight=0.5, B_weight=0.5
    7=B definitely much higher -> A_weight=0.0, B_weight=1.0
    """
    # Linear interpolation
    if score == 4:
        return 0.5, 0.5
    # Scale 1-7 to 0-1, where 1 = certainly A wins, 7 = certainly B wins
    # Map: 1->1.0, 2->0.83, 3->0.67, 4->0.5, 5->0.33, 6->0.17, 7->0.0
    a_weight = (7 - score) / 6.0
    return a_weight, 1 - a_weight


def fit_bt(items: list, weighted_wins: list[tuple[int, int, float]]) -> dict:
    """Fit BT model.
    weighted_wins: list of (winner_idx, loser_idx, weight).
    """
    n = len(items)
    idx = {it: i for i, it in enumerate(items)}

    def neg_loglik(s):
        s = np.concatenate([[0.0], s])
        ll = 0.0
        for w, l, wt in weighted_wins:
            diff = s[w] - s[l]
            if diff > 0:
                ll += wt * (-np.log1p(np.exp(-diff)))
            else:
                ll += wt * (diff - np.log1p(np.exp(diff)))
        return -ll

    x0 = np.zeros(n - 1)
    res = minimize(neg_loglik, x0, method="L-BFGS-B", options={"maxiter": 500})
    s = np.concatenate([[0.0], res.x])
    return {it: float(s[i]) for it, i in idx.items()}


def build_scores_for_model(pairs_df: pd.DataFrame, all_ids: list, label: str) -> pd.DataFrame:
    print(f"\n=== {label} BT fit ===")
    out_cols = {"episode_id": all_ids}
    for feat in FEATURES:
        sub = pairs_df[pairs_df["feature"] == feat]
        weighted_wins = []
        for _, r in sub.iterrows():
            a, b = r["ep_a"], r["ep_b"]
            score = int(r["score"])
            a_w, b_w = score_to_weights(score)
            if a_w > 0:
                weighted_wins.append((all_ids.index(a), all_ids.index(b), a_w))
            if b_w > 0:
                weighted_wins.append((all_ids.index(b), all_ids.index(a), b_w))
        scores_map = fit_bt(all_ids, weighted_wins)
        arr = np.array([scores_map[i] for i in all_ids])
        arr_z = (arr - arr.mean()) / (arr.std() + 1e-9)
        out_cols[f"bt_{label}__{feat}"] = arr
        out_cols[f"btz_{label}__{feat}"] = arr_z
        print(f"  {feat:25s}  mean={arr.mean():+.2f} std={arr.std():.2f}  range=[{arr.min():+.2f},{arr.max():+.2f}]")
    return pd.DataFrame(out_cols)


def main():
    pc = pd.read_parquet(PC_FP)
    pg = pd.read_parquet(PG_FP)
    eps = pd.read_parquet(EPS_FP)
    all_ids = sorted(set(eps["episode_id"]) & set(pc["ep_a"]).union(pc["ep_b"]))
    print(f"[load] eps={len(eps)}; ids covered by pairs={len(all_ids)}")

    df_c = build_scores_for_model(pc, all_ids, "claude")
    df_g = build_scores_for_model(pg, all_ids, "gpt")

    merged = df_c.merge(df_g, on="episode_id", how="outer")

    # Cross-LLM agreement
    print(f"\n=== Cross-LLM BT agreement (Pearson r) ===")
    for f in FEATURES:
        if f"bt_claude__{f}" in merged.columns and f"bt_gpt__{f}" in merged.columns:
            r = merged[[f"bt_claude__{f}", f"bt_gpt__{f}"]].corr().iloc[0, 1]
            print(f"  {f:25s}  r = {r:+.3f}")

    # Consensus = z-average
    for f in FEATURES:
        merged[f"btz_consensus__{f}"] = (merged[f"btz_claude__{f}"] + merged[f"btz_gpt__{f}"]) / 2

    merged.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")


if __name__ == "__main__":
    main()
