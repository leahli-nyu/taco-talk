# Preliminary Findings (Rule-based Labels)

> Generated 2026-05-11 ~04:30. These are based on the **rule-based** A/B/C classifier (N=111 A-class).
> Will be re-generated after LLM relabel completes — expect mostly stable patterns, finer signal.

## Y1 Outcome Distribution (per-post matching)

| Outcome | N | % |
|---|---|---|
| executed | 38 | 34.2% |
| modified_or_withdrawn | 19 | 17.1% |
| announced_unresolved | 20 | 18.0% |
| struck_down | (in "other") | — |
| other | 25 | 22.5% |
| investigation | 6 | 5.4% |
| unmatched | 3 | 2.7% |

**Match rate: 97.3%** (108/111 posts matched to a PIIE timeline event)

## Y2: Market Reaction (S&P 500 event study, N=99 with sufficient pre-event data)

| Window | Mean CAR | Std | 25th | 75th |
|---|---|---|---|---|
| 1-day | -0.05% | 1.99% | -1.03% | +0.89% |
| 5-day | +0.26% | 2.44% | -1.32% | +1.04% |
| 30-day | -0.09% | — | — | — |
| Peak drawdown (30d) | **-4.51%** | 4.20% | -6.50% | -1.90% |
| Max recovery (30d) | **+3.50%** | 5.01% | +0.24% | +5.40% |

**Key observation**: Mean 30-day CAR is essentially zero (-0.09%), but the *path* swings widely (peak -4.5%, recovery +3.5%). This is the classic TACO pattern: initial overshoot followed by mean reversion.

## Feature → Market Correlations (preliminary)

Strongest |Pearson r| between features and market outcomes:

| Feature | Strongest market signal | r | Interpretation |
|---|---|---|---|
| lm_uncertainty | peak_drawdown_30d | **-0.21** | Uncertainty words → deeper drawdowns |
| lm_uncertainty | car_5d | -0.18 | Uncertainty → 5-day negative reaction |
| lm_uncertainty | car_30d | -0.18 | Sustained negative |
| lm_hedging | max_recovery_30d | -0.17 | Hedging → less recovery |
| is_first_mention | car_1d | +0.17 | Novelty → less initial drop |
| repeat_count_7d | max_recovery_30d | **+0.16** | Repetition → more recovery (TACO!) |
| neighbor_event_count | car_1d | +0.15 | Clustering → bigger reaction |

### Standout finding: `repeat_count_7d` ↔ `max_recovery_30d`

When Trump repeats the same topic within 7 days, the 30-day **recovery is greater**. This is the
empirical signature of TACO: repeated threats are read by the market as less credible, leading to
larger eventual mean-reversion.

## Contrastive Language: Executed vs Withdrawn

Most distinctive unigrams in **modified_or_withdrawn** posts (vs executed):
- "peace", "ceasefire", "historic", "pharmaceutical", "credit card", "san francisco"
- Trump uses *positive relational* vocabulary when softening: "thank president", "both countries", "china agreed"

Most distinctive unigrams in **executed** posts (vs modified_or_withdrawn):
- "ICE", "border patrol", "law enforcement officers"
- Immigration-related language tied to action (note: matches B-class-ish content in rule-based labels — should clean up after LLM relabel)

Most distinctive in **executed** vs **announced_unresolved**:
- "city", "market", "ICE", "Mexico", "officers", "illegal aliens"
- Concrete, action-oriented words

## What This Means

1. **Uncertainty/hedging signals work in the expected direction**: Trump's hedging language predicts
   greater market drawdown — consistent with the market reading hedging as low-credibility threat
   that nonetheless raises uncertainty premium.

2. **Repetition (`repeat_count_7d`) is the TACO marker**: posts that recur within a week predict
   eventual market recovery — i.e., repeated threats are less likely to be executed.

3. **First-mention threats have smaller immediate reaction**: surprise novelty doesn't shock the
   market as much, possibly because anchoring on prior policy is weak.

4. **Domain matters**: Immigration-tagged content (ICE, border) is over-represented in "executed";
   peace/ceasefire/agreement language is over-represented in "withdrawn". This suggests the
   linguistic predictor is partly capturing domain rather than commitment strength alone.

## What's Still TBD (after LLM relabel)

- Reducing false-positive A-class (the rule-based pipeline mis-classifies some ICE/immigration posts as A)
- Confirming `repeat_count_7d` ↔ recovery relationship holds with cleaner labels
- Cox PH hazard ratios (currently waiting on episode_clustering)
- Comparison to LLM zero-shot baseline
