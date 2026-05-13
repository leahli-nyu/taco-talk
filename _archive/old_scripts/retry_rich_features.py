"""Retry failed rich features calls (rate-limit errors).

Lower concurrency (3 threads) + exponential backoff.
"""
from __future__ import annotations
import json
import os
import time
import random
import re
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

IN_FP = ROOT / "data" / "processed" / "rich_features.parquet"
CONSENSUS_A = ROOT / "data" / "processed" / "consensus_a.parquet"

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
- 0: unconditional
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
{"commitment_strength": <0-10>, "specificity": <0-10>, "hedging_level": <0-10>,
 "dramatization": <0-10>, "conditional_framing": <0-10>, "audience_cost": <0-10>,
 "precedent_invocation": <0-10>, "negotiation_framing": <0-10>,
 "personal_attack": <0-10>, "ego_centric_framing": <0-10>,
 "target_entity": "<...>", "policy_action": "<...>", "deadline_phrase": "<...>"}

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
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        return {"_parse_err": raw[:300]}


def call_claude_retry(text: str, max_retries: int = 5) -> dict:
    client = Anthropic()
    for attempt in range(max_retries):
        try:
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                timeout=30.0,
                messages=[{"role": "user", "content": PROMPT.replace("{POST}", text[:2000])}],
            )
            return parse_json(msg.content[0].text)
        except Exception as e:
            es = str(e)
            if "429" in es or "rate_limit" in es.lower() or "overloaded" in es.lower():
                wait = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait)
                continue
            return {"_api_err": es[:120]}
    return {"_api_err": f"retried {max_retries} times"}


def call_gpt_retry(text: str, max_retries: int = 5) -> dict:
    client = OpenAI()
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=500,
                timeout=30.0,
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": PROMPT.replace("{POST}", text[:2000])}],
            )
            return parse_json(resp.choices[0].message.content)
        except Exception as e:
            es = str(e)
            if "429" in es or "rate_limit" in es.lower():
                wait = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait)
                continue
            return {"_api_err": es[:120]}
    return {"_api_err": f"retried {max_retries} times"}


def main():
    raw = pd.read_parquet(IN_FP)
    consensus = pd.read_parquet(CONSENSUS_A)
    consensus["_id"] = consensus["_id"].astype(str)
    raw["_id"] = raw["_id"].astype(str)

    # Identify failed calls (any of: _api_err, _parse_err, or missing feature columns)
    feature_cols = ["commitment_strength", "specificity", "hedging_level"]
    raw["is_failed"] = (raw.get("_api_err").notna() if "_api_err" in raw.columns else False) | \
                      (raw.get("_parse_err").notna() if "_parse_err" in raw.columns else False)
    # If a row has _api_err / _parse_err OR all feature columns are NaN, it's failed
    feat_present = raw[feature_cols].notna().any(axis=1) if all(c in raw.columns for c in feature_cols) else False
    raw["is_failed"] = raw["is_failed"] | (~feat_present)
    failed = raw[raw["is_failed"]].copy()
    print(f"Total raw rows: {len(raw)}")
    print(f"Failed: {len(failed)}")
    if len(failed) == 0:
        print("Nothing to retry!")
        return

    # Build retry tasks
    text_map = {str(r["_id"]): str(r["content"]) for _, r in consensus.iterrows()}

    def runner(idx):
        row = failed.iloc[idx]
        pid = row["_id"]
        call_name = row["call_name"]
        text = text_map.get(pid, "")
        if not text:
            return idx, {"_api_err": "no text in consensus"}
        if call_name.startswith("claude"):
            out = call_claude_retry(text)
        else:
            out = call_gpt_retry(text)
        return idx, out

    t0 = time.time()
    new_results = {}
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(runner, i): i for i in range(len(failed))}
        completed = 0
        for f in as_completed(futures):
            idx, result = f.result()
            new_results[idx] = result
            completed += 1
            if completed % 10 == 0 or completed == len(failed):
                elapsed = time.time() - t0
                rate = completed / elapsed if elapsed > 0 else 0
                eta = (len(failed) - completed) / rate if rate > 0 else 0
                print(f"  [{completed}/{len(failed)}] rate={rate:.2f}/s eta={eta:.0f}s", flush=True)

    # Update raw with new results
    for idx, new_res in new_results.items():
        for k, v in new_res.items():
            raw.at[failed.index[idx], k] = v

    # Drop the helper column
    if "is_failed" in raw.columns:
        del raw["is_failed"]

    raw.to_parquet(IN_FP)
    still_failed = ((raw.get("_api_err").notna() if "_api_err" in raw.columns else False) |
                    (raw.get("_parse_err").notna() if "_parse_err" in raw.columns else False))
    print(f"\n[saved] {IN_FP}")
    print(f"Still failed: {still_failed.sum()}")


if __name__ == "__main__":
    main()
