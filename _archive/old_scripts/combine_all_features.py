"""Combine all features for consensus A class:
- LLM features (median of 3 Claude + 1 GPT, from features_aggregated.parquet)
- Dictionary features (L-M lite, NRC-lite, etc., from extract_features logic)
- Regex stylistic features (caps, emoji, exclamation, etc.)
- Metadata (date, target, etc., from consensus_a.parquet)

Output: data/processed/all_features.parquet
"""
from __future__ import annotations
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Reuse logic from extract_features.py
import sys
sys.path.insert(0, str(ROOT / "src"))
from extract_features import feature_text, add_temporal_features  # noqa

CONSENSUS = ROOT / "data" / "processed" / "consensus_a.parquet"
LLM_FEATS = ROOT / "data" / "processed" / "features_aggregated.parquet"
OUT = ROOT / "data" / "processed" / "all_features.parquet"


# Additional stylistic features (user-requested)
def stylistic_features(text: str) -> dict:
    """Caps phrases, emoji, exclamation, etc. — pure regex."""
    if not isinstance(text, str):
        text = ""
    tokens = re.findall(r"\S+", text)
    n_tokens = max(len(tokens), 1)
    n_chars = max(len(text), 1)

    # Caps phrases (3+ consecutive all-caps words)
    caps_phrase_matches = re.findall(r"\b(?:[A-Z]{2,}\W+){2,}[A-Z]{2,}\b", text)
    # All-caps sentence (entire sentence in caps)
    all_caps_sent = re.findall(r"[A-Z][A-Z\s\d!?.,;:'\"-]{20,}", text)
    # Exclamation density
    excl = text.count("!")
    # Multi-exclamation chains
    excl_chains = len(re.findall(r"!!+", text))
    # Ellipsis
    ellipsis = len(re.findall(r"\.{2,}", text))
    # Emoji (rough — count high-unicode chars)
    emoji = len(re.findall(r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF]", text))
    # Word repetition (max times any word repeats in post)
    word_counts = pd.Series(re.findall(r"\b[a-zA-Z]+\b", text.lower())).value_counts()
    word_rep_max = int(word_counts.max()) if len(word_counts) else 0
    # Char elongation (e.g., GREAAAT)
    char_elong = len(re.findall(r"([a-zA-Z])\1{2,}", text))
    return {
        "exclamation_density": excl / n_tokens,
        "exclamation_chains": excl_chains,
        "caps_phrase_count": len(caps_phrase_matches),
        "all_caps_sentence_count": len(all_caps_sent),
        "ellipsis_count": ellipsis,
        "emoji_count": emoji,
        "word_repetition_max": word_rep_max,
        "char_elongation_count": char_elong,
        "_n_tokens_text": n_tokens,
    }


def main():
    consensus = pd.read_parquet(CONSENSUS)
    llm = pd.read_parquet(LLM_FEATS)
    print(f"[load] consensus={len(consensus)}  llm_feats={len(llm)}")

    consensus["_id"] = consensus["_id"].astype(str)
    llm["_id"] = llm["_id"].astype(str)

    # Extract regex/dict features per consensus post
    dict_feats = consensus["content"].apply(feature_text).apply(pd.Series)
    style_feats = consensus["content"].apply(stylistic_features).apply(pd.Series)
    consensus_features = pd.concat(
        [consensus.reset_index(drop=True),
         dict_feats.reset_index(drop=True),
         style_feats.reset_index(drop=True)],
        axis=1,
    )

    # Temporal features (recurrence, etc.)
    consensus_features = consensus_features.rename(columns={"id": "_id_post"})
    # add_temporal_features expects 'target' column (from rule-based labeler) — use claude_policy if missing
    if "target" not in consensus_features.columns:
        consensus_features["target"] = consensus_features.get("claude_policy", consensus_features.get("gpt_policy"))
    consensus_features = add_temporal_features(consensus_features)

    # Merge LLM-rated features
    final = consensus_features.merge(llm, on="_id", how="left")
    print(f"[merged] {len(final)} rows × {len(final.columns)} cols")
    final.to_parquet(OUT)
    print(f"[saved] {OUT}")

    # Print all feature columns summary
    feat_cols = [c for c in final.columns if not c.startswith("_")
                 and c not in ("id", "content", "url", "media", "year_month",
                               "year_month_dup", "date", "claude_label", "gpt_label",
                               "claude_policy", "gpt_policy", "claude_commissive",
                               "gpt_commissive", "claude_conf", "gpt_conf",
                               "target", "target_entity", "policy_action",
                               "deadline_phrase", "claude_1__target_entity")]
    feat_cols = [c for c in feat_cols if not c.endswith("__target_entity")
                 and not c.endswith("__policy_action") and not c.endswith("__deadline_phrase")]
    print(f"\nNumeric feature columns ({len(feat_cols)}):")
    for c in feat_cols[:30]:
        print(f"  {c}")
    if len(feat_cols) > 30:
        print(f"  ... and {len(feat_cols) - 30} more")


if __name__ == "__main__":
    main()
