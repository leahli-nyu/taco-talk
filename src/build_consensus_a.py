"""Identify consensus A-class posts (both Claude and GPT classify as A)."""
from __future__ import annotations
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    c = pd.read_parquet(ROOT / "data" / "processed" / "labeled_v2_claude.parquet")
    g = pd.read_parquet(ROOT / "data" / "processed" / "labeled_v2_gpt.parquet")
    posts = pd.read_parquet(ROOT / "data" / "processed" / "truth_second_term.parquet")

    c["_id"] = c["_id"].astype(str)
    g["_id"] = g["_id"].astype(str)
    posts["id"] = posts["id"].astype(str)

    consensus_a = c[c["label"] == "A"][["_id"]].merge(
        g[g["label"] == "A"][["_id"]], on="_id", how="inner"
    )
    print(f"Consensus A: {len(consensus_a)}")

    # Build full record with original text + LLM agreement metadata
    a_full = consensus_a.merge(posts, left_on="_id", right_on="id", how="left")
    # Join Claude features
    a_full = a_full.merge(
        c.rename(columns={"label": "claude_label", "policy_area": "claude_policy",
                          "commissive_confidence": "claude_conf",
                          "is_commissive": "claude_commissive"}
        )[["_id", "claude_label", "claude_policy", "claude_conf", "claude_commissive"]],
        on="_id", how="left"
    )
    a_full = a_full.merge(
        g.rename(columns={"label": "gpt_label", "policy_area": "gpt_policy",
                          "commissive_confidence": "gpt_conf",
                          "is_commissive": "gpt_commissive"}
        )[["_id", "gpt_label", "gpt_policy", "gpt_conf", "gpt_commissive"]],
        on="_id", how="left"
    )

    print(f"\nPolicy area agreement (top):")
    print(pd.crosstab(a_full.claude_policy, a_full.gpt_policy).head(10))

    out_fp = ROOT / "data" / "processed" / "consensus_a.parquet"
    a_full.to_parquet(out_fp)
    print(f"\n[saved] {out_fp}")

if __name__ == "__main__":
    main()
