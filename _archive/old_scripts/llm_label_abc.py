"""LLM labeler for A/B/C classification using Speech Act framework.

A = Commissive (will/going to/promising) + economic policy + financial transmission
B = Commissive + non-economic policy (immigration enforcement, military, judicial)
C = Non-commissive (complaint, retweet commentary, endorsement, boast)

Uses Anthropic Claude Haiku (cheap, fast). ~$0.05 for 501 posts.
"""
from __future__ import annotations
import json
import os
import time
from pathlib import Path
import pandas as pd
from anthropic import Anthropic

ROOT = Path(__file__).resolve().parents[1]

# Load .env if present (project-scoped API key)
_env = ROOT / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")
IN_FP = ROOT / "data" / "processed" / "econ_candidates.parquet"
OUT_FP = ROOT / "data" / "processed" / "labeled_abc.parquet"
SAMPLE_FP = ROOT / "data" / "processed" / "qa_sample_50.json"

PROMPT_TEMPLATE = """You classify a Trump Truth Social post into one of three categories using Speech Act Theory.

CATEGORIES:
- A (Economic Commissive Threat): The post is a COMMISSIVE speech act (Trump commits/promises future action — uses "will", "going to", "I plan to", etc.) AND the action is a government-executable policy AND the policy has a direct economic or financial transmission channel. Examples: tariffs, trade deals/breaks, sanctions, import/export bans, Fed rate pressure, currency action, commodity bans.

- B (Non-Economic Commissive Threat): Commissive speech act + government-executable policy, but the action's PRIMARY impact is NOT economic/financial. Examples: deportations, military deployments, prosecuting opponents, firing officials (non-Fed).

- C (Not a Threat): Anything else. Includes: complaints, attacks, boasts, endorsements, descriptions of past actions, news commentary, conditional/hypothetical without commitment.

OUTPUT FORMAT (strict JSON, nothing else):
{"label": "A" | "B" | "C", "target": "<country/entity/sector or null>", "policy_action": "<short noun phrase or null>", "deadline_phrase": "<verbatim or null>", "confidence": 0.0-1.0, "reason": "<one short sentence>"}

POST:
\"\"\"
{post}
\"\"\""""

def label_one(client: Anthropic, text: str, timeout_s: float = 20.0) -> dict:
    prompt = PROMPT_TEMPLATE.replace("{post}", text[:2000])
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            timeout=timeout_s,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        return {"label": "API_ERR", "err": str(e)[:120]}
    raw = msg.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw.strip())
    except Exception as e:
        return {"label": "PARSE_ERR", "raw": raw[:200], "err": str(e)}

def main(limit: int | None = None, qa_n: int = 50):
    df = pd.read_parquet(IN_FP)
    if limit:
        df = df.head(limit)
    print(f"[load] {len(df)} candidates", flush=True)
    client = Anthropic()
    results = []
    t0 = time.time()
    for i, r in df.iterrows():
        out = label_one(client, r["content"])
        out["_id"] = r["id"]
        out["_date"] = str(r["created_at"])
        out["_text"] = r["content"][:500]
        results.append(out)
        if (i + 1) % 25 == 0 or i == len(df) - 1:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            eta = (len(df) - i - 1) / rate if rate > 0 else 0
            print(f"  [{i + 1}/{len(df)}]  rate={rate:.2f}/s  eta={eta:.0f}s", flush=True)
            # Incremental save every 25
            pd.DataFrame(results).to_parquet(OUT_FP)
    labeled = pd.DataFrame(results)
    labeled.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}  total_time={time.time()-t0:.1f}s", flush=True)
    # Pull a stratified QA sample (mostly A class, some B and C)
    a = labeled[labeled.label == "A"].sample(min(30, (labeled.label == "A").sum()), random_state=7) if (labeled.label == "A").any() else labeled.head(0)
    b = labeled[labeled.label == "B"].sample(min(10, (labeled.label == "B").sum()), random_state=7) if (labeled.label == "B").any() else labeled.head(0)
    c = labeled[labeled.label == "C"].sample(min(10, (labeled.label == "C").sum()), random_state=7) if (labeled.label == "C").any() else labeled.head(0)
    qa = pd.concat([a, b, c])
    qa.to_json(SAMPLE_FP, orient="records", indent=2, force_ascii=False)
    print(f"[saved] {SAMPLE_FP}  ({len(qa)} for human QA)")
    # Print summary
    print("\nLabel counts:")
    print(labeled["label"].value_counts())

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(limit=n)
