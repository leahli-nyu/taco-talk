"""Match A-class threats to Y1 outcomes from PIIE/Wikipedia/Tax Foundation timeline.

For each threat (Truth Social post), find the closest timeline event by:
  - date proximity (threat must be on or before announced date in timeline)
  - target match (country / product overlap)

Then assign Y1 outcome:
  - "executed_fully": effective date exists, status in {in_effect, modified}
  - "executed_partial": status = modified
  - "withdrawn_TACO": status = withdrawn OR (announced but no effective date)
  - "struck_down": status = struck_down (executed then judicial reversal)
  - "paused": status = paused
  - "unmatched": no timeline match found
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from datetime import timedelta
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
THREATS_FP = ROOT / "data" / "processed" / "features.parquet"
TIMELINE_FP = ROOT / "data" / "raw" / "tariff_timeline_ground_truth.json"
OUT = ROOT / "data" / "processed" / "threats_with_outcomes.parquet"

# Topic keyword mapping (for matching threat text to timeline target)
TOPIC_PATTERNS = {
    "China":       re.compile(r"\bchin(a|ese)\b", re.I),
    "Mexico":      re.compile(r"\bmexic", re.I),
    "Canada":      re.compile(r"\bcanad", re.I),
    "Brazil":      re.compile(r"\bbrazil", re.I),
    "India":       re.compile(r"\bindia\b", re.I),
    "Russia":      re.compile(r"\bruss", re.I),
    "EU":          re.compile(r"\b(EU|European)\b", re.I),
    "Japan":       re.compile(r"\bjapan", re.I),
    "Korea":       re.compile(r"\b(?:south )?korea\b", re.I),
    "UK":          re.compile(r"\b(UK|Britain|British|United Kingdom)\b", re.I),
    "steel":       re.compile(r"\bsteel|\baluminum|\balumin", re.I),
    "autos":       re.compile(r"\bauto|\bcar\b|\bvehicle", re.I),
    "pharma":      re.compile(r"\bpharma|\bdrug\b|\bmedic", re.I),
    "semiconductor": re.compile(r"\bsemiconductor|\bchip\b", re.I),
    "lumber":      re.compile(r"\blumber|\bwood|\bfurniture", re.I),
    "agricultural": re.compile(r"\bcoffee\b|\bsoybean|\btea\b|\bfarm", re.I),
    "copper":      re.compile(r"\bcopper", re.I),
}

STATUS_TO_OUTCOME = {
    "in_effect": "executed_fully",
    "modified": "executed_partial",
    "struck_down": "struck_down",
    "withdrawn": "withdrawn_TACO",
    "paused": "paused",
    "investigation": "pending",
}

def topic_match(text: str, target: str) -> bool:
    """Check if a threat text mentions a target from the timeline."""
    if not isinstance(text, str): return False
    text = text.lower()
    # Direct target string in text
    if target.lower() in text:
        return True
    # Via topic pattern
    for topic, pat in TOPIC_PATTERNS.items():
        if topic.lower() in target.lower() and pat.search(text):
            return True
    return False

def assign_outcome(threat_row, timeline) -> dict:
    """For one threat, find best matching timeline event."""
    threat_date = pd.to_datetime(threat_row["created_at"]).date()
    threat_text = threat_row.get("content", "")
    threat_target = threat_row.get("target")

    best_match = None
    best_score = 0
    for ev in timeline:
        ann = pd.to_datetime(ev["announced"]).date()
        # Threat should be on or near announcement date (within ±10 days)
        day_diff = abs((ann - threat_date).days)
        if day_diff > 10:
            continue
        # Score: prefer same/closer date + target match
        target_match = False
        if threat_target and ev["target"]:
            target_match = threat_target.lower() in ev["target"].lower() or \
                           ev["target"].lower() in threat_target.lower()
        if not target_match:
            target_match = topic_match(threat_text, ev["target"])
        score = (1 if target_match else 0) * 10 + max(0, 10 - day_diff)
        if score > best_score:
            best_score = score
            best_match = ev
    if best_match is None or best_score < 5:
        return {
            "y1_outcome": "unmatched",
            "y1_match_score": best_score,
            "y1_days_to_resolution": None,
            "matched_target": None,
            "matched_authority": None,
            "matched_announced": None,
            "matched_effective": None,
            "matched_status": None,
        }
    status = best_match.get("status", "unknown")
    outcome = STATUS_TO_OUTCOME.get(status, "other")
    # Days to resolution
    days_to_res = None
    if best_match.get("effective"):
        eff = pd.to_datetime(best_match["effective"]).date()
        days_to_res = (eff - threat_date).days
    return {
        "y1_outcome": outcome,
        "y1_match_score": best_score,
        "y1_days_to_resolution": days_to_res,
        "matched_target": best_match["target"],
        "matched_authority": best_match["authority"],
        "matched_announced": best_match["announced"],
        "matched_effective": best_match.get("effective"),
        "matched_status": best_match.get("status"),
    }

def main():
    threats = pd.read_parquet(THREATS_FP)
    print(f"[load] {len(threats)} A-class threats")
    timeline = json.loads(TIMELINE_FP.read_text())["events"]
    print(f"[load] {len(timeline)} timeline events")

    outcomes = threats.apply(lambda r: assign_outcome(r, timeline), axis=1).apply(pd.Series)
    merged = pd.concat([threats.reset_index(drop=True), outcomes.reset_index(drop=True)], axis=1)
    merged.to_parquet(OUT)
    print(f"[saved] {OUT}")

    print("\nY1 outcome distribution:")
    print(merged["y1_outcome"].value_counts())
    print(f"\nFraction matched (any timeline event): {(merged['y1_outcome'] != 'unmatched').mean():.1%}")

    print("\nDays-to-resolution distribution (matched events with effective date):")
    res = merged.loc[merged["y1_days_to_resolution"].notna(), "y1_days_to_resolution"]
    if len(res):
        print(res.describe())

if __name__ == "__main__":
    main()
