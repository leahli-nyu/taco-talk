"""Rule-based A/B/C labeler (fallback when LLM API unavailable).

This is a recall-first heuristic. Expected to be ~70-80% accurate vs LLM.
User QA can refine the prompt / re-run with LLM later.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN_FP = ROOT / "data" / "processed" / "econ_candidates.parquet"
OUT_FP = ROOT / "data" / "processed" / "labeled_abc.parquet"
SAMPLE_FP = ROOT / "data" / "processed" / "qa_sample_50.json"

# Commissive markers — first-person commitment by Trump
COMMISSIVE = re.compile(
    r"\b(?:i|we)\s+(?:will|am going to|going to|plan|intend|promise|am gonna|gonna)\b"
    r"|\b(?:i\s+)?will (?:be )?(?:impos|raise|cut|lift|remove|sign|deliv|stop)"
    r"|\bwill (?:impose|put|hit|slap|add|raise|charge|levy|institute)\b"
    r"|\bi\b.*\bsign(?:ing)?\b"
    r"|\bgoing to (?:impose|put|hit|raise|cut)\b"
    r"|\bwe (?:must|need to|have to|are going to)\b",
    re.I,
)

# Negative — clearly non-commissive
NON_COMMISSIVE = re.compile(
    r"\b(?:said|stated|reported|claimed|wrote|tweeted)\b"  # reporting
    r"|\b(?:terrible|horrible|disaster|stupid|dumb|crooked|rigged|fake)\b"  # complaint markers
    r"|^\".*\"$",  # pure quote
    re.I,
)

# Economic transmission keywords (already in econ_candidates filter, but split A/B more sharply)
A_CLASS_KEYWORDS = re.compile(
    r"\btariff|\bdut(?:y|ies)\b|\bimport (?:tax|tariff)|\bSection\s*(232|301)"
    r"|\btrade deal|\btrade war|\bbilateral trade|\bWTO"
    r"|\bsanction|\bembargo|\bSDN list|\bOFAC"
    r"|\bPowell|\binterest rate|\brate cut|\brate hike|\bFed(?:eral Reserve)?"
    r"|\b(?:ban|block|halt)\s+(?:imports|exports|trade)"
    r"|\bsemiconductor|\bchip\b|\bsteel|\baluminum|\bcoffee|\bsoybean",
    re.I,
)

# B class: non-economic policy threats
B_CLASS_KEYWORDS = re.compile(
    r"\bdeport|\bICE\b|\bborder|\billegal immigrant|\bmigrant"
    r"|\bmilitary|\bdeploy|\bstrike|\binvad|\bnuclear"
    r"|\bprosecut|\bindict|\binvestigate|\bjudge|\bcrook|\bspecial counsel",
    re.I,
)


def classify(text: str) -> dict:
    if not isinstance(text, str):
        text = ""
    is_commissive = bool(COMMISSIVE.search(text))
    is_non_commissive = bool(NON_COMMISSIVE.search(text)) and not is_commissive
    has_a_keyword = bool(A_CLASS_KEYWORDS.search(text))
    has_b_keyword = bool(B_CLASS_KEYWORDS.search(text))

    if not is_commissive:
        label = "C"
        confidence = 0.6 if is_non_commissive else 0.5
    elif has_a_keyword and not has_b_keyword:
        label = "A"; confidence = 0.75
    elif has_a_keyword and has_b_keyword:
        # mixed — default to A (econ dominant), low confidence
        label = "A"; confidence = 0.5
    elif has_b_keyword:
        label = "B"; confidence = 0.7
    else:
        label = "C"; confidence = 0.4

    # Crude target extraction
    target = None
    countries = re.search(r"\b(China|Mexico|Canada|Russia|Brazil|India|Japan|Germany|France|UK|Britain|EU|Europe|Iran|Venezuela|Cuba|Argentina|Australia|South Korea)\b", text, re.I)
    if countries:
        target = countries.group(0)
    return {"label": label, "target": target, "confidence": confidence,
            "is_commissive": int(is_commissive)}


def main():
    df = pd.read_parquet(IN_FP)
    print(f"[load] {len(df)} candidates")
    results = df["content"].apply(classify).apply(pd.Series)
    out = pd.concat([df.reset_index(drop=True), results.reset_index(drop=True)], axis=1)
    out["_id"] = out["id"].astype(str)
    out["_date"] = out["created_at"].astype(str)
    out["_text"] = out["content"].str[:500]
    # match LLM output schema
    out_cols = ["_id", "_date", "_text", "label", "target", "confidence",
                "is_commissive", "created_at", "content"]
    out_save = out[out_cols + [c for c in out.columns if c.startswith("has_")]]
    out_save.to_parquet(OUT_FP)
    print(f"[saved] {OUT_FP}")
    print("\nLabel counts:")
    print(out["label"].value_counts())
    print(f"\nMean confidence per label:")
    print(out.groupby("label")["confidence"].mean())

    # QA sample: stratified
    qa_pieces = []
    for lab in ["A", "B", "C"]:
        sub = out[out.label == lab]
        if len(sub) > 0:
            n = min(20 if lab == "A" else 15, len(sub))
            qa_pieces.append(sub.sample(n, random_state=7))
    qa = pd.concat(qa_pieces)
    qa_export = qa[["_id", "_date", "label", "target", "confidence", "_text"]].to_dict(orient="records")
    SAMPLE_FP.write_text(json.dumps(qa_export, indent=2, ensure_ascii=False))
    print(f"[saved] {SAMPLE_FP}  ({len(qa)} for human QA)")

if __name__ == "__main__":
    main()
