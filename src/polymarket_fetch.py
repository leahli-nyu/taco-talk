"""Fetch Polymarket tariff-related events + price histories.

Output:
  data/raw/polymarket_tariff_events.json    (event metadata)
  data/raw/polymarket_price_histories/      (one parquet per market)
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from urllib.parse import urlencode
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT_EVENTS = ROOT / "data" / "raw" / "polymarket_tariff_events.json"
OUT_HISTORIES = ROOT / "data" / "raw" / "polymarket_price_histories"
OUT_HISTORIES.mkdir(exist_ok=True, parents=True)

# Tags to pull (broad coverage)
TARGET_TAGS = [
    ("Trump Presidency", 101191),
    ("Trump", 126),
    ("Tariff", 101737),
    ("general tariff", 103860),
    ("Taxes", 100207),
    ("trade", 311),
]

# Keywords to filter event titles after pulling
TARIFF_KEYWORDS = [
    "tariff", "trade", "impose", "trade-war", "section 232", "section 301",
    "china", "mexico", "canada", "steel", "aluminum", "copper", "lumber",
    "auto", "semiconductor", "chip", "pharmaceutical", "fentanyl",
    "greenland", "denmark", "europe", "india", "japan", "korea", "vietnam",
    "brazil", "uk", "britain", "russia", "venezuela", "argentina",
    "de minimis", "trade deal", "import",
]


def http_get_json(url):
    req = urllib.request.Request(url, headers={"accept": "application/json", "User-Agent": "research-bot"})
    with urllib.request.urlopen(req, timeout=30) as f:
        return json.loads(f.read())


def fetch_events_by_tag(tag_id, limit=500):
    url = f"https://gamma-api.polymarket.com/events?{urlencode({'tag_id': tag_id, 'limit': limit})}"
    return http_get_json(url)


def is_tariff_related(event):
    t = str(event.get("title", "")).lower()
    return any(k in t for k in TARIFF_KEYWORDS)


def fetch_price_history(token_id, start_ts=None, end_ts=None, interval="1d"):
    params = {"market": token_id, "interval": interval, "fidelity": 60}
    if start_ts: params["startTs"] = start_ts
    if end_ts: params["endTs"] = end_ts
    url = f"https://clob.polymarket.com/prices-history?{urlencode(params)}"
    return http_get_json(url)


def main():
    # 1. Fetch events across tags
    all_events = []
    seen_ids = set()
    for name, tid in TARGET_TAGS:
        try:
            evs = fetch_events_by_tag(tid)
            print(f"[{name} tag={tid}] got {len(evs)} events")
            for e in evs:
                if e["id"] in seen_ids:
                    continue
                if is_tariff_related(e):
                    seen_ids.add(e["id"])
                    all_events.append(e)
            time.sleep(0.5)
        except Exception as ex:
            print(f"  err: {ex}")

    print(f"\n[total tariff events] {len(all_events)}")

    OUT_EVENTS.write_text(json.dumps(all_events, indent=2))
    print(f"[saved] {OUT_EVENTS}  ({OUT_EVENTS.stat().st_size//1024} KB)")

    # 2. For each event, pull price history for first/main market (binary yes/no)
    import pandas as pd
    fetched = 0
    skipped = 0
    for e in all_events:
        markets = e.get("markets", [])
        if not markets:
            skipped += 1
            continue
        m = markets[0]  # primary market
        # condition_id needed but prices-history uses clobTokenIds (token IDs)
        clob_tokens = m.get("clobTokenIds")
        if isinstance(clob_tokens, str):
            try:
                clob_tokens = json.loads(clob_tokens)
            except Exception:
                pass
        if not clob_tokens or not isinstance(clob_tokens, list) or len(clob_tokens) == 0:
            skipped += 1
            continue
        # YES token is typically first
        yes_token = clob_tokens[0]
        market_slug = e.get("slug", str(e["id"]))
        out_fp = OUT_HISTORIES / f"{market_slug[:80]}.json"
        if out_fp.exists():
            fetched += 1
            continue
        try:
            data = fetch_price_history(yes_token, interval="1d")
            hist = data.get("history", [])
            out_fp.write_text(json.dumps({
                "event_id": e["id"],
                "event_slug": e["slug"],
                "event_title": e["title"],
                "market_token_id": yes_token,
                "condition_id": m.get("conditionId"),
                "start_date": e.get("startDate"),
                "end_date": e.get("endDate"),
                "history": hist,
            }))
            fetched += 1
            time.sleep(0.2)  # rate-limit politely
        except Exception as ex:
            print(f"  fetch fail for {market_slug}: {ex}")
            skipped += 1

    print(f"\n[fetched price histories] {fetched}")
    print(f"[skipped] {skipped}")


if __name__ == "__main__":
    main()
