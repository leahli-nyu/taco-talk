"""Cluster A-class threats into 'policy episodes' (same-topic sequences).

Pipeline:
  1. Sentence-transformer embedding of each post
  2. Episode = posts within 30 days with cosine similarity > 0.55 OR
     posts in same fortnight + LLM-assigned target match
  3. LLM names each episode
  4. Output: episodes parquet + topic labels JSON

Episode-level features:
  - first_post_date, last_post_date
  - n_posts (recurrence)
  - anticipation_period (days from first post to matched PIIE event)
  - first_post_features (snapshot when episode started)
  - max_intensity_features (peak rhetoric)
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from datetime import timedelta
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Load .env
env = ROOT / ".env"
if env.exists():
    for line in env.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

THREATS_FP = ROOT / "data" / "processed" / "threats_with_outcomes_v2.parquet"
LABELED_FP = ROOT / "data" / "processed" / "labeled_abc.parquet"
EPISODES_FP = ROOT / "data" / "processed" / "episodes.parquet"
TOPICS_FP = ROOT / "data" / "processed" / "episode_topics.json"

# Lazy imports
def _embed(texts: list[str]) -> np.ndarray:
    try:
        from sentence_transformers import SentenceTransformer
        # Upgrade from MiniLM (384d) to BGE-large (1024d) for better clustering quality
        model = SentenceTransformer("BAAI/bge-large-en-v1.5")
        return model.encode(texts, batch_size=16, show_progress_bar=False, normalize_embeddings=True)
    except Exception as e:
        print(f"  [warn] sentence-transformers failed ({e!s:.80}), falling back to TF-IDF")
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import normalize
        vec = TfidfVectorizer(max_features=2000, ngram_range=(1, 2),
                              stop_words="english", min_df=2)
        X = vec.fit_transform(texts).toarray().astype(np.float32)
        return normalize(X, norm="l2", axis=1)

def cosine_sim_matrix(emb: np.ndarray) -> np.ndarray:
    return emb @ emb.T   # already normalized

def cluster_into_episodes(df: pd.DataFrame, emb: np.ndarray, sim_threshold=0.55, window_days=30) -> pd.DataFrame:
    df = df.sort_values("created_at").reset_index(drop=True)
    n = len(df)
    sim = cosine_sim_matrix(emb)
    parent = list(range(n))   # union-find

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
            if sim[i, j] > sim_threshold:
                union(i, j)

    df["episode_id"] = [find(i) for i in range(n)]
    # Relabel to compact integers
    label_map = {ep: idx for idx, ep in enumerate(sorted(df["episode_id"].unique()))}
    df["episode_id"] = df["episode_id"].map(label_map)
    return df

def aggregate_episodes(df: pd.DataFrame) -> pd.DataFrame:
    df["created_at"] = pd.to_datetime(df["created_at"])
    eps = df.groupby("episode_id").agg(
        n_posts=("_id", "count"),
        first_post_date=("created_at", "min"),
        last_post_date=("created_at", "max"),
        any_target=("target", lambda s: s.dropna().mode().iloc[0] if s.dropna().any() else None),
        first_text=("content", lambda s: s.iloc[0][:300] if isinstance(s.iloc[0], str) else ""),
        all_text=("content", lambda s: " || ".join(str(x)[:200] for x in s.iloc[:5])),
    ).reset_index()
    eps["episode_span_days"] = (eps["last_post_date"] - eps["first_post_date"]).dt.days
    return eps

def name_episodes_with_llm(episodes: pd.DataFrame) -> dict:
    """Use Claude Haiku to name each episode (single topic phrase)."""
    from anthropic import Anthropic
    client = Anthropic()
    topics = {}
    for _, ep in episodes.iterrows():
        prompt = f"""Look at these posts (joined with ||):

{ep['all_text']}

Return ONLY a 2-6 word topic label naming what specific policy/event these posts are about.
Examples: "China tariff escalation Apr 2025", "Brazil tariff Bolsonaro", "Steel and aluminum tariffs", "Fed rate criticism".
Just the label, no other text."""
        try:
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=30,
                messages=[{"role": "user", "content": prompt}],
            )
            topics[int(ep["episode_id"])] = msg.content[0].text.strip().strip('"')
        except Exception as e:
            topics[int(ep["episode_id"])] = f"(error: {e})"
    return topics

def main():
    threats = pd.read_parquet(THREATS_FP)
    print(f"[load] {len(threats)} A-class threats")
    texts = threats["content"].astype(str).tolist()
    print("[embed] sentence-transformer ...")
    emb = _embed(texts)
    print(f"  shape={emb.shape}")

    clustered = cluster_into_episodes(threats, emb)
    n_episodes = clustered["episode_id"].nunique()
    print(f"[cluster] {n_episodes} episodes from {len(clustered)} posts")
    eps = aggregate_episodes(clustered)
    print(f"\nEpisode size distribution:")
    print(eps["n_posts"].value_counts().sort_index().to_string())
    print(f"\nEpisode span days:")
    print(eps["episode_span_days"].describe().to_string())

    # Save the per-post version with episode_id
    clustered.to_parquet(THREATS_FP)
    print(f"[saved] {THREATS_FP} (added episode_id)")

    print("[llm] naming episodes ...")
    topics = name_episodes_with_llm(eps)
    eps["episode_topic"] = eps["episode_id"].map(topics)
    eps.to_parquet(EPISODES_FP)
    TOPICS_FP.write_text(json.dumps({str(k): v for k, v in topics.items()}, indent=2, ensure_ascii=False))
    print(f"[saved] {EPISODES_FP}, {TOPICS_FP}")

    print("\n--- Sample 10 episode labels ---")
    for _, ep in eps.sample(min(10, len(eps)), random_state=3).iterrows():
        print(f"  [ep {ep['episode_id']:3d}, n={ep['n_posts']:2d}, span={ep['episode_span_days']:3d}d] "
              f"{ep['episode_topic']!r}")

if __name__ == "__main__":
    main()
