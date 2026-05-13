"""Loose matching ablation: use Claude OR GPT match (not strict consensus).

Sample-size sensitivity: shows what happens if we accept any single-LLM match.
Trade-off: more episodes, lower per-match quality.
"""
from __future__ import annotations
import warnings
import json
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]

CLAUDE_FP = ROOT / "data" / "processed" / "episode_matches_hc_claude.parquet"
GPT_FP = ROOT / "data" / "processed" / "episode_matches_hc_gpt.parquet"
EPS_NARROW_FP = ROOT / "data" / "processed" / "episodes_v2_narrow.parquet"
BT_FP = ROOT / "data" / "processed" / "episodes_bt_scores.parquet"
GT_FP = ROOT / "data" / "raw" / "tariff_timeline_ground_truth.json"

OUT_FP = ROOT / "data" / "processed" / "loose_match_summary.parquet"

BT_FEATURES = [
    "btz__commitment_strength",
    "btz__hedging_level",
    "btz__specificity",
    "btz__audience_cost",
]


def build_modeling(eps_in, matches_dict, gt_events, bt):
    """matches_dict: {episode_id: evt_idx or None}"""
    df = eps_in.copy()
    df["matched_evt_idx"] = df["episode_id"].map(matches_dict)
    df["status_raw"] = df["matched_evt_idx"].map(
        lambda idx: gt_events[int(idx)]["status"] if idx is not None and not pd.isna(idx) else None
    )

    bucket = {
        "in_effect": "executed",
        "modified": "modified_or_withdrawn",
        "withdrawn": "modified_or_withdrawn",
        "paused": "modified_or_withdrawn",
        "struck_down": "struck_down",
        "investigation": "investigation",
    }
    df["y1_outcome"] = df["status_raw"].map(lambda s: bucket.get(s, "no_policy_event_found") if s else "no_policy_event_found")

    # anticipation
    df["matched_date"] = df["matched_evt_idx"].map(
        lambda idx: gt_events[int(idx)]["announced"] if idx is not None and not pd.isna(idx) else None
    )
    df["anticipation_days"] = None
    for i, r in df.iterrows():
        if r["matched_date"]:
            ev_d = pd.to_datetime(r["matched_date"]).date()
            ep_d = pd.to_datetime(r["first_post_date"]).date()
            df.at[i, "anticipation_days"] = (ev_d - ep_d).days

    df = df.merge(bt[["episode_id"] + BT_FEATURES], on="episode_id", how="left")
    df["event"] = df["y1_outcome"].isin(["executed", "modified_or_withdrawn", "struck_down"]).astype(int)
    df["duration_days"] = pd.to_numeric(df["anticipation_days"], errors="coerce")
    cutoff = pd.Timestamp("2026-05-12", tz="UTC")
    pending = df["duration_days"].isna()
    if pending.any():
        fp = pd.to_datetime(df.loc[pending, "first_post_date"], errors="coerce", utc=True)
        df.loc[pending, "duration_days"] = (cutoff - fp).dt.days
    df = df[df["duration_days"] > 0].copy()
    df = df.dropna(subset=BT_FEATURES)
    return df


