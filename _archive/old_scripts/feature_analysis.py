"""Unsupervised exploration of features.

Outputs:
  - figures/eda07_feature_correlations.png
  - figures/eda08_feature_distributions.png
  - figures/eda09_pca_threats.png
  - figures/eda10_outcome_vs_features.png
  - data/processed/feature_eda_report.json
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN_FP = ROOT / "data" / "processed" / "threats_with_outcomes_v2.parquet"
EVENT_FP = ROOT / "data" / "processed" / "event_study_results.parquet"
OUT_JSON = ROOT / "data" / "processed" / "feature_eda_report.json"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

FEATURES = [
    "deontic_strength", "temporal_specificity", "has_conditional",
    "ner_target_proxy", "number_count", "all_caps_ratio",
    "affect_count", "lm_hedging", "lm_uncertainty",
    "repeat_count_7d", "is_first_mention", "neighbor_event_count",
]

def main():
    df = pd.read_parquet(IN_FP)
    es = pd.read_parquet(EVENT_FP)
    df["_id"] = df["_id"].astype(str)
    es["_id"] = es["_id"].astype(str)
    df = df.merge(es[["_id", "car_1d", "car_5d", "car_30d", "peak_drawdown_30d", "max_recovery_30d"]],
                  on="_id", how="left")
    print(f"[load] {len(df)} threats × {len(FEATURES)} features + market outcomes")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # --- 1. Feature correlation heatmap ---
    corr = df[FEATURES].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(FEATURES))); ax.set_xticklabels(FEATURES, rotation=45, ha="right")
    ax.set_yticks(range(len(FEATURES))); ax.set_yticklabels(FEATURES)
    plt.colorbar(im, ax=ax, label="correlation")
    ax.set_title("Feature correlation matrix (Pearson)")
    plt.tight_layout()
    plt.savefig(FIG / "eda07_feature_correlations.png", dpi=120)
    plt.close()
    print(f"[saved] {FIG / 'eda07_feature_correlations.png'}")

    # --- 2. Distributions ---
    fig, axes = plt.subplots(3, 4, figsize=(15, 9))
    for ax, feat in zip(axes.flat, FEATURES):
        ax.hist(df[feat].dropna(), bins=20, color="#c7342a", alpha=0.7)
        ax.set_title(feat, fontsize=10)
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
    plt.tight_layout()
    plt.savefig(FIG / "eda08_feature_distributions.png", dpi=120)
    plt.close()
    print(f"[saved] {FIG / 'eda08_feature_distributions.png'}")

    # --- 3. PCA on features ---
    X = df[FEATURES].fillna(0).values
    X = (X - X.mean(0)) / (X.std(0) + 1e-9)
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    pc = X @ Vt.T[:, :2]
    df["pc1"], df["pc2"] = pc[:, 0], pc[:, 1]

    fig, ax = plt.subplots(figsize=(9, 7))
    outcome_color = {
        "executed": "#4e7c3a",
        "modified_or_withdrawn": "#e8b63c",
        "struck_down": "#c7342a",
        "announced_unresolved": "#4a3f33",
        "investigation": "#b8d050",
        "other": "#aaaaaa",
        "unmatched": "#dddddd",
    }
    for outc, sub in df.groupby("y1_outcome"):
        ax.scatter(sub["pc1"], sub["pc2"], label=outc, alpha=0.7,
                   color=outcome_color.get(outc, "#666"), s=40, edgecolors="#1b1612", linewidths=0.5)
    ax.set_xlabel(f"PC1 ({S[0]**2/sum(S**2)*100:.1f}% var)")
    ax.set_ylabel(f"PC2 ({S[1]**2/sum(S**2)*100:.1f}% var)")
    ax.set_title("PCA of 12 features, colored by outcome")
    ax.legend(fontsize=9, loc="best")
    plt.tight_layout()
    plt.savefig(FIG / "eda09_pca_threats.png", dpi=120)
    plt.close()
    print(f"[saved] {FIG / 'eda09_pca_threats.png'}")

    # --- 4. Mean feature value by outcome ---
    by_outcome = df.groupby("y1_outcome")[FEATURES].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    by_outcome_norm = (by_outcome - by_outcome.mean()) / (by_outcome.std() + 1e-9)
    im = ax.imshow(by_outcome_norm.values, cmap="RdBu_r", aspect="auto", vmin=-2, vmax=2)
    ax.set_xticks(range(len(FEATURES))); ax.set_xticklabels(FEATURES, rotation=45, ha="right")
    ax.set_yticks(range(len(by_outcome))); ax.set_yticklabels(by_outcome.index)
    plt.colorbar(im, ax=ax, label="z-score of mean")
    ax.set_title("Feature mean by Y1 outcome (z-score)")
    plt.tight_layout()
    plt.savefig(FIG / "eda10_outcome_vs_features.png", dpi=120)
    plt.close()
    print(f"[saved] {FIG / 'eda10_outcome_vs_features.png'}")

    # --- 5. Feature vs market outcome ---
    print("\n--- Feature correlations with market outcome ---")
    market_outcomes = ["car_1d", "car_5d", "car_30d", "peak_drawdown_30d", "max_recovery_30d"]
    corr_market = df[FEATURES + market_outcomes].corr().loc[FEATURES, market_outcomes]
    print(corr_market.round(3).to_string())

    # --- 6. Report findings ---
    report = {
        "n_threats": int(len(df)),
        "feature_top_correlations": {},
        "feature_vs_outcome": {},
        "most_predictive_for_y2": [],
    }
    # Identify top abs correlations between features (multicollinearity check)
    pairs = []
    for i, f1 in enumerate(FEATURES):
        for j, f2 in enumerate(FEATURES):
            if i < j:
                pairs.append((f1, f2, float(corr.iloc[i, j])))
    pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    report["top_feature_pairs_correlation"] = [{"a": a, "b": b, "r": r} for a, b, r in pairs[:5]]
    # Most predictive features for Y2 (any market outcome)
    abs_corr = corr_market.abs().max(axis=1).sort_values(ascending=False)
    report["most_predictive_features_for_y2"] = [
        {"feature": f, "max_abs_corr": float(abs_corr[f])} for f in abs_corr.head(5).index
    ]
    # Feature differences executed vs withdrawn
    if "executed" in df["y1_outcome"].values and "modified_or_withdrawn" in df["y1_outcome"].values:
        exec_mean = df[df["y1_outcome"] == "executed"][FEATURES].mean()
        with_mean = df[df["y1_outcome"] == "modified_or_withdrawn"][FEATURES].mean()
        diff = (exec_mean - with_mean).abs().sort_values(ascending=False)
        report["features_distinguishing_executed_vs_withdrawn"] = [
            {"feature": f, "executed_mean": float(exec_mean[f]), "withdrawn_mean": float(with_mean[f]),
             "abs_diff": float(diff[f])}
            for f in diff.head(5).index
        ]
    OUT_JSON.write_text(json.dumps(report, indent=2))
    print(f"\n[saved] {OUT_JSON}")

if __name__ == "__main__":
    main()
