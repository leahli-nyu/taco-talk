"""Build v3 web app data from V5 narrow + V6 anon BT pipeline.

Updates:
- Summary uses V5 narrow tariff-adjacent (77 episodes / 27 matched / 16 events)
- Adds key_results block with V5 + V6 Cox HRs
- Adds method_metadata block describing pipeline versions
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
POSTS_FP = ROOT / "data" / "processed" / "all_features.parquet"
EPS_NARROW_FP = ROOT / "data" / "processed" / "episodes_with_hc_outcomes_narrow.parquet"
ES_FP = ROOT / "data" / "processed" / "event_study_v2.parquet"
FR_FP = ROOT / "data" / "raw" / "federal_register_tariff_eos.json"
GT_FP = ROOT / "data" / "raw" / "tariff_timeline_ground_truth.json"
COX_V5_FP = ROOT / "data" / "processed" / "cox_v5_narrow_summary.parquet"
COX_V6_FP = ROOT / "data" / "processed" / "cox_v6_anon_bt_summary.parquet"
EIV_FP = ROOT / "data" / "processed" / "cox_eiv_sensitivity.parquet"
LOOSE_FP = ROOT / "data" / "processed" / "loose_match_summary.parquet"
BT_V2_FP = ROOT / "data" / "processed" / "episodes_bt_v2_scores.parquet"

OUT_JSON = ROOT / "app" / "data.json"
OUT_JS = ROOT / "app" / "data.js"
OUT_BACKUP = ROOT / "app" / "data_v2_backup.json"


def clean(v):
    try:
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        if pd.isna(v):
            return None
    except Exception:
        pass
    return v


def main():
    # Back up current
    if OUT_JSON.exists() and not OUT_BACKUP.exists():
        OUT_BACKUP.write_text(OUT_JSON.read_text())
        print(f"[backup] {OUT_BACKUP}")

    posts = pd.read_parquet(POSTS_FP)
    eps_n = pd.read_parquet(EPS_NARROW_FP)
    es = pd.read_parquet(ES_FP)
    gt = json.loads(GT_FP.read_text())["events"]

    posts["_id"] = posts["_id"].astype(str)
    es["_id"] = es["_id"].astype(str)

    # Restrict to tariff-adjacent A class
    posts_narrow = posts[posts["claude_policy"].isin(["tariff", "trade_agreement", "commodity_intervention"])].copy()
    print(f"[posts narrow]: {len(posts_narrow)} / 141")

    # Join with V5 narrow episodes
    merged = posts_narrow.merge(
        eps_n[["episode_id", "y1_outcome", "anticipation_days", "matched_target", "matched_status_raw"]],
        on="episode_id", how="left",
    )
    merged = merged.merge(
        es[["_id", "car_1d", "car_5d", "car_30d", "peak_drawdown_30d", "max_recovery_30d"]],
        on="_id", how="left",
    )
    merged = merged.sort_values("created_at", ascending=False).reset_index(drop=True)

    # Summary
    n_matched = (merged["y1_outcome"].fillna("no_policy_event_found") != "no_policy_event_found").sum()
    summary = {
        "pipeline_version": "v5 narrow tariff-adjacent + v6 anon BT",
        "deadline_date": "2026-05-12",
        "n_threats_total": int(len(posts)),
        "n_threats_tariff_adjacent": int(len(posts_narrow)),
        "n_episodes_narrow": int(eps_n["episode_id"].nunique()),
        "n_consensus_matches": int((eps_n["match_status"] == "consensus_match").sum() if "match_status" in eps_n.columns else 0),
        "ground_truth": {
            "tier_1_primary": "Hand-compiled (Wikipedia + Tax Foundation Trump Tariffs Tracker)",
            "tier_1_n_events": int(len(gt)),
            "tier_2_validation": "Federal Register Presidential Documents (tariff)",
            "tier_2_n_eos": int(len(json.loads(FR_FP.read_text())["results"])),
            "tier_3_robustness": "PIIE Trump Trade War Timeline 2.0 (LLM-cleaned status)",
            "tier_3_n_events": 145,
        },
        "match_method": "Cross-LLM consensus (Claude Haiku 4.5 + GPT-4o-mini both pick same event)",
        "data_through": str(merged["created_at"].max())[:10] if len(merged) else None,
    }

    # Y2 stats
    es_stats = {
        "n_event_study_obs": int(len(es)),
        "mean_car_30d_pct": float(es["car_30d"].mean() * 100),
        "median_car_30d_pct": float(es["car_30d"].median() * 100),
        "mean_peak_drawdown_30d_pct": float(es["peak_drawdown_30d"].mean() * 100),
        "mean_max_recovery_30d_pct": float(es["max_recovery_30d"].mean() * 100),
    }

    # V5 + V6 Cox results
    key_results = {"specifications": []}
    for fp, label in [(COX_V5_FP, "V5 Primary (narrow A, BT v1 original-text)"),
                      (COX_V6_FP, "V6 Anon + 1-7 BT (Claude/GPT/Consensus)")]:
        if fp.exists():
            df = pd.read_parquet(fp)
            for _, r in df.iterrows():
                key_results["specifications"].append({
                    "spec": str(r.get("label", label)),
                    "feature": str(r["feature"]).replace("btz_claude__", "").replace("btz__", "").replace("btz_consensus__", "").replace("btz_gpt__", ""),
                    "n": int(r["n"]),
                    "events": int(r["events"]),
                    "hr": float(r["hr"]),
                    "boot_lo": float(r["boot_lo"]),
                    "boot_hi": float(r["boot_hi"]),
                    "p_empirical": float(r["p_empirical"]),
                })

    # EIV sensitivity
    eiv_summary = None
    if EIV_FP.exists():
        eiv = pd.read_parquet(EIV_FP)
        eiv_summary = eiv[eiv["feature"] == "specificity"].to_dict(orient="records")

    # Loose match comparison
    loose_summary = None
    if LOOSE_FP.exists():
        l = pd.read_parquet(LOOSE_FP)
        loose_summary = l[l["feature"] == "btz__specificity"].to_dict(orient="records")

    # Cross-LLM BT v2 agreement
    bt_cross_llm = None
    if BT_V2_FP.exists():
        bt = pd.read_parquet(BT_V2_FP)
        bt_cross_llm = {}
        for f in ["commitment_strength", "hedging_level", "specificity", "audience_cost"]:
            cc, gc = f"bt_claude__{f}", f"bt_gpt__{f}"
            if cc in bt.columns and gc in bt.columns:
                r = bt[[cc, gc]].corr().iloc[0, 1]
                bt_cross_llm[f] = round(float(r), 3) if pd.notna(r) else None

    # threats (sample rows for app display)
    threat_rows = []
    for _, r in merged.head(150).iterrows():
        threat_rows.append({
            "id": str(r["_id"]),
            "date": str(r["created_at"])[:16],
            "text_preview": str(r["content"])[:280] if pd.notna(r.get("content")) else "",
            "policy_area": clean(r.get("claude_policy")),
            "target": clean(r.get("matched_target")),
            "y1_outcome": clean(r.get("y1_outcome")) or "no_policy_event_found",
            "matched_status_raw": clean(r.get("matched_status_raw")),
            "anticipation_days": clean(r.get("anticipation_days")),
            "car_1d": clean(r.get("car_1d")),
            "car_5d": clean(r.get("car_5d")),
            "car_30d": clean(r.get("car_30d")),
            "peak_drawdown_30d": clean(r.get("peak_drawdown_30d")),
            "max_recovery_30d": clean(r.get("max_recovery_30d")),
            "hedging_level": clean(r.get("claude_med__hedging_level")),
            "commitment_strength": clean(r.get("claude_med__commitment_strength")),
            "specificity": clean(r.get("claude_med__specificity")),
            "audience_cost": clean(r.get("claude_med__audience_cost")),
        })

    data = {
        "summary": summary,
        "y2_stats": es_stats,
        "key_results": key_results,
        "eiv_sensitivity_specificity": eiv_summary,
        "loose_match_ablation": loose_summary,
        "cross_llm_bt_v2_agreement": bt_cross_llm,
        "threats_sample": threat_rows,
    }

    OUT_JSON.write_text(json.dumps(data, indent=2, default=str))
    OUT_JS.write_text(f"window.appData = {json.dumps(data, default=str)};")
    print(f"[saved] {OUT_JSON} ({OUT_JSON.stat().st_size} bytes)")
    print(f"[saved] {OUT_JS}")


if __name__ == "__main__":
    main()