def run_cox_with_bootstrap(df, label):
    from lifelines import CoxPHFitter
    rows = []
    print(f"\n=== {label} ===")
    print(f"  N={len(df)}, events={int(df['event'].sum())}")
    if len(df) < 15 or df["event"].sum() < 5:
        print("  ⚠ too few")
        return rows

    cph = CoxPHFitter(penalizer=0.05)
    cph.fit(df[["duration_days", "event"] + BT_FEATURES],
            duration_col="duration_days", event_col="event")
    print(cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].round(3))

    # bootstrap
    rng = np.random.RandomState(42)
    boot = []
    n = len(df)
    for b in range(1000):
        idx = rng.choice(n, n, replace=True)
        try:
            c2 = CoxPHFitter(penalizer=0.05)
            c2.fit(df.iloc[idx][["duration_days", "event"] + BT_FEATURES],
                   duration_col="duration_days", event_col="event")
            boot.append(c2.params_.to_dict())
        except Exception:
            pass
    bdf = pd.DataFrame(boot)

    print("Bootstrap 95% CIs:")
    for f in BT_FEATURES:
        if f in bdf.columns:
            s = bdf[f].dropna()
            if len(s) >= 100:
                lo, hi = np.percentile(np.exp(s), [2.5, 97.5])
                med = np.median(np.exp(s))
                p_emp = min((s >= 0).mean(), (s <= 0).mean()) * 2
                hr = cph.summary.loc[f, "exp(coef)"]
                p_ana = cph.summary.loc[f, "p"]
                star = "***" if p_emp < 0.01 else ("**" if p_emp < 0.05 else ("*" if p_emp < 0.10 else ""))
                print(f"  {f:32s}  HR={hr:.2f}  [{lo:.2f},{hi:.2f}]  p_emp={p_emp:.3f}  {star}")
                rows.append({"label": label, "feature": f, "hr": hr, "boot_lo": lo, "boot_hi": hi,
                             "boot_med": med, "p_analytic": p_ana, "p_empirical": p_emp,
                             "n": len(df), "events": int(df["event"].sum())})
    return rows


def main():
    c = pd.read_parquet(CLAUDE_FP)
    g = pd.read_parquet(GPT_FP)
    eps = pd.read_parquet(EPS_NARROW_FP)
    bt = pd.read_parquet(BT_FP)
    gt = json.load(open(GT_FP))["events"]

    # Build 3 match versions
    # Version 1: STRICT (consensus) -- both agree on same event
    m_strict = {}
    merged = c.merge(g, on="episode_id", suffixes=("_c", "_g"))
    for _, r in merged.iterrows():
        if not pd.isna(r["matched_evt_idx_c"]) and r["matched_evt_idx_c"] == r["matched_evt_idx_g"]:
            m_strict[r["episode_id"]] = int(r["matched_evt_idx_c"])

    # Version 2: LOOSE - "either model matched" => use claude pick if available, else gpt
    m_loose = {}
    for _, r in merged.iterrows():
        if not pd.isna(r["matched_evt_idx_c"]):
            m_loose[r["episode_id"]] = int(r["matched_evt_idx_c"])
        elif not pd.isna(r["matched_evt_idx_g"]):
            m_loose[r["episode_id"]] = int(r["matched_evt_idx_g"])

    # Version 3: GPT-only (since GPT is more aggressive at matching)
    m_gpt_only = {}
    for _, r in merged.iterrows():
        if not pd.isna(r["matched_evt_idx_g"]):
            m_gpt_only[r["episode_id"]] = int(r["matched_evt_idx_g"])

    # Apply on narrow episodes only
    narrow_ids = set(eps["episode_id"])
    m_strict = {k: v for k, v in m_strict.items() if k in narrow_ids}
    m_loose = {k: v for k, v in m_loose.items() if k in narrow_ids}
    m_gpt_only = {k: v for k, v in m_gpt_only.items() if k in narrow_ids}

    print(f"\n=== Match counts on narrow (77 episodes) ===")
    print(f"  Strict consensus: {len(m_strict)}")
    print(f"  Loose (either):   {len(m_loose)}")
    print(f"  GPT-only:         {len(m_gpt_only)}")

    all_results = []
    for label, mapping in [
        ("V5 strict consensus (primary)", m_strict),
        ("V5b loose (either LLM)", m_loose),
        ("V5c GPT-only", m_gpt_only),
    ]:
        df = build_modeling(eps, mapping, gt, bt)
        rows = run_cox_with_bootstrap(df, label)
        all_results.extend(rows)

    out = pd.DataFrame(all_results)
    out.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")
    print("\n=== Side-by-side specificity comparison ===")
    spec_rows = out[out["feature"] == "btz__specificity"]
    print(spec_rows[["label", "n", "events", "hr", "boot_lo", "boot_hi", "p_empirical"]].to_string(index=False))


if __name__ == "__main__":
    main()
