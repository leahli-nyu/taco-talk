"""Aggregate rich_features.parquet:
- median + SD across 3 Claude calls
- single GPT-4o-mini call as cross-LLM validation
- compute Claude↔GPT agreement (Pearson r per feature)
"""
from __future__ import annotations
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_FP = ROOT / "data" / "processed" / "rich_features.parquet"
OUT_FP = ROOT / "data" / "processed" / "features_aggregated.parquet"

FEATURE_NAMES = [
    "commitment_strength", "specificity", "hedging_level", "dramatization",
    "conditional_framing", "audience_cost", "precedent_invocation",
    "negotiation_framing", "personal_attack", "ego_centric_framing",
]


def main():
    df = pd.read_parquet(IN_FP)
    print(f"[load] {len(df)} raw rows")
    # Pivot: for each post, get claude_1, claude_2, claude_3, gpt
    rows = []
    for pid, sub in df.groupby("_id"):
        row = {"_id": pid}
        for call in ("claude_1", "claude_2", "claude_3", "gpt"):
            cs = sub[sub["call_name"] == call]
            if len(cs) == 0:
                continue
            c = cs.iloc[0]
            for f in FEATURE_NAMES:
                if f in c.index and pd.notna(c[f]):
                    row[f"{call}__{f}"] = c[f]
            # also keep target / action / deadline (from claude_1 first if available)
            if call == "claude_1":
                for k in ("target_entity", "policy_action", "deadline_phrase"):
                    if k in c.index and pd.notna(c[k]):
                        row[k] = c[k]
        # Compute median + SD across claude calls
        for f in FEATURE_NAMES:
            vals = [row.get(f"claude_{n}__{f}") for n in (1, 2, 3)]
            vals = [float(v) for v in vals if v is not None and not pd.isna(v)]
            if vals:
                row[f"claude_med__{f}"] = float(np.median(vals))
                row[f"claude_sd__{f}"] = float(np.std(vals)) if len(vals) > 1 else 0.0
        rows.append(row)

    out = pd.DataFrame(rows)
    out.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}  rows={len(out)}")

    # Claude<->GPT agreement
    print("\n=== Claude (median of 3) vs GPT (1 call) Pearson r ===")
    for f in FEATURE_NAMES:
        c_col = f"claude_med__{f}"
        g_col = f"gpt__{f}"
        if c_col in out.columns and g_col in out.columns:
            sub = out[[c_col, g_col]].dropna()
            if len(sub) >= 10:
                r = sub[c_col].corr(sub[g_col])
                print(f"  {f:25s}  r = {r:+.3f}  (N={len(sub)})")

    # Claude internal consistency (test-retest reliability across 3 calls)
    print("\n=== Claude test-retest reliability (mean of 3 pairwise correlations) ===")
    for f in FEATURE_NAMES:
        cols = [f"claude_{n}__{f}" for n in (1, 2, 3) if f"claude_{n}__{f}" in out.columns]
        if len(cols) < 2:
            continue
        sub = out[cols].dropna()
        if len(sub) < 10:
            continue
        rs = []
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                r = sub[cols[i]].corr(sub[cols[j]])
                rs.append(r)
        if rs:
            mean_r = np.mean(rs)
            print(f"  {f:25s}  mean r = {mean_r:+.3f}  (N={len(sub)})")


if __name__ == "__main__":
    main()
