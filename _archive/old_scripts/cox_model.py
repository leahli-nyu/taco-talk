"""Cox Proportional Hazards model for episode-level Y1 outcome.

Outcome: whether/when matched policy event is in_effect vs withdrawn.
Episode-level (one row per episode) to avoid the post-level temporal contamination.

Survival = until episode resolves to a known outcome.
Event = "policy resolved" (either executed or withdrawn).
We model the COMPETING risk crudely by classifying:
  - executed → "event=1, time=anticipation_days"
  - modified_or_withdrawn → "event=1, time=anticipation_days" (different sign in feature?)
  - announced_unresolved → "event=0, time = days observed so far"

For a clean Cox: just predict TIME-TO-RESOLUTION regardless of direction,
then separately predict DIRECTION with logistic.

Outputs:
  - data/processed/cox_coefficients.parquet
  - figures/eda11_cox_forest.png
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
EPISODES_FP = ROOT / "data" / "processed" / "episodes_with_outcomes.parquet"
THREATS_FP = ROOT / "data" / "processed" / "threats_with_outcomes_v2.parquet"
OUT_COEF = ROOT / "data" / "processed" / "cox_coefficients.parquet"
FIG = ROOT / "figures"

FEATURES = [
    "deontic_strength", "temporal_specificity", "has_conditional",
    "number_count", "all_caps_ratio",
    "affect_count", "lm_hedging", "lm_uncertainty",
]

def build_episode_features(eps: pd.DataFrame, posts: pd.DataFrame) -> pd.DataFrame:
    """Aggregate post-level features to episode-level (first-post snapshot)."""
    posts = posts.copy()
    posts["created_at"] = pd.to_datetime(posts["created_at"])
    # First post per episode
    first_posts = posts.sort_values("created_at").groupby("episode_id").first().reset_index()
    # Keep features
    cols = ["episode_id"] + [f for f in FEATURES if f in first_posts.columns]
    return first_posts[cols]

def main():
    eps = pd.read_parquet(EPISODES_FP)
    posts = pd.read_parquet(THREATS_FP)
    print(f"[load] {len(eps)} episodes × {len(posts)} A-class posts")

    if "episode_id" not in posts.columns:
        print("[err] threats_with_outcomes_v2.parquet missing episode_id — run episode_clustering.py first")
        return

    feat = build_episode_features(eps, posts)
    print(f"[features] {feat.shape}")

    # Define survival outcome
    df = eps.merge(feat, on="episode_id", how="left")
    df["event"] = df["y1_outcome"].isin(["executed", "modified_or_withdrawn", "struck_down"]).astype(int)
    df["duration_days"] = df["anticipation_days"]
    # For non-events (still pending), duration = days from first_post to data cutoff
    cutoff = pd.Timestamp("2026-05-11", tz="UTC")
    pending_mask = df["duration_days"].isna()
    if pending_mask.any():
        fp = pd.to_datetime(df.loc[pending_mask, "first_post_date"], errors="coerce", utc=True)
        df.loc[pending_mask, "duration_days"] = (cutoff - fp).dt.days
    # Cox requires duration > 0
    df = df[df["duration_days"] > 0].copy()
    print(f"[modeling sample] {len(df)} episodes (events: {df['event'].sum()})")

    # Drop rows with NaN features
    df = df.dropna(subset=FEATURES)
    print(f"  after dropna: {len(df)}")
    if len(df) < 20:
        print("[err] not enough data for Cox PH")
        return

    from lifelines import CoxPHFitter
    cph = CoxPHFitter()
    cph.fit(df[["duration_days", "event"] + FEATURES],
            duration_col="duration_days", event_col="event",
            show_progress=False)
    print("\n--- Cox PH summary ---")
    summary = cph.summary
    print(summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].round(3))

    summary.to_parquet(OUT_COEF)
    print(f"\n[saved] {OUT_COEF}")

    # Forest plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        s = summary.sort_values("exp(coef)")
        fig, ax = plt.subplots(figsize=(9, 4))
        y = range(len(s))
        ax.errorbar(s["exp(coef)"], y,
                    xerr=[s["exp(coef)"] - s["exp(coef) lower 95%"],
                          s["exp(coef) upper 95%"] - s["exp(coef)"]],
                    fmt="o", color="#c7342a", capsize=4)
        ax.axvline(1, color="black", linewidth=0.5, linestyle="--")
        ax.set_yticks(list(y)); ax.set_yticklabels(s.index)
        ax.set_xlabel("Hazard ratio (95% CI)")
        ax.set_title("Cox PH: features → time-to-resolution of policy episode")
        plt.tight_layout()
        plt.savefig(FIG / "eda11_cox_forest.png", dpi=120)
        plt.close()
        print(f"[saved] {FIG / 'eda11_cox_forest.png'}")
    except Exception as e:
        print(f"[plot warn] {e}")

if __name__ == "__main__":
    main()
