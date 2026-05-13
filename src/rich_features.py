"""Rich feature extraction on consensus A class.

For each post:
- 3 calls via Claude Haiku 4.5 → median + SD per feature
- 1 call via GPT-4o-mini → cross-LLM validation

Output: data/processed/rich_features.parquet with columns:
  _id, claude_call_1_<feature>, claude_call_2_<feature>, claude_call_3_<feature>,
  gpt_<feature>, claude_median_<feature>, claude_sd_<feature>, ...
"""
from __future__ import annotations
import json
import os
import re
import time
import statistics
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
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

from anthropic import Anthropic
from openai import OpenAI

CONSENSUS_A = ROOT / "data" / "processed" / "consensus_a.parquet"
OUT_FP = ROOT / "data" / "processed" / "rich_features.parquet"

FEATURE_NAMES = [
    "commitment_strength", "specificity", "hedging_level", "dramatization",
    "conditional_framing", "audience_cost", "precedent_invocation",
    "negotiation_framing", "personal_attack", "ego_centric_framing",
]

PROMPT = """You are scoring a Trump Truth Social post on 10 linguistic dimensions.

The post has already been classified as an Economic Commissive Threat (A class).

For each dimension, rate from 0 to 10 using the anchor examples.

[commitment_strength] How strongly does Trump commit himself?
- 0: "I'm thinking about possibly considering tariffs at some point"
- 3: "We are looking at China tariffs"
- 6: "I will look at imposing tariffs"
- 10: "I AM SIGNING the executive order TODAY at 3pm"

[specificity] How concrete is the target/action/timeline?
- 0: "tariffs are coming"
- 3: "China tariffs are coming"
- 6: "China tariffs at 25%"
- 10: "100% tariff on Chinese EVs effective March 15, 2026"

[hedging_level] How much does Trump leave himself an out?
- 0: "WILL impose 100% tariff TOMORROW!"
- 3: "We are considering tariffs"
- 6: "Maybe we should look at China tariffs"
- 10: "Perhaps eventually we might consider exploring options"

[dramatization] Trump-style hyperbole and emphasis
- 0: technical / measured
- 3: "important", "significant"
- 6: "huge", "tremendous"
- 10: "BIGLY MASSIVE TREMENDOUS DISASTER!!!" all-caps + multi-exclamation

[conditional_framing] Is action contingent on others' behavior?
- 0: unconditional ("I will do X")
- 5: "If they don't comply, X"
- 10: "Unless they immediately do A, B, AND C, then maybe X"

[audience_cost] Is commitment publicly irreversible-feeling?
- 0: "We're thinking about it"
- 5: "I publicly commit to X"
- 10: "Before the entire world, I promise X. Bookmark this."

[precedent_invocation] Reference to Reagan, prior policies, history
- 0: no historical reference
- 5: passing reference to past
- 10: extended Reagan/Lincoln/American history invocation

[negotiation_framing] Is threat a negotiating chip or final?
- 0: "Final decision, no negotiation"
- 5: "Unless they come to the table"
- 10: "I'm using this as leverage to get what we really want"

[personal_attack] Targeted at named individual?
- 0: target is country/entity
- 5: country + leader named
- 10: extensive personal attack on named individual

[ego_centric_framing] How much is "I/me/my" central?
- 0: "the government", "the country"
- 5: "we", "the administration"
- 10: "I personally", "my decision alone", "as your president, I"

Output strict JSON only:
{
  "commitment_strength": <int 0-10>,
  "specificity": <int 0-10>,
  "hedging_level": <int 0-10>,
  "dramatization": <int 0-10>,
  "conditional_framing": <int 0-10>,
  "audience_cost": <int 0-10>,
  "precedent_invocation": <int 0-10>,
  "negotiation_framing": <int 0-10>,
  "personal_attack": <int 0-10>,
  "ego_centric_framing": <int 0-10>,
  "target_entity": "<country/sector/company or null>",
  "policy_action": "<short verb phrase or null>",
  "deadline_phrase": "<verbatim or null>"
}

Post:
\"\"\"
{POST}
\"\"\""""


def parse_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        # Try to extract JSON substring
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        return {"_parse_err": raw[:300]}


def call_claude(text: str) -> dict:
    client = Anthropic()
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            timeout=25.0,
            messages=[{"role": "user", "content": PROMPT.replace("{POST}", text[:2000])}],
        )
        return parse_json(msg.content[0].text)
    except Exception as e:
        return {"_api_err": str(e)[:120]}


def call_gpt(text: str) -> dict:
    client = OpenAI()
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=500,
            timeout=25.0,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": PROMPT.replace("{POST}", text[:2000])}],
        )
        return parse_json(resp.choices[0].message.content)
    except Exception as e:
        return {"_api_err": str(e)[:120]}


def main():
    df = pd.read_parquet(CONSENSUS_A)
    print(f"[load] {len(df)} consensus A posts")

    results = []
    t0 = time.time()
    total_calls = len(df) * 4  # 3 Claude + 1 GPT per post

    # We submit ALL calls (3 claude + 1 gpt for each post) in one thread pool
    tasks = []
    for i, r in df.iterrows():
        post_id = str(r["_id"]) if "_id" in r.index else str(r["id"])
        text = str(r["content"])
        for call_n in (1, 2, 3):
            tasks.append((post_id, text, f"claude_{call_n}", call_claude))
        tasks.append((post_id, text, "gpt", call_gpt))

    completed = 0

    def runner(task):
        post_id, text, name, fn = task
        out = fn(text)
        return post_id, name, out

    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(runner, t): t for t in tasks}
        for f in as_completed(futures):
            post_id, name, result = f.result()
            results.append({"_id": post_id, "call_name": name, **result})
            completed += 1
            if completed % 25 == 0 or completed == total_calls:
                elapsed = time.time() - t0
                rate = completed / elapsed if elapsed > 0 else 0
                eta = (total_calls - completed) / rate if rate > 0 else 0
                print(f"  [{completed}/{total_calls}] rate={rate:.2f}/s eta={eta:.0f}s", flush=True)

    out = pd.DataFrame(results)
    out.to_parquet(OUT_FP)
    print(f"\n[saved] {OUT_FP}")
    print(out["call_name"].value_counts())
    print(f"\nParse errors: {out['_parse_err'].notna().sum() if '_parse_err' in out.columns else 0}")
    print(f"API errors:   {out['_api_err'].notna().sum() if '_api_err' in out.columns else 0}")


if __name__ == "__main__":
    main()
