"""Event study CAR on consensus A class posts (re-run with new sample).

Same methodology as event_study_y2.py but reads consensus A.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "data" / "processed" / "all_features.parquet"
MARKET = ROOT / "data" / "raw" / "market_daily.parquet"
OUT = ROOT / "data" / "processed" / "event_study_v2.parquet"
FIG = ROOT / "figures"


def load_mkt(ticker="SP500"):
    df = pd.read_parquet(MARKET)
    df = df[df["ticker"] == ticker].copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.sort_values("date").reset_index(drop=True)
    df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))
    return df


def event_study(threat_date, mkt, pre=60, gap=10, post=30):
    threat_date = pd.to_datetime(threat_date).date()
    idx_after = mkt[mkt["date"] >= threat_date].index
    if len(idx_after) == 0:
        return None
    t0 = idx_after[0]
    est_start = t0 - gap - pre
    if est_start < 0:
        return None
    est = mkt.iloc[est_start:t0 - gap]
    mu = est["log_return"].mean()
    out = {"t0_idx": int(t0), "mu_pre": float(mu)}
    for d in (1, 5, 10, 30):
        ti = t0 + d
        if ti < len(mkt):
            sub = mkt.iloc[t0:ti + 1].copy()
            out[f"car_{d}d"] = float((sub["log_return"] - mu).sum())
        else:
            out[f"car_{d}d"] = np.nan
    # Drawdown / recovery within 30 days
    if t0 + 30 < len(mkt):
        sub = mkt.iloc[t0:t0 + 31].copy()
        sub["ar"] = sub["log_return"] - mu
        sub["car"] = sub["ar"].cumsum()
        out["peak_drawdown_30d"] = float(sub["car"].min())
        out["max_recovery_30d"] = float(sub["car"].max())
    return out


def main():
    df = pd.read_parquet(POSTS)
    print(f"[load] {len(df)} consensus A posts")
    mkt_sp = load_mkt("SP500")
    mkt_vx = load_mkt("VIX")
    rows = []
    for _, r in df.iterrows():
        res = event_study(r["created_at"], mkt_sp)
        if res is None: continue
        # VIX
        vx = event_study(r["created_at"], mkt_vx)
        if vx:
            for k in ("car_1d", "car_5d", "car_30d"):
                res[f"vix_{k}"] = vx.get(k)
        res["_id"] = str(r["_id"])
        rows.append(res)
    out = pd.DataFrame(rows)
    out.to_parquet(OUT)
    print(f"[saved] {OUT}  rows={len(out)}")
    print(f"\nCAR distribution:")
    print(out[["car_1d", "car_5d", "car_30d", "peak_drawdown_30d", "max_recovery_30d"]].describe())


if __name__ == "__main__":
    main()
