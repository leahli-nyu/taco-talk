"""Filter Trump posts down to tariff-related threats (pre-labeling).

This is the *pre-filter* — strict regex / keyword filter to narrow the corpus
from ~50K posts to a few hundred candidates for LLM labeling.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path
import pandas as pd

TARIFF_TERMS = [
    r"\btariff", r"\bduties\b", r"\bduty\b",
    r"\bimport tax", r"\btrade deal", r"\btrade war",
    r"\bsection\s*(232|301)", r"\bUSMCA\b",
    r"\bsanction", r"\bembargo",
]

THREAT_MARKERS = [
    r"\bwill\b", r"\bgoing to\b", r"\bplan(?:s|ning)?\b",
    r"\bif (?:they|china|mexico|canada|eu|europe)",
    r"\b(?:i|we) will (?:impose|put|add|raise|hit|slap)",
    r"\b\d{1,3}\s*%", r"\b\d{1,3}\s*percent",
]

T_PAT = re.compile("|".join(TARIFF_TERMS), re.I)
THR_PAT = re.compile("|".join(THREAT_MARKERS), re.I)

def is_candidate(text: str) -> tuple[bool, dict]:
    """Return (is_candidate, evidence_dict)."""
    if not isinstance(text, str):
        return False, {}
    has_tariff = bool(T_PAT.search(text))
    has_threat = bool(THR_PAT.search(text))
    has_percent = bool(re.search(r"\b\d{1,3}\s*%", text))
    evidence = {
        "has_tariff_term": has_tariff,
        "has_threat_marker": has_threat,
        "has_percent": has_percent,
    }
    # Be permissive at this stage; LLM will filter further
    return (has_tariff and (has_threat or has_percent)), evidence

def main(in_fp: Path, out_dir: Path) -> None:
    df = pd.read_parquet(in_fp)
    print(f"[load] {len(df)} posts from {in_fp}")
    df = df[~df["is_repost"].fillna(False)]
    print(f"[filter repost] {len(df)} remaining")
    keep, evid = [], []
    for txt in df["text"]:
        ok, e = is_candidate(txt)
        keep.append(ok)
        evid.append(e)
    df = df.assign(**pd.DataFrame(evid))
    cand = df[keep].copy().reset_index(drop=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    fp = out_dir / "tariff_threat_candidates.parquet"
    cand.to_parquet(fp)
    print(f"[saved] {fp}  candidates={len(cand)}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_fp",
                   default="data/raw/trump_posts_unified.parquet")
    p.add_argument("--out", default="data/processed")
    a = p.parse_args()
    main(Path(a.in_fp), Path(a.out))
