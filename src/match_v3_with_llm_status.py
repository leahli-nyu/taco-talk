"""Re-run v3 strict PIIE matching but use LLM-cleaned status (replaces regex bug).

Output: data/processed/episodes_with_outcomes_v3_llmstatus.parquet
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
V3_FP = ROOT / "data" / "processed" / "episodes_with_outcomes_v3_strict.parquet"
PIIE_LLM_FP = ROOT / "data" / "processed" / "piie_timeline_llm_clean.parquet"
OUT_FP = ROOT / "data" / "processed" / "episodes_with_outcomes_v3_llmstatus.parquet"

STATUS_BUCKET = {
    "in_effect": "executed",
    "modified_or_withdrawn": "modified_or_withdrawn",
    "struck_down": "struck_down",
    "announced": "announced_unresolved",
    "investigation": "investigation",
    "other": "other",
}


def main():
    v3 = pd.read_parquet(V3_FP)
    piie_llm = pd.read_parquet(PIIE_LLM_FP)
    print(f"[load] v3 {len(v3)} episodes ({v3['anticipation_days'].notna().sum()} matched)")

    # Build lookup: (date, country, category) -> llm_status
    piie_llm["date_str"] = pd.to_datetime(piie_llm["date"]).dt.date.astype(str)
    piie_llm["country_str"] = piie_llm["country"].fillna("None").astype(str)
    piie_llm["category_str"] = piie_llm["category"].fillna("None").astype(str)
    lookup = {}
    for _, r in piie_llm.iterrows():
        key = (r["date_str"], r["country_str"], r["category_str"])
        lookup[key] = r["status_llm"]

    # Apply
    matched_mask = v3["anticipation_days"].notna()
    new_y1 = []
    n_changed = 0
    for _, r in v3.iterrows():
        if pd.isna(r["anticipation_days"]):
            new_y1.append(r["y1_outcome"])
            continue
        key = (str(r["matched_date"]), str(r["matched_country"]) if r["matched_country"] else "None",
               str(r["matched_category"]) if r["matched_category"] else "None")
        if key in lookup:
            new_status = lookup[key]
            new_bucket = STATUS_BUCKET.get(new_status, "other")
            if new_bucket != r["y1_outcome"]:
                n_changed += 1
            new_y1.append(new_bucket)
        else:
            new_y1.append(r["y1_outcome"])

    v3["y1_outcome_llm"] = new_y1
    v3.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")
    print(f"  status labels changed (within matched): {n_changed}/{matched_mask.sum()}")
    print(f"\n=== y1_outcome (regex) ===")
    print(v3.loc[matched_mask, "y1_outcome"].value_counts())
    print(f"\n=== y1_outcome_llm ===")
    print(v3.loc[matched_mask, "y1_outcome_llm"].value_counts())


if __name__ == "__main__":
    main()
