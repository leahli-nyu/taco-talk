"""Definitive Polymarket × episodes analysis.

For each consensus-matched episode:
  - Find best Polymarket market (by title keyword overlap + temporal proximity)
  - Compute prob features in [threat_date − 7d, threat_date + 30d]
  - Tabulate vs GT outcome and text-feature predictions

Outputs:
  data/processed/episodes_polymarket_features_v2.parquet
  Console comparison: Polymarket prob trajectory vs GT outcome
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
OUT_FP = ROOT / "data" / "processed" / "episodes_polymarket_features_v2.parquet"

TARGET_KEYWORDS = {
    "general": ["tariff", "trade"],
    "Mexico": ["mexico"],
    "Canada": ["canada"],
    "China": ["china"],
    "steel_aluminum": ["steel", "aluminum", "aluminium"],
    "all_countries": ["any country", "reciprocal", "blanket", "liberation", "all"],
    "autos": ["auto", "car"],
    "copper": ["copper"],
    "lumber": ["lumber", "wood"],
    "aluminum_cans_beer": ["aluminum", "beer"],
    "57_countries": ["countries", "reciprocal", "liberation"],
    "China_HK_de_minimis": ["china", "de minimis"],
    "heavy_trucks_buses": ["truck"],
    "tariff_stacking": ["tariff"],
    "auto_parts": ["auto"],
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
    "agricultural_products": ["agricultural", "soybean", "farm"],
    "UK_pharmaceuticals": ["uk", "britain", "pharmaceutical"],
    "wooden_furniture": ["furniture", "wood"],
    "semiconductors": ["semiconductor", "chip"],
    "8_european_countries": ["europe", "denmark", "greenland", "european", "eu"],
    "IEEPA_tariffs": ["ieepa", "court", "supreme", "scotus", "block"],
    "global": ["global", "blanket", "any country"],
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


def load_strict_tariff_markets():
    markets = []
    for fp in glob.glob(str(PM_DIR / "*.json")):
        d = json.load(open(fp))
        if not d.get("history"):
            continue
        title = d.get("event_title", "").lower()
        # MUST be tariff-related
        if not any(k in title for k in ["tariff", "impose", "trade deal", "section", "duty"]):
            continue
        # exclude non-tariff topics that slipped through
        if any(k in title for k in ["nfl", "harden", "ukraine", "ceasefire", "cricket"]):
            continue
        markets.append(d)
    return markets


def find_best_match(target, threat_date, markets):
    """Score each market for (target, threat_date). Return top match or None."""
    keywords = TARGET_KEYWORDS.get(target, [str(target).lower()])
    best = None
    best_score = -1
    for m in markets:
        title = m["event_title"].lower()
        m_start = parse_dt(m.get("start_date"))
        m_end = parse_dt(m.get("end_date"))
        if not m_start or not m_end:
            continue

        # Active overlap with threat
        # Allow market to start up to 90 days BEFORE threat (so we have pre-threat data)
        # AND market must still be active around threat_date
        if m_end < threat_date - timedelta(days=5):
            continue  # market closed before threat
        if m_start > threat_date + timedelta(days=10):
            continue  # market started long after threat

        # Score: keyword hits
        kw_hits = sum(1 for k in keywords if k in title)
        if kw_hits == 0:
            continue
        score = kw_hits * 20

        # Temporal score: prefer markets with active period overlapping [threat-7, threat+30]
        overlap_start = max(m_start, threat_date - timedelta(days=7))
        overlap_end = min(m_end, threat_date + timedelta(days=30))
        overlap_days = (overlap_end - overlap_start).days
        if overlap_days < 0:
            continue
        score += min(overlap_days, 30)

        # Volume bonus (larger market = more reliable signal)
        vol = m.get("volume", 0)
        if vol and vol > 0:
            score += min(int(np.log10(max(vol, 1))), 7)

        if score > best_score:
            best_score = score
            best = m
    return best


def trajectory_metrics(history, threat_date, post_days=30):
    if not history:
        return {}
    threat_dt = datetime.combine(threat_date, datetime.min.time())
    threat_ts = int(threat_dt.timestamp())
    pre_ts = int((threat_dt - timedelta(days=7)).timestamp())
    post_ts = int((threat_dt + timedelta(days=post_days)).timestamp())

    pre = [h["p"] for h in history if pre_ts <= h["t"] < threat_ts]
    at = [h["p"] for h in history if threat_ts <= h["t"] <= threat_ts + 86400 * 2]
    post = [h["p"] for h in history if threat_ts < h["t"] <= post_ts]

    return {
        "prob_pre_7d": np.mean(pre) if pre else None,
        "prob_at_threat": np.mean(at) if at else (history[0]["p"] if history else None),
        "prob_post_max_30d": max(post) if post else None,
        "prob_post_min_30d": min(post) if post else None,
        "prob_post_end_30d": post[-1] if post else None,
        "prob_final": history[-1]["p"],
        "n_hist_points": len(history),
        "n_pre_points": len(pre),
        "n_post_points": len(post),
    }


def main():
    eps = pd.read_parquet(EPS_FP)
    matched = eps[eps["match_status"] == "consensus_match"].copy()
    print(f"[load] {len(matched)} consensus episodes")

    markets = load_strict_tariff_markets()
    print(f"[load] {len(markets)} strict tariff Polymarket markets")

    rows = []
    for _, ep in matched.iterrows():
        target = ep.get("matched_target")
        threat_date = parse_dt(ep["first_post_date"])
        gt_outcome = ep["y1_outcome"]

        if not target or not threat_date:
            continue
        match = find_best_match(target, threat_date, markets)

        row = {
            "episode_id": ep["episode_id"],
            "matched_target": target,
            "threat_date": threat_date,
            "y1_outcome": gt_outcome,
            "anticipation_days": ep.get("anticipation_days"),
        }
        if match is None:
            row["pm_matched"] = False
            rows.append(row)
            continue

        metrics = trajectory_metrics(match["history"], threat_date)
        row.update({
            "pm_matched": True,
            "pm_title": match["event_title"][:140],
            "pm_event_id": match.get("event_id"),
            **metrics,
        })
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")
    n_pm = df["pm_matched"].sum()
    print(f"\n=== Match summary ===")
    print(f"  Episodes with Polymarket match: {n_pm}/{len(matched)}")

    if n_pm == 0:
        return

    mm = df[df["pm_matched"]].copy()
    # Define directional metric: prob_final indicates market belief at resolution
    # Compare with GT outcome
    mm["pm_predicts_execution"] = (mm["prob_final"] > 0.5).astype(int)
    mm["gt_executed"] = mm["y1_outcome"].isin(["executed"]).astype(int)
    mm["gt_walked_back"] = mm["y1_outcome"].isin(["modified_or_withdrawn", "struck_down"]).astype(int)

    print(f"\n=== Polymarket final prob vs GT outcome ===")
    print(mm.groupby("y1_outcome").agg(
        n=("episode_id", "count"),
        prob_final_mean=("prob_final", "mean"),
        prob_final_std=("prob_final", "std"),
        prob_at_threat_mean=("prob_at_threat", "mean"),
        prob_post_max_mean=("prob_post_max_30d", "mean"),
        prob_post_min_mean=("prob_post_min_30d", "mean"),
    ).round(3))

    print(f"\n=== Spot-check matched episodes ===")
    for _, r in mm.iterrows():
        print(f"\n  ep{int(r['episode_id']):>3d} [{str(r['matched_target'])[:20]:20s}] threat={r['threat_date']}  GT={r['y1_outcome']}")
        print(f"    PM: {r['pm_title']}")
        pre = r.get('prob_pre_7d')
        at = r.get('prob_at_threat')
        mx = r.get('prob_post_max_30d')
        mn = r.get('prob_post_min_30d')
        fn = r.get('prob_final')
        print(f"    Pre-7d={pre if pre is None else round(pre,2)}  At={at if at is None else round(at,2)}  PostMax={mx if mx is None else round(mx,2)}  PostMin={mn if mn is None else round(mn,2)}  Final={fn if fn is None else round(fn,2)}")


if __name__ == "__main__":
    main()
