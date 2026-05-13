"""Match Polymarket markets to our 27 consensus matched episodes.

For each episode (with first_post_date + matched GT event date + target):
  - Find Polymarket markets that mention the same target/keyword
  - Filter to markets whose active period overlaps with [first_post - 7d, first_post + 30d]
  - Pick the highest-volume / best-matched
  - Compute prob-trajectory features

Output: data/processed/episodes_polymarket_features.parquet
"""
from __future__ import annotations
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EPS_FP = ROOT / "data" / "processed" / "episodes_with_hc_outcomes_narrow.parquet"
PM_DIR = ROOT / "data" / "raw" / "polymarket_price_histories"
OUT_FP = ROOT / "data" / "processed" / "episodes_polymarket_features.parquet"

# Target keyword expansion (GT target → polymarket-title keywords)
TARGET_KEYWORDS = {
    "general": ["tariff", "trade"],
    "Mexico": ["mexico"],
    "Canada": ["canada"],
    "China": ["china"],
    "steel_aluminum": ["steel", "aluminum"],
    "all_countries": ["all", "any country", "reciprocal", "blanket", "liberation"],
    "autos": ["auto", "car"],
    "copper": ["copper"],
    "lumber": ["lumber", "wood"],
    "aluminum_cans_beer": ["aluminum", "can"],
    "57_countries": ["countries", "reciprocal", "liberation"],
    "China_HK_de_minimis": ["china", "de minimis"],
    "heavy_trucks_buses": ["truck", "bus"],
    "tariff_stacking": ["tariff"],
    "auto_parts": ["auto", "part"],
    "household_appliances_metal": ["appliance"],
    "global_de_minimis": ["de minimis"],
    "pharmaceuticals": ["pharmaceutical", "drug"],
    "Brazil": ["brazil"],
    "407_metal_products": ["metal"],
    "India": ["india"],
    "furniture_cabinets": ["furniture"],
    "pharmaceuticals_branded": ["pharmaceutical"],
    "China_additional": ["china"],
    "China_fentanyl": ["china", "fentanyl"],
    "agricultural_products": ["agricultural", "soybean"],
    "UK_pharmaceuticals": ["uk", "britain", "pharmaceutical"],
    "wooden_furniture": ["furniture", "wood"],
    "semiconductors": ["semiconductor", "chip"],
    "8_european_countries": ["europe", "greenland", "denmark", "ally"],
    "IEEPA_tariffs": ["ieepa", "court", "supreme", "scotus"],
    "global": ["global", "blanket", "all country"],
    "16_countries_excess_capacity": ["excess", "capacity"],
    "metal_products_clarified": ["metal"],
    "pharmaceuticals_patented": ["pharmaceutical"],
}


def parse_dt(s):
    if not s: return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "").split(".")[0]).date()
    except Exception:
        return None


def load_polymarket():
    markets = []
    for fp in glob.glob(str(PM_DIR / "*.json")):
        d = json.load(open(fp))
        if not d.get("history"):
            continue
        markets.append(d)
    return markets


def history_metrics(history, threat_date, window_post_days=30):
    """Compute prob trajectory metrics around threat_date."""
    if not history:
        return None
    threat_dt = datetime.combine(threat_date, datetime.min.time())
    threat_ts = int(threat_dt.timestamp())
    pre_ts = int((threat_dt - timedelta(days=7)).timestamp())
    post_ts = int((threat_dt + timedelta(days=window_post_days)).timestamp())

    pre_window = [h for h in history if pre_ts <= h["t"] < threat_ts]
    at_window = [h for h in history if threat_ts <= h["t"] <= threat_ts + 86400]  # 1d
    post_window = [h for h in history if threat_ts < h["t"] <= post_ts]

    if not history:
        return None
    prob_pre = np.mean([h["p"] for h in pre_window]) if pre_window else None
    prob_at = np.mean([h["p"] for h in at_window]) if at_window else None
    prob_post_max = max([h["p"] for h in post_window]) if post_window else None
    prob_post_min = min([h["p"] for h in post_window]) if post_window else None
    prob_final = history[-1]["p"]
    return {
        "prob_pre_threat_7d": prob_pre,
        "prob_at_threat": prob_at,
        "prob_post_max_30d": prob_post_max,
        "prob_post_min_30d": prob_post_min,
        "prob_final": prob_final,
        "n_history_points": len(history),
        "prob_change_pre_to_post": (prob_post_max - prob_pre) if (prob_pre and prob_post_max) else None,
        "prob_range_post_30d": (prob_post_max - prob_post_min) if (prob_post_max is not None and prob_post_min is not None) else None,
    }


