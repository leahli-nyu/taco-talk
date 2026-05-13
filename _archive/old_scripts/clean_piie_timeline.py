"""Clean PIIE Trump Trade War Timeline CSV (user-downloaded from Google Sheets).

Input: data/raw/Trump's trade war timeline 2.0_ An up-to-date guide - Sheet1.csv
Output: data/processed/piie_timeline_clean.parquet

Inferring 'outcome' from Category + Description text:
  - Tariff (in effect / paused / withdrawn / struck down)
  - Deal (reduced tariffs, exemption granted)
  - Threat (announcement before implementation)
  - Investigation (Section 232/301 initiated)
"""
from __future__ import annotations
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN_FP = ROOT / "data" / "raw" / "Trump’s trade war timeline 2.0_ An up-to-date guide - Sheet1.csv"
OUT_FP = ROOT / "data" / "processed" / "piie_timeline_clean.parquet"

def parse_date(s):
    if pd.isna(s) or not isinstance(s, str): return None
    try:
        return pd.to_datetime(s, format="%d-%b-%y").date()
    except Exception:
        try:
            return pd.to_datetime(s).date()
        except Exception:
            return None

# Status inference patterns
STATUS_PATTERNS = [
    (re.compile(r"\b(withdr[aw]|retract|backed? off|pause|delay|reduce|exempt|deal)\b", re.I), "modified_or_withdrawn"),
    (re.compile(r"\bstruck down|invalidat|court rul|supreme court\b", re.I), "struck_down"),
    (re.compile(r"\bin effect|impose|enact|effective|implement|go(?:es)? into\b", re.I), "in_effect"),
    (re.compile(r"\b(announce|threat|warn|promise|will|going to|plans?)\b", re.I), "announced"),
    (re.compile(r"\binvestigat|inquiry|review\b", re.I), "investigation"),
]

def infer_status(text):
    if pd.isna(text) or not isinstance(text, str): return "unknown"
    for pat, status in STATUS_PATTERNS:
        if pat.search(text):
            return status
    return "other"

def main():
    df = pd.read_csv(IN_FP)
    # Keep only rows with Date + Description (drop section dividers)
    df = df[df["Date"].notna() & df["Description"].notna()].copy()
    df["date"] = df["Date"].apply(parse_date)
    df = df[df["date"].notna()].reset_index(drop=True)
    df = df.rename(columns={"Country": "country", "Category": "category",
                            "Description": "description", "Links": "links"})
    df["status_inferred"] = df["description"].apply(infer_status)
    df = df[["date", "country", "category", "description", "links", "status_inferred"]]
    df.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}  rows={len(df)}")
    print("\nStatus distribution:")
    print(df["status_inferred"].value_counts())
    print("\nCategory distribution (top 15):")
    print(df["category"].value_counts().head(15))
    print("\nCountry distribution (top 10):")
    print(df["country"].value_counts().head(10))
    return df

if __name__ == "__main__":
    main()
