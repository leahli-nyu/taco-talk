"""Episode clustering for consensus A class, using bge-large embedding.

Input: data/processed/all_features.parquet (141 posts)
Output: data/processed/episodes_v2.parquet  (episode-level aggregates)
        data/processed/all_features.parquet (updated with episode_id column)
"""
from __future__ import annotations
import os
from pathlib import Path
from datetime import timedelta
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Load .env
_env = ROOT / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")

IN_FP = ROOT / "data" / "processed" / "all_features.parquet"
OUT_EPS = ROOT / "data" / "processed" / "episodes_v2.parquet"


def embed(texts: list[str]) -> np.ndarray:
    try:
        from sentence_transformers import SentenceTransformer
        print("[embed] loading BAAI/bge-large-en-v1.5 (first call may download ~1.3GB)")
        model = SentenceTransformer("BAAI/bge-large-en-v1.5")
        print(f"[embed] encoding {len(texts)} texts")
        return model.encode(texts, batch_size=8, show_progress_bar=False, normalize_embeddings=True)
    except Exception as e:
        print(f"[fallback] sentence-transformers failed: {e}")
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import normalize
        vec = TfidfVectorizer(max_features=2000, ngram_range=(1, 2),
                              stop_words="english", min_df=2)
        X = vec.fit_transform(texts).toarray().astype(np.float32)
        return normalize(X, norm="l2", axis=1)


def cluster_episodes(df: pd.DataFrame, emb: np.ndarray, sim_thr=0.82, window_days=30):
    """Single-link union-find with both cosine sim AND date window."""
    df = df.sort_values("created_at").reset_index(drop=True)
    n = len(df)
    sim = emb @ emb.T  # normalized
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[max(ra, rb)] = min(ra, rb)

    dates = pd.to_datetime(df["created_at"]).dt.date.tolist()
    for i in range(n):
        for j in range(i + 1, n):
            day_diff = (dates[j] - dates[i]).days
            if day_diff > window_days: break
            if sim[i, j] > sim_thr:
                union(i, j)

    df["episode_id"] = [find(i) for i in range(n)]
    label_map = {ep: idx for idx, ep in enumerate(sorted(df["episode_id"].unique()))}
    df["episode_id"] = df["episode_id"].map(label_map)
    return df


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate post-level data to episode-level."""
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    # First-post features (for predicting outcome)
    fp_first = df.sort_values("created_at").groupby("episode_id").first().reset_index()
    # Numeric feature columns
    LLM_FEATS = [f"claude_med__{f}" for f in [
        "commitment_strength", "specificity", "hedging_level", "dramatization",
        "conditional_framing", "audience_cost", "precedent_invocation",
        "negotiation_framing", "personal_attack", "ego_centric_framing",
    ]]
    DICT_FEATS = ["deontic_strength", "temporal_specificity", "has_conditional",
                  "ner_target_proxy", "number_count", "all_caps_ratio",
                  "affect_count", "lm_hedging", "lm_uncertainty"]
    STYLE_FEATS = ["exclamation_density", "exclamation_chains", "caps_phrase_count",
                   "all_caps_sentence_count", "ellipsis_count", "emoji_count",
                   "word_repetition_max", "char_elongation_count"]
    TEMP_FEATS = ["repeat_count_7d", "is_first_mention", "neighbor_event_count"]
    ALL_FEATS = LLM_FEATS + DICT_FEATS + STYLE_FEATS + TEMP_FEATS

    target_col = None
    for cand in ("target_entity", "claude_1__target_entity", "target"):
        if cand in df.columns:
            target_col = cand
            break

    agg_dict = dict(
        n_posts=("_id", "count"),
        first_post_date=("created_at", "min"),
        last_post_date=("created_at", "max"),
        first_post_id=("_id", lambda s: s.iloc[0] if len(s) else None),
        all_text=("content", lambda s: " || ".join(str(x)[:200] for x in s.iloc[:5])),
        first_text=("content", "first"),
    )
    if target_col:
        agg_dict["any_target"] = (target_col, lambda s: s.dropna().mode().iloc[0] if s.dropna().any() else None)
    eps = df.groupby("episode_id").agg(**agg_dict).reset_index()
    eps["episode_span_days"] = (eps["last_post_date"] - eps["first_post_date"]).dt.days

    # Attach first-post numeric features
    for f in ALL_FEATS:
        if f in fp_first.columns:
            eps = eps.merge(fp_first[["episode_id", f]].rename(columns={f: f"fp__{f}"}),
                            on="episode_id", how="left")

    return eps


def main():
    df = pd.read_parquet(IN_FP)
    print(f"[load] {len(df)} consensus A posts")
    texts = df["content"].astype(str).tolist()
    emb = embed(texts)
    print(f"[embed] shape={emb.shape}")
    clustered = cluster_episodes(df, emb)
    n_ep = clustered["episode_id"].nunique()
    print(f"[cluster] {n_ep} episodes from {len(clustered)} posts")
    clustered.to_parquet(IN_FP)
    print(f"[saved] {IN_FP} (added episode_id)")
    eps = aggregate(clustered)
    eps.to_parquet(OUT_EPS)
    print(f"[saved] {OUT_EPS}")
    print(f"\nEpisode size distribution:")
    print(eps["n_posts"].value_counts().sort_index())
    print(f"\nEpisode span (days):")
    print(eps["episode_span_days"].describe())


if __name__ == "__main__":
    main()
