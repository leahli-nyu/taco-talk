"""Fetch market data for ground truth: prices around threat timestamps."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import yfinance as yf

# Tickers we care about for tariff-threat market reaction
TICKERS = {
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DJ": "^DJI",
    "VIX": "^VIX",
    # Sector ETFs sensitive to trade
    "XLI": "XLI",        # industrials
    "XLB": "XLB",        # materials
    "SOXX": "SOXX",      # semiconductors (China exposure)
    "XLY": "XLY",        # consumer discretionary
    # Currencies / commodities reacting to tariff news
    "DXY": "DX-Y.NYB",   # dollar index
    "CNY": "CNY=X",      # USD/CNY
    "MXN": "MXN=X",      # USD/MXN
    "EUR": "EURUSD=X",   # EUR/USD
    "Oil": "CL=F",       # crude oil
    "Gold": "GC=F",      # gold
}

def fetch(start: str, end: str, out_dir: Path) -> pd.DataFrame:
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    for name, tk in TICKERS.items():
        print(f"[fetch] {name} ({tk})")
        df = yf.download(tk, start=start, end=end, interval="1d",
                         auto_adjust=True, progress=False)
        if df.empty:
            print(f"  WARN: empty for {tk}")
            continue
        df = df.reset_index().rename(columns={"Date": "date"})
        df["ticker"] = name
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    fp = out_dir / "market_daily.parquet"
    out.to_parquet(fp)
    print(f"[saved] {fp}  rows={len(out)}")
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--start", default="2017-01-01")
    p.add_argument("--end", default="2026-05-10")
    p.add_argument("--out", default="data/raw")
    a = p.parse_args()
    fetch(a.start, a.end, Path(a.out))
