"""Granger causality test: do Trump A-class posts Granger-cause market moves,
or does market move Granger-cause Trump posts (reverse causality)?

Build daily time series:
- post_intensity = count of A-class posts per day
- avg_specificity = mean LLM specificity per day (or 0 if no posts)
- mean_commitment = mean LLM commitment_strength per day
- sp500_ret = S&P 500 daily return
- vix_level = daily VIX close

Run Granger F-tests at lags 1, 3, 5:
- H0: lagged X does NOT help predict Y given Y's own lags

If post_intensity → sp500_ret significant: posts predict market (text drives market)
If sp500_ret → post_intensity significant: market drives posts (reverse causality)
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
OUT_FP = ROOT / "data" / "processed" / "granger_results.parquet"


def main():
    af = pd.read_parquet(AF_FP)
    af["created_at"] = pd.to_datetime(af["created_at"]).dt.tz_localize(None)
    af["date"] = af["created_at"].dt.date

    daily = af.groupby("date").agg(
        post_count=("_id","count"),
        mean_specificity=("claude_med__specificity","mean"),
        mean_commitment=("claude_med__commitment_strength","mean"),
        mean_hedging=("claude_med__hedging_level","mean"),
    ).reset_index()
    daily["date"] = pd.to_datetime(daily["date"])

    mkt = pd.read_parquet(MKT_FP)
    mkt["date"] = pd.to_datetime(mkt["date"])
    sp = mkt[mkt["ticker"]=="SP500"].sort_values("date")
    vix = mkt[mkt["ticker"]=="VIX"].sort_values("date")
    sp["sp500_ret"] = sp["Close"].pct_change()
    sp["sp500_abs_ret"] = sp["sp500_ret"].abs()
    vix_d = vix[["date","Close"]].rename(columns={"Close":"vix_level"})
    vix_d["vix_change"] = vix_d["vix_level"].diff()

    # Daily panel: trading days only
    panel = sp[["date","sp500_ret","sp500_abs_ret"]].merge(vix_d, on="date", how="left")
    panel = panel.merge(daily, on="date", how="left")
    panel["post_count"] = panel["post_count"].fillna(0)
    for c in ["mean_specificity","mean_commitment","mean_hedging"]:
        panel[c] = panel[c].fillna(panel[c].mean())  # impute missing with grand mean

    panel = panel.dropna().reset_index(drop=True)
    print(f"Daily panel: {len(panel)} trading days")
    print(f"  posts/day mean: {panel['post_count'].mean():.2f}, max: {panel['post_count'].max()}")
    print(f"  posts==0 days: {(panel['post_count']==0).sum()}")

    # Granger
    from statsmodels.tsa.stattools import grangercausalitytests
    pairs = [
        # (cause, effect)
        ("post_count", "sp500_ret",       "Trump post count → SP500 return"),
        ("post_count", "sp500_abs_ret",   "Trump post count → SP500 abs return (vol)"),
        ("post_count", "vix_change",      "Trump post count → VIX change"),
        ("mean_specificity", "sp500_ret", "Trump avg specificity → SP500 return"),
        ("mean_specificity", "sp500_abs_ret","Trump avg specificity → SP500 abs return"),
        ("mean_commitment", "sp500_ret",  "Trump avg commitment → SP500 return"),
        # Reverse
        ("sp500_ret", "post_count",       "SP500 return → Trump post count"),
        ("sp500_abs_ret", "post_count",   "SP500 abs return → Trump post count"),
        ("vix_change", "post_count",      "VIX change → Trump post count"),
        ("sp500_ret", "mean_specificity", "SP500 return → Trump specificity"),
        ("sp500_abs_ret", "mean_specificity","SP500 abs return → Trump specificity"),
    ]

    results = []
    for cause, effect, label in pairs:
        # Granger: does past values of cause help predict effect, controlling for past effect?
        # statsmodels grangercausalitytests expects [effect, cause] (in that order; first column is dependent)
        sub = panel[[effect, cause]].dropna()
        if len(sub) < 50: continue
        try:
            gres = grangercausalitytests(sub, maxlag=5, verbose=False)
        except Exception as e:
            print(f"[err] {label}: {e}")
            continue
        for lag in [1, 3, 5]:
            f_test = gres[lag][0]["ssr_ftest"]
            f_stat, p_value = f_test[0], f_test[1]
            results.append({
                "cause": cause,
                "effect": effect,
                "lag": lag,
                "f_stat": float(f_stat),
                "p_value": float(p_value),
                "label": label,
            })

    out = pd.DataFrame(results)
    out.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")

    # Print summary
    print("\n=== Granger F-test p-values (H0: cause does NOT predict effect) ===")
    pivot = out.pivot_table(index=["label"], columns="lag", values="p_value", aggfunc="first")
    print(pivot.round(4))

    # Highlight significant
    sig = out[out["p_value"] < 0.05]
    if len(sig):
        print(f"\n=== Significant at p<0.05 ===")
        for _, r in sig.iterrows():
            print(f"  lag={r['lag']}: {r['label']:60s}  F={r['f_stat']:.2f}  p={r['p_value']:.4f}")
    else:
        print("\n[no Granger relationship significant at p<0.05]")


if __name__ == "__main__":
    main()
