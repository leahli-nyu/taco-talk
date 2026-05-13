"""Fetch Trump posts from public archives.

Sources:
  - Trump Twitter Archive (2009-2021):
      https://www.thetrumparchive.com/  (CSV available)
  - Truth Social 2024 Election dataset:
      https://github.com/kashish-s/TruthSocial_2024ElectionInitiative
  - Kaggle: muhammetakkurt/trump-2024-campaign-truthsocial-truths-tweets

This script downloads the public CSVs and produces a unified DataFrame
with columns: id, platform, date, text, is_repost, raw_metadata.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import requests
import pandas as pd

TRUMP_TWITTER_CSV = (
    "https://raw.githubusercontent.com/MarkHershey/CompleteTrumpTweetsArchive/"
    "master/data/realDonaldTrump_in_office.csv"
)

def download(url: str, dest: Path) -> Path:
    if dest.exists():
        print(f"[skip] {dest} exists")
        return dest
    print(f"[get]  {url}")
    r = requests.get(url, timeout=60,
                     headers={"User-Agent": "academic-research/1.0"})
    r.raise_for_status()
    dest.write_bytes(r.content)
    print(f"[saved] {dest}  size={dest.stat().st_size}")
    return dest

def load_twitter(fp: Path) -> pd.DataFrame:
    df = pd.read_csv(fp)
    # Normalize columns (the archive has been re-released a few times; cope)
    df.columns = [c.lower() for c in df.columns]
    text_col = "content" if "content" in df.columns else "text"
    date_col = "date" if "date" in df.columns else "created_at"
    out = pd.DataFrame({
        "id": df.get("id", pd.RangeIndex(len(df))).astype(str),
        "platform": "twitter",
        "date": pd.to_datetime(df[date_col], errors="coerce"),
        "text": df[text_col].astype(str),
        "is_repost": df.get("is_retweet", False),
    })
    return out.dropna(subset=["date", "text"])

def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    tw_fp = out_dir / "trump_twitter.csv"
    download(TRUMP_TWITTER_CSV, tw_fp)
    tw = load_twitter(tw_fp)
    print(f"[twitter] rows={len(tw)}  date_range={tw.date.min()}..{tw.date.max()}")
    # Truth Social: user needs to download via Kaggle/GitHub manually
    # (avoids putting Kaggle credentials in this script)
    truth_path = out_dir / "trump_truthsocial.csv"
    if not truth_path.exists():
        print(f"[note] Truth Social data not found at {truth_path}.")
        print("       Download from one of:")
        print("       - https://github.com/kashish-s/TruthSocial_2024ElectionInitiative")
        print("       - https://www.kaggle.com/datasets/muhammetakkurt/trump-2024-campaign-truthsocial-truths-tweets")
        unified = tw
    else:
        ts = pd.read_csv(truth_path)
        ts.columns = [c.lower() for c in ts.columns]
        ts_norm = pd.DataFrame({
            "id": ts.get("id", pd.RangeIndex(len(ts))).astype(str),
            "platform": "truthsocial",
            "date": pd.to_datetime(ts.get("created_at", ts.get("date")), errors="coerce"),
            "text": ts.get("content", ts.get("text")).astype(str),
            "is_repost": ts.get("is_retweet", False),
        }).dropna(subset=["date", "text"])
        unified = pd.concat([tw, ts_norm], ignore_index=True)
    unified.to_parquet(out_dir / "trump_posts_unified.parquet")
    print(f"[saved] {out_dir / 'trump_posts_unified.parquet'}  rows={len(unified)}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="data/raw")
    a = p.parse_args()
    main(Path(a.out))
