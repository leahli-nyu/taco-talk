"""Refetch Polymarket price histories with fidelity=720 (works for closed markets)."""
from __future__ import annotations
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
EVENTS_FP = ROOT / "data" / "raw" / "polymarket_tariff_events.json"
OUT_DIR = ROOT / "data" / "raw" / "polymarket_price_histories"
OUT_DIR.mkdir(exist_ok=True, parents=True)

# Browser headers required
HEADERS = {
    "accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0",
}


def fetch(token_id, fidelity=720):
    params = {"market": token_id, "interval": "max", "fidelity": fidelity}
    url = f"https://clob.polymarket.com/prices-history?{urlencode(params)}"
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=30) as f:
        return json.loads(f.read())


def main():
    events = json.load(open(EVENTS_FP))
    print(f"[load] {len(events)} events")

    success, empty, err = 0, 0, 0
    for i, e in enumerate(events):
        slug = e.get("slug", str(e["id"]))[:80]
        out_fp = OUT_DIR / f"{slug}.json"

        markets = e.get("markets", [])
        if not markets:
            err += 1
            continue
        m = markets[0]
        tokens = m.get("clobTokenIds")
        if isinstance(tokens, str):
            try:
                tokens = json.loads(tokens)
            except Exception:
                err += 1
                continue
        if not tokens:
            err += 1
            continue

        try:
            data = fetch(tokens[0], fidelity=720)
            hist = data.get("history", [])
            payload = {
                "event_id": e["id"],
                "event_slug": e["slug"],
                "event_title": e["title"],
                "market_token_id_yes": tokens[0],
                "market_token_id_no": tokens[1] if len(tokens) > 1 else None,
                "condition_id": m.get("conditionId"),
                "start_date": e.get("startDate"),
                "end_date": e.get("endDate"),
                "closed_time": m.get("closedTime"),
                "final_outcome_prices": m.get("outcomePrices"),
                "history_fidelity_min": 720,
                "history": hist,
            }
            out_fp.write_text(json.dumps(payload))
            if hist:
                success += 1
            else:
                empty += 1
            time.sleep(0.4)
        except Exception as ex:
            print(f"  err on {slug}: {ex}")
            err += 1
            time.sleep(1)

        if (i + 1) % 20 == 0:
            print(f"  [{i+1}/{len(events)}] success={success} empty={empty} err={err}", flush=True)

    print(f"\n[final] success={success} empty={empty} err={err}")


if __name__ == "__main__":
    main()
