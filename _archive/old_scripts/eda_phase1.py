"""Phase 1 EDA: data overview after loading Truth Social archive.

Produces:
  - data/processed/truth_second_term.parquet  (cleaned, only second term)
  - figures/eda01_posts_per_month.png
  - figures/eda02_post_length_dist.png
  - figures/eda03_hour_of_day.png
  - data/processed/eda_summary.json (numerical stats for the user)
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "truth_archive.json"
OUT_DATA = ROOT / "data" / "processed"
OUT_FIG = ROOT / "figures"
OUT_DATA.mkdir(parents=True, exist_ok=True)
OUT_FIG.mkdir(parents=True, exist_ok=True)

# Second term era: from Nov 6, 2024 (AP called the race) onward.
# Pre-inauguration period (Nov 6, 2024 → Jan 19, 2025) counts because
# the market treated him as president-elect from race-call onward.
SECOND_TERM_START = "2024-11-06"

def load() -> pd.DataFrame:
    print(f"[load] {RAW}")
    data = json.loads(RAW.read_text())
    df = pd.DataFrame(data)
    df["created_at"] = pd.to_datetime(df["created_at"])
    print(f"  raw entries: {len(df):,}")
    return df

def classify_entry(row) -> str:
    """Classify each entry: original / repost / empty."""
    c = str(row.get("content", "")).strip()
    if not c:
        return "empty"
    # Reposts have content = just a truthsocial URL
    if c.startswith("http") and "truthsocial.com/users/" in c and len(c.split()) < 3:
        return "repost"
    return "original"

def main():
    df = load()
    df["entry_type"] = df.apply(classify_entry, axis=1)
    df["text_length"] = df["content"].astype(str).str.len()
    df["hour"] = df["created_at"].dt.hour
    df["date"] = df["created_at"].dt.date
    df["year_month"] = df["created_at"].dt.to_period("M").astype(str)

    # Filter to second term originals
    mask_2nd = df["created_at"] >= SECOND_TERM_START
    mask_orig = df["entry_type"] == "original"
    df_2nd = df[mask_2nd & mask_orig].copy().reset_index(drop=True)

    print(f"\n[second term originals] {len(df_2nd):,} posts")
    print(f"  date range: {df_2nd.created_at.min()} → {df_2nd.created_at.max()}")

    # Save filtered second-term data
    out_fp = OUT_DATA / "truth_second_term.parquet"
    df_2nd[[
        "id", "created_at", "content", "text_length", "hour", "date",
        "replies_count", "reblogs_count", "favourites_count",
    ]].to_parquet(out_fp)
    print(f"[saved] {out_fp}")

    # Plots
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Plot 1: posts per month
        counts = df_2nd.groupby("year_month").size().reset_index(name="n")
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.bar(counts["year_month"], counts["n"])
        ax.set_title(f"Trump Truth Social original posts per month (second term, N={len(df_2nd):,})")
        ax.set_xlabel("month"); ax.set_ylabel("count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(OUT_FIG / "eda01_posts_per_month.png", dpi=120)
        plt.close()
        print(f"[saved] {OUT_FIG / 'eda01_posts_per_month.png'}")

        # Plot 2: post length distribution
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(df_2nd["text_length"].clip(upper=1500), bins=60)
        ax.set_title("Post length distribution (chars, clipped at 1500)")
        ax.set_xlabel("characters"); ax.set_ylabel("count")
        plt.tight_layout()
        plt.savefig(OUT_FIG / "eda02_post_length_dist.png", dpi=120)
        plt.close()
        print(f"[saved] {OUT_FIG / 'eda02_post_length_dist.png'}")

        # Plot 3: hour of day (UTC, since CNN data is in Z)
        fig, ax = plt.subplots(figsize=(8, 4))
        hr_counts = df_2nd["hour"].value_counts().sort_index()
        ax.bar(hr_counts.index, hr_counts.values)
        ax.set_title("Posting time (hour of day, UTC)")
        ax.set_xlabel("hour"); ax.set_ylabel("count")
        ax.set_xticks(range(0, 24))
        plt.tight_layout()
        plt.savefig(OUT_FIG / "eda03_hour_of_day.png", dpi=120)
        plt.close()
        print(f"[saved] {OUT_FIG / 'eda03_hour_of_day.png'}")
    except Exception as e:
        print(f"[plot warn] {e}")

    # Summary stats JSON
    summary = {
        "second_term_start": SECOND_TERM_START,
        "raw_total_entries": len(df),
        "raw_originals": int((df.entry_type == "original").sum()),
        "raw_reposts": int((df.entry_type == "repost").sum()),
        "raw_empty": int((df.entry_type == "empty").sum()),
        "second_term_originals": len(df_2nd),
        "second_term_date_range": [
            str(df_2nd.created_at.min()),
            str(df_2nd.created_at.max()),
        ],
        "median_post_length_chars": float(df_2nd.text_length.median()),
        "mean_post_length_chars": float(df_2nd.text_length.mean()),
        "max_post_length_chars": int(df_2nd.text_length.max()),
        "posts_per_month": df_2nd.groupby("year_month").size().to_dict(),
    }
    (OUT_DATA / "eda_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"[saved] {OUT_DATA / 'eda_summary.json'}")

    return df_2nd, summary

if __name__ == "__main__":
    main()
