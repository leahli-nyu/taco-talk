"""Fetch market data covering second term (2025-01-01 to today)."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

# Core (must-have)
CORE = {
    "SP500":  "^GSPC",
    "VIX":    "^VIX",
    "DXY":    "DX-Y.NYB",
    "NASDAQ": "^IXIC",
    "SPY":    "SPY",    # ETF for cleaner fills
}

# Target-specific (used when threat targets a known country/sector)
TARGET_SPECIFIC = {
    "FXI":   "FXI",     # China large-cap
    "KWEB":  "KWEB",    # China internet
    "EWW":   "EWW",     # Mexico
    "EWC":   "EWC",     # Canada
    "EWZ":   "EWZ",     # Brazil
    "EFA":   "EFA",     # developed mkts (EU/Japan)
    "SOXX":  "SOXX",    # semiconductors
    "XLB":   "XLB",     # materials (steel/alu)
    "XLE":   "XLE",     # energy
    "XLI":   "XLI",     # industrials
    "XLY":   "XLY",     # consumer discretionary
    "DBA":   "DBA",     # agriculture
    "TLT":   "TLT",     # long-term Treasuries (Fed sensitive)
}

CURRENCIES = {
    "USDCNY": "CNY=X",
    "USDMXN": "MXN=X",
    "USDCAD": "CAD=X",
    "EURUSD": "EURUSD=X",
}

COMMODITIES = {
    "Oil":  "CL=F",
    "Gold": "GC=F",
}

ALL = {**CORE, **TARGET_SPECIFIC, **CURRENCIES, **COMMODITIES}

def fetch_daily(start="2024-11-01", end=None):
    """Daily data — enough for event study with 60-day pre-event baseline."""
    frames = []
    for name, ticker in ALL.items():
        print(f"[daily] {name}")
        try:
            df = yf.download(ticker, start=start, end=end, interval="1d",
                             auto_adjust=True, progress=False)
            if df.empty:
                print(f"  WARN: empty for {ticker}")
                continue
            df = df.reset_index().rename(columns={"Date": "date"})
            df.columns = [c if isinstance(c, str) else c[0] for c in df.columns]
            df["ticker"] = name
            frames.append(df)
        except Exception as e:
            print(f"  ERR: {ticker} -> {e}")
    out = pd.concat(frames, ignore_index=True)
    fp = OUT / "market_daily.parquet"
    out.to_parquet(fp)
    print(f"[saved] {fp}  rows={len(out):,}  tickers={out.ticker.nunique()}")
    return out

if __name__ == "__main__":
    fetch_daily()
