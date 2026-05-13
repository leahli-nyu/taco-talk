"""Event study: compute abnormal returns around each A-class threat.

For each threat at time t=0:
  - estimation window: t-60d to t-10d (used to estimate "normal" returns)
  - event window: t-1d to t+30d (where we measure reactions)
  - daily abnormal_return = actual_return - market_model_predicted
  - CAR = cumulative sum over window

Outputs:
  - data/processed/event_study_results.parquet
  - figures/eda05_y1_outcome_distribution.png (will help pick window)
  - figures/eda06_avg_car_around_threats.png
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import timedelta
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
THREATS = ROOT / "data" / "processed" / "features.parquet"
MARKET = ROOT / "data" / "raw" / "market_daily.parquet"
TIMELINE = ROOT / "data" / "raw" / "tariff_timeline_ground_truth.json"
OUT = ROOT / "data" / "processed" / "event_study_results.parquet"
FIG = ROOT / "figures"

# Event windows (trading days)
ESTIMATION_PRE = 60     # 60 trading days before event
ESTIMATION_PRE_GAP = 10  # gap between estimation and event window
EVENT_PRE = 1
EVENT_POST = 30

def load_market(ticker: str = "SP500") -> pd.DataFrame:
    df = pd.read_parquet(MARKET)
    df = df[df["ticker"] == ticker].copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.sort_values("date").reset_index(drop=True)
    df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))
    return df

def event_study_one(threat_date, mkt: pd.DataFrame) -> dict:
    """Compute event study windows around a single threat date."""
    threat_date = pd.to_datetime(threat_date).date()
    mkt = mkt.reset_index(drop=True)
    # Find index closest to threat_date
    idx = mkt[mkt["date"] >= threat_date].index
    if len(idx) == 0:
        return {"error": "no future market data"}
    t0 = idx[0]
    # Estimation window: t0-PRE-GAP-PRE to t0-GAP
    est_start = t0 - ESTIMATION_PRE_GAP - ESTIMATION_PRE
    est_end   = t0 - ESTIMATION_PRE_GAP
    if est_start < 0:
        return {"error": "not enough pre-event data"}
    est = mkt.iloc[est_start:est_end]
    mean_return = est["log_return"].mean()
    std_return = est["log_return"].std()
    # Event window
    ev_start = max(0, t0 - EVENT_PRE)
    ev_end   = min(len(mkt) - 1, t0 + EVENT_POST)
    ev = mkt.iloc[ev_start:ev_end + 1].copy()
    ev["abnormal_return"] = ev["log_return"] - mean_return
    ev["car"] = ev["abnormal_return"].cumsum()
    # Key window stats
    car_1d = ev.loc[ev_start + EVENT_PRE:ev_start + EVENT_PRE + 1, "car"].sum()
    # CAR at +5, +10, +30 days post event
    def car_at(days):
        target_i = t0 + days
        if target_i >= len(mkt): return np.nan
        sub = mkt.iloc[ev_start:target_i + 1].copy()
        sub["abnormal_return"] = sub["log_return"] - mean_return
        return sub["abnormal_return"].sum()
    return {
        "event_date": str(threat_date),
        "trading_day_index": int(t0),
        "mean_return_estimation_window": float(mean_return),
        "std_return_estimation_window": float(std_return),
        "car_1d": float(car_at(1)),
        "car_5d": float(car_at(5)),
        "car_10d": float(car_at(10)),
        "car_30d": float(car_at(30)),
        "peak_drawdown_30d": float(ev["car"].min()),
        "max_recovery_30d": float(ev["car"].max()),
    }

def main():
    threats = pd.read_parquet(THREATS)
    threats["event_date"] = pd.to_datetime(threats["created_at"]).dt.date
    print(f"[load] {len(threats)} A-class threats")

    mkt_sp = load_market("SP500")
    mkt_vix = load_market("VIX")

    rows = []
    for _, t in threats.iterrows():
        es = event_study_one(t["event_date"], mkt_sp)
        es["_id"] = t["_id"]
        es["target_from_label"] = t.get("target")
        es["text_preview"] = str(t.get("content", ""))[:200]
        # also compute VIX reaction
        vx = event_study_one(t["event_date"], mkt_vix)
        es["car_1d_vix"] = vx.get("car_1d")
        es["car_5d_vix"] = vx.get("car_5d")
        es["car_30d_vix"] = vx.get("car_30d")
        rows.append(es)

    df = pd.DataFrame(rows)
    df.to_parquet(OUT)
    print(f"[saved] {OUT}")
    print(f"\nCAR summary (S&P 500, log returns):")
    print(df[["car_1d", "car_5d", "car_10d", "car_30d",
              "peak_drawdown_30d", "max_recovery_30d"]].describe())

    # Plot average CAR trajectory
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        # average CAR by day-out
        windows = [1, 2, 3, 5, 10, 15, 20, 30]
        means_sp = [df[f"car_{w}d"].mean() if f"car_{w}d" in df.columns else np.nan for w in [1, 5, 10, 30]]
        labels = ["1d", "5d", "10d", "30d"]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, means_sp, color="#e15759")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_title(f"Avg CAR on S&P 500 around A-class threats (N={len(df)})")
        ax.set_ylabel("Avg Cumulative Abnormal Return")
        plt.tight_layout()
        plt.savefig(FIG / "eda06_avg_car_around_threats.png", dpi=120)
        plt.close()
        print(f"[saved] {FIG / 'eda06_avg_car_around_threats.png'}")
    except Exception as e:
        print(f"[plot warn] {e}")

if __name__ == "__main__":
    main()
