"""V2: Match A-class threats to PIIE timeline outcomes.

Uses cleaned PIIE timeline (156 events) instead of hand-compiled 43.
"""
from __future__ import annotations
import re
from pathlib import Path
from datetime import timedelta
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
THREATS_FP = ROOT / "data" / "processed" / "features.parquet"
TIMELINE_FP = ROOT / "data" / "processed" / "piie_timeline_clean.parquet"
OUT = ROOT / "data" / "processed" / "threats_with_outcomes_v2.parquet"

# Status → outcome bucket mapping (4-class)
STATUS_BUCKET = {
    "in_effect": "executed",
    "modified_or_withdrawn": "modified_or_withdrawn",
    "struck_down": "struck_down",
    "announced": "announced_unresolved",
    "investigation": "investigation",
    "other": "other",
    "unknown": "unknown",
}

# Country alias (loose match)
COUNTRY_ALIASES = {
    "China": ["chin"],
    "Mexico": ["mexic"],
    "Canada": ["canad"],
    "European Union": ["eu", "europ"],
    "Japan": ["japan"],
    "Brazil": ["brazil"],
    "United Kingdom": ["uk", "britain", "british"],
    "India": ["india"],
    "Russia": ["russ"],
    "Korea": ["korea"],
    "Taiwan": ["taiwan"],
    "World": [],
}

def country_match(threat_text: str, country: str) -> bool:
    if not isinstance(threat_text, str) or not isinstance(country, str):
        return False
    t = threat_text.lower()
    if country.lower() in t: return True
    for alias in COUNTRY_ALIASES.get(country, []):
        if alias in t: return True
    return False

def assign_outcome(threat_row, timeline) -> dict:
    threat_date = pd.to_datetime(threat_row["created_at"]).date()
    threat_text = threat_row.get("content", "")
    threat_target = (threat_row.get("target") or "").lower()

    best = None; best_score = 0
    for _, ev in timeline.iterrows():
        ev_date = ev["date"]
        if not isinstance(ev_date, type(threat_date)):
            ev_date = pd.to_datetime(ev_date).date()
        day_diff = abs((ev_date - threat_date).days)
        if day_diff > 14:
            continue
        # target match
        country = ev.get("country", "")
        category = ev.get("category", "") or ""
        target_match = country_match(threat_text, country) if country else False
        if not target_match and threat_target:
            if isinstance(country, str) and (threat_target in country.lower() or country.lower() in threat_target):
                target_match = True
        if not target_match and isinstance(category, str):
            target_match = category.lower() in threat_text.lower()
        score = (1 if target_match else 0) * 10 + max(0, 14 - day_diff)
        if score > best_score:
            best_score = score
            best = ev
    if best is None or best_score < 5:
        return {
            "y1_outcome": "unmatched",
            "y1_status": None,
            "y1_match_score": best_score,
            "matched_country": None,
            "matched_category": None,
            "matched_date": None,
            "days_threat_to_event": None,
        }
    ev_date = pd.to_datetime(best["date"]).date() if not isinstance(best["date"], type(threat_date)) else best["date"]
    return {
        "y1_outcome": STATUS_BUCKET.get(best["status_inferred"], "other"),
        "y1_status": best["status_inferred"],
        "y1_match_score": best_score,
        "matched_country": best["country"],
        "matched_category": best["category"],
        "matched_date": str(ev_date),
        "days_threat_to_event": (ev_date - threat_date).days,
    }

def main():
    threats = pd.read_parquet(THREATS_FP)
    timeline = pd.read_parquet(TIMELINE_FP)
    print(f"[load] {len(threats)} threats × {len(timeline)} timeline events")
    outcomes = threats.apply(lambda r: assign_outcome(r, timeline), axis=1).apply(pd.Series)
    merged = pd.concat([threats.reset_index(drop=True), outcomes.reset_index(drop=True)], axis=1)
    merged.to_parquet(OUT)
    print(f"[saved] {OUT}")
    print("\nY1 outcome distribution (v2 with PIIE):")
    print(merged["y1_outcome"].value_counts())
    print(f"\nMatch rate: {(merged['y1_outcome'] != 'unmatched').mean():.1%}")
    print("\nDays threat → event:")
    sub = merged.loc[merged["days_threat_to_event"].notna(), "days_threat_to_event"]
    if len(sub): print(sub.describe())

if __name__ == "__main__":
    main()
