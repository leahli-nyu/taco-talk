"""Cox PH + discrete-time logistic on hand-compiled GT cross-LLM consensus matches.

This is the FINAL Y1 analysis pipeline:
- Sample: 110 episodes (29 consensus matched + 81 censored)
- Outcome: Y1 event = executed | modified_or_withdrawn | struck_down
- Features: BOTH original 0-10 (claude_med__*) AND BT-derived ranks (btz__*)
- Methods: Cox PH (with PH test), 1000 bootstrap, discrete-time logistic
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

EP_FP = ROOT / "data" / "processed" / "episodes_with_hc_outcomes.parquet"
BT_FP = ROOT / "data" / "processed" / "episodes_bt_scores.parquet"
OUT_DIR = ROOT / "data" / "processed"
FIG = ROOT / "figures"

ORIG_FEATURES = [
    "fp__claude_med__commitment_strength",
    "fp__claude_med__hedging_level",
    "fp__claude_med__specificity",
    "fp__claude_med__audience_cost",
    "fp__claude_med__conditional_framing",
]
BT_FEATURES = [
    "btz__commitment_strength",
    "btz__hedging_level",
    "btz__specificity",
    "btz__audience_cost",
]

N_BOOTSTRAP = 1000
SEED = 42


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
    return df


def fit_cox(df, features, penalizer=0.05):
    from lifelines import CoxPHFitter
    cph = CoxPHFitter(penalizer=penalizer)
    cph.fit(df[["duration_days", "event"] + features].dropna(),
            duration_col="duration_days", event_col="event",
            show_progress=False)
    return cph


def bootstrap_cox(df, features, n_boot=N_BOOTSTRAP, seed=SEED):
    rng = np.random.RandomState(seed)
    rows = []
    sub = df[["duration_days", "event"] + features].dropna().reset_index(drop=True)
    n = len(sub)
    for b in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        try:
            cph = fit_cox(sub.iloc[idx], features)
            rows.append(cph.params_.to_dict())
        except Exception:
            pass
        if (b + 1) % 200 == 0:
            print(f"    boot [{b+1}/{n_boot}]", flush=True)
    return pd.DataFrame(rows)


def report_cox(label, df, features, ph_test=True):
    print(f"\n=== {label} ===")
    sub = df[["duration_days", "event"] + features].dropna()
    print(f"  N={len(sub)}, events={int(sub['event'].sum())}")
    if len(sub) < 15 or sub["event"].sum() < 5:
        print("  ⚠️  Too few samples/events for reliable Cox; results indicative only")

    cph = fit_cox(df, features)
    print("\nCox PH summary:")
    print(cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].round(3))

    # PH test
    if ph_test:
        try:
            ph = cph.check_assumptions(sub, show_plots=False, p_value_threshold=0.05)
            print("\nPH test:")
            if ph and len(ph):
                for tbl in ph:
                    print(tbl)
        except Exception as e:
            print(f"  PH test failed: {e}")

    print(f"\n  Running {N_BOOTSTRAP} bootstrap...")
    boot = bootstrap_cox(df, features)
    print(f"\nBootstrap percentile 95% CIs:")
    rows = []
    for f in features:
        if f in boot.columns:
            samples = boot[f].dropna()
            if len(samples) >= 100:
                lo, hi = np.percentile(np.exp(samples), [2.5, 97.5])
                med = np.median(np.exp(samples))
                p_emp = min((samples >= 0).mean(), (samples <= 0).mean()) * 2
                hr = cph.summary.loc[f, "exp(coef)"]
                p_ana = cph.summary.loc[f, "p"]
                star = "***" if p_emp < 0.01 else ("**" if p_emp < 0.05 else ("*" if p_emp < 0.10 else ""))
                print(f"  {f:42s}  HR={hr:.2f}  boot_med={med:.2f}  "
                      f"[{lo:.2f},{hi:.2f}]  p_ana={p_ana:.3f}  p_emp={p_emp:.3f}  {star}")
                rows.append({"label": label, "feature": f, "hr": hr, "boot_lo": lo, "boot_hi": hi,
                             "boot_med": med, "p_analytic": p_ana, "p_empirical": p_emp,
                             "n": len(sub), "events": int(sub["event"].sum())})
    return pd.DataFrame(rows), cph, boot


def discrete_time_logistic(df, features):
    from sklearn.linear_model import LogisticRegression
    buckets = [(0, 2), (3, 7), (8, 30), (31, 90)]
    rows = []
    for _, ep in df.iterrows():
        dur = ep["duration_days"]
        evt = ep["event"]
        if any(pd.isna(ep[f]) for f in features):
            continue
        for lo, hi in buckets:
            if dur < lo:
                continue
            had_event = (evt == 1) and (dur <= hi)
            row = {f: ep[f] for f in features}
            row["bucket_lo"] = lo
            row["bucket_hi"] = hi
            row["event_in_bucket"] = int(had_event)
            rows.append(row)
            if had_event:
                break
            if dur < hi:
                break
    pp = pd.DataFrame(rows)
    print(f"\n[discrete-time logistic] person-period rows: {len(pp)}, events: {int(pp['event_in_bucket'].sum())}")
    out = []
    for lo, hi in buckets:
        sub = pp[pp["bucket_lo"] == lo]
        if sub["event_in_bucket"].sum() < 3 or len(sub) < 10:
            continue
        X = sub[features].values
        y = sub["event_in_bucket"].values
        Xz = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-9)
        lr = LogisticRegression(penalty="l2", C=1.0, max_iter=1000)
        lr.fit(Xz, y)
        for f, c in zip(features, lr.coef_[0]):
            out.append({"bucket": f"{lo}-{hi}d", "feature": f, "coef": c,
                        "n_obs": len(sub), "n_events": int(sub["event_in_bucket"].sum())})
    out_df = pd.DataFrame(out)
    print()
    for bucket in out_df["bucket"].unique():
        sub = out_df[out_df["bucket"] == bucket].sort_values("coef", key=abs, ascending=False)
        print(f"[{bucket}] n={sub.iloc[0]['n_obs']}, events={sub.iloc[0]['n_events']}")
        for _, r in sub.iterrows():
            fname = r["feature"].replace("fp__claude_med__", "C:").replace("btz__", "BT:")
            print(f"  {fname:28s}  z-coef={r['coef']:+.3f}")
    return out_df


def main():
    eps = pd.read_parquet(EP_FP)
    bt = pd.read_parquet(BT_FP)
    print(f"[load] {len(eps)} episodes, BT scores for {bt[BT_FEATURES[0]].notna().sum()}")
    df = build_modeling(eps, bt)
    print(f"[modeling] N={len(df)}, events={int(df['event'].sum())}")

    # Original 0-10 features
    r1, cph1, boot1 = report_cox("Original 0-10 features", df, ORIG_FEATURES)
    # BT features
    r2, cph2, boot2 = report_cox("BT-derived features", df, BT_FEATURES)

    combined = pd.concat([r1, r2], ignore_index=True)
    combined.to_parquet(OUT_DIR / "cox_v4_hc_summary.parquet")
    print(f"\n[saved] {OUT_DIR / 'cox_v4_hc_summary.parquet'}")

    print("\n\n=== Discrete-time logistic (BT features) ===")
    dt = discrete_time_logistic(df, BT_FEATURES)
    dt.to_parquet(OUT_DIR / "cox_v4_hc_dt_logistic.parquet")


if __name__ == "__main__":
    main()
