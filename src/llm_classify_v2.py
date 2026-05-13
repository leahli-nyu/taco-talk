"""LLM A/B/C classification with operationalized Speech Act Theory.

Phase 1 (full corpus): label each of ~6,943 posts as A/B/C.
Cross-model: Claude Haiku 4.5 + GPT-4o-mini.

Output: data/processed/labeled_v2_{claude,gpt}.parquet
"""
from __future__ import annotations
import json
import os
import time
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Load .env
_env = ROOT / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")

IN_FP = ROOT / "data" / "processed" / "truth_second_term.parquet"

PROMPT = """You are classifying a Trump Truth Social post.

STEP 1: Determine whether this post is a COMMISSIVE speech act.

A commissive is a statement where Trump COMMITS HIMSELF to taking a future action.

Markers of commissive:
- First-person subject: "I", "we", "my administration", "the United States" (when Trump is the agent)
- Future-oriented verb: "will", "going to", "plan to", "intend to", "am signing"
- Specific action attributable to the speaker as agent

Examples of COMMISSIVE:
- "I will impose 25% tariff on Mexico"
- "We are going to sign the executive order tomorrow"
- "I plan to fire Powell if he doesn't lower rates"
- "On Day One, my administration will end the war"

Examples of NOT COMMISSIVE:
- "China will pay for this!"  (prediction about China, not commitment by Trump)
- "The tariff is working great!"  (boast about past action)
- "Putin should withdraw from Ukraine"  (directive to others)
- "Tariffs are tremendous for America"  (assertive opinion)
- "Crooked Joe destroyed the economy"  (attack on others)

BORDERLINE: "If X, then I will Y" (conditional commitment) — rate as commissive with lower confidence.

STEP 2: If commissive, determine POLICY AREA.

Economic-financial transmission (->Label A):
- tariff (import duties on foreign goods)
- sanctions (OFAC, embargo, financial restrictions)
- trade_agreement (USMCA, bilateral trade deals)
- fed_monetary (Powell, interest rates, currency policy)
- commodity_intervention (oil exports, agricultural subsidies, mineral controls)
- antitrust_tech (regulation of tech firms)
- financial_regulation (banking, SEC, crypto rules)

Non-economic primary (->Label B):
- immigration_enforcement (ICE actions, deportations, border)
- military_action (deployments, strikes)
- judicial_prosecution (DOJ investigations)
- social_cultural (education, gender policy, free speech regulation)
- foreign_diplomacy_non_econ (state visits, non-trade diplomacy)

STEP 3: Output strict JSON ONLY (no other text):
{"is_commissive": true|false, "commissive_confidence": 0.0-1.0, "policy_area": "<one of above or 'other'>", "label": "A"|"B"|"C", "reason": "<one sentence>"}

Decision tree:
- is_commissive == false -> C
- is_commissive == true && policy_area in {tariff, sanctions, trade_agreement, fed_monetary, commodity_intervention, antitrust_tech, financial_regulation} -> A
- is_commissive == true && policy_area in {immigration_enforcement, military_action, judicial_prosecution, social_cultural, foreign_diplomacy_non_econ} -> B
- is_commissive == true && policy_area == 'other' -> B (default conservatively)

Post:
\"\"\"
{POST_TEXT}
\"\"\""""


def parse_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        # strip code fences
        raw = raw.split("```", 2)[1] if raw.count("```") >= 2 else raw[3:]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    try:
        return json.loads(raw)
    except Exception as e:
        return {"label": "PARSE_ERR", "raw": raw[:200], "err": str(e)}


def label_claude(client, text: str) -> dict:
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            timeout=20.0,
            messages=[{"role": "user", "content": PROMPT.replace("{POST_TEXT}", text[:2000])}],
        )
        return parse_json(msg.content[0].text)
    except Exception as e:
        return {"label": "API_ERR", "err": str(e)[:120]}


def label_gpt(client, text: str) -> dict:
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=300,
            timeout=20.0,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": PROMPT.replace("{POST_TEXT}", text[:2000])}],
        )
        return parse_json(resp.choices[0].message.content)
    except Exception as e:
        return {"label": "API_ERR", "err": str(e)[:120]}


def main(model: str = "claude", limit: int | None = None):
    df = pd.read_parquet(IN_FP)
    if limit:
        df = df.head(limit)
    print(f"[load] {len(df)} posts", flush=True)

    if model == "claude":
        from anthropic import Anthropic
        client = Anthropic()
        labeler = label_claude
        out_fp = ROOT / "data" / "processed" / "labeled_v2_claude.parquet"
    elif model == "gpt":
        from openai import OpenAI
        client = OpenAI()
        labeler = label_gpt
        out_fp = ROOT / "data" / "processed" / "labeled_v2_gpt.parquet"
    else:
        raise ValueError(f"unknown model: {model}")

    results = []
    t0 = time.time()
    save_every = 100
    for i, r in df.iterrows():
        out = labeler(client, str(r["content"]))
        out["_id"] = str(r["id"])
        out["_date"] = str(r["created_at"])
        out["_text"] = str(r["content"])[:300]
        results.append(out)
        if (i + 1) % 25 == 0 or i == len(df) - 1:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            eta = (len(df) - i - 1) / rate if rate > 0 else 0
            print(f"  [{model}] [{i + 1}/{len(df)}]  rate={rate:.2f}/s  eta={eta:.0f}s", flush=True)
            if (i + 1) % save_every == 0:
                pd.DataFrame(results).to_parquet(out_fp)

    pd.DataFrame(results).to_parquet(out_fp)
    print(f"[saved] {out_fp}  total_time={time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=["claude", "gpt"], required=True)
    p.add_argument("--limit", type=int, default=None)
    a = p.parse_args()
    main(model=a.model, limit=a.limit)
