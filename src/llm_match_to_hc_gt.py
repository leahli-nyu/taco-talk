"""LLM-based matching: each episode → hand-compiled GT event (or none).

Pipeline:
1. For each of 110 episodes, find candidate events in [-10, +60d] window.
2. Send episode first_text + candidate list to Claude AND GPT separately.
3. Each model returns: event_idx (0..N) or "none".
4. Consensus matching: keep only matches where BOTH models agree on same event_idx.
5. If models disagree → record as ambiguous (not used in main analysis, in robustness).

Output:
  data/processed/episode_matches_hc_claude.parquet
  data/processed/episode_matches_hc_gpt.parquet
  data/processed/episodes_with_hc_outcomes.parquet (consensus)
"""
from __future__ import annotations
import json
import os
import re
from pathlib import Path
from datetime import timedelta
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Load .env
ENV_FP = ROOT / ".env"
if ENV_FP.exists():
    for line in ENV_FP.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")

GT_FP = ROOT / "data" / "raw" / "tariff_timeline_ground_truth.json"
EP_FP = ROOT / "data" / "processed" / "episodes_v2.parquet"
OUT_CLAUDE = ROOT / "data" / "processed" / "episode_matches_hc_claude.parquet"
OUT_GPT = ROOT / "data" / "processed" / "episode_matches_hc_gpt.parquet"
OUT_CONS = ROOT / "data" / "processed" / "episodes_with_hc_outcomes.parquet"

WINDOW_BACK = 10
WINDOW_FORWARD = 60

CLAUDE_MODEL = "claude-haiku-4-5-20251001"
GPT_MODEL = "gpt-4o-mini"


def load_gt():
    gt = json.load(open(GT_FP))
    events = []
    for i, e in enumerate(gt["events"]):
        events.append({
            "evt_idx": i,
            "announced": e.get("announced"),
            "effective": e.get("effective"),
            "target": e.get("target"),
            "status": e.get("status"),
            "rate_pct": e.get("rate_pct"),
            "authority": e.get("authority"),
            "note": e.get("note", ""),
        })
    df = pd.DataFrame(events)
    df["announced_date"] = pd.to_datetime(df["announced"], errors="coerce").dt.date
    return df


def candidates_for_episode(ep_date, gt):
    """Return list of (evt_idx, announced_date, target, status, note) candidates in window."""
    ep_date = pd.to_datetime(ep_date).date()
    out = []
    for _, e in gt.iterrows():
        if e["announced_date"] is None:
            continue
        signed = (e["announced_date"] - ep_date).days
        if -WINDOW_BACK <= signed <= WINDOW_FORWARD:
            out.append({
                "evt_idx": int(e["evt_idx"]),
                "date": str(e["announced_date"]),
                "target": e["target"],
                "status": e["status"],
                "note": e["note"][:160] if isinstance(e["note"], str) else "",
                "signed_days": signed,
            })
    return out


def build_prompt(ep_text: str, candidates: list[dict]) -> str:
    if not candidates:
        return None
    lines = []
    for c in candidates:
        lines.append(
            f"  [{c['evt_idx']}] {c['date']} (Δ{c['signed_days']:+d}d) | target={c['target']} | "
            f"status={c['status']} | {c['note']}"
        )
    cand_block = "\n".join(lines)
    return f"""You are matching a Trump tariff/economic threat post to its actual policy event.

POST (truncated):
\"\"\"
{ep_text[:1200]}
\"\"\"

CANDIDATE policy events (within -10 to +60 days of this post):
{cand_block}

Pick the ONE event most clearly referenced by the post, considering:
- target match (post mentions the country/commodity)
- temporal plausibility (event happens after the threat, ideally <30 days)
- topical match (the post is about THIS policy area, not just same country)

If NO candidate is a clear match, return "none".

Output STRICTLY a JSON object with no other text:
{{"matched_evt_idx": <int or "none">, "confidence": <"high"|"medium"|"low">}}"""


_JSON_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


def parse_response(text: str) -> dict | None:
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


def call_claude(prompt: str) -> dict | None:
    import anthropic
    client = anthropic.Anthropic()
    try:
        resp = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return parse_response(resp.content[0].text)
    except Exception as e:
        print(f"  claude err: {type(e).__name__}: {e}")
        return None


