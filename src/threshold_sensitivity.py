"""Episode clustering threshold sensitivity.

Reruns bge-large embedding + union-find clustering at thresholds 0.78, 0.82, 0.85, 0.90.
Reports number of episodes + how many remain after tariff-adjacent narrowing.

Pure local compute, no API.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
POSTS_FP = ROOT / "data" / "processed" / "all_features.parquet"
EMB_CACHE = ROOT / "data" / "processed" / "consensus_a_bge_embeddings.npy"
OUT_FP = ROOT / "data" / "processed" / "threshold_sensitivity.parquet"

THRESHOLDS = [0.78, 0.80, 0.82, 0.85, 0.90]
WINDOW_DAYS = 30
TARIFF_ADJACENT = {"tariff", "trade_agreement", "commodity_intervention"}


def embed_or_load(texts):
    if EMB_CACHE.exists():
        emb = np.load(EMB_CACHE)
        if emb.shape[0] == len(texts):
            print(f"[cache] loaded {emb.shape}")
            return emb
    print("[embed] computing bge-large-en-v1.5 ...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("BAAI/bge-large-en-v1.5")
    emb = model.encode(texts, batch_size=8, show_progress_bar=True, normalize_embeddings=True)
    np.save(EMB_CACHE, emb)
    print(f"[cached] {EMB_CACHE}")
    return emb


def cluster(df, emb, sim_thr, window_days=WINDOW_DAYS):
    df = df.sort_values("created_at").reset_index(drop=True)
    n = len(df)
    sim = emb @ emb.T
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    dates = pd.to_datetime(df["created_at"]).dt.date.tolist()
    for i in range(n):
        for j in range(i + 1, n):
            day_diff = (dates[j] - dates[i]).days
            if day_diff > window_days:
                break
            if sim[i, j] > sim_thr:
                union(i, j)

    ep_ids = [find(i) for i in range(n)]
    label_map = {ep: idx for idx, ep in enumerate(sorted(set(ep_ids)))}
    df = df.copy()
    df["episode_id"] = [label_map[e] for e in ep_ids]
    return df


def main():
    af = pd.read_parquet(POSTS_FP)
    # Re-sort so embedding order matches
    af = af.sort_values("created_at").reset_index(drop=True)
    print(f"[load] {len(af)} consensus A posts")

    emb = embed_or_load(af["content"].tolist())

    rows = []
    for thr in THRESHOLDS:
        df = cluster(af, emb, sim_thr=thr)
        n_eps = df["episode_id"].nunique()
        # Each episode's first-post policy_area
        ep_first_policy = df.sort_values("created_at").groupby("episode_id")["claude_policy"].first()
        n_tariff_adj = ep_first_policy.isin(TARIFF_ADJACENT).sum()
        # Mixed episodes
        ep_pol_unique = df.groupby("episode_id")["claude_policy"].nunique()
        n_mixed = (ep_pol_unique > 1).sum()
        rows.append({
            "threshold": thr,
            "n_episodes_total": n_eps,
            "n_tariff_adjacent": n_tariff_adj,
            "n_mixed_policy_eps": n_mixed,
            "pct_monothematic": (1 - n_mixed / n_eps) * 100,
        })
        print(f"  thr={thr}  total_eps={n_eps:3d}  tariff_adj={n_tariff_adj:3d}  mixed_eps={n_mixed} ({(1-n_mixed/n_eps)*100:.1f}% monothematic)")

    df_out = pd.DataFrame(rows)
    df_out.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")
    print(df_out.to_string(index=False))


if __name__ == "__main__":
    main()
