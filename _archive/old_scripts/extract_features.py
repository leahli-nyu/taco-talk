"""Feature extraction for A-class threats.

12 baseline features (per DECISIONS.md):
 1. deontic_strength       — modal commitment score
 2. temporal_specificity   — deadline phrase concreteness
 3. has_conditional        — "if/unless/until" present
 4. ner_target_count       — named entities for targets
 5. number_count           — % and $ figures
 6. all_caps_ratio         — fraction of all-caps words
 7. affect_count           — emotional words (NRC-lite)
 8. lm_hedging             — Loughran-McDonald weak-modal/hedging count
 9. lm_uncertainty         — L-M uncertainty count
10. repeat_count_7d        — recurring same-topic in last 7d
11. is_first_mention       — dummy
12. neighbor_event_count   — # of A-class threats in [-6h, +6h]
"""
from __future__ import annotations
import re
from pathlib import Path
from datetime import timedelta
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LABELED_FP = ROOT / "data" / "processed" / "labeled_abc.parquet"
CANDIDATES_FP = ROOT / "data" / "processed" / "econ_candidates.parquet"
OUT_FP = ROOT / "data" / "processed" / "features.parquet"

# Deontic modal dictionary with strength
DEONTIC = {
    # commit (high)
    "will": 1.0, "going to": 1.0, "gonna": 1.0,
    "shall": 0.9, "must": 0.9, "have to": 0.85,
    "intend to": 0.8, "plan to": 0.75, "planning to": 0.75,
    # neutral
    "should": 0.5, "ought to": 0.5,
    # weak
    "may": 0.3, "might": 0.25, "could": 0.25, "would consider": 0.2,
    "thinking about": 0.2, "looking at": 0.2,
    "possibly": 0.15,
}

# L-M lite (handful of the most common; full dict is 600+ but these dominate)
LM_HEDGING = {"may", "might", "could", "perhaps", "possibly", "potentially",
              "approximately", "roughly", "appears", "seems", "suggests",
              "indicates", "tends"}
LM_UNCERTAINTY = {"approximate", "approximately", "depend", "depending", "depends",
                  "fluctuate", "fluctuates", "probably", "probable", "uncertain",
                  "uncertainty", "unknown", "unstable", "unpredictable", "vague",
                  "variability", "volatile"}

# NRC-lite affect words (a small high-frequency subset)
AFFECT_WORDS = {
    "terrible", "horrible", "awful", "disaster", "catastrophic", "destroyed",
    "great", "fantastic", "amazing", "wonderful", "tremendous", "huge", "massive",
    "beautiful", "incredible", "winning", "winners", "losers", "weak", "strong",
    "evil", "stupid", "dumb", "smart", "genius", "rigged", "unfair", "fair",
    "fake", "true", "real",
}

# Conditional structure markers
CONDITIONAL = re.compile(r"\b(if|unless|until|when they|provided that)\b", re.I)

# Temporal phrases (deadline specificity)
TEMPORAL_PATTERNS = [
    (re.compile(r"\b(today|tomorrow|tonight|this morning|this afternoon)\b", re.I), 3),
    (re.compile(r"\b(by|in)\s+(\d+\s*(?:days?|hours?|weeks?|months?))\b", re.I), 3),
    (re.compile(r"\b(this|next)\s+(week|month|quarter|year)\b", re.I), 2),
    (re.compile(r"\b(soon|shortly|imminent)\b", re.I), 1),
    (re.compile(r"\b(eventually|someday|down the road)\b", re.I), 0),
]

NUMBER_PATTERN = re.compile(r"(\d{1,4}\s*%|\$\s*\d|\d+\s*(?:billion|million|trillion|percent))", re.I)

