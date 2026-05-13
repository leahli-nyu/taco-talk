"""Cox PH using BT-derived ranking scores (z-standardized) instead of saturated 0-10.

Tests whether the null result was caused by feature saturation.
Runs on both V2 (loose match, N~90) and V3 strict (N=36).
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

EP_V2 = ROOT / "data" / "processed" / "episodes_with_outcomes_v2.parquet"
EP_V3 = ROOT / "data" / "processed" / "episodes_with_outcomes_v3_strict.parquet"
BT_FP = ROOT / "data" / "processed" / "episodes_bt_scores.parquet"
OUT = ROOT / "data" / "processed" / "cox_with_bt_summary.parquet"

BT_FEATURES = [
    "btz__commitment_strength",
    "btz__hedging_level",
    "btz__specificity",
    "btz__audience_cost",
]


def build_modeling(eps, bt):
    df = eps.merge(bt[["episode_id"] + BT_FEATURES], on="episode_id", how="left")
    df["event"] = df["y1_outcome"].isin(["executed", "modified_or_withdrawn", "struck_down"]).astype(int)
    df["duration_days"] = df["anticipation_days"]
    cutoff = pd.Timestamp("2026-05-12", tz="UTC")
    pending = df["duration_days"].isna()
    if pending.any():
        fp = pd.to_datetime(df.loc[pending, "first_post_date"], errors="coerce", utc=True)
        df.loc[pending, "duration_days"] = (cutoff - fp).dt.days
    df = df[df["duration_days"] > 0].copy()
    df = df.dropna(subset=BT_FEATURES)
    return df


def fit_cox(df, features, penalizer=0.05):
    from lifelines import CoxPHFitter
    cph = CoxPHFitter(penalizer=penalizer)
    cph.fit(df[["duration_days", "event"] + features],
            duration_col="duration_days", event_col="event",
            show_progress=False)
    return cph


def bootstrap_cox(df, features, n_boot=1000, seed=42, penalizer=0.05):
    rng = np.random.RandomState(seed)
    rows = []
    n = len(df)
    for b in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        try:
            cph = fit_cox(df.iloc[idx], features, penalizer=penalizer)
            rows.append(cph.params_.to_dict())
        except Exception:
            pass
        if (b + 1) % 200 == 0:
            print(f"    boot [{b+1}/{n_boot}]", flush=True)
    return pd.DataFrame(rows)


def run_one(label, eps_fp, bt):
    print(f"\n\n=== {label} ===")
    eps = pd.read_parquet(eps_fp)
    df = build_modeling(eps, bt)
    print(f"[modeling] N={len(df)}, events={int(df['event'].sum())}")
    if len(df) < 20:
        print("  too few samples, skipping")
        return None
    cph = fit_cox(df, BT_FEATURES)
    print(cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].round(3))
    print(f"\n  Running bootstrap...")
    boot = bootstrap_cox(df, BT_FEATURES, n_boot=1000)
    print(f"\n  [bootstrap percentile CIs]")
    out_rows = []
    for f in BT_FEATURES:
        if f in boot.columns:
            samples = boot[f].dropna()
            if len(samples) >= 100:
                lo, hi = np.percentile(np.exp(samples), [2.5, 97.5])
                med = np.median(np.exp(samples))
                p_emp = min((samples >= 0).mean(), (samples <= 0).mean()) * 2
                hr = cph.summary.loc[f, "exp(coef)"]
                p_ana = cph.summary.loc[f, "p"]
                print(f"    {f:32s}  HR={hr:.2f}  boot_med={med:.2f}  "
                      f"[{lo:.2f},{hi:.2f}]  p_ana={p_ana:.3f}  p_emp={p_emp:.3f}")
                out_rows.append({"sample": label, "feature": f, "hr": hr,
                                 "boot_lo": lo, "boot_hi": hi, "boot_med": med,
                                 "p_analytic": p_ana, "p_empirical": p_emp,
                                 "n": len(df), "events": int(df["event"].sum())})
    return pd.DataFrame(out_rows)


def main():
    bt = pd.read_parquet(BT_FP)
    print(f"[load] BT scores: {len(bt)} rows, "
          f"with-data={bt[BT_FEATURES[0]].notna().sum()}")

    results = []
    r1 = run_one("V2 loose (collisions)", EP_V2, bt)
    if r1 is not None:
        results.append(r1)
    r2 = run_one("V3 strict (one-to-one)", EP_V3, bt)
    if r2 is not None:
        results.append(r2)

    if results:
        combined = pd.concat(results, ignore_index=True)
        combined.to_parquet(OUT)
        print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    main()
