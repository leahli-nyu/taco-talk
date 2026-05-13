"""Cross-validate hand-compiled GT 'in_effect' labels against Federal Register EOs.

For each in_effect event, check if there's a Presidential Document published
within [-3, +7] days of the announced date. Reports coverage.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import timedelta
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
GT_FP = ROOT / "data" / "raw" / "tariff_timeline_ground_truth.json"
FR_FP = ROOT / "data" / "raw" / "federal_register_tariff_eos.json"
OUT_FP = ROOT / "data" / "processed" / "fr_cross_validation.parquet"


def main():
    gt = json.load(open(GT_FP))["events"]
    fr = json.load(open(FR_FP))["results"]

    fr_df = pd.DataFrame([{
        "doc": r.get("document_number"),
        "date": pd.to_datetime(r["publication_date"]).date(),
        "title": r.get("title"),
    } for r in fr])

    print(f"[load] {len(gt)} hand-compiled events, {len(fr_df)} FR presidential docs")

    rows = []
    for e in gt:
        ad = pd.to_datetime(e.get("announced"), errors="coerce")
        if pd.isna(ad):
            continue
        ad_d = ad.date()
        # search FR ±7 days
        lo = ad_d - timedelta(days=3)
        hi = ad_d + timedelta(days=14)
        nearby = fr_df[(fr_df["date"] >= lo) & (fr_df["date"] <= hi)]
        rows.append({
            "announced": e.get("announced"),
            "target": e.get("target"),
            "status": e.get("status"),
            "n_fr_nearby": len(nearby),
            "fr_titles": "; ".join(nearby["title"].tolist())[:300] if len(nearby) else "",
        })
    df = pd.DataFrame(rows)
    df.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}")

    print(f"\n=== Coverage by status (FR Presidential Doc within [-3, +14d]) ===")
    cov = df.groupby("status").agg(
        n=("status", "size"),
        n_with_fr=("n_fr_nearby", lambda s: (s > 0).sum()),
    )
    cov["coverage"] = (cov["n_with_fr"] / cov["n"] * 100).round(1).astype(str) + "%"
    print(cov)

    print(f"\n=== In_effect events WITHOUT nearby FR doc (suspicious) ===")
    susp = df[(df["status"] == "in_effect") & (df["n_fr_nearby"] == 0)]
    for _, r in susp.iterrows():
        print(f"  {r['announced']} | target={r['target']} | NO FR doc nearby")

    print(f"\n=== In_effect events WITH nearby FR doc (confirmed) ===")
    conf = df[(df["status"] == "in_effect") & (df["n_fr_nearby"] > 0)]
    print(f"  N={len(conf)}/{(df['status']=='in_effect').sum()}")


if __name__ == "__main__":
    main()
