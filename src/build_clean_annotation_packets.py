"""Regenerate all 5 annotation packets WITHOUT showing LLM ratings / labels.
- Posts randomized (not sorted by LLM rating)
- No "LLM rating: X" headers
- No cosine similarity shown
- Packet B's collapsible LLM labels removed
- Packet E (new): cross-LLM disagree resolution
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANN = ROOT / "annotation"
corpus = json.load(open(ANN / "annotation_corpus.json"))
corp_idx = {str(c["id"]): c for c in corpus}

RNG = np.random.RandomState(42)

#============ PACKET A: SPECIFICITY (no LLM rating shown) ============
pa = pd.read_parquet(ROOT / "data/processed/annotation_packet_A_ids.parquet")
# RANDOMIZE order; hide LLM rating
shuffled = pa.sample(frac=1, random_state=42).reset_index(drop=True)

content = ["# Packet A · Specificity 0-10 Annotation",
           "",
           "> 给每条帖打一个 specificity 分数 (0-10)。锚定见 [RUBRIC.md](RUBRIC.md) 第 1 节。",
           "> **40 条**，随机顺序。",
           "> 在每条下方填 `Your rating: __`。可以加 notes 解释边界 case。",
           "",
           "---",
           ""]
seq = 0
for i, r in shuffled.iterrows():
    _id = str(r["_id"])
    if _id not in corp_idx: continue
    seq += 1
    c = corp_idx[_id]
    content.append(f"## Item {seq}")
    content.append("")
    content.append(f"**Date**: {c['date']}")
    content.append("")
    content.append("**EN**:")
    content.append(f"> {c['text_en']}")
    content.append("")
    content.append("**ZH**:")
    content.append(f"> {c['text_zh']}")
    content.append("")
    content.append("**Your specificity rating (0-10)**: __")
    content.append("")
    content.append("**Notes (optional)**: __")
    content.append("")
    content.append("---")
    content.append("")

(ANN / "packet_A_specificity.md").write_text("\n".join(content))
print(f"Packet A: {seq} items (randomized, no LLM rating shown)")


#============ PACKET B: BORDERLINE A/B/C (no LLM labels shown) ============
claude = pd.read_parquet(ROOT / "data/processed/labeled_v2_claude.parquet")[["_id","label","policy_area"]].rename(columns={"label":"c_label","policy_area":"c_policy"})
gpt = pd.read_parquet(ROOT / "data/processed/labeled_v2_gpt.parquet")[["_id","label","policy_area"]].rename(columns={"label":"g_label","policy_area":"g_policy"})
m = claude.merge(gpt, on="_id")

only_c = m[(m["c_label"]=="A") & (m["g_label"]!="A")].sample(15, random_state=42)
only_g = m[(m["c_label"]!="A") & (m["g_label"]=="A")].sample(15, random_state=42)
b_items = pd.concat([only_c, only_g], ignore_index=True).sample(frac=1, random_state=99).reset_index(drop=True)
b_items["_id"] = b_items["_id"].astype(str)

content = ["# Packet B · A/B/C 边界 case 验证",
           "",
           "> 独立判断 A/B/C。锚定见 [RUBRIC.md](RUBRIC.md) 第 2-3 节。",
           "> **30 条**，随机顺序。",
           "",
           "---",
           ""]
seq = 0
# Persist mapping so we can compare to LLM labels later
b_key = []
for i, r in b_items.iterrows():
    _id = r["_id"]
    if _id not in corp_idx: continue
    seq += 1
    c = corp_idx[_id]
    b_key.append({"item": seq, "_id": _id, "c_label": r["c_label"], "g_label": r["g_label"],
                  "c_policy": r.get("c_policy"), "g_policy": r.get("g_policy")})
    content.append(f"## Item {seq}")
    content.append("")
    content.append(f"**Date**: {c['date']}")
    content.append("")
    content.append("**EN**:")
    content.append(f"> {c['text_en'][:1500]}")
    content.append("")
    content.append("**ZH**:")
    content.append(f"> {c['text_zh'][:1500]}")
    content.append("")
    content.append("**Your call**:")
    content.append("- Is commissive? (Y/N): __")
    content.append("- A / B / C: __")
    content.append("- Reason (1 line): __")
    content.append("")
    content.append("---")
    content.append("")

(ANN / "packet_B_borderline_abc.md").write_text("\n".join(content))
# save key for parsing
pd.DataFrame(b_key).to_parquet(ROOT / "data/processed/annotation_packet_B_key.parquet")
print(f"Packet B: {seq} items (randomized, no LLM labels)")


#============ PACKET C: MATCH VALIDATION (already has no LLM source info — keep) ============
import json as _json
gt = _json.load(open(ROOT / "data/raw/tariff_timeline_ground_truth.json"))["events"]
eps_n = pd.read_parquet(ROOT / "data/processed/episodes_with_hc_outcomes_narrow.parquet")
matched = eps_n[eps_n["match_status"]=="consensus_match"].copy().reset_index(drop=True)
matched = matched.sample(frac=1, random_state=77).reset_index(drop=True)  # randomize

content = ["# Packet C · Cross-LLM Match 验证",
           "",
           "> 判断 27 个 episode-event match 是否正确。锚定见 [RUBRIC.md](RUBRIC.md) 第 4 节。",
           "> 随机顺序。",
           "",
           "---",
           ""]
c_key = []
for i, r in matched.iterrows():
    evt = gt[int(r["matched_evt_idx"])]
    c_key.append({"item": i+1, "episode_id": int(r["episode_id"]),
                  "matched_evt_idx": int(r["matched_evt_idx"]),
                  "matched_target": evt["target"],
                  "matched_status": evt["status"]})
    content.append(f"## Match {i+1}")
    content.append("")
    content.append(f"**Episode first-post text** (EN):")
    content.append(f"> {str(r['first_text'])[:500]}")
    content.append("")
    content.append(f"**First-post date**: {str(r['first_post_date'])[:10]}")
    content.append("")
    content.append(f"**Matched event**:")
    content.append(f"- Target: `{evt['target']}`")
    content.append(f"- Announced: {evt['announced']}")
    content.append(f"- Status: {evt['status']}")
    content.append(f"- Note: {evt.get('note','')}")
    content.append(f"- Anticipation days: {r['anticipation_days']} (first-post → event)")
    content.append("")
    content.append("**Your judgment** (✓ correct / ⚠ borderline / ✗ wrong topic): __")
    content.append("")
    content.append("**Comment**: __")
    content.append("")
    content.append("---")
    content.append("")

(ANN / "packet_C_match_validation.md").write_text("\n".join(content))
pd.DataFrame(c_key).to_parquet(ROOT / "data/processed/annotation_packet_C_key.parquet")
print(f"Packet C: {len(matched)} items (randomized)")


#============ PACKET D: CLUSTERING PAIRS (no cosine shown, random order) ============
emb = np.load(ROOT / "data/processed/consensus_a_bge_embeddings.npy")
af = pd.read_parquet(ROOT / "data/processed/all_features.parquet").sort_values("created_at").reset_index(drop=True)
sim = emb @ emb.T
n = len(af)

sim_bins = [(0.50, 0.65), (0.65, 0.78), (0.78, 0.82), (0.82, 0.88), (0.88, 0.95)]
np.random.seed(42)
pair_items = []
for lo, hi in sim_bins:
    candidates = []
    for i in range(n):
        for j in range(i+1, n):
            if lo <= sim[i,j] < hi:
                dt_diff = abs((af.iloc[i]["created_at"] - af.iloc[j]["created_at"]).days)
                if dt_diff <= 30:
                    candidates.append((i, j, float(sim[i,j])))
    if not candidates: continue
    chosen = np.random.choice(len(candidates), min(4, len(candidates)), replace=False)
    for idx in chosen:
        i, j, s = candidates[idx]
        pair_items.append((af.iloc[i], af.iloc[j], s))

# RANDOMIZE
pair_items_shuffled = list(pair_items)
RNG.shuffle(pair_items_shuffled)

content = ["# Packet D · Episode 聚类 pair 验证",
           "",
           "> 判断 20 对帖是不是同主题。锚定见 [RUBRIC.md](RUBRIC.md) 第 5 节。",
           "> 随机顺序。",
           "",
           "---",
           ""]
d_key = []
for k, (post_a, post_b, s) in enumerate(pair_items_shuffled):
    a_id, b_id = str(post_a["_id"]), str(post_b["_id"])
    a_corp = corp_idx.get(a_id)
    b_corp = corp_idx.get(b_id)
    a_en = a_corp["text_en"][:400] if a_corp else str(post_a["content"])[:400]
    a_zh = a_corp["text_zh"][:400] if a_corp else "(无翻译)"
    b_en = b_corp["text_en"][:400] if b_corp else str(post_b["content"])[:400]
    b_zh = b_corp["text_zh"][:400] if b_corp else "(无翻译)"
    d_key.append({"item": k+1, "a_id": a_id, "b_id": b_id, "cosine": s})

    content.append(f"## Pair {k+1}")
    content.append("")
    content.append(f"**Post A** ({str(post_a['created_at'])[:10]}):")
    content.append("")
    content.append(f"EN: > {a_en}")
    content.append("")
    content.append(f"ZH: > {a_zh}")
    content.append("")
    content.append(f"**Post B** ({str(post_b['created_at'])[:10]}):")
    content.append("")
    content.append(f"EN: > {b_en}")
    content.append("")
    content.append(f"ZH: > {b_zh}")
    content.append("")
    content.append("**Your judgment**: 同主题 / 相关 / 不同 → __")
    content.append("")
    content.append("**Notes**: __")
    content.append("")
    content.append("---")
    content.append("")

(ANN / "packet_D_clustering_pairs.md").write_text("\n".join(content))
pd.DataFrame(d_key).to_parquet(ROOT / "data/processed/annotation_packet_D_key.parquet")
print(f"Packet D: {len(pair_items_shuffled)} pairs (randomized, no cosine shown)")


#============ PACKET E: DISAGREE RESOLUTION ============
# Get the 24 disagree cases on tariff-adjacent narrow sample
c_matches = pd.read_parquet(ROOT / "data/processed/episode_matches_hc_claude.parquet")
g_matches = pd.read_parquet(ROOT / "data/processed/episode_matches_hc_gpt.parquet")
eps_narrow = pd.read_parquet(ROOT / "data/processed/episodes_v2_narrow.parquet")
narrow_ids = set(eps_narrow["episode_id"])

merged = c_matches.merge(g_matches, on="episode_id", suffixes=("_c","_g"))
disagree_mask = (merged["matched_evt_idx_c"].notna() ^ merged["matched_evt_idx_g"].notna()) | \
                ((merged["matched_evt_idx_c"].notna() & merged["matched_evt_idx_g"].notna()) &
                 (merged["matched_evt_idx_c"] != merged["matched_evt_idx_g"]))
disagree = merged[disagree_mask & merged["episode_id"].isin(narrow_ids)].copy()
print(f"Found {len(disagree)} disagree cases on narrow sample")

# Get episode full text + first-post date
eps_full = pd.read_parquet(ROOT / "data/processed/episodes_v2.parquet")[["episode_id","first_text","first_post_date","all_text"]]
disagree = disagree.merge(eps_full, on="episode_id")

# For each, find candidate events in [-10, +60d] window
gt = json.load(open(ROOT / "data/raw/tariff_timeline_ground_truth.json"))["events"]

def candidates_for(ep_date):
    out = []
    for idx, e in enumerate(gt):
        try:
            ed = pd.to_datetime(e["announced"]).date()
        except: continue
        diff = (ed - pd.to_datetime(ep_date).date()).days
        if -10 <= diff <= 60:
            out.append((idx, e, diff))
    return out

# Build packet — randomize order, don't tell user which LLM picked what
disagree_shuffled = disagree.sample(frac=1, random_state=42).reset_index(drop=True)

content = ["# Packet E · Cross-LLM 分歧的 Match 人工裁决",
           "",
           "> 24 个 episode：两个 LLM 在 match 哪个事件上分歧。",
           "> 你的任务：根据 episode 文本 + 候选事件列表，**选一个最匹配的 event**（或选 none）。",
           "> 这个标注**直接增加 paper 的 N**（每个你 resolve 的 case 可能变成新的 match）。",
           "> 锚定：跟 Packet C 一样判断 topic 是否对得上。",
           "",
           "**注意**：候选事件按日期排序。`Δd` 是 event 发生日距 episode 首帖的天数（正数=事件在帖之后）。",
           "",
           "---",
           ""]

e_key = []
for i, r in disagree_shuffled.iterrows():
    cands = candidates_for(r["first_post_date"])
    if not cands: continue
    e_key.append({
        "item": i+1, "episode_id": int(r["episode_id"]),
        "c_pick": r.get("matched_evt_idx_c"),
        "g_pick": r.get("matched_evt_idx_g"),
        "candidate_idxs": [c[0] for c in cands],
    })

    content.append(f"## Case {i+1} · Episode {r['episode_id']}")
    content.append("")
    content.append(f"**Episode first-post date**: {str(r['first_post_date'])[:10]}")
    content.append("")
    content.append("**Episode first-post text** (EN):")
    content.append(f"> {str(r['first_text'])[:1000]}")
    content.append("")
    if r.get("all_text") and len(str(r["all_text"])) > len(str(r["first_text"])):
        content.append("**Full episode all-text** (EN, truncated):")
        content.append(f"> {str(r['all_text'])[:1500]}")
        content.append("")

    content.append("**Candidate events in [-10d, +60d] window:**")
    content.append("")
    for cand_idx, evt, diff in cands:
        content.append(f"- **[{cand_idx}]** `{evt['announced']}` Δ{diff:+d}d | target: `{evt['target']}` | status: `{evt['status']}` | note: {evt.get('note','')[:120]}")
    content.append("")
    content.append("**Your pick**: 写 candidate 编号 [N]，或写 `none` 表示没一个匹配 → __")
    content.append("")
    content.append("**Notes (if borderline)**: __")
    content.append("")
    content.append("---")
    content.append("")

(ANN / "packet_E_disagree_resolution.md").write_text("\n".join(content))
pd.DataFrame(e_key).to_parquet(ROOT / "data/processed/annotation_packet_E_key.parquet")
print(f"Packet E: {len(e_key)} disagree cases")

print("\n[done] all 5 packets regenerated")
EOF
