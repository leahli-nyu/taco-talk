"""Errors-in-variables (EIV) sensitivity analysis for Cox HRs.

LLM-rated features carry measurement error. We use test-retest reliability
(from 3-call Claude replicates) as the proxy for reliability ρ, then attenuation-
correct the Cox coefficients:
    β_corrected = β_observed / ρ
    HR_corrected = exp(β_corrected)

We report a sensitivity table across ρ ∈ {0.95, 0.85, 0.70, 0.50} — covering
the range from within-Claude test-retest (~0.95) to cross-LLM agreement (~0.50).

This is a standard correction-for-attenuation analysis (Spearman 1904; Prentice 1982
for Cox PH).
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

EPS_FP = ROOT / "data" / "processed" / "episodes_with_hc_outcomes_narrow.parquet"
BT_V1_FP = ROOT / "data" / "processed" / "episodes_bt_scores.parquet"
BT_V2_FP = ROOT / "data" / "processed" / "episodes_bt_v2_scores.parquet"
OUT_FP = ROOT / "data" / "processed" / "cox_eiv_sensitivity.parquet"

RELIABILITIES = [1.00, 0.95, 0.85, 0.70, 0.50]


def fit_cox(df, feats):
    from lifelines import CoxPHFitter
    cph = CoxPHFitter(penalizer=0.05)
    cph.fit(df[["duration_days", "event"] + feats],
            duration_col="duration_days", event_col="event")
    return cph


def attenuation_correct(hr, rho):
    """Naive correction: β_corrected = β / ρ, HR = exp(β_corrected)."""
    if hr <= 0 or rho <= 0:
        return np.nan
    beta = np.log(hr)
    beta_corr = beta / rho
    return float(np.exp(beta_corr))


def main():
    eps = pd.read_parquet(EPS_FP)
    bt_v1 = pd.read_parquet(BT_V1_FP)
    bt_v2 = pd.read_parquet(BT_V2_FP)

    # Three feature variants to sensitivity-correct
    variants = [
        ("V5 primary (BT v1)", bt_v1, [f"btz__{f}" for f in
                                       ["commitment_strength","hedging_level","specificity","audience_cost"]]),
        ("V6 Claude BT v2 (anon+1-7)", bt_v2, [f"btz_claude__{f}" for f in
                                                ["commitment_strength","hedging_level","specificity","audience_cost"]]),
        ("V6 Consensus avg BT v2", bt_v2, [f"btz_consensus__{f}" for f in
                                            ["commitment_strength","hedging_level","specificity","audience_cost"]]),
    ]

    all_rows = []
    for label, bt, feats in variants:
        df = eps.merge(bt[["episode_id"] + feats], on="episode_id", how="left")
        df["event"] = df["y1_outcome"].isin(["executed","modified_or_withdrawn","struck_down"]).astype(int)
        df["duration_days"] = df["anticipation_days"]
        cutoff = pd.Timestamp("2026-05-12", tz="UTC")
        pending = df["duration_days"].isna()
        if pending.any():
            fp = pd.to_datetime(df.loc[pending,"first_post_date"], errors="coerce", utc=True)
            df.loc[pending,"duration_days"] = (cutoff - fp).dt.days
        df["duration_days"] = pd.to_numeric(df["duration_days"], errors="coerce")
        df = df[df["duration_days"]>0].copy()
        df = df.dropna(subset=feats)

        if len(df) < 15 or df["event"].sum() < 5:
            continue

        cph = fit_cox(df, feats)
        print(f"\n=== {label}  N={len(df)}, events={int(df['event'].sum())} ===")
        for f in feats:
            hr_obs = cph.summary.loc[f, "exp(coef)"]
            row = {"variant": label, "feature": f.split("__")[-1], "hr_observed": hr_obs}
            for rho in RELIABILITIES:
                row[f"hr_at_rho_{rho}"] = attenuation_correct(hr_obs, rho)
            all_rows.append(row)
            print(f"  {f.split('__')[-1]:25s}  HR obs={hr_obs:.2f}   "
                  + "   ".join([f"ρ={rho}: HR={attenuation_correct(hr_obs,rho):.2f}" for rho in RELIABILITIES]))

    out = pd.DataFrame(all_rows)
    out.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")
    print("\n=== Specificity sensitivity to reliability ρ ===")
    s = out[out["feature"]=="specificity"]
    print(s.to_string(index=False))


if __name__ == "__main__":
    main()
