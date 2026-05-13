"""Cox PH on V3 strict matches (N=36, one-to-one with PIIE).

Also runs discrete-time logistic to test PH-free alternative.
Compares to v2 results to see if collision noise was masking signal.
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

EP_FP = ROOT / "data" / "processed" / "episodes_with_outcomes_v3_strict.parquet"
OUT_SUMMARY = ROOT / "data" / "processed" / "cox_v3_summary.parquet"
OUT_BOOT = ROOT / "data" / "processed" / "cox_v3_bootstrap.parquet"
OUT_PHTEST = ROOT / "data" / "processed" / "cox_v3_ph_test.parquet"
OUT_DTLOG = ROOT / "data" / "processed" / "discrete_logistic_v3.parquet"
FIG = ROOT / "figures"

FEATURES = [
    "fp__claude_med__commitment_strength",
    "fp__claude_med__hedging_level",
    "fp__claude_med__specificity",
    "fp__claude_med__audience_cost",
    "fp__claude_med__conditional_framing",
    "fp__lm_hedging",
    "fp__exclamation_density",
]

N_BOOTSTRAP = 1000
RANDOM_SEED = 42


def build_modeling_df(eps):
    df = eps.copy()
    df["event"] = df["y1_outcome"].isin(["executed", "modified_or_withdrawn", "struck_down"]).astype(int)
    df["duration_days"] = df["anticipation_days"]
    cutoff = pd.Timestamp("2026-05-12", tz="UTC")
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
    cph = CoxPHFitter(penalizer=0.05)  # higher penalty for small N
    cph.fit(df[["duration_days", "event"] + features],
            duration_col="duration_days", event_col="event",
            show_progress=False)
    return cph


def bootstrap_cox(df, n_boot=N_BOOTSTRAP, seed=RANDOM_SEED):
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
        if (b + 1) % 200 == 0:
            print(f"  bootstrap [{b + 1}/{n_boot}]", flush=True)
    return pd.DataFrame(boot_coefs)


def discrete_time_logistic(df):
    """Person-period dataset, then logistic regression by time bucket."""
    from sklearn.linear_model import LogisticRegression
    buckets = [(0, 2), (3, 7), (8, 30), (31, 60)]
    rows = []
    for _, ep in df.iterrows():
        dur = ep["duration_days"]
        evt = ep["event"]
        for lo, hi in buckets:
            if dur < lo:
                continue
            # entered this bucket
            had_event = (evt == 1) and (dur >= lo) and (dur <= hi)
            row = {f: ep[f] for f in FEATURES}
            row["bucket_lo"] = lo
            row["bucket_hi"] = hi
            row["event_in_bucket"] = int(had_event)
            rows.append(row)
            if had_event:
                break
            if dur < hi:
                break  # censored mid-bucket
    pp = pd.DataFrame(rows)
    print(f"[dt-logistic] person-period rows: {len(pp)}, events: {pp['event_in_bucket'].sum()}")

    # Bucket-stratified logistic
    results = []
    for lo, hi in buckets:
        sub = pp[pp["bucket_lo"] == lo]
        if sub["event_in_bucket"].sum() < 3 or len(sub) < 10:
            continue
        X = sub[FEATURES].values
        y = sub["event_in_bucket"].values
        # standardize features
        Xz = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-9)
        lr = LogisticRegression(penalty="l2", C=1.0, max_iter=1000, solver="lbfgs")
        lr.fit(Xz, y)
        for f, c in zip(FEATURES, lr.coef_[0]):
            results.append({"bucket": f"{lo}-{hi}d", "feature": f, "coef": c,
                            "n_obs": len(sub), "n_events": int(sub["event_in_bucket"].sum())})
    return pd.DataFrame(results)


def main():
    eps = pd.read_parquet(EP_FP)
    print(f"[load] {len(eps)} episodes from V3 strict")
    df = build_modeling_df(eps)
    print(f"[modeling sample] {len(df)} episodes ({int(df['event'].sum())} events)")

    if len(df) < 20:
        print("[err] too few samples for Cox")
        return

    # 1) Cox PH
    cph = fit_cox(df)
    print("\n=== V3 Cox PH (strict matches) ===")
    print(cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].round(3))
    cph.summary.to_parquet(OUT_SUMMARY)

    # 2) PH assumption test
    try:
        ph_test = cph.check_assumptions(df[["duration_days", "event"] + FEATURES],
                                        show_plots=False, p_value_threshold=0.05)
        # check_assumptions returns list of dataframes
        if ph_test and len(ph_test):
            print("\n=== PH assumption test ===")
            for tbl in ph_test:
                print(tbl)
                tbl.to_parquet(OUT_PHTEST)
        else:
            print("\n[PH test] no violations flagged at p<0.05")
    except Exception as e:
        print(f"[PH test warn] {e}")

    # 3) Bootstrap
    print(f"\nRunning {N_BOOTSTRAP} bootstrap iterations...")
    boot = bootstrap_cox(df)
    boot.to_parquet(OUT_BOOT)
    print(f"[saved] bootstrap rows={len(boot)}")

    print("\n=== Bootstrap percentile 95% CIs ===")
    for f in FEATURES:
        if f in boot.columns:
            samples = boot[f].dropna()
            if len(samples) >= 100:
                lo, hi = np.percentile(np.exp(samples), [2.5, 97.5])
                med = np.median(np.exp(samples))
                p_emp = min((samples >= 0).mean(), (samples <= 0).mean()) * 2
                hr = cph.summary.loc[f, "exp(coef)"]
                p = cph.summary.loc[f, "p"]
                print(f"  {f:42s}  HR={hr:.2f}  bootstrap median={med:.2f}  "
                      f"[{lo:.2f},{hi:.2f}]  p_analytic={p:.3f}  p_empirical={p_emp:.3f}")

    # 4) Discrete-time logistic
    print("\n=== Discrete-time logistic (PH-free) ===")
    dt = discrete_time_logistic(df)
    dt.to_parquet(OUT_DTLOG)
    if len(dt):
        for bucket in dt["bucket"].unique():
            sub = dt[dt["bucket"] == bucket].sort_values("coef", key=abs, ascending=False)
            print(f"\n[{bucket}] n={sub.iloc[0]['n_obs']}, events={sub.iloc[0]['n_events']}")
            for _, r in sub.iterrows():
                fname = r["feature"].replace("fp__claude_med__", "C:").replace("fp__", "")
                print(f"  {fname:30s}  z-coef={r['coef']:+.3f}")


if __name__ == "__main__":
    main()
