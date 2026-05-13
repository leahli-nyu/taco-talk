"""Sector / Country DID event study.

For each Trump A-class threat, identify the target (country / commodity), then compare
the target ETF's response to a non-target ETF's response. Difference-in-differences
isolates the tariff-specific signal from generic market noise.

Target mapping:
- China-related threats -> FXI (target), EWW (non-target Mexico)
- Mexico/Canada -> EWW/EWC (target), FXI (non-target China)
- EU -> EFA, FXI (non-target)
- Semiconductors -> SOXX, XLB (non-target materials)
- Steel/Aluminum -> XLB, XLI (non-target industrials)
- Auto -> CARZ if available, else XLI

Method:
- t0 = threat date
- pre window [t0-70, t0-10] for mean baseline
- DID = (target_CAR - target_CAR_pre_mean) - (non_target_CAR - non_target_CAR_pre_mean)

We also run a placebo: same comparison on random non-threat dates.

Output: data/processed/sector_did_summary.parquet
"""
from __future__ import annotations
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
MKT_FP = ROOT / "data" / "raw" / "market_daily.parquet"
AF_FP = ROOT / "data" / "processed" / "all_features.parquet"
OUT_FP = ROOT / "data" / "processed" / "sector_did_summary.parquet"


# Map keyword in post text -> (target ticker, non-target tickers)
# We pick by keyword search in content
TARGET_MAP = [
    # (keyword_regex, target_ticker, target_label, non_target_ticker)
    ("china|beijing|xi |chinese", "FXI", "China", "EWZ"),  # Brazil as non-target
    ("mexico|mexican", "EWW", "Mexico", "FXI"),
    ("canada|canadian|trudeau|carney", "EWC", "Canada", "FXI"),
    ("europe|european|eu |\\beu\\b|germany|france|brussels", "EFA", "Europe", "FXI"),
    ("brazil|bolsonaro|lula", "EWZ", "Brazil", "EFA"),
    ("japan|japanese", "EFA", "Japan-via-EFA", "EWZ"),
    ("semiconductor|chip|soxx", "SOXX", "Semiconductor", "XLE"),
    ("steel|aluminum|aluminium|metal", "XLB", "Metals", "XLY"),
    ("auto|car |vehicle", "XLI", "Auto-via-Industrial", "XLB"),
    ("oil|crude|opec|energy", "XLE", "Energy", "XLI"),
]


def get_ticker_returns(mkt, ticker):
    sub = mkt[mkt["ticker"]==ticker].sort_values("date").reset_index(drop=True)
    if len(sub) < 100: return None
    sub["ret"] = sub["Close"].pct_change()
    sub["date"] = pd.to_datetime(sub["date"])
    return sub


def cumulative(rets, mu_pre):
    return np.cumsum(rets - mu_pre)


def compute_did(target_data, nt_data, t0_date, pre=(70,10), post_days=30):
    """Returns (target_drawdown, target_recovery, nt_drawdown, nt_recovery, did_drawdown, did_recovery)."""
    def find_t0(df):
        idx = df.index[df["date"].dt.date >= t0_date]
        return idx[0] if len(idx) else None

    t_t0 = find_t0(target_data)
    n_t0 = find_t0(nt_data)
    if t_t0 is None or n_t0 is None: return None
    if t_t0 < pre[0] or t_t0 > len(target_data) - post_days - 1: return None
    if n_t0 < pre[0] or n_t0 > len(nt_data) - post_days - 1: return None

    t_pre = target_data["ret"].iloc[t_t0-pre[0]:t_t0-pre[1]].mean()
    n_pre = nt_data["ret"].iloc[n_t0-pre[0]:n_t0-pre[1]].mean()

    t_post = target_data["ret"].iloc[t_t0+1:t_t0+post_days+1].values
    n_post = nt_data["ret"].iloc[n_t0+1:n_t0+post_days+1].values

    t_car = cumulative(t_post, t_pre)
    n_car = cumulative(n_post, n_pre)

    return {
        "target_peak_drawdown": float(t_car.min()),
        "target_max_recovery": float(t_car.max()),
        "target_car_30d": float(t_car[-1]) if len(t_car) else 0,
        "nt_peak_drawdown": float(n_car.min()),
        "nt_max_recovery": float(n_car.max()),
        "nt_car_30d": float(n_car[-1]) if len(n_car) else 0,
        # DID = target - non-target (negative if target dropped more)
        "did_drawdown": float(t_car.min() - n_car.min()),
        "did_recovery": float(t_car.max() - n_car.max()),
        "did_car_30d": float(t_car[-1] - n_car[-1]) if len(t_car) and len(n_car) else 0,
    }


