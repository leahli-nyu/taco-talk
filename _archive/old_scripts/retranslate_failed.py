"""Retry failed translations from annotation_corpus.json.

Lower concurrency (3 threads) + exponential backoff.
"""
from __future__ import annotations
import json
import os
import time
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

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

CORPUS_FP = ROOT / "data" / "processed" / "annotation_corpus.json"

PROMPT = """请把下面这条 Trump 的 Truth Social 帖子翻译成中文，要求：

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


def translate_with_retry(client, text: str, max_retries: int = 4) -> str:
    for attempt in range(max_retries):
        try:
            msg = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2000,
                messages=[{"role": "user", "content": PROMPT.replace("{POST}", text[:2000])}],
            )
            return msg.content[0].text.strip()
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate_limit" in err_str.lower():
                wait = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait)
                continue
            return f"[翻译失败: {err_str[:80]}]"
    return f"[翻译失败: 重试 {max_retries} 次仍 rate limited]"


def main():
    data = json.loads(CORPUS_FP.read_text())
    failed_idx = [i for i, r in enumerate(data) if r["text_zh"].startswith("[翻译失败")]
    print(f"[load] {len(data)} total, {len(failed_idx)} failed — retrying these")

    if not failed_idx:
        print("All good!")
        return

    client = Anthropic()

    def task(i):
        return i, translate_with_retry(client, data[i]["text_en"])

    t0 = time.time()
    # Lower concurrency (3 threads, was 8 originally)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(task, i): i for i in failed_idx}
        completed = 0
        for f in as_completed(futures):
            i, zh = f.result()
            data[i]["text_zh"] = zh
            completed += 1
            if completed % 5 == 0 or completed == len(failed_idx):
                elapsed = time.time() - t0
                rate = completed / elapsed if elapsed > 0 else 0
                eta = (len(failed_idx) - completed) / rate if rate > 0 else 0
                print(f"  [{completed}/{len(failed_idx)}] rate={rate:.1f}/s eta={eta:.0f}s", flush=True)

    CORPUS_FP.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    still_failed = [r for r in data if r["text_zh"].startswith("[翻译失败")]
    print(f"\n[saved] {CORPUS_FP}")
    print(f"Still failed: {len(still_failed)} / {len(data)}")
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
