"""Generate the 4 key figures for paper / web from v2 pipeline outputs.

1. cox_v2_forest.png — already done by cox_with_bootstrap.py
2. car_trajectory.png — average S&P CAR trajectory + drawdown/recovery
3. outcome_distribution.png — bar chart of Y1 outcomes
4. cross_llm_agreement.png — Claude vs GPT Pearson r per feature
5. feature_correlation.png — feature correlation heatmap
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# Color palette (matches TACO-trade-inspired web)
COLORS = {
    "primary": "#d44528",
    "success": "#15803d",
    "warning": "#ca8a04",
    "danger": "#b91c1c",
    "info": "#1d4ed8",
    "neutral": "#5a5a66",
    "rule": "#e1e4ea",
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter", "Helvetica", "Arial"],
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def fig_outcome_distribution():
    eps = pd.read_parquet(ROOT / "data" / "processed" / "episodes_with_outcomes_v2.parquet")
    counts = eps["y1_outcome"].value_counts()
    order = ["executed", "modified_or_withdrawn", "other", "announced_unresolved",
             "investigation", "no_policy_event_found"]
    counts = counts.reindex(order).fillna(0)
    color_map = {
        "executed": COLORS["success"],
        "modified_or_withdrawn": COLORS["warning"],
        "struck_down": COLORS["danger"],
        "announced_unresolved": COLORS["info"],
        "investigation": COLORS["neutral"],
        "other": "#a0a0ab",
        "no_policy_event_found": COLORS["rule"],
    }
    colors = [color_map.get(k, COLORS["neutral"]) for k in counts.index]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(range(len(counts)), counts.values, color=colors)
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels([k.replace("_", " ") for k in counts.index])
    ax.invert_yaxis()
    for i, (k, v) in enumerate(counts.items()):
        if v > 0:
            ax.text(v + 0.5, i, f"{int(v)}", va="center", fontsize=10)
    ax.set_xlabel("episodes (N)")
    ax.set_title(f"Outcome distribution across {int(counts.sum())} policy episodes")
    plt.tight_layout()
    out = FIG / "v2_outcome_distribution.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"[saved] {out}")


def fig_car_trajectory():
    """Average S&P CAR trajectory over 30 days, with shaded peak drawdown / recovery."""
    es = pd.read_parquet(ROOT / "data" / "processed" / "event_study_v2.parquet")
    # We have car_1d, car_5d, car_10d, car_30d, peak_drawdown_30d, max_recovery_30d
    # Approximate trajectory at 0, 1, 5, 10, 30
    days = [0, 1, 5, 10, 30]
    means = [0]
    p25 = [0]
    p75 = [0]
    for d in (1, 5, 10, 30):
        c = es.get(f"car_{d}d")
        if c is not None:
            means.append(c.mean())
            p25.append(c.quantile(0.25))
            p75.append(c.quantile(0.75))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.fill_between(days, [p * 100 for p in p25], [p * 100 for p in p75],
                    color=COLORS["primary"], alpha=0.12, label="25-75% range")
    ax.plot(days, [m * 100 for m in means], color=COLORS["primary"],
            linewidth=2.5, marker="o", markersize=7, label="mean CAR")
    ax.axhline(0, color="black", linewidth=0.5, linestyle="-", alpha=0.4)
    ax.set_xlabel("trading days after threat")
    ax.set_ylabel("S&P 500 cumulative abnormal return (%)")
    n = len(es)
    ax.set_title(f"Average S&P 500 reaction after Trump tariff threats (N={n})")
    # Annotate avg peak drawdown and recovery
    pd_mean = es["peak_drawdown_30d"].mean() * 100
    rec_mean = es["max_recovery_30d"].mean() * 100
    ax.annotate(f"avg peak drawdown: {pd_mean:.1f}%",
                xy=(0.05, 0.05), xycoords="axes fraction", fontsize=10,
                color=COLORS["danger"])
    ax.annotate(f"avg max recovery: +{rec_mean:.1f}%",
                xy=(0.05, 0.13), xycoords="axes fraction", fontsize=10,
                color=COLORS["success"])
    ax.legend(loc="upper right")
    plt.tight_layout()
    out = FIG / "v2_car_trajectory.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"[saved] {out}")


def fig_cross_llm_agreement():
    feat = pd.read_parquet(ROOT / "data" / "processed" / "features_aggregated.parquet")
    FEATURES = ["commitment_strength", "specificity", "hedging_level", "dramatization",
                "conditional_framing", "audience_cost", "precedent_invocation",
                "negotiation_framing", "personal_attack", "ego_centric_framing"]
    rs = []
    for f in FEATURES:
        c_col = f"claude_med__{f}"
        g_col = f"gpt__{f}"
        if c_col in feat.columns and g_col in feat.columns:
            sub = feat[[c_col, g_col]].dropna()
            if len(sub) >= 10:
                rs.append((f, sub[c_col].corr(sub[g_col]), len(sub)))
    rs.sort(key=lambda x: x[1])
    names = [x[0].replace("_", " ") for x in rs]
    vals = [x[1] for x in rs]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(range(len(rs)), vals, color=[
        COLORS["primary"] if v >= 0.7 else
        COLORS["warning"] if v >= 0.5 else
        COLORS["danger"] for v in vals
    ])
    ax.set_yticks(range(len(rs)))
    ax.set_yticklabels(names)
    ax.axvline(0.5, color="black", linewidth=0.5, linestyle="--", alpha=0.5)
    ax.axvline(0.7, color="black", linewidth=0.5, linestyle="--", alpha=0.5)
    for i, v in enumerate(vals):
        ax.text(v + 0.01, i, f"{v:.2f}", va="center", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Pearson r")
    ax.set_title("Cross-LLM feature agreement: Claude vs GPT-4o-mini\n(dashed lines: r=0.5, r=0.7)")
    plt.tight_layout()
    out = FIG / "v2_cross_llm_agreement.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"[saved] {out}")


def fig_test_retest():
    feat = pd.read_parquet(ROOT / "data" / "processed" / "features_aggregated.parquet")
    FEATURES = ["commitment_strength", "specificity", "hedging_level", "dramatization",
                "conditional_framing", "audience_cost", "precedent_invocation",
                "negotiation_framing", "personal_attack", "ego_centric_framing"]
    rs = []
    for f in FEATURES:
        cols = [f"claude_{n}__{f}" for n in (1, 2, 3) if f"claude_{n}__{f}" in feat.columns]
        if len(cols) < 2: continue
        sub = feat[cols].dropna()
        if len(sub) < 10: continue
        pair_rs = []
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                pair_rs.append(sub[cols[i]].corr(sub[cols[j]]))
        if pair_rs:
            rs.append((f, np.mean(pair_rs), len(sub)))
    rs.sort(key=lambda x: x[1])
    names = [x[0].replace("_", " ") for x in rs]
    vals = [x[1] for x in rs]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(range(len(rs)), vals, color=COLORS["info"])
    ax.set_yticks(range(len(rs)))
    ax.set_yticklabels(names)
    for i, v in enumerate(vals):
        ax.text(v + 0.005, i, f"{v:.2f}", va="center", fontsize=10)
    ax.set_xlim(0.5, 1.0)
    ax.set_xlabel("mean pairwise Pearson r across 3 calls")
    ax.set_title("Within-Claude test-retest reliability\n(3 independent calls per post)")
    plt.tight_layout()
    out = FIG / "v2_test_retest.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"[saved] {out}")


def fig_zero_shot_confusion():
    z = pd.read_parquet(ROOT / "data" / "processed" / "zero_shot_baseline.parquet")
    def harmonize(s):
        if s == "executed": return "executed"
        if s == "modified_or_withdrawn": return "modified_or_withdrawn"
        if s == "announced_unresolved": return "unresolved"
        return s
    z["actual_h"] = z["actual_outcome"].apply(harmonize)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, model in zip(axes, ("claude_pred", "gpt_pred")):
        valid = z[~z[model].isin(["PARSE_ERR", "API_ERR", None])]
        cm = pd.crosstab(valid["actual_h"], valid[model])
        order_rows = ["executed", "modified_or_withdrawn", "unresolved"]
        order_cols = ["executed", "modified_or_withdrawn", "unresolved"]
        cm = cm.reindex(index=order_rows, columns=order_cols).fillna(0)
        im = ax.imshow(cm.values, cmap="Reds", aspect="auto")
        ax.set_xticks(range(len(order_cols)))
        ax.set_xticklabels(order_cols, rotation=45, ha="right")
        ax.set_yticks(range(len(order_rows)))
        ax.set_yticklabels(order_rows)
        for i in range(len(order_rows)):
            for j in range(len(order_cols)):
                ax.text(j, i, int(cm.iloc[i, j]), ha="center", va="center",
                        color="white" if cm.iloc[i, j] > cm.values.max() * 0.5 else "black")
        acc = (valid[model] == valid["actual_h"]).mean()
        model_name = "Claude Haiku 4.5" if model == "claude_pred" else "GPT-4o-mini"
        ax.set_title(f"{model_name}\naccuracy = {acc:.1%}")
        ax.set_xlabel("predicted")
        ax.set_ylabel("actual")
    plt.suptitle(f"LLM zero-shot outcome prediction (random baseline: 33%)", fontsize=13)
    plt.tight_layout()
    out = FIG / "v2_zero_shot_confusion.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"[saved] {out}")


def fig_feature_correlation():
    feat = pd.read_parquet(ROOT / "data" / "processed" / "all_features.parquet")
    cols = [c for c in feat.columns if c.startswith("claude_med__")] + \
           ["deontic_strength", "lm_hedging", "lm_uncertainty", "all_caps_ratio",
            "exclamation_density", "caps_phrase_count"]
    cols = [c for c in cols if c in feat.columns]
    sub = feat[cols].dropna()
    corr = sub.corr()
    names = [c.replace("claude_med__", "C: ").replace("_", " ") for c in cols]
    fig, ax = plt.subplots(figsize=(11, 9))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(cols)))
    ax.set_yticklabels(names, fontsize=9)
    plt.colorbar(im, ax=ax, label="Pearson r")
    ax.set_title("Feature correlation matrix (consensus A class, N=141)")
    plt.tight_layout()
    out = FIG / "v2_feature_correlation.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"[saved] {out}")


def main():
    fig_outcome_distribution()
    fig_car_trajectory()
    fig_cross_llm_agreement()
    fig_test_retest()
    fig_zero_shot_confusion()
    fig_feature_correlation()
    print("\n[done] v2 paper figures")


if __name__ == "__main__":
    main()
