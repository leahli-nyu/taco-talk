"""Find n-grams distinctive of each Y1 outcome.

For each outcome class, compute pointwise mutual information of n-grams
relative to the corpus baseline. Surfaces phrases like "going to impose",
"absolutely", "perhaps", "next week" etc. that distinguish executed from
withdrawn threats.

Useful as:
  - feature engineering inspiration
  - paper Discussion fodder
  - app showcase of "tells"
"""
from __future__ import annotations
import json
import re
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN_FP = ROOT / "data" / "processed" / "threats_with_outcomes_v2.parquet"
OUT = ROOT / "data" / "processed" / "contrastive_ngrams.json"

STOPWORDS = set("""
the of a an in on at to for is are was were be been being have has had do does did
i we my our you your he she his her it its they them their this that these those
and or but if so as that not no yes one two three with by from up out over under
about there here when what who which why how very really just only also too more
most some any all each every its been would could should might may will going
""".split())

def tokenize(text: str) -> list[str]:
    if not isinstance(text, str): return []
    text = text.lower()
    # strip URLs
    text = re.sub(r"https?://\S+", " ", text)
    tokens = re.findall(r"[a-z]+", text)
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

def ngrams(tokens: list[str], n: int) -> list[str]:
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def top_distinctive(corpus_a: list[str], corpus_b: list[str], n: int, k: int = 25, min_count: int = 3) -> list[tuple]:
    """Top k n-grams more common in A relative to B (using PMI-like score)."""
    grams_a = Counter()
    grams_b = Counter()
    for txt in corpus_a:
        grams_a.update(ngrams(tokenize(txt), n))
    for txt in corpus_b:
        grams_b.update(ngrams(tokenize(txt), n))
    total_a = sum(grams_a.values()) or 1
    total_b = sum(grams_b.values()) or 1
    scores = []
    for w, ca in grams_a.items():
        if ca < min_count: continue
        cb = grams_b.get(w, 0)
        # Laplace smoothing
        pa = (ca + 1) / (total_a + len(grams_a))
        pb = (cb + 1) / (total_b + len(grams_b))
        scores.append((w, ca, cb, float(np.log(pa / pb))))
    scores.sort(key=lambda x: x[3], reverse=True)
    return scores[:k]

def main():
    df = pd.read_parquet(IN_FP)
    print(f"[load] {len(df)} A-class threats")

    by_outcome = df.groupby("y1_outcome")["content"].apply(list).to_dict()
    print("\nOutcome corpus sizes:")
    for k, v in by_outcome.items():
        print(f"  {k:30s} n={len(v)}")

    pairs_to_compare = [
        ("executed", "modified_or_withdrawn"),
        ("modified_or_withdrawn", "executed"),
        ("executed", "announced_unresolved"),
        ("struck_down", "executed"),
    ]
    out = {"_meta": {"corpus_size_by_outcome": {k: len(v) for k, v in by_outcome.items()}}}

    for a, b in pairs_to_compare:
        if a not in by_outcome or b not in by_outcome:
            print(f"  skip {a} vs {b} (missing class)")
            continue
        if len(by_outcome[a]) < 5 or len(by_outcome[b]) < 5:
            print(f"  skip {a} vs {b} (class too small)")
            continue
        for n in [1, 2, 3]:
            print(f"\n>>> Top {n}-grams in {a!r} vs {b!r}:")
            top = top_distinctive(by_outcome[a], by_outcome[b], n)
            for w, ca, cb, s in top[:10]:
                print(f"  {w:40s}  count={ca:3d} (vs {cb:3d})  logpmi={s:+.3f}")
            out[f"{a}_vs_{b}_{n}grams"] = [
                {"phrase": w, "count_a": ca, "count_b": cb, "log_pmi": s}
                for w, ca, cb, s in top
            ]

    OUT.write_text(json.dumps(out, indent=2))
    print(f"\n[saved] {OUT}")

if __name__ == "__main__":
    main()
