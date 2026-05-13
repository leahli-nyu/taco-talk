"""Cox v6: same narrow tariff-adjacent sample, NEW BT scores from anonymized 1-7 pairwise.

Compares three feature variants:
- Claude-only BT v2 (anonymized + 1-7)
- GPT-only BT v2 (anonymized + 1-7)
- Consensus average BT v2

Output: data/processed/cox_v6_anon_bt_summary.parquet
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

EPS_FP = ROOT / "data" / "processed" / "episodes_with_hc_outcomes_narrow.parquet"
BT_V2_FP = ROOT / "data" / "processed" / "episodes_bt_v2_scores.parquet"
OUT_FP = ROOT / "data" / "processed" / "cox_v6_anon_bt_summary.parquet"

FEATURES_BASE = ["commitment_strength", "hedging_level", "specificity", "audience_cost"]


def make_modeling_df(eps, bt, prefix="btz_claude__"):
    feats = [f"{prefix}{f}" for f in FEATURES_BASE]
    df = eps.merge(bt[["episode_id"] + feats], on="episode_id", how="left")
    df["event"] = df["y1_outcome"].isin(["executed", "modified_or_withdrawn", "struck_down"]).astype(int)
    df["duration_days"] = df["anticipation_days"]
    cutoff = pd.Timestamp("2026-05-12", tz="UTC")
    pending = df["duration_days"].isna()
    if pending.any():
        fp = pd.to_datetime(df.loc[pending, "first_post_date"], errors="coerce", utc=True)
        df.loc[pending, "duration_days"] = (cutoff - fp).dt.days
    df["duration_days"] = pd.to_numeric(df["duration_days"], errors="coerce")
    df = df[df["duration_days"] > 0].copy()
    df = df.dropna(subset=feats)
    return df, feats


def run_cox(df, feats, label):
    from lifelines import CoxPHFitter
    print(f"\n=== {label}  (N={len(df)}, events={int(df['event'].sum())}) ===")
    if len(df) < 15 or df["event"].sum() < 5:
        print("  ⚠ too few")
        return []

    cph = CoxPHFitter(penalizer=0.05)
    cph.fit(df[["duration_days", "event"] + feats],
            duration_col="duration_days", event_col="event")
    print(cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].round(3))

    rng = np.random.RandomState(42)
    boot = []
    for b in range(1000):
        idx = rng.choice(len(df), len(df), replace=True)
        try:
            c2 = CoxPHFitter(penalizer=0.05)
            c2.fit(df.iloc[idx][["duration_days", "event"] + feats],
                   duration_col="duration_days", event_col="event")
            boot.append(c2.params_.to_dict())
        except Exception:
            pass
    bdf = pd.DataFrame(boot)

    print("Bootstrap CIs:")
    rows = []
    for f in feats:
        if f in bdf.columns:
            s = bdf[f].dropna()
            if len(s) >= 100:
                lo, hi = np.percentile(np.exp(s), [2.5, 97.5])
                med = np.median(np.exp(s))
                p_emp = min((s >= 0).mean(), (s <= 0).mean()) * 2
                hr = cph.summary.loc[f, "exp(coef)"]
                p_ana = cph.summary.loc[f, "p"]
                star = "***" if p_emp < 0.01 else ("**" if p_emp < 0.05 else ("*" if p_emp < 0.10 else ""))
                print(f"  {f:38s}  HR={hr:.2f}  [{lo:.2f},{hi:.2f}]  p_emp={p_emp:.3f}  {star}")
                rows.append({"label": label, "feature": f.split("__")[-1], "hr": hr,
                             "boot_lo": lo, "boot_hi": hi, "boot_med": med,
                             "p_analytic": p_ana, "p_empirical": p_emp,
                             "n": len(df), "events": int(df["event"].sum())})
    return rows


def main():
    eps = pd.read_parquet(EPS_FP)
    bt = pd.read_parquet(BT_V2_FP)
    print(f"[load] {len(eps)} narrow episodes, BT v2 scores")

    all_rows = []
    for prefix, label in [
        ("btz_claude__", "V6 Claude-BT v2 (anon+1-7)"),
        ("btz_gpt__", "V6 GPT-BT v2 (anon+1-7)"),
        ("btz_consensus__", "V6 Consensus avg BT v2 (anon+1-7)"),
    ]:
        df, feats = make_modeling_df(eps, bt, prefix=prefix)
        rows = run_cox(df, feats, label)
        all_rows.extend(rows)

    out = pd.DataFrame(all_rows)
    out.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")
    # specificity side-by-side
    print("\n=== specificity across feature variants ===")
    s = out[out["feature"] == "specificity"]
    print(s[["label", "n", "events", "hr", "boot_lo", "boot_hi", "p_empirical"]].to_string(index=False))


if __name__ == "__main__":
    main()