def call_gpt(prompt: str) -> dict | None:
    from openai import OpenAI
    client = OpenAI()
    try:
        resp = client.chat.completions.create(
            model=GPT_MODEL,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return parse_response(resp.choices[0].message.content)
    except Exception as e:
        print(f"  gpt err: {type(e).__name__}: {e}")
        return None


def run_one_model(eps, gt, call_fn, model_name):
    rows = []
    for i, ep in eps.iterrows():
        cands = candidates_for_episode(ep["first_post_date"], gt)
        if not cands:
            rows.append({
                "episode_id": ep["episode_id"],
                "n_candidates": 0,
                "matched_evt_idx": None,
                "confidence": "no_candidates",
            })
            continue
        prompt = build_prompt(ep["first_text"] or "", cands)
        result = call_fn(prompt)
        if result is None:
            rows.append({
                "episode_id": ep["episode_id"],
                "n_candidates": len(cands),
                "matched_evt_idx": None,
                "confidence": "call_failed",
            })
            continue
        idx = result.get("matched_evt_idx")
        # normalize - GPT may return as string
        if idx in (None, "none", "None", ""):
            idx = None
        else:
            try:
                idx = int(idx)
            except Exception:
                idx = None
        rows.append({
            "episode_id": ep["episode_id"],
            "n_candidates": len(cands),
            "matched_evt_idx": idx,
            "confidence": result.get("confidence", "unknown"),
        })
        if (i + 1) % 20 == 0:
            n_matched = sum(1 for r in rows if r["matched_evt_idx"] is not None)
            print(f"  [{model_name} {i+1}/{len(eps)}] matched={n_matched}", flush=True)
    return pd.DataFrame(rows)


def main():
    gt = load_gt()
    eps = pd.read_parquet(EP_FP)
    print(f"[load] {len(eps)} episodes × {len(gt)} hand-compiled events")
    # candidate-pool diagnostics
    cand_counts = [len(candidates_for_episode(e["first_post_date"], gt)) for _, e in eps.iterrows()]
    print(f"[diagnostics] candidate counts: mean={sum(cand_counts)/len(cand_counts):.1f}, "
          f"max={max(cand_counts)}, episodes with 0 candidates={sum(1 for c in cand_counts if c==0)}")

    print("\n=== Running Claude ===")
    df_c = run_one_model(eps, gt, call_claude, "claude")
    df_c.to_parquet(OUT_CLAUDE)
    print(f"[saved] {OUT_CLAUDE}")
    print(f"  Claude matched: {df_c['matched_evt_idx'].notna().sum()}/{len(df_c)}")

    print("\n=== Running GPT ===")
    df_g = run_one_model(eps, gt, call_gpt, "gpt")
    df_g.to_parquet(OUT_GPT)
    print(f"[saved] {OUT_GPT}")
    print(f"  GPT matched: {df_g['matched_evt_idx'].notna().sum()}/{len(df_g)}")

    # Consensus: both pick same event (or both pick none)
    merged = df_c.merge(df_g, on="episode_id", suffixes=("_c", "_g"))
    merged["consensus"] = merged.apply(
        lambda r: r["matched_evt_idx_c"] if r["matched_evt_idx_c"] == r["matched_evt_idx_g"] else None,
        axis=1,
    )
    agree_total = (merged["matched_evt_idx_c"] == merged["matched_evt_idx_g"]).sum()
    both_matched_same = ((merged["matched_evt_idx_c"].notna()) &
                         (merged["matched_evt_idx_c"] == merged["matched_evt_idx_g"])).sum()
    both_none = ((merged["matched_evt_idx_c"].isna()) &
                 (merged["matched_evt_idx_g"].isna())).sum()
    print(f"\n=== Cross-LLM consensus ===")
    print(f"  Both agree (matched OR none): {agree_total}/{len(merged)}")
    print(f"    └─ both matched same event: {both_matched_same}")
    print(f"    └─ both none:               {both_none}")
    print(f"    └─ disagree:                {len(merged) - agree_total}")

    # Build final episode-level outcome
    ep_status_bucket = {
        "in_effect": "executed",
        "modified": "modified_or_withdrawn",
        "withdrawn": "modified_or_withdrawn",
        "paused": "modified_or_withdrawn",
        "struck_down": "struck_down",
        "investigation": "investigation",
    }

    final = eps.copy()
    final["match_status"] = "unmatched"  # default
    final["matched_evt_idx"] = None
    final["y1_outcome"] = "no_policy_event_found"
    final["matched_target"] = None
    final["matched_announced_date"] = None
    final["matched_status_raw"] = None
    final["anticipation_days"] = None
    final["match_confidence"] = "no_candidates"
    final["match_consensus"] = "no"

    for _, r in merged.iterrows():
        ep_id = r["episode_id"]
        c_idx = r["matched_evt_idx_c"]
        g_idx = r["matched_evt_idx_g"]
        # find episode row
        mask = final["episode_id"] == ep_id
        if not mask.any():
            continue
        ep_row = final[mask].iloc[0]
        if pd.isna(c_idx) and pd.isna(g_idx):
            final.loc[mask, "match_status"] = "both_none"
            final.loc[mask, "match_consensus"] = "yes"
            continue
        if c_idx == g_idx and not pd.isna(c_idx):
            # consensus match
            evt = gt.iloc[int(c_idx)]
            final.loc[mask, "match_status"] = "consensus_match"
            final.loc[mask, "match_consensus"] = "yes"
            final.loc[mask, "matched_evt_idx"] = int(c_idx)
            final.loc[mask, "y1_outcome"] = ep_status_bucket.get(evt["status"], "other")
            final.loc[mask, "matched_target"] = evt["target"]
            final.loc[mask, "matched_announced_date"] = str(evt["announced_date"])
            final.loc[mask, "matched_status_raw"] = evt["status"]
            ep_d = pd.to_datetime(ep_row["first_post_date"]).date()
            ant = (evt["announced_date"] - ep_d).days if evt["announced_date"] else None
            final.loc[mask, "anticipation_days"] = ant
            final.loc[mask, "match_confidence"] = "consensus"
        else:
            # disagree
            final.loc[mask, "match_status"] = "disagree"
            final.loc[mask, "match_consensus"] = "no"

    final.to_parquet(OUT_CONS)
    print(f"\n[saved] {OUT_CONS}")
    print(f"\nConsensus match outcome distribution:")
    print(final["y1_outcome"].value_counts())
    print(f"\nMatch status distribution:")
    print(final["match_status"].value_counts())
    matched_only = final[final["match_status"] == "consensus_match"]
    if len(matched_only):
        print(f"\nAnticipation days (consensus matched, N={len(matched_only)}):")
        print(matched_only["anticipation_days"].describe())


if __name__ == "__main__":
    main()
