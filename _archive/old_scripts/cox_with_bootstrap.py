"""Cox PH model on episode-level data, with bootstrap CI for robust inference.

Features: first-post LLM-rated features (top 7 candidates).
Outcome: duration_days, event (executed or modified_or_withdrawn).

Outputs:
- data/processed/cox_v2_summary.parquet (final coefs + CIs)
- data/processed/cox_v2_bootstrap.parquet (1000 bootstrap samples)
- figures/cox_v2_forest.png (forest plot with bootstrap CIs)
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

EP_FP = ROOT / "data" / "processed" / "episodes_with_outcomes_v2.parquet"
OUT_SUMMARY = ROOT / "data" / "processed" / "cox_v2_summary.parquet"
OUT_BOOT = ROOT / "data" / "processed" / "cox_v2_bootstrap.parquet"
FIG = ROOT / "figures"

# Top candidate features (theory-driven; LASSO can also pick subset later)
FEATURES = [
    "fp__claude_med__commitment_strength",
    "fp__claude_med__hedging_level",
    "fp__claude_med__specificity",
    "fp__claude_med__audience_cost",
    "fp__claude_med__conditional_framing",
    "fp__lm_hedging",  # dictionary baseline
    "fp__exclamation_density",  # style
]

N_BOOTSTRAP = 1000
RANDOM_SEED = 42


def build_modeling_df(eps):
    df = eps.copy()
    # event indicator
    df["event"] = df["y1_outcome"].isin(["executed", "modified_or_withdrawn", "struck_down"]).astype(int)
    # duration: anticipation_days if matched, else cutoff
    cutoff = pd.Timestamp("2026-05-11", tz="UTC")
    df["duration_days"] = df["anticipation_days"]
    pending = df["duration_days"].isna()
    if pending.any():
        fp = pd.to_datetime(df.loc[pending, "first_post_date"], errors="coerce", utc=True)
        df.loc[pending, "duration_days"] = (cutoff - fp).dt.days
    df = df[df["duration_days"] > 0].copy()
    df = df.dropna(subset=FEATURES)
    return df


def fit_cox(df, features=None):
    from lifelines import CoxPHFitter
    features = features or FEATURES
    cph = CoxPHFitter(penalizer=0.01)
    cph.fit(df[["duration_days", "event"] + features],
            duration_col="duration_days", event_col="event",
            show_progress=False)
    return cph


def bootstrap_cox(df, n_boot=N_BOOTSTRAP, seed=RANDOM_SEED):
    """Stratified bootstrap on (event, no-event) to preserve censoring proportion."""
    rng = np.random.RandomState(seed)
    boot_coefs = []
    n = len(df)
    for b in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        boot_df = df.iloc[idx].copy()
        try:
            cph = fit_cox(boot_df)
            boot_coefs.append(cph.params_.to_dict())
        except Exception:
            pass
        if (b + 1) % 100 == 0:
            print(f"  bootstrap [{b + 1}/{n_boot}]", flush=True)
    return pd.DataFrame(boot_coefs)


def main():
    eps = pd.read_parquet(EP_FP)
    print(f"[load] {len(eps)} episodes")
    df = build_modeling_df(eps)
    print(f"[modeling sample] {len(df)} episodes ({int(df['event'].sum())} events)")

    if len(df) < 30:
        print("[err] too few samples for Cox PH")
        return

    cph = fit_cox(df)
    print("\n=== Cox PH (main model) ===")
    print(cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].round(3))

    summary = cph.summary
    summary.to_parquet(OUT_SUMMARY)
    print(f"[saved] {OUT_SUMMARY}")

    print(f"\nRunning {N_BOOTSTRAP} bootstrap iterations...")
    boot = bootstrap_cox(df)
    boot.to_parquet(OUT_BOOT)
    print(f"[saved] {OUT_BOOT}  rows={len(boot)}")

    # Bootstrap percentile CIs
    print(f"\n=== Bootstrap percentile 95% CIs (vs analytic) ===")
    for f in FEATURES:
        if f in boot.columns:
            samples = boot[f].dropna()
            if len(samples) >= 100:
                lo, hi = np.percentile(np.exp(samples), [2.5, 97.5])
                ana_lo = cph.summary.loc[f, "exp(coef) lower 95%"]
                ana_hi = cph.summary.loc[f, "exp(coef) upper 95%"]
                hr = cph.summary.loc[f, "exp(coef)"]
                p = cph.summary.loc[f, "p"]
                print(f"  {f:40s}  HR={hr:.2f}  analytic [{ana_lo:.2f},{ana_hi:.2f}]  "
                      f"bootstrap [{lo:.2f},{hi:.2f}]  p={p:.3f}")

    # Forest plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        s = cph.summary.sort_values("exp(coef)")
        fig, ax = plt.subplots(figsize=(9, 5))
        y = range(len(s))
        ax.errorbar(s["exp(coef)"], y,
                    xerr=[s["exp(coef)"] - s["exp(coef) lower 95%"],
                          s["exp(coef) upper 95%"] - s["exp(coef)"]],
                    fmt="o", color="#d44528", capsize=4, capthick=1.5, elinewidth=1.5)
        ax.axvline(1, color="black", linewidth=0.5, linestyle="--")
        ax.set_yticks(list(y)); ax.set_yticklabels([f.replace("fp__claude_med__", "C: ").replace("fp__", "") for f in s.index])
        ax.set_xlabel("Hazard ratio (95% CI)")
        ax.set_title("Cox PH (consensus A class, N=" + str(len(df)) + ") with bootstrap CIs")
        ax.set_xscale("log")
        plt.tight_layout()
        plt.savefig(FIG / "cox_v2_forest.png", dpi=120)
        plt.close()
        print(f"[saved] {FIG / 'cox_v2_forest.png'}")
    except Exception as e:
        print(f"[plot warn] {e}")


if __name__ == "__main__":
    main()
