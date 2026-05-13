"""Match policy episodes (not individual posts) to PIIE timeline events.

This is the corrected version. For each episode:
  - Find the FIRST post's date (anticipation start)
  - Find the matching PIIE event by topic + date proximity (window: 60 days)
  - anticipation_period = (matched event date) - (first post date)

If no PIIE event found within 60 days after first_post → still "TACO / unresolved".
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EPISODES_FP = ROOT / "data" / "processed" / "episodes.parquet"
PIIE_FP = ROOT / "data" / "processed" / "piie_timeline_clean.parquet"
OUT_FP = ROOT / "data" / "processed" / "episodes_with_outcomes.parquet"

# Wider window (60 days) for episode matching — captures real anticipation
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
    "Taiwan": ["taiwan"], "World": [],
}

def topic_keyword_match(topic_text: str, country: str, category: str) -> bool:
    if not isinstance(topic_text, str): return False
    t = topic_text.lower()
    if isinstance(country, str) and country.lower() in t: return True
    if isinstance(country, str):
        for alias in COUNTRY_ALIASES.get(country, []):
            if alias in t: return True
    if isinstance(category, str):
        cat = category.lower()
        if cat in t: return True
        # plural / singular
        if cat.rstrip("s") in t: return True
    return False

def assign_episode_outcome(ep, timeline) -> dict:
    first_date = pd.to_datetime(ep["first_post_date"]).date()
    topic_text = (ep.get("episode_topic") or "") + " " + (ep.get("first_text") or "") + " " + (ep.get("all_text") or "")
    target = (ep.get("any_target") or "").lower()

    best = None; best_score = 0
    for _, evt in timeline.iterrows():
        evt_date = pd.to_datetime(evt["date"]).date()
        day_diff_signed = (evt_date - first_date).days     # positive = event AFTER first post
        day_diff = abs(day_diff_signed)
        # Only match events on or after first post (no point matching events that already happened)
        # ...but allow small negative (a few days) for retrospective posts
        if day_diff_signed < -7 or day_diff_signed > WINDOW_DAYS:
            continue
        country = evt.get("country", "") or ""
        category = evt.get("category", "") or ""
        target_match = topic_keyword_match(topic_text, country, category)
        if not target_match and target:
            if isinstance(country, str) and (target in country.lower() or country.lower() in target):
                target_match = True
        # Score: prefer target match strongly; prefer events that happen AFTER first post
        score = (1 if target_match else 0) * 10
        if day_diff_signed >= 0:
            score += max(0, WINDOW_DAYS - day_diff_signed)
        else:
            score += max(0, 7 + day_diff_signed)  # 1-7 for retrospective; less than anticipatory
        if score > best_score:
            best_score = score
            best = evt
    if best is None or best_score < 5:
        return {
            "y1_outcome": "no_policy_event_found",
            "y1_status": None,
            "y1_match_score": best_score,
            "matched_country": None,
            "matched_category": None,
            "matched_date": None,
            "anticipation_days": None,
        }
    matched_date = pd.to_datetime(best["date"]).date()
    return {
        "y1_outcome": STATUS_BUCKET.get(best["status_inferred"], "other"),
        "y1_status": best["status_inferred"],
        "y1_match_score": best_score,
        "matched_country": best["country"],
        "matched_category": best["category"],
        "matched_date": str(matched_date),
        "anticipation_days": (matched_date - first_date).days,
    }

def main():
    eps = pd.read_parquet(EPISODES_FP)
    timeline = pd.read_parquet(PIIE_FP)
    print(f"[load] {len(eps)} episodes × {len(timeline)} timeline events")

    outcomes = eps.apply(lambda r: assign_episode_outcome(r, timeline), axis=1).apply(pd.Series)
    merged = pd.concat([eps.reset_index(drop=True), outcomes.reset_index(drop=True)], axis=1)
    merged.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}")

    print("\nEpisode-level Y1 outcome distribution:")
    print(merged["y1_outcome"].value_counts())
    print(f"\nMatch rate: {(merged['y1_outcome'] != 'no_policy_event_found').mean():.1%}")

    matched = merged.loc[merged["y1_outcome"] != "no_policy_event_found"].copy()
    print("\nAnticipation period (first post → matched event) - days:")
    print(matched["anticipation_days"].describe())

    print("\nEpisode size (n_posts) by outcome:")
    print(matched.groupby("y1_outcome")["n_posts"].describe()[["count", "mean", "max"]])

if __name__ == "__main__":
    main()
