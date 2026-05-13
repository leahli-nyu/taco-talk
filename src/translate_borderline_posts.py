"""Translate borderline A/B/C posts (where Claude and GPT disagree).
These aren't in consensus A class, so weren't in all_features.parquet."""
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

PROMPT = """Translate the following Trump Truth Social post into Chinese.
- Preserve emphasis (capitals -> **bold**)
- Keep policy/legal terms in English on first mention
- Use 【】 for emphatic markers
- No commentary

POST:
\"\"\"
{POST}
\"\"\"

Output ONLY Chinese:"""


def main():
    corpus = json.load(open(CORPUS_FP))
    have_ids = {str(c["id"]) for c in corpus}

    claude = pd.read_parquet(ROOT / "data" / "processed" / "labeled_v2_claude.parquet")
    gpt = pd.read_parquet(ROOT / "data" / "processed" / "labeled_v2_gpt.parquet")[["_id","label","policy_area","reason"]].rename(columns={"label":"g_label","policy_area":"g_policy","reason":"g_reason"})

    c = claude[["_id","label","policy_area","reason","_text","_date"]].rename(columns={"label":"c_label","policy_area":"c_policy","reason":"c_reason"})
    m = c.merge(gpt, on="_id")

    # 15 Claude-only A, 15 GPT-only A
    only_c = m[(m["c_label"]=="A") & (m["g_label"]!="A")].sample(15, random_state=42)
    only_g = m[(m["c_label"]!="A") & (m["g_label"]=="A")].sample(15, random_state=42)
    target = pd.concat([only_c, only_g], ignore_index=True)
    target["_id"] = target["_id"].astype(str)

    missing = target[~target["_id"].isin(have_ids)]
    print(f"Borderline: total {len(target)}, need translation: {len(missing)}")

    if not len(missing):
        return

    import anthropic
    client = anthropic.Anthropic()
    new_items = []
    for i, r in missing.iterrows():
        text_en = str(r["_text"])[:3000]
        prompt = PROMPT.replace("{POST}", text_en)
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2000,
                messages=[{"role":"user","content":prompt}],
            )
            text_zh = resp.content[0].text.strip()
        except Exception as e:
            print(f"  err on {r['_id']}: {e}")
            text_zh = "[翻译失败]"

        new_items.append({
            "id": r["_id"],
            "date": str(r["_date"])[:16],
            "text_en": text_en,
            "text_zh": text_zh,
            "llm_label": f"C:{r['c_label']}/G:{r['g_label']}",
            "llm_target": "?",
        })
        if (len(new_items)) % 10 == 0:
            print(f"  [{len(new_items)}/{len(missing)}]", flush=True)

    corpus.extend(new_items)
    CORPUS_FP.write_text(json.dumps(corpus, indent=2, ensure_ascii=False))
    print(f"\n[saved] total corpus items: {len(corpus)}")


if __name__ == "__main__":
    main()
