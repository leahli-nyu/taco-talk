"""V2 pairwise Bradley-Terry comparison.

Improvements over v1:
- Anonymized text input (countries / industries / dates / amounts -> placeholders)
- 1-7 graduated scale instead of A/B/tie (more BT signal granularity)
- Cross-LLM: Claude AND GPT both rate same pairs; consensus is reported

Scale (per feature, A vs B comparison):
  1 = A definitely much higher
  2 = A clearly higher
  3 = A slightly higher
  4 = tie
  5 = B slightly higher
  6 = B clearly higher
  7 = B definitely much higher

Outputs:
  data/processed/pairwise_bt_v2_claude.parquet
  data/processed/pairwise_bt_v2_gpt.parquet
"""
from __future__ import annotations
import json
import os
import random
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ENV_FP = ROOT / ".env"
if ENV_FP.exists():
    for line in ENV_FP.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")

EP_FP = ROOT / "data" / "processed" / "episodes_v2_narrow_anon.parquet"
OUT_C = ROOT / "data" / "processed" / "pairwise_bt_v2_claude.parquet"
OUT_G = ROOT / "data" / "processed" / "pairwise_bt_v2_gpt.parquet"

FEATURES = ["commitment_strength", "hedging_level", "specificity", "audience_cost"]
DEFS = {
    "commitment_strength": "How firmly committed to action? Unconditional/direct=high; conditional/hedged=low.",
    "hedging_level": "How much hedging language (may, might, could, perhaps, possibly)? More hedging=higher.",
    "specificity": "How concrete are details (placeholders standing for specific numbers/dates/targets still count)?",
    "audience_cost": "How public/costly to back down from? Named ultimatums + public deadlines = higher.",
}

N_PAIRS = 200
SEED = 42

CLAUDE_MODEL = "claude-haiku-4-5-20251001"
GPT_MODEL = "gpt-4o-mini"


def sample_pairs(n_items, n_pairs, seed):
    rng = random.Random(seed)
    all_pairs = [(i, j) for i in range(n_items) for j in range(i + 1, n_items)]
    rng.shuffle(all_pairs)
    return all_pairs[:n_pairs]


def make_prompt(a, b):
    feat_text = "\n".join(f"- **{f}**: {DEFS[f]}" for f in FEATURES)
    schema = ", ".join(f'"{f}": <int 1-7>' for f in FEATURES)
    return f"""Compare two Trump-style political posts (anonymized: [COUNTRY] / [INDUSTRY] / [PERCENT] / [DATE] / [AMOUNT] are placeholders) on 4 linguistic dimensions.

For EACH dimension, rate on this 1-7 scale:
  1 = A definitely much higher
  2 = A clearly higher
  3 = A slightly higher
  4 = tie
  5 = B slightly higher
  6 = B clearly higher
  7 = B definitely much higher

Dimensions:
{feat_text}

POST A:
{a}

POST B:
{b}

Output ONLY this JSON, no other text:
{{{schema}}}"""


_JSON_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


def parse(text: str) -> dict | None:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1] if "```" in text[3:] else text[3:]
        text = text.lstrip("json").strip()
    try:
        return json.loads(text)
    except Exception:
        m = _JSON_RE.search(text)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


def call_claude(prompt):
    import anthropic
    client = anthropic.Anthropic()
    try:
        r = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return parse(r.content[0].text)
    except Exception as e:
        print(f"  claude err: {e}")
        return None


def call_gpt(prompt):
    from openai import OpenAI
    client = OpenAI()
    try:
        r = client.chat.completions.create(
            model=GPT_MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return parse(r.choices[0].message.content)
    except Exception as e:
        print(f"  gpt err: {e}")
        return None


def run_model(eps, pairs, call_fn, name):
    rows = []
    skipped = 0
    for idx, (i, j) in enumerate(pairs):
        a = eps.iloc[i]["first_text_anon"][:800]
        b = eps.iloc[j]["first_text_anon"][:800]
        prompt = make_prompt(a, b)
        result = call_fn(prompt)
        if result is None:
            skipped += 1
            continue
        for f in FEATURES:
            score = result.get(f, 4)
            try:
                score = int(score)
            except Exception:
                score = 4
            if score < 1 or score > 7:
                score = 4
            rows.append({
                "pair_idx": idx,
                "ep_a": eps.iloc[i]["episode_id"],
                "ep_b": eps.iloc[j]["episode_id"],
                "feature": f,
                "score": score,  # 1=A high, 7=B high, 4=tie
            })
        if (idx + 1) % 25 == 0:
            print(f"  [{name} {idx+1}/{len(pairs)}] skipped={skipped}", flush=True)
    return pd.DataFrame(rows), skipped


def main():
    eps = pd.read_parquet(EP_FP).reset_index(drop=True)
    print(f"[load] {len(eps)} anonymized episodes")
    pairs = sample_pairs(len(eps), N_PAIRS, SEED)
    items_seen = set()
    for i, j in pairs:
        items_seen.add(i); items_seen.add(j)
    print(f"[pairs] {len(pairs)}; coverage {len(items_seen)}/{len(eps)} eps")

    print("\n=== Running Claude ===")
    dc, sc = run_model(eps, pairs, call_claude, "claude")
    dc.to_parquet(OUT_C)
    print(f"[saved] {OUT_C}  rows={len(dc)}  skipped={sc}")
    print("Score distribution (Claude):")
    print(dc.groupby("feature")["score"].describe()[["mean", "std", "min", "max"]])

    print("\n=== Running GPT ===")
    dg, sg = run_model(eps, pairs, call_gpt, "gpt")
    dg.to_parquet(OUT_G)
    print(f"[saved] {OUT_G}  rows={len(dg)}  skipped={sg}")
    print("Score distribution (GPT):")
    print(dg.groupby("feature")["score"].describe()[["mean", "std", "min", "max"]])


if __name__ == "__main__":
    main()
