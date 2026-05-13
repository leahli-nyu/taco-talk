"""Anonymize episode texts before BT comparison.

Replaces concrete entities with generic placeholders so that LLM ranks
on substantive linguistic features (commitment, hedging, specificity)
rather than surface tokens (country names, percentages, dollar amounts).

Output: data/processed/episodes_v2_narrow_anon.parquet
"""
from __future__ import annotations
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN_FP = ROOT / "data" / "processed" / "episodes_v2_narrow.parquet"
OUT_FP = ROOT / "data" / "processed" / "episodes_v2_narrow_anon.parquet"

# Country aliases for anonymization
COUNTRIES = [
    "China", "Chinese", "Beijing",
    "Mexico", "Mexican",
    "Canada", "Canadian",
    "European Union", "EU ", " EU", "Europe", "European",
    "Japan", "Japanese",
    "Brazil", "Brazilian",
    "United Kingdom", "UK ", " UK", "Britain", "British", "England",
    "India", "Indian",
    "Russia", "Russian", "Moscow",
    "Korea", "Korean", "Seoul",
    "Taiwan", "Taiwanese",
    "Indonesia",
    "Vietnam", "Vietnamese",
    "Argentina",
    "Switzerland", "Swiss",
    "Australia", "Australian",
    "Cambodia", "Cambodian",
    "Thailand", "Thai",
    "Nicaragua",
    "Denmark", "Danish",
    "Greenland",
    "Iran", "Iranian",
    "Venezuela", "Venezuelan",
    "Ukraine", "Ukrainian",
    "Philippines", "Filipino",
    "Malaysia",
    "Singapore",
]

# Industries / commodities
INDUSTRIES = [
    "steel", "aluminum", "aluminium",
    "copper", "lumber", "timber", "softwood",
    "automobile", "automobiles", "auto ", "autos", "car ", "vehicle",
    "semiconductor", "semiconductors", "chip",
    "pharmaceutical", "pharmaceuticals", "drug compan",
    "soybean", "soybeans", "agricultural", "agriculture",
    "rare earth", "critical mineral",
    "Apple", "iPhone", "Samsung",
    "Boeing", "aircraft",
    "fentanyl", "drug",
    "lumber",
    "furniture",
    "appliance",
    "crane",
    "robotics",
]

# People (Trump-adjacent named entities)
PERSONS = [
    "Xi Jinping", "Xi ", "Putin", "Powell", "Jerome Powell",
    "Lula", "da Silva",
    "Modi",
    "Carney", "Mark Carney",
    "von der Leyen", "Ursula",
    "Macron",
    "Merkel",
    "Bolsonaro",
    "Sheinbaum",
    "Trudeau",
    "Navarro", "Peter Navarro",
    "Bessent",
    "Lighthizer",
    "Greer",
]


def anonymize(text: str) -> str:
    """Replace specific entities with generic placeholders."""
    if not isinstance(text, str):
        return text
    s = text

    # Percentages (e.g., "100%", "25 percent")
    s = re.sub(r"\b\d+(\.\d+)?\s*%", "[PERCENT]", s)
    s = re.sub(r"\b\d+(\.\d+)?\s*percent\b", "[PERCENT]", s, flags=re.IGNORECASE)

    # Dollar amounts (e.g., "$10 billion", "$166B")
    s = re.sub(r"\$\d+(\.\d+)?\s*(billion|million|trillion|B|M|T)?", "[AMOUNT]", s, flags=re.IGNORECASE)
    s = re.sub(r"\b\d+(\.\d+)?\s*(billion|million|trillion)\s*dollars?", "[AMOUNT]", s, flags=re.IGNORECASE)

    # Dates (basic patterns: "January 20", "Feb 3rd", "April 2nd", "2025")
    s = re.sub(
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+(st|nd|rd|th)?,?\s*(\d{4})?",
        "[DATE]", s, flags=re.IGNORECASE,
    )
    s = re.sub(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?\s+\d+(st|nd|rd|th)?,?\s*(\d{4})?",
               "[DATE]", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(20\d{2})\b", "[YEAR]", s)
    s = re.sub(r"\bDay\s+One\b", "[DATE]", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(today|tomorrow|yesterday)\b", "[DATE]", s, flags=re.IGNORECASE)

    # Country names — case-sensitive matching for proper nouns
    for c in COUNTRIES:
        # use case-sensitive replacement to avoid mangling common words
        s = re.sub(re.escape(c), "[COUNTRY]", s)
    # Common adjectivals lowercase variant
    for c in ["chinese", "mexican", "canadian", "european", "japanese", "indian", "russian", "korean"]:
        s = re.sub(r"\b" + c + r"\b", "[COUNTRY_ADJ]", s, flags=re.IGNORECASE)

    # Industry / commodities
    for ind in INDUSTRIES:
        s = re.sub(r"\b" + re.escape(ind) + r"\b", "[INDUSTRY]", s, flags=re.IGNORECASE)

    # Persons
    for p in PERSONS:
        s = re.sub(re.escape(p), "[PERSON]", s)

    # Collapse repeated placeholders ("[COUNTRY] and [COUNTRY]" -> "[COUNTRY] and [COUNTRY]")
    # leave as is; gives info about list-of-targets

    return s


def main():
    eps = pd.read_parquet(IN_FP)
    eps["first_text_anon"] = eps["first_text"].apply(anonymize)
    eps.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}  rows={len(eps)}")
    print("\n=== Sample anonymizations ===")
    for i in [0, 5, 12, 20]:
        if i < len(eps):
            print(f"\n--- Episode {eps.iloc[i]['episode_id']} ---")
            print(f"  ORIG: {eps.iloc[i]['first_text'][:200]}")
            print(f"  ANON: {eps.iloc[i]['first_text_anon'][:200]}")


if __name__ == "__main__":
    main()