def main():
    mkt = pd.read_parquet(MKT_FP)
    af = pd.read_parquet(AF_FP)
    af["created_at"] = pd.to_datetime(af["created_at"]).dt.tz_localize(None)

    # Cache ticker returns
    import re
    ticker_data = {}
    for tk in set(t for _,t,_,_ in TARGET_MAP for t in [t,]) | set(t for _,_,_,t in TARGET_MAP):
        d = get_ticker_returns(mkt, tk)
        if d is not None:
            ticker_data[tk] = d

    # For each post, determine target
    results = []
    for _, post in af.iterrows():
        text = str(post.get("content","")).lower()
        for regex, target_tk, target_label, nt_tk in TARGET_MAP:
            if re.search(regex, text):
                if target_tk not in ticker_data or nt_tk not in ticker_data: continue
                did = compute_did(ticker_data[target_tk], ticker_data[nt_tk], post["created_at"].date())
                if did is None: continue
                did["_id"] = str(post["_id"])
                did["target_label"] = target_label
                did["target_tk"] = target_tk
                did["nt_tk"] = nt_tk
                did["claude_policy"] = post.get("claude_policy","?")
                results.append(did)
                break  # only first match per post

    df = pd.DataFrame(results)
    print(f"Sector DID: {len(df)} matched posts")
    if not len(df): return

    print("\n=== By target ===")
    print(df.groupby("target_label").agg(
        n=("did_drawdown","count"),
        mean_target_dd=("target_peak_drawdown","mean"),
        mean_nt_dd=("nt_peak_drawdown","mean"),
        mean_did_dd=("did_drawdown","mean"),
        mean_did_rec=("did_recovery","mean"),
    ).round(4))

    # Pooled
    print("\n=== Pooled (all targets) ===")
    print(f'N={len(df)}')
    print(f'Mean target peak drawdown:    {df["target_peak_drawdown"].mean()*100:+.2f}%')
    print(f'Mean non-target peak drawdown:{df["nt_peak_drawdown"].mean()*100:+.2f}%')
    print(f'Mean DID drawdown (T-NT):     {df["did_drawdown"].mean()*100:+.2f}pp')
    print(f'Mean DID recovery (T-NT):     {df["did_recovery"].mean()*100:+.2f}pp')

    # t-test: is target drawdown different from non-target drawdown? (within-event paired)
    from scipy import stats
    t, p = stats.ttest_rel(df["target_peak_drawdown"], df["nt_peak_drawdown"])
    print(f'\nPaired t-test (target vs non-target drawdown): t={t:.2f}, p={p:.4f}')

    t, p = stats.ttest_rel(df["target_max_recovery"], df["nt_max_recovery"])
    print(f'Paired t-test (target vs non-target recovery): t={t:.2f}, p={p:.4f}')

    # PLACEBO: sample 200 random non-threat dates, compute same DID
    print('\n=== PLACEBO (random non-threat dates, same target/nt pairs) ===')
    np.random.seed(42)
    trump_dates = set(af["created_at"].dt.date)
    placebo_results = []
    sp500 = ticker_data.get("EWZ")  # just use any to get date range
    if sp500 is None:
        sp500 = list(ticker_data.values())[0]
    candidate_dates = sp500["date"].dt.date.values[70:-31]
    candidate_dates = [d for d in candidate_dates if d not in trump_dates]
    # pick 200 random
    if len(candidate_dates) > 200:
        chosen = np.random.choice(len(candidate_dates), 200, replace=False)
        placebo_dates = [candidate_dates[i] for i in chosen]
    else:
        placebo_dates = candidate_dates

    # For each placebo date, run DID across all target/nt pairs and average
    for pd_date in placebo_dates:
        for regex, target_tk, target_label, nt_tk in TARGET_MAP:
            if target_tk not in ticker_data or nt_tk not in ticker_data: continue
            did = compute_did(ticker_data[target_tk], ticker_data[nt_tk], pd_date)
            if did is None: continue
            did["target_label"] = target_label
            placebo_results.append(did)
    pdf = pd.DataFrame(placebo_results)
    print(f'placebo N (all target/nt pairs * dates): {len(pdf)}')
    print(f'Placebo mean DID drawdown: {pdf["did_drawdown"].mean()*100:+.3f}pp')
    print(f'Placebo mean DID recovery: {pdf["did_recovery"].mean()*100:+.3f}pp')

    # Compare actual to placebo
    from scipy import stats as sst
    t, p = sst.ttest_ind(df["did_drawdown"], pdf["did_drawdown"], equal_var=False)
    print(f'\nActual DID drawdown vs placebo: actual={df["did_drawdown"].mean()*100:+.3f}pp vs placebo={pdf["did_drawdown"].mean()*100:+.3f}pp; t={t:.2f} p={p:.4f}')
    t, p = sst.ttest_ind(df["did_recovery"], pdf["did_recovery"], equal_var=False)
    print(f'Actual DID recovery vs placebo: actual={df["did_recovery"].mean()*100:+.3f}pp vs placebo={pdf["did_recovery"].mean()*100:+.3f}pp; t={t:.2f} p={p:.4f}')

    df.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")


if __name__ == "__main__":
    main()
