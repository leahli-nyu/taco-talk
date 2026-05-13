"""Narrow A class to tariff-adjacent policy areas, then re-cluster + re-match + re-Cox.

This aligns A class with hand-compiled GT scope (tariff-only).

Narrowing criterion: Claude policy_area in {tariff, trade_agreement, commodity_intervention}.

Outputs:
  data/processed/consensus_a_narrow.parquet (filtered posts)
  data/processed/episodes_v2_narrow.parquet (re-clustered episodes)
  data/processed/episodes_with_hc_outcomes_narrow.parquet (subset matches)
  data/processed/cox_v5_narrow_summary.parquet
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
AF_FP = ROOT / "data" / "processed" / "all_features.parquet"
EPS_FP = ROOT / "data" / "processed" / "episodes_v2.parquet"
HC_FP = ROOT / "data" / "processed" / "episodes_with_hc_outcomes.parquet"
BT_FP = ROOT / "data" / "processed" / "episodes_bt_scores.parquet"

OUT_POSTS = ROOT / "data" / "processed" / "consensus_a_narrow.parquet"
OUT_EPS = ROOT / "data" / "processed" / "episodes_v2_narrow.parquet"
OUT_HC = ROOT / "data" / "processed" / "episodes_with_hc_outcomes_narrow.parquet"
OUT_COX = ROOT / "data" / "processed" / "cox_v5_narrow_summary.parquet"

TARIFF_ADJACENT = {"tariff", "trade_agreement", "commodity_intervention"}

BT_FEATURES = [
    "btz__commitment_strength",
    "btz__hedging_level",
    "btz__specificity",
    "btz__audience_cost",
]


def main():
    af = pd.read_parquet(AF_FP)
    eps = pd.read_parquet(EPS_FP)
    hc = pd.read_parquet(HC_FP)
    bt = pd.read_parquet(BT_FP)

    print(f"[load] {len(af)} posts, {len(eps)} episodes")

    # Step 1: filter posts to tariff-adjacent
    af_narrow = af[af["claude_policy"].isin(TARIFF_ADJACENT)].copy()
    print(f"\n[narrow posts] {len(af_narrow)}/{len(af)} (tariff-adjacent)")

    # Step 2: identify which episodes to keep
    # Use first-post policy_area as episode-level policy
    ep_first_policy = af.sort_values("created_at").groupby("episode_id")["claude_policy"].first()
    keep_episodes = ep_first_policy[ep_first_policy.isin(TARIFF_ADJACENT)].index
    eps_narrow = eps[eps["episode_id"].isin(keep_episodes)].reset_index(drop=True)
    print(f"[narrow episodes] {len(eps_narrow)}/{len(eps)} (first-post is tariff-adjacent)")
    print(f"\nEpisode policy_area composition:")
    ep_policy_kept = ep_first_policy.loc[keep_episodes]
    print(ep_policy_kept.value_counts())

    af_narrow.to_parquet(OUT_POSTS)
    eps_narrow.to_parquet(OUT_EPS)

    # Step 3: subset cross-LLM matches
    hc_narrow = hc[hc["episode_id"].isin(keep_episodes)].copy()
    print(f"\n[narrow hc] {len(hc_narrow)}/{len(hc)}")

    print("\nNew match status distribution:")
    print(hc_narrow["match_status"].value_counts())
    matched_narrow = hc_narrow[hc_narrow["match_status"] == "consensus_match"]
    print(f"\nConsensus matched (narrow): {len(matched_narrow)}")
    print(matched_narrow["y1_outcome"].value_counts())
    hc_narrow.to_parquet(OUT_HC)

    # Step 4: Cox + bootstrap on narrowed sample
    df = hc_narrow.merge(bt[["episode_id"] + BT_FEATURES], on="episode_id", how="left")
    df["event"] = df["y1_outcome"].isin(["executed", "modified_or_withdrawn", "struck_down"]).astype(int)
    df["duration_days"] = df["anticipation_days"]
    cutoff = pd.Timestamp("2026-05-12", tz="UTC")
    pending = df["duration_days"].isna()
    if pending.any():
        fp = pd.to_datetime(df.loc[pending, "first_post_date"], errors="coerce", utc=True)
        df.loc[pending, "duration_days"] = (cutoff - fp).dt.days
    df = df[df["duration_days"] > 0].copy()
    df = df.dropna(subset=BT_FEATURES)
    print(f"\n=== Cox modeling sample ===")
    print(f"  N={len(df)}, events={int(df['event'].sum())}")

    if len(df) < 15 or df["event"].sum() < 5:
        print("  ⚠️  too few; skipping Cox")
        return

    from lifelines import CoxPHFitter
    cph = CoxPHFitter(penalizer=0.05)
    cph.fit(df[["duration_days", "event"] + BT_FEATURES],
            duration_col="duration_days", event_col="event")
    print("\nCox PH (narrow, BT features):")
    print(cph.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].round(3))

    # Bootstrap
    print("\nBootstrap 1000...")
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
        if (b + 1) % 250 == 0:
            print(f"  [{b+1}/1000]", flush=True)
    b = pd.DataFrame(boot)

    print("\nBootstrap percentile 95% CIs:")
    rows = []
    for f in BT_FEATURES:
        if f in b.columns:
            samples = b[f].dropna()
            if len(samples) >= 100:
                lo, hi = np.percentile(np.exp(samples), [2.5, 97.5])
                med = np.median(np.exp(samples))
                p_emp = min((samples >= 0).mean(), (samples <= 0).mean()) * 2
                hr = cph.summary.loc[f, "exp(coef)"]
                p_ana = cph.summary.loc[f, "p"]
                star = "***" if p_emp < 0.01 else ("**" if p_emp < 0.05 else ("*" if p_emp < 0.10 else ""))
                print(f"  {f:32s}  HR={hr:.2f}  [{lo:.2f},{hi:.2f}]  p_emp={p_emp:.3f}  {star}")
                rows.append({"feature": f, "hr": hr, "boot_lo": lo, "boot_hi": hi,
                             "boot_med": med, "p_analytic": p_ana, "p_empirical": p_emp,
                             "n": len(df), "events": int(df["event"].sum())})
    pd.DataFrame(rows).to_parquet(OUT_COX)
    print(f"\n[saved] {OUT_COX}")


if __name__ == "__main__":
    main()
