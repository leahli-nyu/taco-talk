"""Pull Federal Register entries related to tariffs / trade for ground truth.

Federal Register API is public, no auth needed.
Docs: https://www.federalregister.gov/developers/documentation/api/v1
"""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
import requests

BASE = "https://www.federalregister.gov/api/v1/documents.json"

# Search terms for tariff-relevant federal register entries
QUERIES = [
    "tariff",
    "Section 301",
    "Section 232",
    "trade with China",
    "import duty",
    "Reciprocal Trade",
    "USMCA",
    "import restriction",
]

def fetch_query(query: str, start: str, end: str) -> list[dict]:
    """Fetch all FR docs matching `query` between dates."""
    out, page = [], 1
    while True:
        params = {
            "conditions[term]": query,
            "conditions[publication_date][gte]": start,
            "conditions[publication_date][lte]": end,
            "conditions[type][]": ["PRESDOCU", "RULE", "PRORULE", "NOTICE"],
            "per_page": 100,
            "page": page,
            "fields[]": [
                "document_number", "title", "type", "abstract",
                "publication_date", "signing_date", "president",
                "html_url", "pdf_url", "agencies", "topics",
            ],
        }
        r = requests.get(BASE, params=params, timeout=30)
        r.raise_for_status()
        js = r.json()
        results = js.get("results", [])
        if not results:
            break
        out.extend(results)
        if len(out) >= js.get("count", 0) or page * 100 >= js.get("count", 0):
            break
        page += 1
        time.sleep(0.4)  # be polite
    return out

def main(start: str, end: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    seen = set()
    all_docs = []
    for q in QUERIES:
        print(f"[query] {q}")
        docs = fetch_query(q, start, end)
        for d in docs:
            if d["document_number"] in seen:
                continue
            seen.add(d["document_number"])
            d["_matched_query"] = q
            all_docs.append(d)
        print(f"  +{len(docs)} (total unique: {len(all_docs)})")
    fp = out_dir / "federal_register_tariff.json"
    fp.write_text(json.dumps(all_docs, indent=2))
    print(f"[saved] {fp}  total={len(all_docs)}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--start", default="2017-01-01")
    p.add_argument("--end", default="2026-05-10")
    p.add_argument("--out", default="data/raw")
    a = p.parse_args()
    main(a.start, a.end, Path(a.out))
