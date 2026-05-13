"""Match episodes to PIIE timeline events. Wider window (60d) + topic match."""
from __future__ import annotations
import re
from datetime import timedelta
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EP_FP = ROOT / "data" / "processed" / "episodes_v2.parquet"
PIIE_FP = ROOT / "data" / "processed" / "piie_timeline_clean.parquet"
OUT_FP = ROOT / "data" / "processed" / "episodes_with_outcomes_v2.parquet"

WINDOW_DAYS = 60

STATUS_BUCKET = {
    "in_effect": "executed",
    "modified_or_withdrawn": "modified_or_withdrawn",
    "struck_down": "struck_down",
    "announced": "announced_unresolved",
    "investigation": "investigation",
    "other": "other",
    "unknown": "unknown",
}

COUNTRY_ALIASES = {
    "China": ["chin"], "Mexico": ["mexic"], "Canada": ["canad"],
    "European Union": ["eu", "europ"], "Japan": ["japan"],
    "Brazil": ["brazil"], "United Kingdom": ["uk", "britain", "british"],
    "India": ["india"], "Russia": ["russ"], "Korea": ["korea"],
    "Taiwan": ["taiwan"], "Indonesia": ["indonesi"], "Vietnam": ["vietnam"],
    "Argentina": ["argentin"], "Switzerland": ["switz"], "World": [],
}


def country_match(threat_text: str, country: str) -> bool:
    if not isinstance(threat_text, str) or not isinstance(country, str): return False
    t = threat_text.lower()
    if country.lower() in t: return True
    for alias in COUNTRY_ALIASES.get(country, []):
        if alias in t: return True
    return False


def assign(ep, timeline) -> dict:
    first_date = pd.to_datetime(ep["first_post_date"]).date()
    text = (str(ep.get("first_text") or "") + " " + str(ep.get("all_text") or "")).lower()
    target = (str(ep.get("any_target") or "")).lower()

    best, best_score = None, 0
    for _, evt in timeline.iterrows():
        evt_date = pd.to_datetime(evt["date"]).date()
        signed = (evt_date - first_date).days
        if signed < -10 or signed > WINDOW_DAYS:
            continue
        country = str(evt.get("country") or "")
        category = str(evt.get("category") or "")
        # target match
        target_hit = country_match(text, country)
        if not target_hit and target and country:
            target_hit = target in country.lower() or country.lower() in target
        if not target_hit and category:
            target_hit = category.lower() in text
        # score
        score = (1 if target_hit else 0) * 20
        if signed >= 0:
            score += max(0, WINDOW_DAYS - signed)
        else:
            score += max(0, 10 + signed)
        if score > best_score:
            best_score = score
            best = evt
    if best is None or best_score < 10:
        return {"y1_outcome": "no_policy_event_found", "y1_match_score": best_score,
                "matched_country": None, "matched_category": None,
                "matched_date": None, "anticipation_days": None}
    md = pd.to_datetime(best["date"]).date()
    return {
        "y1_outcome": STATUS_BUCKET.get(best["status_inferred"], "other"),
        "y1_match_score": best_score,
        "matched_country": best["country"],
        "matched_category": best["category"],
        "matched_date": str(md),
        "anticipation_days": (md - first_date).days,
    }


def main():
    eps = pd.read_parquet(EP_FP)
    timeline = pd.read_parquet(PIIE_FP)
    print(f"[load] {len(eps)} episodes × {len(timeline)} timeline events")
    outcomes = eps.apply(lambda r: assign(r, timeline), axis=1).apply(pd.Series)
    merged = pd.concat([eps.reset_index(drop=True), outcomes.reset_index(drop=True)], axis=1)
    merged.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}")
    print("\nY1 distribution:")
    print(merged["y1_outcome"].value_counts())
    print(f"\nMatch rate: {(merged['y1_outcome'] != 'no_policy_event_found').mean():.1%}")
    matched = merged[merged["anticipation_days"].notna()]
    print(f"\nAnticipation days (matched):")
    print(matched["anticipation_days"].describe())


if __name__ == "__main__":
    main()
