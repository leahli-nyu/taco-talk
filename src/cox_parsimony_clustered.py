"""Cox with 2 features only + clustered SE.

Two improvements over V5 primary:
1. Reduce features from 4 to 2 (specificity + commitment_strength) to fix EPV
   (events per variable): 16 events / 2 features = 8:1, closer to 10:1 rule
2. Cluster bootstrap by matched_evt_idx to handle 5 SCOTUS-tied events as
   non-independent (currently treated as independent which overstates power)
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
EPS_FP = ROOT / "data" / "processed" / "episodes_with_hc_outcomes_narrow.parquet"
BT_FP = ROOT / "data" / "processed" / "episodes_bt_scores.parquet"
BT_V2_FP = ROOT / "data" / "processed" / "episodes_bt_v2_scores.parquet"
OUT_FP = ROOT / "data" / "processed" / "cox_parsimony_clustered.parquet"

FEATURES_2 = ["btz__specificity", "btz__commitment_strength"]


def build_modeling(eps, bt):
    feats = FEATURES_2
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
    return df, feats


def cluster_bootstrap(df, feats, n_boot=1000, seed=42):
    """Bootstrap clusters (matched_evt_idx) instead of individual rows."""
    from lifelines import CoxPHFitter
    rng = np.random.RandomState(seed)
    # Cluster = matched_evt_idx (NaN for unmatched -> own singleton cluster)
    df = df.copy()
    df["cluster"] = df["matched_evt_idx"].fillna(
        # give each unmatched a unique cluster id
        pd.Series(range(-len(df), 0), index=df.index)
    )
    clusters = df["cluster"].unique()
    rows = []
    for b in range(n_boot):
        sampled_clusters = rng.choice(clusters, len(clusters), replace=True)
        sampled_rows = pd.concat([df[df["cluster"]==c] for c in sampled_clusters])
        try:
            c2 = CoxPHFitter(penalizer=0.05)
            c2.fit(sampled_rows[["duration_days","event"] + feats],
                   duration_col="duration_days", event_col="event")
            rows.append(c2.params_.to_dict())
        except Exception:
            pass
        if (b+1) % 250 == 0:
            print(f"  cluster-boot [{b+1}/{n_boot}]", flush=True)
    return pd.DataFrame(rows)


def standard_bootstrap(df, feats, n_boot=1000, seed=42):
    from lifelines import CoxPHFitter
    rng = np.random.RandomState(seed)
    rows = []
    n = len(df)
    for b in range(n_boot):
        idx = rng.choice(n, n, replace=True)
        try:
            c2 = CoxPHFitter(penalizer=0.05)
            c2.fit(df.iloc[idx][["duration_days","event"] + feats],
                   duration_col="duration_days", event_col="event")
            rows.append(c2.params_.to_dict())
        except Exception:
            pass
    return pd.DataFrame(rows)


def report(df, feats, boot, label):
    from lifelines import CoxPHFitter
    cph = CoxPHFitter(penalizer=0.05)
    cph.fit(df[["duration_days","event"] + feats],
            duration_col="duration_days", event_col="event")
    print(f"\n=== {label}  N={len(df)}, events={int(df['event'].sum())} ===")
    print(cph.summary[["exp(coef)","exp(coef) lower 95%","exp(coef) upper 95%","p"]].round(3))

    rows = []
    for f in feats:
        s = boot[f].dropna()
        if len(s) >= 100:
            lo, hi = np.percentile(np.exp(s), [2.5, 97.5])
            med = np.median(np.exp(s))
            p_emp = min((s>=0).mean(), (s<=0).mean()) * 2
            hr = cph.summary.loc[f, "exp(coef)"]
            p_ana = cph.summary.loc[f, "p"]
            star = "***" if p_emp<0.01 else ("**" if p_emp<0.05 else ("*" if p_emp<0.10 else ""))
            print(f"  {f:32s}  HR={hr:.2f}  [{lo:.2f},{hi:.2f}]  p_emp={p_emp:.3f}  {star}")
            rows.append({"label": label, "feature": f.split("__")[-1], "hr": hr,
                         "boot_lo": lo, "boot_hi": hi, "boot_med": med,
                         "p_analytic": p_ana, "p_empirical": p_emp,
                         "n": len(df), "events": int(df["event"].sum())})
    return rows


def main():
    eps = pd.read_parquet(EPS_FP)
    bt_v1 = pd.read_parquet(BT_FP)
    bt_v2 = pd.read_parquet(BT_V2_FP)

    all_rows = []

    # BT v1 parsimonious
    df, feats = build_modeling(eps, bt_v1)
    print('\n--- BT v1 parsimonious (2 features) ---')
    boot_std = standard_bootstrap(df, feats)
    all_rows += report(df, feats, boot_std, "V5p (BT v1, 2 feat, standard boot)")
    print('\n  with CLUSTER bootstrap (handle SCOTUS-tied events):')
    boot_cl = cluster_bootstrap(df, feats)
    all_rows += report(df, feats, boot_cl, "V5p (BT v1, 2 feat, CLUSTER boot)")

    # BT v2 (anon+1-7) Claude parsimonious
    bt_v2_renamed = bt_v2.rename(columns={f"btz_claude__{f}": f"btz__{f}" for f in ["commitment_strength","specificity","hedging_level","audience_cost"]})
    df2, feats2 = build_modeling(eps, bt_v2_renamed)
    print('\n--- BT v2 Claude anonymized parsimonious (2 features) ---')
    boot_std = standard_bootstrap(df2, feats2)
    all_rows += report(df2, feats2, boot_std, "V6p Claude (BT v2 anon, 2 feat, std boot)")
    print('\n  with CLUSTER bootstrap:')
    boot_cl = cluster_bootstrap(df2, feats2)
    all_rows += report(df2, feats2, boot_cl, "V6p Claude (BT v2 anon, 2 feat, CLUSTER boot)")

    pd.DataFrame(all_rows).to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")


if __name__ == "__main__":
    main()
