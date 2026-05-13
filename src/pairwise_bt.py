"""Pairwise Bradley-Terry comparison for 4 features on 110 episode first-posts.

Forces LLM to make a *relative* judgment ("which is more X") instead of an absolute
0-10 score. This breaks the saturation problem where Trump's posts all score 7-9 on
commitment_strength etc.

Output: data/processed/pairwise_bt_raw.parquet (pair-level winners) and
        data/processed/episodes_bt_scores.parquet (BT score per episode per feature)
"""
from __future__ import annotations
import json
import os
import random
import time
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EP_FP = ROOT / "data" / "processed" / "episodes_v2.parquet"
OUT_PAIRS = ROOT / "data" / "processed" / "pairwise_bt_raw.parquet"
OUT_SCORES = ROOT / "data" / "processed" / "episodes_bt_scores.parquet"
LOG = ROOT / "data" / "processed" / "pairwise_bt.log"

# Features to compare (the 4 saturated ones)
FEATURES_TO_COMPARE = [
    "commitment_strength",
    "hedging_level",
    "specificity",
    "audience_cost",
]

FEATURE_DEFS = {
    "commitment_strength": "How firmly is the speaker committing to take action? Higher = unconditional, direct, no escape hatch. Lower = conditional, hypothetical, hedged.",
    "hedging_level": "How much hedging language (may, might, could, perhaps, possibly, etc.) does it contain? Higher = more hedging.",
    "specificity": "How concrete are the details (specific numbers, dates, named targets, named policies)? Higher = more specific.",
    "audience_cost": "How public/costly to back down from is this statement? Higher = harder to walk back without reputational loss (named ultimatum, public deadline, named adversary).",
}

N_PAIRS = 200
RANDOM_SEED = 42

# Load .env for ANTHROPIC_API_KEY (force-set, matching other scripts)
ENV_FP = ROOT / ".env"
if ENV_FP.exists():
    for line in ENV_FP.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")

MODEL = "claude-haiku-4-5-20251001"


def sample_pairs(n_items: int, n_pairs: int, seed: int = RANDOM_SEED) -> list[tuple[int, int]]:
    """Sample n_pairs (i, j) with i<j ensuring decent coverage of items."""
    rng = random.Random(seed)
    all_pairs = [(i, j) for i in range(n_items) for j in range(i + 1, n_items)]
    rng.shuffle(all_pairs)
    return all_pairs[:n_pairs]


def build_prompt(text_a: str, text_b: str) -> str:
    feat_text = "\n".join(f"- **{f}**: {FEATURE_DEFS[f]}" for f in FEATURES_TO_COMPARE)
    schema = ", ".join(f'"{f}": "A"|"B"|"tie"' for f in FEATURES_TO_COMPARE)
    return f"""Compare two Trump social-media posts on 4 dimensions. For EACH dimension, pick which post (A or B) ranks higher, or "tie".

Dimensions:
{feat_text}

POST A:
{text_a}

POST B:
{text_b}

Output ONLY this JSON, nothing else, no markdown fences, no reasoning:
{{{schema}}}"""


import re as _re
_JSON_RE = _re.compile(r"\{[^{}]*\}", _re.DOTALL)


def call_claude(prompt: str) -> dict | None:
    """One Claude Haiku call, returns parsed dict or None on failure."""
    import anthropic
    client = anthropic.Anthropic()
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text.strip()
        # strip code fences if present
        if text.startswith("```"):
            text = text.split("```")[1] if "```" in text[3:] else text[3:]
            text = text.lstrip("json").strip()
        # try direct parse
        try:
            return json.loads(text)
        except Exception:
            pass
        # fallback: regex first JSON object
        m = _JSON_RE.search(text)
        if m:
            return json.loads(m.group(0))
        return None
    except Exception as e:
        print(f"  call failed: {type(e).__name__}: {e}")
        return None


def main():
    eps = pd.read_parquet(EP_FP)[["episode_id", "first_text"]].reset_index(drop=True)
    eps = eps.dropna(subset=["first_text"]).reset_index(drop=True)
    # Truncate long posts to keep cost down
    eps["text_short"] = eps["first_text"].str.slice(0, 800)
    n_items = len(eps)
    print(f"[load] {n_items} episodes for pairwise BT")

    pairs = sample_pairs(n_items, N_PAIRS)
    print(f"[sampled] {len(pairs)} pairs")

    # Coverage check
    items_seen = set()
    for a, b in pairs:
        items_seen.add(a)
        items_seen.add(b)
    print(f"[coverage] {len(items_seen)}/{n_items} episodes appear in at least one pair")

    rows = []
    skipped = 0
    log_lines = []
    for idx, (i, j) in enumerate(pairs):
        ep_a = eps.iloc[i]
        ep_b = eps.iloc[j]
        prompt = build_prompt(ep_a["text_short"], ep_b["text_short"])
        result = call_claude(prompt)
        if result is None:
            skipped += 1
            continue
        for f in FEATURES_TO_COMPARE:
            verdict = result.get(f, "tie")
            if verdict not in ("A", "B", "tie"):
                verdict = "tie"
            rows.append({
                "pair_idx": idx,
                "ep_a": ep_a["episode_id"],
                "ep_b": ep_b["episode_id"],
                "feature": f,
                "winner": verdict,  # "A", "B", or "tie"
            })
        if (idx + 1) % 25 == 0:
            print(f"  [{idx + 1}/{len(pairs)}] skipped={skipped}", flush=True)
            log_lines.append(f"{idx+1}/{len(pairs)} ok, skipped={skipped}")

    df = pd.DataFrame(rows)
    df.to_parquet(OUT_PAIRS)
    LOG.write_text("\n".join(log_lines))
    print(f"\n[saved] {OUT_PAIRS}  rows={len(df)}  skipped_calls={skipped}")
    print(f"\nWinner distribution per feature:")
    print(df.groupby("feature")["winner"].value_counts())


if __name__ == "__main__":
    main()
