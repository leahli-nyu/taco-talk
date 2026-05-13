"""Phase 2 pre-filter + EDA: narrow 6,228 posts to econ-threat candidates.

This is a *recall-first* filter — we'd rather over-include and let the
LLM A/B/C labeler do the precise classification.

Produces:
  - data/processed/econ_candidates.parquet
  - figures/eda04_candidate_count_by_term.png
  - data/processed/keyword_counts.json
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN_FP = ROOT / "data" / "processed" / "truth_second_term.parquet"
OUT_DATA = ROOT / "data" / "processed"
OUT_FIG = ROOT / "figures"

# Recall-first keyword groups
KEYWORD_GROUPS = {
    "tariff": [r"\btariff", r"\bduties\b", r"\bduty\b", r"\bimport tax",
               r"\bSection\s*(232|301)", r"\breciprocal trade"],
    "trade_relations": [r"\btrade deal", r"\btrade war", r"\btrade agreement",
                        r"\bUSMCA", r"\bbilateral", r"\bWTO"],
    "import_export": [r"\bimport(?:ing|s|ed)?\b", r"\bexport(?:ing|s|ed)?\b",
                      r"\bembargo", r"\bblockad"],
    "sanctions": [r"\bsanction", r"\bOFAC\b", r"\bSDN list"],
    "fed_powell": [r"\bPowell", r"\bFed(?:eral Reserve)?", r"\binterest rate",
                   r"\brate cut", r"\brate hike"],
    "currency": [r"\bdollar\b", r"\byuan", r"\bpeso", r"\beuro\b", r"\bcurrency"],
    "specific_goods": [r"\bsteel", r"\baluminum", r"\bsemiconductor", r"\bchip",
                       r"\bauto[s\b]", r"\bag(?:riculture|ricultural)",
                       r"\boil\b", r"\bgas\b", r"\bcoffee\b"],
    "threat_markers": [r"\bwill\b", r"\bgoing to\b",
                       r"\b(?:I|we) (?:will|am going to|plan)",
                       r"\b\d{1,3}\s*%", r"\b\d{1,3}\s*percent"],
    "policy_action_verbs": [r"\bimpos\w*", r"\braise\w*", r"\bcut\w*",
                            r"\blift\w*", r"\bremove\w*", r"\bblock\w*",
                            r"\bban\b", r"\bbann\w+"],
}

# Compile
COMPILED = {k: re.compile("|".join(pats), re.I) for k, pats in KEYWORD_GROUPS.items()}

def evidence_for(text: str) -> dict:
    if not isinstance(text, str):
        return {}
    return {f"has_{k}": bool(p.search(text)) for k, p in COMPILED.items()}

def is_candidate(ev: dict) -> bool:
    """Recall-first: include if ANY econ-related term + ANY threat/action marker."""
    econ = any(ev.get(f"has_{k}", False) for k in [
        "tariff", "trade_relations", "import_export", "sanctions",
        "fed_powell", "specific_goods",
    ])
    actionable = ev.get("has_threat_markers", False) or ev.get("has_policy_action_verbs", False)
    return econ and actionable

def main():
    df = pd.read_parquet(IN_FP)
    print(f"[load] {len(df):,} second-term originals")

    ev = df["content"].apply(evidence_for).apply(pd.Series)
    df = pd.concat([df, ev], axis=1)
    df["is_candidate"] = ev.apply(is_candidate, axis=1)

    cand = df[df["is_candidate"]].copy().reset_index(drop=True)
    cand["year_month"] = pd.to_datetime(cand["created_at"]).dt.to_period("M").astype(str)
    print(f"[candidate] {len(cand):,} posts ({100*len(cand)/len(df):.1f}% of corpus)")

    # Save
    out_fp = OUT_DATA / "econ_candidates.parquet"
    cand.to_parquet(out_fp)
    print(f"[saved] {out_fp}")

    # Keyword stats
    kw_counts = {k: int(ev[f"has_{k}"].sum()) for k in KEYWORD_GROUPS}
    kw_counts["TOTAL_CANDIDATES"] = len(cand)
    kw_counts["TOTAL_CORPUS"] = len(df)
    (OUT_DATA / "keyword_counts.json").write_text(json.dumps(kw_counts, indent=2))
    print(f"[saved] {OUT_DATA / 'keyword_counts.json'}")

    # Plot candidate counts per month
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        cm = cand.groupby("year_month").size().reset_index(name="n_candidates")
        all_m = df.copy()
        all_m["year_month"] = pd.to_datetime(all_m["created_at"]).dt.to_period("M").astype(str)
        am = all_m.groupby("year_month").size().reset_index(name="n_total")
        merged = am.merge(cm, on="year_month", how="left").fillna(0)

        fig, ax = plt.subplots(figsize=(11, 4))
        x = range(len(merged))
        ax.bar(x, merged["n_total"], label="all originals", alpha=0.4, color="#aaa")
        ax.bar(x, merged["n_candidates"], label="econ-threat candidates", color="#e15759")
        ax.set_xticks(x); ax.set_xticklabels(merged["year_month"], rotation=45, ha="right")
        ax.set_title(f"Econ-threat candidates per month "
                     f"({len(cand):,} of {len(df):,} posts)")
        ax.legend()
        plt.tight_layout()
        plt.savefig(OUT_FIG / "eda04_candidate_count_by_month.png", dpi=120)
        plt.close()
        print(f"[saved] {OUT_FIG / 'eda04_candidate_count_by_month.png'}")
    except Exception as e:
        print(f"[plot warn] {e}")

    # Print 5 random candidates for sanity check
    print("\n--- 5 random candidates ---")
    for i, r in cand.sample(5, random_state=2).iterrows():
        print(f"\n[{r.created_at}]")
        print(r.content[:350])

    return cand

if __name__ == "__main__":
    main()
