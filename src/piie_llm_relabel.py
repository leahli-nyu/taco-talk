"""Re-label PIIE status using Claude (replaces regex). 145 events.

Output: data/processed/piie_timeline_llm_clean.parquet
"""
from __future__ import annotations
import json, os, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ENV_FP = ROOT / ".env"
if ENV_FP.exists():
    for line in ENV_FP.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=",1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")

IN_FP = ROOT / "data" / "processed" / "piie_timeline_clean.parquet"
OUT_FP = ROOT / "data" / "processed" / "piie_timeline_llm_clean.parquet"

PROMPT_TMPL = """Classify the **policy outcome status** of this tariff/trade event.

Description: "{desc}"
Country: {country}
Category: {category}

Choose ONE label that best describes what happened to this specific event:
- "in_effect": The action was IMPLEMENTED. Tariff actually imposed; EO signed and went into effect; rule promulgated; took effect on stated date.
- "modified_or_withdrawn": The action was REDUCED, DELAYED, EXEMPTED, PAUSED, or part of a WALK-BACK DEAL where the original threat was softened. Includes new trade deals that lower tariffs from a higher threatened level.
- "struck_down": Invalidated by a COURT or SCOTUS (e.g., IEEPA ruling).
- "announced": Threatened/announced but NOT YET implemented at the time of this event (action still pending).
- "investigation": Section 232/301 or similar investigation initiated, no tariff imposed yet.
- "other": Doesn't fit above (e.g., procedural update, study, framework agreement with no concrete tariff change).

Return strict JSON only: {{"status": "<label>"}}"""

_JSON_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)
def parse(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1] if "```" in text[3:] else text[3:]
        text = text.lstrip("json").strip()
    try: return json.loads(text)
    except Exception:
        m = _JSON_RE.search(text)
        if m:
            try: return json.loads(m.group(0))
            except Exception: return None
    return None


def main():
    df = pd.read_parquet(IN_FP).reset_index(drop=True)
    print(f"[load] {len(df)} PIIE events")
    import anthropic
    client = anthropic.Anthropic()
    new_labels = []
    for i, r in df.iterrows():
        prompt = PROMPT_TMPL.format(
            desc=str(r["description"])[:1500],
            country=r["country"] or "—",
            category=r["category"] or "—",
        )
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=60,
                messages=[{"role":"user","content":prompt}],
            )
            d = parse(resp.content[0].text)
            label = d.get("status") if d else "parse_err"
            if label not in ("in_effect","modified_or_withdrawn","struck_down","announced","investigation","other"):
                label = "other"
        except Exception as e:
            print(f"  err on {i}: {e}")
            label = "error"
        new_labels.append(label)
        if (i+1) % 20 == 0:
            print(f"  [{i+1}/{len(df)}]", flush=True)

    df["status_llm"] = new_labels
    df.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")

    # Compare to regex labels
    print("\nLLM vs regex status crosstab:")
    print(pd.crosstab(df["status_inferred"], df["status_llm"], margins=True))
    changed = (df["status_inferred"] != df["status_llm"]).sum()
    print(f"\nChanged labels: {changed}/{len(df)}")


if __name__ == "__main__":
    main()
