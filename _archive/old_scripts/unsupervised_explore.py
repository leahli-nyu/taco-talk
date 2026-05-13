"""Unsupervised exploration: embedding clusters + UMAP viz.

No LLM needed (uses sentence-transformers all-MiniLM-L6-v2 = free).

Goal: see what natural structure exists in the A-class threats.
Outputs:
  - figures/eda12_umap_threats_by_outcome.png
  - figures/eda13_umap_threats_by_topic.png
  - data/processed/threats_with_embeddings.parquet
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
IN_FP = ROOT / "data" / "processed" / "threats_with_outcomes_v2.parquet"
OUT_EMB = ROOT / "data" / "processed" / "threats_embeddings.npy"
FIG = ROOT / "figures"

def main():
    df = pd.read_parquet(IN_FP)
    print(f"[load] {len(df)} A-class threats")

    texts = df["content"].astype(str).tolist()
    try:
        print("[embed] all-MiniLM-L6-v2 ...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        emb = model.encode(texts, batch_size=32, show_progress_bar=False, normalize_embeddings=True)
    except Exception as e:
        print(f"  [warn] sentence-transformers failed ({e!s:.80}); falling back to TF-IDF")
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import normalize
        vec = TfidfVectorizer(max_features=2000, ngram_range=(1, 2),
                              stop_words="english", min_df=2)
        X = vec.fit_transform(texts).toarray().astype(np.float32)
        emb = normalize(X, norm="l2", axis=1)
    np.save(OUT_EMB, emb)
    print(f"  saved embeddings {emb.shape} → {OUT_EMB}")

    # UMAP to 2D
    try:
        import umap
        reducer = umap.UMAP(n_neighbors=10, min_dist=0.2, metric="cosine", random_state=7)
        emb_2d = reducer.fit_transform(emb)
    except Exception as e:
        print(f"[umap fail] {e}, falling back to PCA")
        Z = emb - emb.mean(0)
        U, S, Vt = np.linalg.svd(Z, full_matrices=False)
        emb_2d = Z @ Vt.T[:, :2]
    df["umap1"], df["umap2"] = emb_2d[:, 0], emb_2d[:, 1]

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # By outcome
    outcome_color = {
        "executed": "#4e7c3a", "modified_or_withdrawn": "#e8b63c",
        "struck_down": "#c7342a", "announced_unresolved": "#4a3f33",
        "investigation": "#b8d050", "other": "#aaaaaa", "unmatched": "#dddddd",
    }
    fig, ax = plt.subplots(figsize=(10, 7))
    for outc, sub in df.groupby("y1_outcome"):
        ax.scatter(sub["umap1"], sub["umap2"], label=outc, alpha=0.7,
                   color=outcome_color.get(outc, "#666"), s=50, edgecolors="#1b1612", linewidths=0.5)
    ax.set_title(f"UMAP of {len(df)} A-class threat embeddings, colored by Y1 outcome")
    ax.legend(fontsize=9, loc="best")
    ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout()
    plt.savefig(FIG / "eda12_umap_threats_by_outcome.png", dpi=120)
    plt.close()
    print(f"[saved] {FIG / 'eda12_umap_threats_by_outcome.png'}")

    # By target country
    fig, ax = plt.subplots(figsize=(10, 7))
    targets = df["target"].fillna("unknown").astype(str)
    top_targets = targets.value_counts().head(8).index.tolist()
    palette = ["#c7342a", "#e8b63c", "#4e7c3a", "#b8d050", "#4a3f33",
               "#8f1f18", "#1b1612", "#ede3cc"]
    for i, t in enumerate(top_targets):
        sub = df[targets == t]
        ax.scatter(sub["umap1"], sub["umap2"], label=t, alpha=0.7,
                   color=palette[i % len(palette)], s=50,
                   edgecolors="#1b1612", linewidths=0.5)
    ax.set_title(f"UMAP of A-class threats colored by TARGET (top 8)")
    ax.legend(fontsize=9, loc="best")
    ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout()
    plt.savefig(FIG / "eda13_umap_threats_by_target.png", dpi=120)
    plt.close()
    print(f"[saved] {FIG / 'eda13_umap_threats_by_target.png'}")

    # HDBSCAN clustering (if available)
    try:
        import hdbscan
        clu = hdbscan.HDBSCAN(min_cluster_size=4, metric="euclidean").fit(emb_2d)
        df["cluster"] = clu.labels_
        n_clusters = int(clu.labels_.max() + 1)
        print(f"\nHDBSCAN found {n_clusters} clusters + {(clu.labels_ == -1).sum()} noise")

        fig, ax = plt.subplots(figsize=(10, 7))
        for c in sorted(set(clu.labels_)):
            sub = df[df["cluster"] == c]
            if c == -1:
                ax.scatter(sub["umap1"], sub["umap2"], color="#dddddd", s=30, alpha=0.4, label="noise")
            else:
                ax.scatter(sub["umap1"], sub["umap2"], s=50, edgecolors="#1b1612",
                           linewidths=0.5, alpha=0.8, label=f"c{c} (n={len(sub)})")
        ax.set_title(f"HDBSCAN clusters of A-class threats (n_clusters={n_clusters})")
        ax.legend(fontsize=8, loc="best", ncol=2)
        ax.set_xticks([]); ax.set_yticks([])
        plt.tight_layout()
        plt.savefig(FIG / "eda14_hdbscan_clusters.png", dpi=120)
        plt.close()
        print(f"[saved] {FIG / 'eda14_hdbscan_clusters.png'}")

        # Print one example per cluster
        print("\n--- Example post per cluster ---")
        for c in sorted(set(clu.labels_)):
            if c == -1: continue
            sub = df[df["cluster"] == c]
            print(f"\n[cluster {c}, n={len(sub)}]")
            for txt in sub["content"].head(2):
                print(f"  - {str(txt)[:150]}")
    except ImportError:
        print("[skip] hdbscan not installed — skipping cluster step")

    print(f"\n[done] saved embeddings + 2-4 UMAP plots")

if __name__ == "__main__":
    main()