def feature_text(text: str) -> dict:
    """Extract per-post text features (features 1-9 only — temporal features need date join)."""
    if not isinstance(text, str):
        text = ""
    lower = text.lower()
    tokens = re.findall(r"[a-zA-Z]+|\d+", text)
    n_tokens = max(len(tokens), 1)

    # 1. Deontic strength (max match)
    deontic_score = 0.0
    for phrase, w in DEONTIC.items():
        if re.search(rf"\b{re.escape(phrase)}\b", lower):
            deontic_score = max(deontic_score, w)

    # 2. Temporal specificity (max match)
    temporal_score = 0
    for pat, s in TEMPORAL_PATTERNS:
        if pat.search(text):
            temporal_score = max(temporal_score, s)

    # 3. Conditional
    has_conditional = int(bool(CONDITIONAL.search(text)))

    # 4. NER target count — light proxy (capitalized 2+ char tokens not at sentence start)
    cap_tokens = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)
    ner_proxy = max(0, len(set(cap_tokens)) - 5)  # subtract baseline of generic caps

    # 5. Numbers
    number_count = len(NUMBER_PATTERN.findall(text))

    # 6. All-caps ratio
    all_caps_tokens = re.findall(r"\b[A-Z]{2,}\b", text)
    all_caps_ratio = len(all_caps_tokens) / n_tokens

    # 7. Affect
    lower_tokens = re.findall(r"[a-z]+", lower)
    affect_count = sum(1 for t in lower_tokens if t in AFFECT_WORDS)

    # 8. L-M hedging
    lm_hedge = sum(1 for t in lower_tokens if t in LM_HEDGING)

    # 9. L-M uncertainty
    lm_uncertain = sum(1 for t in lower_tokens if t in LM_UNCERTAINTY)

    return {
        "deontic_strength": deontic_score,
        "temporal_specificity": temporal_score,
        "has_conditional": has_conditional,
        "ner_target_proxy": ner_proxy,
        "number_count": number_count,
        "all_caps_ratio": all_caps_ratio,
        "affect_count": affect_count,
        "lm_hedging": lm_hedge,
        "lm_uncertainty": lm_uncertain,
        "n_tokens": n_tokens,
    }

def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add 10/11/12: temporal-context features that need the full dataframe."""
    df = df.sort_values("created_at").reset_index(drop=True)
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    repeat_counts, first_mentions, neighbor_counts = [], [], []
    # We use the LLM-extracted target if available, else fall back to the post id
    targets = df["target"].fillna("UNKNOWN").astype(str).tolist()
    dts = df["created_at"].tolist()
    n = len(df)
    for i in range(n):
        d, tgt = dts[i], targets[i]
        # 7-day backward window
        cutoff_7d = d - timedelta(days=7)
        same_topic_recent = 0
        for j in range(i):
            if dts[j] >= cutoff_7d and targets[j] == tgt and tgt != "UNKNOWN":
                same_topic_recent += 1
        repeat_counts.append(same_topic_recent)
        first_mentions.append(int(same_topic_recent == 0))
        # ±6h neighbor (any A-class)
        cutoff_lo = d - timedelta(hours=6)
        cutoff_hi = d + timedelta(hours=6)
        neighbors = 0
        for j in range(n):
            if j == i: continue
            if cutoff_lo <= dts[j] <= cutoff_hi:
                neighbors += 1
        neighbor_counts.append(neighbors)
    df["repeat_count_7d"] = repeat_counts
    df["is_first_mention"] = first_mentions
    df["neighbor_event_count"] = neighbor_counts
    return df

def main():
    # Need labeled_abc.parquet to exist — wait for labeler
    if not LABELED_FP.exists():
        print(f"[wait] {LABELED_FP} not yet present. Run llm_label_abc.py first.")
        return
    labels = pd.read_parquet(LABELED_FP)
    # LLM labeler stores _text (truncated). Join back full content + created_at
    # from candidates so feature_text() sees full post.
    if "content" not in labels.columns:
        cand = pd.read_parquet(CANDIDATES_FP)[["id", "created_at", "content"]].rename(
            columns={"id": "_id"}
        )
        labels["_id"] = labels["_id"].astype(str)
        cand["_id"] = cand["_id"].astype(str)
        labels = labels.merge(cand, on="_id", how="left", suffixes=("", "_dup"))
        # if both _date and created_at exist, drop the latter and re-derive
        if "created_at" not in labels.columns and "_date" in labels.columns:
            labels["created_at"] = pd.to_datetime(labels["_date"], errors="coerce")
    # Filter to A class for main analysis
    a_class = labels[labels["label"] == "A"].copy()
    print(f"[A class] {len(a_class)} posts")

    # Extract text features
    text_feats = a_class["content"].apply(feature_text).apply(pd.Series)
    a_class = pd.concat([a_class.reset_index(drop=True),
                         text_feats.reset_index(drop=True)], axis=1)

    # Add temporal features
    a_class = add_temporal_features(a_class)

    a_class.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}")
    print(a_class[["deontic_strength", "temporal_specificity", "has_conditional",
                   "number_count", "all_caps_ratio", "affect_count",
                   "repeat_count_7d", "neighbor_event_count"]].describe())

if __name__ == "__main__":
    main()
