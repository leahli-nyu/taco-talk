"""V3 strict matching: require target match + greedy one-to-one allocation.

Fixes two bugs in v2:
1. v2 allowed matching by date alone when target_match=False (105 collision matches)
2. v2 let multiple episodes claim the same PIIE event (83/108 collided)

V3 rules:
- target_match REQUIRED (score must include the 20-point target bonus)
- Window: [-10, 60] days (threat -> event)
- Each PIIE event matched by at most 1 episode (greedy: smallest anticipation_days wins)
- Episodes that can't get a 1-to-1 match -> next-best unclaimed event, else unmatched

Output: data/processed/episodes_with_outcomes_v3_strict.parquet
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EP_FP = ROOT / "data" / "processed" / "episodes_v2.parquet"
PIIE_FP = ROOT / "data" / "processed" / "piie_timeline_clean.parquet"
OUT_FP = ROOT / "data" / "processed" / "episodes_with_outcomes_v3_strict.parquet"

WINDOW_DAYS = 60
WINDOW_BACK = 10  # allow event to precede threat by up to 10 days

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
    "European Union": ["eu ", " eu", "europ"], "Japan": ["japan"],
    "Brazil": ["brazil"], "United Kingdom": ["uk ", " uk", "britain", "british", "england"],
    "India": ["india"], "Russia": ["russ"], "Korea": ["korea"],
    "Taiwan": ["taiwan"], "Indonesia": ["indonesi"], "Vietnam": ["vietnam"],
    "Argentina": ["argentin"], "Switzerland": ["switz"],
    "Australia": ["austral"], "Cambodia": ["cambodi"], "Thailand": ["thai"],
    "Nicaragua": ["nicaragu"],
    "World": [],  # World is generic, never auto-matches
}

CATEGORY_KEYWORDS = {
    "Tariff": ["tariff"],
    "Fentanyl and Immigration": ["fentanyl", "immigration", "immigrant", "border", "drug"],
    "Trade Deficits": ["trade deficit", "trade imbalance", "trade gap"],
    "Aluminum": ["aluminum", "aluminium"],
    "Steel": ["steel"],
    "Autos": ["auto ", " car ", "vehicle", "automobile"],
    "Lumber": ["lumber", "timber", "softwood"],
    "Critical minerals": ["mineral", "rare earth"],
    "Crticial minerals": ["mineral", "rare earth"],  # typo in PIIE
    "Cranes": ["crane"],
    "Copper": ["copper"],
    "Trucks": ["truck"],
    "Pharmaceuticals": ["pharmaceutical", "drug", "medicine"],
    "Brazil Sanctions": ["brazil", "lula"],
    "Semiconductors": ["semiconductor", "chip", "soxx"],
    "Excess capacity": ["dumping", "excess capacity"],
    "Seafood": ["seafood", "fish"],
    "Aircrafts": ["aircraft", "boeing", "airplane"],
    "Drones": ["drone"],
    "Polysilicon": ["polysilicon", "solar"],
    "Robotics": ["robot"],
}


def target_match(text: str, country: str, category: str) -> bool:
    """Tiered strictness:
    - Specific country (China/Mexico/etc.): country alias hit alone is sufficient
    - "World" events: require a specific commodity/topic keyword (aluminum, steel, etc.)
    - NULL country: require category keyword hit
    """
    if not isinstance(text, str):
        return False
    t = text.lower()

    cat_hit = False
    if isinstance(category, str) and category and category.strip().lower() not in ("none", "nan"):
        kws = CATEGORY_KEYWORDS.get(category, []) + [category.lower()]
        cat_hit = any(kw in t for kw in kws if kw)

    if not isinstance(country, str) or not country or country.strip().lower() in ("none", "nan"):
        return cat_hit  # NULL country -> rely on category

    if country.lower() == "world":
        return cat_hit  # World requires commodity hit

    aliases = COUNTRY_ALIASES.get(country, []) + [country.lower()]
    country_hit = any(a in t for a in aliases if a)
    return country_hit


def score_pair(ep_first_date, ep_text, evt_date, evt_country, evt_category) -> tuple[float, int]:
    """Returns (score, anticipation_days). Score 0 if no target match."""
    signed = (pd.to_datetime(evt_date).date() - pd.to_datetime(ep_first_date).date()).days
    if signed < -WINDOW_BACK or signed > WINDOW_DAYS:
        return 0.0, signed
    tm = target_match(ep_text, evt_country, evt_category)
    if not tm:
        return 0.0, signed
    # Score = target bonus + proximity bonus (smaller signed = bigger bonus, prefer threat-before-event)
    score = 100.0
    if signed >= 0:
        score += (WINDOW_DAYS - signed)
    else:
        score += (WINDOW_BACK + signed) * 0.5  # backwards match: half weight
    return score, signed


def main():
    eps = pd.read_parquet(EP_FP)
    timeline = pd.read_parquet(PIIE_FP).reset_index(drop=True)
    timeline["evt_idx"] = timeline.index
    print(f"[load] {len(eps)} episodes x {len(timeline)} PIIE events")

    # Compute all valid (episode, event) pairs with target_match=True
    candidates = []
    for ei, ep in eps.iterrows():
        text = (str(ep.get("first_text") or "") + " " + str(ep.get("all_text") or ""))
        for _, evt in timeline.iterrows():
            score, signed = score_pair(
                ep["first_post_date"], text,
                evt["date"], evt.get("country"), evt.get("category"),
            )
            if score > 0:
                candidates.append({
                    "ep_idx": ei,
                    "episode_id": ep["episode_id"],
                    "evt_idx": evt["evt_idx"],
                    "score": score,
                    "anticipation_days": signed,
                    "evt_date": evt["date"],
                    "evt_country": evt.get("country"),
                    "evt_category": evt.get("category"),
                    "evt_status": evt["status_inferred"],
                })
    cand_df = pd.DataFrame(candidates)
    print(f"[candidates] {len(cand_df)} (episode, event) pairs with target_match=True")
    print(f"[ep coverage] {cand_df['ep_idx'].nunique()}/{len(eps)} episodes have at least 1 valid match")

    # Greedy one-to-one: sort by score desc, assign each ep to highest available event
    cand_df = cand_df.sort_values("score", ascending=False).reset_index(drop=True)
    ep_assigned = {}  # ep_idx -> chosen candidate row
    evt_claimed = set()
    for _, row in cand_df.iterrows():
        if row["ep_idx"] in ep_assigned:
            continue
        if row["evt_idx"] in evt_claimed:
            continue
        ep_assigned[row["ep_idx"]] = row
        evt_claimed.add(row["evt_idx"])

    print(f"[assigned] {len(ep_assigned)} episodes one-to-one with unique PIIE events")
    print(f"[unmatched] {len(eps) - len(ep_assigned)} episodes have no available unique match")

    # Build output
    out_rows = []
    for ei, ep in eps.iterrows():
        row = ep.to_dict()
        if ei in ep_assigned:
            a = ep_assigned[ei]
            row["y1_outcome"] = STATUS_BUCKET.get(a["evt_status"], "other")
            row["y1_match_score"] = a["score"]
            row["matched_country"] = a["evt_country"]
            row["matched_category"] = a["evt_category"]
            row["matched_date"] = str(pd.to_datetime(a["evt_date"]).date())
            row["anticipation_days"] = a["anticipation_days"]
        else:
            row["y1_outcome"] = "no_policy_event_found"
            row["y1_match_score"] = 0
            row["matched_country"] = None
            row["matched_category"] = None
            row["matched_date"] = None
            row["anticipation_days"] = None
        out_rows.append(row)
    out = pd.DataFrame(out_rows)
    out.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")

    print("\n=== V3 strict Y1 distribution ===")
    print(out["y1_outcome"].value_counts())
    print(f"Match rate: {(out['y1_outcome'] != 'no_policy_event_found').mean():.1%}")
    matched = out[out["anticipation_days"].notna()]
    if len(matched):
        print(f"\nAnticipation days (matched):")
        print(matched["anticipation_days"].describe())


if __name__ == "__main__":
    main()
