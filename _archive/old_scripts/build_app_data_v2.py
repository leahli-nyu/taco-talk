"""Build app/data.js (and data.json) from v2 pipeline outputs."""
from __future__ import annotations
import json
import math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
POSTS_FP = ROOT / "data" / "processed" / "all_features.parquet"
EPS_FP = ROOT / "data" / "processed" / "episodes_with_outcomes_v2.parquet"
ES_FP = ROOT / "data" / "processed" / "event_study_v2.parquet"
FR_FP = ROOT / "data" / "raw" / "federal_register_tariff_eos.json"
COX_FP = ROOT / "data" / "processed" / "cox_v2_summary.parquet"
OUT_JSON = ROOT / "app" / "data.json"
OUT_JS = ROOT / "app" / "data.js"


def clean(v):
    try:
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        if pd.isna(v): return None
    except Exception:
        pass
    return v


def main():
    posts = pd.read_parquet(POSTS_FP)
    eps = pd.read_parquet(EPS_FP)
    es = pd.read_parquet(ES_FP)
    fr = json.loads(FR_FP.read_text())["results"]
    cox = pd.read_parquet(COX_FP) if COX_FP.exists() else None

    posts["_id"] = posts["_id"].astype(str)
    es["_id"] = es["_id"].astype(str)

    # Join event study results
    merged = posts.merge(
        es[["_id", "car_1d", "car_5d", "car_30d", "peak_drawdown_30d", "max_recovery_30d"]],
        on="_id", how="left",
    )
    # Join episode outcomes via episode_id
    if "episode_id" in merged.columns and "y1_outcome" in eps.columns:
        merged = merged.merge(
            eps[["episode_id", "y1_outcome", "anticipation_days", "matched_country", "matched_category"]],
            on="episode_id", how="left",
        )

    merged = merged.sort_values("created_at", ascending=False).reset_index(drop=True)

    # Threat records
    threat_records = []
    for _, r in merged.iterrows():
        threat_records.append({
            "id": str(r["_id"]),
            "date": str(pd.to_datetime(r["created_at"]).strftime("%Y-%m-%d %H:%M")),
            "text_preview": (str(r.get("content", "") or "")[:240]).replace("\n", " "),
            "target": clean(r.get("matched_country") or r.get("any_target") or r.get("target_entity")),
            "y1_outcome": clean(r.get("y1_outcome")),
            "matched_category": clean(r.get("matched_category")),
            "anticipation_days": clean(r.get("anticipation_days")),
            "car_1d": clean(r.get("car_1d")),
            "car_5d": clean(r.get("car_5d")),
            "car_30d": clean(r.get("car_30d")),
            # LLM features (Claude median, useful for explorer)
            "hedging_level": clean(r.get("claude_med__hedging_level")),
            "commitment_strength": clean(r.get("claude_med__commitment_strength")),
            "specificity": clean(r.get("claude_med__specificity")),
            "dramatization": clean(r.get("claude_med__dramatization")),
        })

    outcome_counts = merged["y1_outcome"].value_counts().to_dict()
    outcome_counts = {k: int(v) for k, v in outcome_counts.items()}

    sub = merged.loc[merged["y1_outcome"] != "no_policy_event_found"]
    n_matched = len(sub)

    out = {
        "summary": {
            "n_threats": int(len(merged)),
            "n_threats_matched": int(n_matched),
            "n_eos": int(len(fr)),
            "match_rate": float(n_matched / len(merged)) if len(merged) else 0.0,
            "data_through": str(pd.to_datetime(merged["created_at"]).max().strftime("%Y-%m-%d")),
            "n_episodes": int(len(eps)),
        },
        "outcome_counts": outcome_counts,
        "ticker": {
            "avg_car_30d": float(es["car_30d"].mean()) if "car_30d" in es.columns else None,
            "median_anticipation_days": float(eps["anticipation_days"].median()) if "anticipation_days" in eps.columns else None,
            "taco_rate": float((sub["y1_outcome"] == "modified_or_withdrawn").mean()) if n_matched else None,
            "execution_rate": float((sub["y1_outcome"] == "executed").mean()) if n_matched else None,
            "avg_peak_drawdown_30d": float(es["peak_drawdown_30d"].mean()) if "peak_drawdown_30d" in es.columns else None,
            "avg_max_recovery_30d": float(es["max_recovery_30d"].mean()) if "max_recovery_30d" in es.columns else None,
        },
        "threats": threat_records,
    }

    # Cox PH summary (for paper / app)
    if cox is not None:
        out["cox_summary"] = []
        for idx, row in cox.iterrows():
            out["cox_summary"].append({
                "feature": idx,
                "hr": float(row["exp(coef)"]),
                "ci_low": float(row["exp(coef) lower 95%"]),
                "ci_high": float(row["exp(coef) upper 95%"]),
                "p": float(row["p"]),
            })

    OUT_JSON.write_text(json.dumps(out, indent=2, default=str))
    print(f"[saved] {OUT_JSON}  ({len(threat_records)} threats)")
    OUT_JS.write_text("window.__APP_DATA__ = " + json.dumps(out, default=str) + ";\n")
    print(f"[saved] {OUT_JS}")

    # Copy to designs
    for d in ("a", "b", "c"):
        target = ROOT / "app" / "designs" / d / "data.js"
        if target.parent.exists():
            target.write_text(OUT_JS.read_text())
            print(f"[copy] {target.relative_to(ROOT)}")
    target_annot = ROOT / "annotation" / "data.js"
    if target_annot.parent.exists():
        target_annot.write_text(OUT_JS.read_text())


if __name__ == "__main__":
    main()
