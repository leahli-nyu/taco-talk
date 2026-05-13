"""Translate A-class posts to Chinese for bilingual annotation.

Uses Claude Sonnet 4.6 for higher-quality translation that preserves Trump's
rhetorical flourishes (all-caps, hyperbole, etc.).
"""
from __future__ import annotations
import json
import os
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

# Use current rule-based + LLM-round-1 labeled A class while v2 classification runs
IN_FP = ROOT / "data" / "processed" / "labeled_abc.parquet"
OUT_FP = ROOT / "data" / "processed" / "annotation_corpus.json"


PROMPT_TEMPLATE = """请把下面这条 Trump 的 Truth Social 帖子翻译成中文，要求：

1. 保留 Trump 的口吻：夸张、自信、情绪化
2. 全大写词（如 MASSIVE、TREMENDOUS）翻译成中文时保留**加粗强调**或用"【】"标记
3. 感叹号保留
4. 政策专有名词（tariff/Section 232 等）可在中文译名后括号原文
5. 不要过度文雅化 — 保持口语化和煽动性
6. 不要意译加注解，直接翻译

只输出中文翻译，不要任何前后缀。

原文：
\"\"\"
{POST}
\"\"\""""


def translate(client, text: str) -> str:
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": PROMPT_TEMPLATE.replace("{POST}", text[:2000])}],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        return f"[翻译失败: {str(e)[:80]}]"


def main():
    df = pd.read_parquet(IN_FP)
    # The labeled parquet might not have full 'content' — join from candidates if needed
    if "content" not in df.columns:
        cand = pd.read_parquet(ROOT / "data" / "processed" / "econ_candidates.parquet")[
            ["id", "content"]
        ].rename(columns={"id": "_id"})
        df["_id"] = df["_id"].astype(str)
        cand["_id"] = cand["_id"].astype(str)
        df = df.merge(cand, on="_id", how="left")
    a_class = df[df["label"] == "A"].copy().reset_index(drop=True)
    print(f"[load] {len(a_class)} A-class posts to translate")

    client = Anthropic()

    # Use threads for parallelism (5 concurrent)
    translations = [None] * len(a_class)

    def task(i, text):
        return i, translate(client, text)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(task, i, str(r["content"])): i for i, r in a_class.iterrows()}
        completed = 0
        for f in as_completed(futures):
            i, zh = f.result()
            translations[i] = zh
            completed += 1
            if completed % 10 == 0 or completed == len(a_class):
                elapsed = time.time() - t0
                rate = completed / elapsed if elapsed > 0 else 0
                eta = (len(a_class) - completed) / rate if rate > 0 else 0
                print(f"  [{completed}/{len(a_class)}] rate={rate:.1f}/s eta={eta:.0f}s", flush=True)

    # Build annotation corpus
    records = []
    for i, r in a_class.iterrows():
        # Try common date column names
        date_val = None
        for col in ("created_at", "_date", "date"):
            if col in r.index and pd.notna(r[col]):
                date_val = str(r[col])
                break
        records.append({
            "id": str(r["_id"]) if "_id" in r.index else str(r.name),
            "date": (date_val or "")[:16],
            "text_en": str(r["content"]),
            "text_zh": translations[i],
            "llm_label": str(r["label"]),
            "llm_target": str(r.get("target") or ""),
        })

    OUT_FP.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    print(f"\n[saved] {OUT_FP}  ({len(records)} records)")
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
