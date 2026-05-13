"""LLM zero-shot baseline: directly ask LLM to predict outcome from text.

This is the comparison point for our feature-engineered Cox PH model.
Paper question: does our pipeline add value beyond raw LLM?

Approach: for each episode, give LLM the first post's text and ask it to predict
outcome bucket. Compare to actual outcome.

Two LLMs: Claude Haiku 4.5 + GPT-4o-mini (cross-validation).
"""
from __future__ import annotations
import json
import os
import re
import time
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

EP_FP = ROOT / "data" / "processed" / "episodes_with_outcomes_v2.parquet"
OUT_FP = ROOT / "data" / "processed" / "zero_shot_baseline.parquet"


PROMPT = """Trump's Truth Social post (commissive tariff/economic threat):

\"\"\"
{POST}
\"\"\"

Predict the outcome within 90 days. Output strict JSON only:
{
  "prediction": "executed" | "modified_or_withdrawn" | "unresolved",
  "confidence": 0.0-1.0,
  "reasoning": "<one sentence>"
}

Notes:
- "executed" = policy enacted in Federal Register
- "modified_or_withdrawn" = threat softened, retracted, or partially implemented (TACO outcome)
- "unresolved" = announced but no formal action yet"""


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
        return {"prediction": "PARSE_ERR", "raw": raw[:200]}


def call_claude(text):
    client = Anthropic()
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=300, timeout=25.0,
            messages=[{"role": "user", "content": PROMPT.replace("{POST}", text[:2000])}],
        )
        return parse_json(msg.content[0].text)
    except Exception as e:
        return {"prediction": "API_ERR", "err": str(e)[:120]}


def call_gpt(text):
    client = OpenAI()
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini", max_tokens=300, timeout=25.0,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": PROMPT.replace("{POST}", text[:2000])}],
        )
        return parse_json(resp.choices[0].message.content)
    except Exception as e:
        return {"prediction": "API_ERR", "err": str(e)[:120]}


def main():
    eps = pd.read_parquet(EP_FP)
    eps = eps[eps["y1_outcome"].isin(
        ["executed", "modified_or_withdrawn", "announced_unresolved"])].copy()
    print(f"[load] {len(eps)} episodes")
    rows = []

    def runner(idx):
        r = eps.iloc[idx]
        text = str(r["first_text"])
        c = call_claude(text)
        g = call_gpt(text)
        return {
            "episode_id": int(r["episode_id"]),
            "actual_outcome": r["y1_outcome"],
            "claude_pred": c.get("prediction"),
            "claude_conf": c.get("confidence"),
            "gpt_pred": g.get("prediction"),
            "gpt_conf": g.get("confidence"),
        }

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(runner, i): i for i in range(len(eps))}
        completed = 0
        for f in as_completed(futures):
            rows.append(f.result())
            completed += 1
            if completed % 25 == 0 or completed == len(eps):
                elapsed = time.time() - t0
                rate = completed / elapsed
                eta = (len(eps) - completed) / rate if rate > 0 else 0
                print(f"  [{completed}/{len(eps)}] rate={rate:.1f}/s eta={eta:.0f}s", flush=True)

    df = pd.DataFrame(rows)
    df.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}")
    print(f"\n=== Zero-shot accuracy ===")
    # Map actuals to predicted classes
    def harmonize(s):
        if s == "executed": return "executed"
        if s == "modified_or_withdrawn": return "modified_or_withdrawn"
        if s == "announced_unresolved": return "unresolved"
        return s
    df["actual_h"] = df["actual_outcome"].apply(harmonize)
    for model in ("claude_pred", "gpt_pred"):
        valid = df[~df[model].isin(["PARSE_ERR", "API_ERR", None])]
        if len(valid):
            acc = (valid[model] == valid["actual_h"]).mean()
            print(f"  {model}: accuracy = {acc:.1%}  (N={len(valid)})")
            print(pd.crosstab(valid["actual_h"], valid[model], margins=True))


if __name__ == "__main__":
    main()
