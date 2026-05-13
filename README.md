# Tariff Talk and Asset Prices

A quantitative analysis of Trump's tariff-relevant Truth Social posts (second term, 2024-11-06 → 2026-05-12), paired with formal policy outcomes and S&P 500 market reactions.

**DS-GA 1015 (Text as Data) · Spring 2026 · Final Project**

---

## Research Questions

- **Q1.** Is the text of an individual tariff threat *associated with* whether and when it gets enacted? Which linguistic dimensions, if any, carry signal?
- **Q2.** How does the S&P 500 react in the 30 trading days following such threats, and is the reaction asymmetric (drawdown then recovery)?

## Headline Findings

1. **S&P 500 path around posts is not Trump-specific.** Average path over 30 trading days following A-class posts: peak drawdown −4.95%, max recovery +3.80%, net CAR ≈ 0 (N=118). Placebo test on same-period random dates shows this path is not statistically distinguishable from baseline volatility, so we report it as descriptive of the period rather than a Trump-specific causal effect.
2. **`Specificity` is direction-consistent under LLM matching, fragile under human matching.** Primary LLM-only specification: HR=1.39 [0.95, 2.14], p=0.076 (N=66, 16 events). Direction holds across nine LLM-only specifications (HR ∈ [1.06, 2.17], HR > 1 in 8/9). Under human-validated matching (Packet E), HR=1.15, p=0.42 (null).
3. **Human validation numbers.** Specificity rank correlation human-vs-Claude r=0.75 (N=40); test-retest r=0.84 on hidden duplicates. Cross-LLM matching precision 63% under human review. Episode clustering threshold (cosine 0.82) sits at the empirical Y/N transition zone (Spearman ρ=0.78, N=39 pairs).
4. **Cross-LLM disagreement is itself a finding.** Anonymized 1-7 pairwise BT scoring lifts Claude `specificity` HR to 2.17 (p<0.001) while leaving GPT-4o-mini null. Measurement-stack sensitivity that single-pipeline analyses cannot diagnose.

---

## Method

```
Truth Social archive (6,943 posts)
  → Cross-LLM A/B/C classification (Claude Haiku 4.5 + GPT-4o-mini consensus)
  → Tariff-adjacent A class (102 posts)
  → Episode clustering (BAAI/bge-large-en-v1.5, cosine 0.82 + 30-day window)
  → 77 episodes
  → Cross-LLM event matching against hand-compiled GT (43 events)
  → 27 consensus matches
  → Cox PH + 1,000 bootstrap + discrete-time logistic
```

**Ground truth — three tiers:**

| Tier | Source | Role |
|---|---|---|
| 1 (primary) | Hand-compiled Wikipedia + Tax Foundation tracker | 43 human-labeled events |
| 2 (validation) | Federal Register Presidential Documents | 71 EOs; 90.5% in_effect cross-confirm |
| 3 (robustness) | PIIE Trade War Timeline (LLM-cleaned status) | 145 events; same direction, larger N noisier |

**Features (per episode first-post):** 10 LLM-rated linguistic dimensions on 0-10 scale (3-call test-retest mean r=0.94), plus four key dimensions re-scored via cross-LLM pairwise Bradley-Terry on anonymized text using a 1-7 graduated scale.

---

## Key files

| File | Purpose |
|---|---|
| [paper/draft.md](paper/draft.md) | Paper draft (Methods + 9-specification robustness analysis) |
| [DECISIONS.md](DECISIONS.md) | Locked research-design decisions |
| [app/index.html](app/index.html) | Web app (TACO Tracker style) |
| [app/DEPLOY.md](app/DEPLOY.md) | GitHub Pages deployment guide |
| [annotation/index.html](annotation/index.html) | Bilingual EN-ZH human-rater interface |
| [figures/](figures/) | 6 paper figures (forest plots + TACO signature) |

## Primary pipeline (run end-to-end)

| # | Script | Output |
|---|---|---|
| 1 | `src/llm_classify_v2.py` | Cross-LLM A/B/C labels |
| 2 | `src/build_consensus_a.py` | `consensus_a.parquet` (141) |
| 3 | `src/rich_features.py` | 10 LLM features × 3 calls |
| 4 | `src/episode_clustering_v2.py` | 110 episodes |
| 5 | `src/narrow_to_tariff_adjacent.py` | 77 tariff-adjacent episodes |
| 6 | `src/anonymize_text.py` | Anonymized texts for BT input |
| 7 | `src/llm_match_to_hc_gt.py` | Cross-LLM event matching → 27 consensus |
| 8 | `src/pairwise_bt_v2.py` + `compute_bt_v2_scores.py` | BT scores (Claude + GPT + Consensus) |
| 9 | `src/event_study_v2.py` | CAR / VIX event study (N=118) |
| 10 | `src/cox_v6_anon_bt.py` | Cox PH + bootstrap (primary results) |
| 11 | `src/generate_paper_figures_v2.py` | 6 figures |
| 12 | `src/build_app_data_v3.py` | Web app data |

## Robustness analyses (paper §5.4)

- `src/cox_eiv_sensitivity.py` — Reliability-adjusted Cox (ρ ∈ {1.0, 0.95, 0.85, 0.70, 0.50})
- `src/loose_match_ablation.py` — "Either LLM matched" vs strict consensus
- `src/threshold_sensitivity.py` — Episode clustering threshold sensitivity
- `src/federal_register_cross_validate.py` — Tier-2 GT cross-check
- `src/piie_llm_relabel.py` + `src/match_v3_with_llm_status.py` — Tier-3 GT robustness

---

## Quick Start

```bash
pip install -r requirements.txt

# View web app locally
cd app && python3 -m http.server 8000
# open http://localhost:8000

# Deploy: see app/DEPLOY.md
```

Create `.env` in project root:
```
ANTHROPIC_API_KEY=sk-ant-your-key
OPENAI_API_KEY=sk-your-key
```

## Data Sources (all public)

- [CNN Truth Social archive](https://ix.cnn.io/data/truth-social/truth_archive.json) — primary corpus
- [Wikipedia: Tariffs in the second Trump administration](https://en.wikipedia.org/wiki/Tariffs_in_the_second_Trump_administration) — Tier-1 GT
- [Tax Foundation Trump Tariffs Tracker](https://taxfoundation.org/research/all/federal/trump-tariffs-trade-war/) — Tier-1 GT
- [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1) — Tier-2 (71 EOs)
- [PIIE Trump Trade War Timeline 2.0](https://www.piie.com/blogs/realtime-economics/2025/trumps-trade-war-timeline-20-date-guide) — Tier-3
- [yfinance](https://pypi.org/project/yfinance/) — daily prices

## Disclaimers

Not financial advice. The estimated `specificity → resolution` association is a correlate, not a causal claim, and is observed with marginal statistical significance (p=0.076 in the primary specification). Sample sizes are small (N=66 modeling sample, 16 events with 5 tied to a single SCOTUS ruling). Treat findings as exploratory.
