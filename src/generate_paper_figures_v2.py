"""Generate paper figures v2: V5 primary + V6 anon BT forest plots + summary."""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# Loaded data
COX_V5_FP = ROOT / "data" / "processed" / "cox_v5_narrow_summary.parquet"
COX_V6_FP = ROOT / "data" / "processed" / "cox_v6_anon_bt_summary.parquet"
EVENT_FP = ROOT / "data" / "processed" / "event_study_v2.parquet"


def forest_plot(rows, title, out_fp, x_lab="Hazard Ratio (95% bootstrap CI)"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = list(rows)
    n = len(rows)
    fig, ax = plt.subplots(figsize=(9, max(3, 0.55 * n + 1.5)))

    # Sort: signal first (highest HR), null at top
    rows = sorted(rows, key=lambda r: r["hr"])
    ys = np.arange(n)

    hrs = [r["hr"] for r in rows]
    los = [r["boot_lo"] for r in rows]
    his = [r["boot_hi"] for r in rows]
    p_emps = [r.get("p_empirical", 1.0) for r in rows]
    labels = [r["feature"].replace("btz_claude__","").replace("btz_consensus__","")
                          .replace("btz_gpt__","").replace("btz__","") for r in rows]

    colors = ["#d44528" if p < 0.10 else "#888" for p in p_emps]

    ax.errorbar(
        hrs, ys,
        xerr=[np.array(hrs) - np.array(los), np.array(his) - np.array(hrs)],
        fmt="o", color="#222", capsize=4, capthick=1.5, elinewidth=1.6, markersize=8,
        ecolor="#666",
    )
    for x, y, c in zip(hrs, ys, colors):
        ax.plot([x], [y], marker="o", color=c, markersize=10, zorder=10)

    ax.axvline(1.0, color="black", linewidth=0.6, linestyle="--", zorder=0)
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel(x_lab, fontsize=11)
    ax.set_title(title, fontsize=12, weight="bold", loc="left")
    ax.set_xscale("log")

    # Annotate HR + p
    for x, y, lo, hi, p in zip(hrs, ys, los, his, p_emps):
        star = "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.10 else ""))
        txt = f"  HR={x:.2f}  p={p:.3f}{star}"
        ax.text(hi * 1.05, y, txt, fontsize=9, va="center", color="#444")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_fp, dpi=140)
    plt.close()
    print(f"[saved] {out_fp}")


def signature_plot(out_fp):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    df = pd.read_parquet(EVENT_FP)
    fig, ax = plt.subplots(figsize=(9, 5))

    # Two bars: peak drawdown and recovery
    means = {
        "Peak\ndrawdown (30d)": df["peak_drawdown_30d"].mean() * 100,
        "Net CAR (30d)": df["car_30d"].mean() * 100,
        "Max\nrecovery (30d)": df["max_recovery_30d"].mean() * 100,
    }
    ses = {
        "Peak\ndrawdown (30d)": df["peak_drawdown_30d"].sem() * 100,
        "Net CAR (30d)": df["car_30d"].sem() * 100,
        "Max\nrecovery (30d)": df["max_recovery_30d"].sem() * 100,
    }
    labels = list(means.keys())
    vals = [means[k] for k in labels]
    errs = [ses[k] * 1.96 for k in labels]
    colors = ["#d44528" if v < 0 else "#2e7d32" if v > 0.5 else "#888" for v in vals]

    ax.bar(labels, vals, yerr=errs, color=colors, capsize=8, alpha=0.85, edgecolor="black", linewidth=0.5)
    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_ylabel("Cumulative abnormal return (%)", fontsize=11)
    ax.set_title(f"TACO Market Signature (S&P 500, N={len(df)} events)", fontsize=12, weight="bold", loc="left")

    for i, (v, e) in enumerate(zip(vals, errs)):
        ax.text(i, v + (0.3 if v >= 0 else -0.3), f"{v:+.2f}%",
                ha="center", va="bottom" if v >= 0 else "top", fontsize=11, weight="bold")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_fp, dpi=140)
    plt.close()
    print(f"[saved] {out_fp}")


def main():
    v5 = pd.read_parquet(COX_V5_FP).to_dict(orient="records")
    v6 = pd.read_parquet(COX_V6_FP).to_dict(orient="records")

    forest_plot(v5,
                "Primary specification: Cox PH (tariff-adjacent A class, cross-LLM matched)\nN=66 episodes / 16 events / penalizer=0.05",
                FIG / "fig_v5_primary_forest.png")

    # V6 has three variants — make 3 separate plots
    for lbl in [r["label"] for r in v6][:1]:  # placeholder, we filter below
        pass
    labels_seen = []
    for variant in ["V6 Claude-BT v2 (anon+1-7)", "V6 GPT-BT v2 (anon+1-7)", "V6 Consensus avg BT v2 (anon+1-7)"]:
        rows = [r for r in v6 if r["label"] == variant]
        if not rows:
            continue
        slug = variant.split()[1].lower().replace("-bt","").replace("(","").replace(")","")
        forest_plot(
            rows,
            f"{variant}\nCox PH on N=66 narrow tariff-adjacent / 16 events",
            FIG / f"fig_v6_{slug}_forest.png",
        )

    signature_plot(FIG / "fig_taco_signature.png")

    # Combined comparison figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, rows, title in [
        (axes[0], v5, "V5 Primary (BT v1, original text)"),
        (axes[1], [r for r in v6 if r["label"]=="V6 Claude-BT v2 (anon+1-7)"], "V6 Claude (BT v2, anonymized 1-7)"),
    ]:
        rows = sorted(rows, key=lambda r: r["hr"])
        ys = np.arange(len(rows))
        hrs = [r["hr"] for r in rows]
        los = [r["boot_lo"] for r in rows]
        his = [r["boot_hi"] for r in rows]
        p_emps = [r.get("p_empirical", 1.0) for r in rows]
        labels = [r["feature"].replace("btz_claude__","").replace("btz__","") for r in rows]
        ax.errorbar(hrs, ys, xerr=[np.array(hrs)-np.array(los), np.array(his)-np.array(hrs)],
                    fmt="o", color="#222", capsize=4, capthick=1.5, elinewidth=1.6, markersize=8)
        for x, y, p in zip(hrs, ys, p_emps):
            c = "#d44528" if p < 0.10 else "#888"
            ax.plot([x],[y], marker="o", color=c, markersize=10, zorder=10)
        ax.axvline(1.0, color="black", linewidth=0.6, linestyle="--")
        ax.set_yticks(ys)
        ax.set_yticklabels(labels, fontsize=11)
        ax.set_xscale("log")
        ax.set_xlim(0.3, 5)
        ax.set_xlabel("Hazard ratio (bootstrap 95% CI)", fontsize=10)
        ax.set_title(title, fontsize=11, weight="bold", loc="left")
        for x, y, lo, hi, p in zip(hrs, ys, los, his, p_emps):
            star = "***" if p<0.01 else ("**" if p<0.05 else ("*" if p<0.10 else ""))
            ax.text(hi*1.05, y, f"  {x:.2f}  p={p:.3f}{star}", fontsize=9, va="center", color="#444")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("V5 vs V6: same data, different BT scoring → different HR estimates", fontsize=12, weight="bold")
    plt.tight_layout()
    plt.savefig(FIG / "fig_v5_v6_compare.png", dpi=140)
    plt.close()
    print(f"[saved] {FIG / 'fig_v5_v6_compare.png'}")


if __name__ == "__main__":
    main()
