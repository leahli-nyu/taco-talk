"""Translate missing posts (those not yet in annotation_corpus.json) to Chinese.

Targets:
- Posts sampled for packet A (specificity) that aren't in the corpus yet
- Posts to be used in packet B (A/B/C borderline)
- Posts in packet C (consensus matches)
- Posts in packet D (clustering pairs)
"""
from __future__ import annotations
import os, json, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ENV_FP = ROOT / ".env"
if ENV_FP.exists():
    for line in ENV_FP.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")

CORPUS_FP = ROOT / "annotation" / "annotation_corpus.json"
POSTS_FP = ROOT / "data" / "processed" / "all_features.parquet"

PROMPT = """Translate the following Trump Truth Social post into Chinese.

REQUIREMENTS:
- Preserve all emphasis (capitals -> Chinese bold marker **like this**, exclamation marks).
- Keep proper nouns in English where helpful (e.g. "tariff" -> "关税(Tariff)" on first mention; just "关税" after).
- Render Trump's style: bombastic, blunt, repetitive.
- Use 【square brackets】 for emphasis preserving emphatic adverbs/adjectives.
- Do NOT add commentary or explanation.

POST:
\"\"\"
{POST}
\"\"\"

Output ONLY the Chinese translation, no other text:"""


def main():
    corpus = json.load(open(CORPUS_FP))
    have_ids = {str(c["id"]) for c in corpus}

    af = pd.read_parquet(POSTS_FP)
    af["_id_str"] = af["_id"].astype(str)

    # Collect ALL needed IDs across packets
    needed_ids = set()

    # Packet A: stratified specificity sample (40 items)
    pa = pd.read_parquet(ROOT / "data" / "processed" / "annotation_packet_A_ids.parquet")
    needed_ids.update(pa["_id"].astype(str))

    # Packet B: borderline A/B/C (Claude-only A or GPT-only A)
    claude = pd.read_parquet(ROOT / "data" / "processed" / "labeled_v2_claude.parquet")[["_id","label"]].rename(columns={"label":"c_label"})
    gpt = pd.read_parquet(ROOT / "data" / "processed" / "labeled_v2_gpt.parquet")[["_id","label"]].rename(columns={"label":"g_label"})
    m = claude.merge(gpt, on="_id")
    only_c = m[(m["c_label"]=="A") & (m["g_label"]!="A")].head(15)
    only_g = m[(m["c_label"]!="A") & (m["g_label"]=="A")].head(15)
    needed_ids.update(only_c["_id"].astype(str))
    needed_ids.update(only_g["_id"].astype(str))

    # Packet C: consensus matched episodes' first_text - already have via narrow
    eps_n = pd.read_parquet(ROOT / "data" / "processed" / "episodes_with_hc_outcomes_narrow.parquet")
    matched = eps_n[eps_n["match_status"]=="consensus_match"]
    # first_post_id should be in af
    if "first_post_id" in matched.columns:
        needed_ids.update(matched["first_post_id"].astype(str))

    # Now figure out which need translation
    missing = [i for i in needed_ids if i not in have_ids]
    print(f"Total needed: {len(needed_ids)}; already in corpus: {len(needed_ids & have_ids)}; need translation: {len(missing)}")

    if not missing:
        print("[ok] All translated, nothing to do.")
        return

    # Translate each
    import anthropic
    client = anthropic.Anthropic()
    new_items = []
    for i, _id in enumerate(missing):
        rows = af[af["_id_str"]==_id]
        if rows.empty:
            print(f"[skip] _id {_id} not in posts")
            continue
        row = rows.iloc[0]
        text_en = str(row.get("content",""))[:3000]
        prompt = PROMPT.replace("{POST}", text_en)
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2000,
                messages=[{"role":"user","content":prompt}],
            )
            text_zh = resp.content[0].text.strip()
        except Exception as e:
            print(f"  err on {_id}: {e}")
            text_zh = "[翻译失败]"

        date = str(row.get("created_at",""))[:16]
        new_items.append({
            "id": _id,
            "date": date,
            "text_en": text_en,
            "text_zh": text_zh,
            "llm_label": row.get("claude_label","?"),
            "llm_target": row.get("claude_target","?"),
        })
        if (i+1) % 10 == 0:
            print(f"  [{i+1}/{len(missing)}]", flush=True)

    # Append to corpus
    corpus.extend(new_items)
    CORPUS_FP.write_text(json.dumps(corpus, indent=2, ensure_ascii=False))
    print(f"\n[saved] {CORPUS_FP}  total items: {len(corpus)}")


if __name__ == "__main__":
    main()
