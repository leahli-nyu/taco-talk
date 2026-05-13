"""Build app/data.json from processed parquet files.

Output schema (consumed by app/app.js):
{
  "summary": {...},
  "ticker": {...},
  "outcome_counts": {...},
  "threats": [ { date, text_preview, target, y1_outcome, car_1d, car_30d } ... ]
}
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
THREATS = ROOT / "data" / "processed" / "threats_with_outcomes_v2.parquet"
EVENT_STUDY = ROOT / "data" / "processed" / "event_study_results.parquet"
FR_EOS = ROOT / "data" / "raw" / "federal_register_tariff_eos.json"
EPISODES_FP = ROOT / "data" / "processed" / "episodes_with_outcomes.parquet"
OUT = ROOT / "app" / "data.json"

def clean(v):
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    if pd.isna(v): return None
    return v

def main():
    threats = pd.read_parquet(THREATS)
    es = pd.read_parquet(EVENT_STUDY)
    fr = json.loads(FR_EOS.read_text())["results"]

    # Join event-study results into threats
    threats["_id"] = threats["_id"].astype(str)
    es["_id"] = es["_id"].astype(str)
    merged = threats.merge(
        es[["_id", "car_1d", "car_5d", "car_30d", "peak_drawdown_30d", "max_recovery_30d"]],
        on="_id", how="left"
    )
    merged = merged.sort_values("created_at", ascending=False).reset_index(drop=True)

    # Threat cards
    threat_records = []
    for _, r in merged.iterrows():
        threat_records.append({
            "id": str(r["_id"]),
            "date": str(pd.to_datetime(r["created_at"]).strftime("%Y-%m-%d %H:%M")),
            "text_preview": (str(r.get("content", "") or "")[:240]).replace("\n", " "),
            "target": clean(r.get("target")),
            "y1_outcome": clean(r.get("y1_outcome")),
            "y1_status": clean(r.get("y1_status")),
            "matched_category": clean(r.get("matched_category")),
            "matched_date": clean(r.get("matched_date")),
            "car_1d": clean(r.get("car_1d")),
            "car_5d": clean(r.get("car_5d")),
            "car_30d": clean(r.get("car_30d")),
            "days_threat_to_event": clean(r.get("days_threat_to_event")),
        })

    # Outcome counts
    outcome_counts = merged["y1_outcome"].value_counts().to_dict()
    outcome_counts = {k: int(v) for k, v in outcome_counts.items()}

    # Ticker stats — use EPISODE-level for anticipation (true predictive horizon)
    sub = merged.loc[merged["y1_outcome"] != "unmatched"]
    avg_car_30d = float(es["car_30d"].mean()) if "car_30d" in es.columns else None
    n_matched = len(sub)
    taco_rate = float((sub["y1_outcome"] == "modified_or_withdrawn").mean()) if n_matched else None
    exec_rate = float((sub["y1_outcome"] == "executed").mean()) if n_matched else None
    # Prefer episode-level anticipation if available
    med_anticip = None
    if EPISODES_FP.exists():
        eps_df = pd.read_parquet(EPISODES_FP)
        eps_matched = eps_df[eps_df["anticipation_days"].notna()]
        if len(eps_matched):
            med_anticip = float(eps_matched["anticipation_days"].median())
    if med_anticip is None:
        med_anticip = float(sub["days_threat_to_event"].median()) if n_matched else None

    # additional stats for app
    avg_drawdown = float(es["peak_drawdown_30d"].mean()) if "peak_drawdown_30d" in es.columns else None
    avg_recovery = float(es["max_recovery_30d"].mean()) if "max_recovery_30d" in es.columns else None
    n_episodes = None
    if EPISODES_FP.exists():
        eps_df = pd.read_parquet(EPISODES_FP)
        n_episodes = int(len(eps_df))

    out = {
        "summary": {
            "n_threats": int(len(merged)),
            "n_threats_matched": int(n_matched),
            "n_eos": int(len(fr)),
            "match_rate": float(n_matched / len(merged)) if len(merged) else 0.0,
            "data_through": str(pd.to_datetime(merged["created_at"]).max().strftime("%Y-%m-%d")),
        },
        "outcome_counts": outcome_counts,
        "ticker": {
            "avg_car_30d": avg_car_30d,
            "median_anticipation_days": med_anticip,
            "taco_rate": taco_rate,
            "execution_rate": exec_rate,
            "avg_peak_drawdown_30d": avg_drawdown,
            "avg_max_recovery_30d": avg_recovery,
        },
        "threats": threat_records,
    }
    # also expose summary['n_episodes']
    out["summary"]["n_episodes"] = n_episodes

    OUT.write_text(json.dumps(out, indent=2, default=str))
    print(f"[saved] {OUT}  ({len(threat_records)} threats)")

    # ALSO write data.js so file:// loading works (CORS bypass via <script>)
    DATA_JS = OUT.parent / "data.js"
    js = "window.__APP_DATA__ = " + json.dumps(out, default=str) + ";\n"
    DATA_JS.write_text(js)
    print(f"[saved] {DATA_JS}")

if __name__ == "__main__":
    main()