def find_match(target, threat_date, markets, top_k=3):
    """Find best matching Polymarket markets for a (target, date) combo."""
    keywords = TARGET_KEYWORDS.get(target, [target.lower()])
    candidates = []
    for m in markets:
        title = m.get("event_title", "").lower()
        # must contain at least one keyword
        if not any(k in title for k in keywords):
            continue
        # filter: market end date is on or after threat (so it's tracking what we want)
        m_end = parse_dt(m.get("end_date"))
        m_start = parse_dt(m.get("start_date"))
        if not m_end or not m_start:
            continue
        # market must have been active during threat date
        if not (m_start <= threat_date <= m_end + timedelta(days=10)):
            continue
        # additional score: prefer markets close in time
        score = 100 - abs((m_end - threat_date).days)
        # tariff/trade keyword bonus
        if "tariff" in title or "impose" in title or "trade" in title:
            score += 20
        candidates.append((score, m))
    candidates.sort(key=lambda x: -x[0])
    return [c[1] for c in candidates[:top_k]]


def main():
    eps = pd.read_parquet(EPS_FP)
    matched = eps[eps["match_status"] == "consensus_match"].copy()
    print(f"[load] {len(matched)} consensus-matched episodes")

    markets = load_polymarket()
    print(f"[load] {len(markets)} Polymarket markets with history")

    rows = []
    for _, ep in matched.iterrows():
        target = ep.get("matched_target")
        threat_date = parse_dt(ep["first_post_date"])
        if not target or not threat_date:
            continue
        cands = find_match(target, threat_date, markets, top_k=1)
        if not cands:
            rows.append({
                "episode_id": ep["episode_id"],
                "matched_target": target,
                "pm_matched": False,
                "pm_event_title": None,
            })
            continue
        pm = cands[0]
        metrics = history_metrics(pm["history"], threat_date) or {}
        rows.append({
            "episode_id": ep["episode_id"],
            "matched_target": target,
            "pm_matched": True,
            "pm_event_title": pm["event_title"][:120],
            "pm_event_id": pm.get("event_id"),
            **metrics,
        })

    df = pd.DataFrame(rows)
    df.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")
    n_pm = df["pm_matched"].sum()
    print(f"Episodes with Polymarket match: {n_pm}/{len(matched)}")
    if n_pm > 0:
        mm = df[df["pm_matched"]]
        print(f"\n=== Polymarket-feature distribution ===")
        for col in ["prob_pre_threat_7d", "prob_at_threat", "prob_post_max_30d",
                    "prob_post_min_30d", "prob_change_pre_to_post", "prob_range_post_30d", "prob_final"]:
            if col in mm:
                s = mm[col].dropna()
                if len(s):
                    print(f"  {col:30s}  N={len(s):>3d}  mean={s.mean():+.3f}  std={s.std():.3f}  range=[{s.min():.3f},{s.max():.3f}]")

        print(f"\n=== Sample matches (first 8) ===")
        for _, r in mm.head(8).iterrows():
            print(f"  ep{r['episode_id']:>3d} [{r['matched_target'][:18]:18s}] → {r['pm_event_title']}")
            print(f"      prob: pre={r.get('prob_pre_threat_7d')}, at={r.get('prob_at_threat')}, max={r.get('prob_post_max_30d')}, final={r.get('prob_final')}")


if __name__ == "__main__":
    main()
