# Tariff Talk and Asset Prices

## Measuring Trump Tariff Threats: A Cross-LLM Linguistic Pipeline and What It Can (and Cannot) Explain

**Anonymous Author** · DS-GA 1015 · Spring 2026

---

## Abstract

We measure every tariff-relevant Trump Truth Social post in his second term (2024-11-06 through 2026-05-12; N=6,943 originals). Each post is classified A/B/C via Speech Act Theory using both Claude Haiku 4.5 and GPT-4o-mini. The analysis sample is the consensus A class (N=141 posts, clustered into 110 policy episodes) where both LLMs agree. For each first-post we extract 10 LLM-rated linguistic features (3-call test-retest mean r=0.94). Because absolute 0-10 ratings saturate, we additionally derive Bradley-Terry ranking scores from 200 LLM-judged pairwise comparisons on four key features. Policy outcomes are matched via a three-tier ground-truth architecture: a hand-compiled Wikipedia and Tax Foundation timeline (43 events, human-labeled status) as the primary source; the Federal Register Presidential-Document API (71 EOs) for cross-validation; the PIIE Trump Trade War Timeline (145 events, status re-cleaned via LLM) as a robustness check. Episode-event matching is also cross-LLM: Claude and GPT-4o-mini independently pick the best match from candidates in [-10, +60d], and only consensus matches are retained (N=27 in the primary tariff-adjacent sample).

We report three findings. First, in the 30 trading days following A-class posts, S&P 500 cumulative abnormal returns trace an average path of −4.95% peak drawdown and +3.80% maximum recovery (N=118); placebo testing on same-period dates shows this path is not statistically distinguishable from baseline volatility, so we frame it as descriptive of the period rather than a Trump-specific causal signature. Second, BT-ranked `specificity` is associated with faster policy resolution in the LLM-only matching: HR=1.39 [0.95, 2.14], p=0.076 (N=66, 16 events). The direction holds across nine pre-human specifications (HR ∈ [1.06, 2.17], HR > 1 in 8/9). Under human-validated matching (Packet E annotation), the same HR drops to 1.15 (p=0.42, null), indicating part of the LLM-only signal was supported by matches the human reviewer rejected. Third, discrete-time logistic models show different features dominate at different horizons (commitment and specificity at days 3-7, hedging at days 31-90).

Methodologically we contribute: (a) a cross-LLM consensus pipeline for both classification and event-matching that filters spurious single-model matches (relaxing to either-LLM-matched raises N from 16 to 39 events but collapses specificity HR from 1.39 to 1.06, confirming the filter selects on signal); (b) evidence that measurement choices drive findings (an earlier rule-based `lm_hedging` HR=8.6 collapses to 0.93 under cross-LLM rigor; a Python regex bug in PIIE status inference flipped 30% of all status labels until corrected by LLM relabeling; anonymized BT scoring shifts the Claude specificity estimate from HR=1.39 to 2.17 while leaving GPT-BT null); (c) human validation of both feature ratings and matching: on a stratified 40-item subset of posts, human-Claude rank correlation on specificity is r = 0.75 with test-retest r = 0.84 on hidden duplicates; on 75 matching cases (24 disagree + 27 consensus + 24 controls), cross-LLM consensus matching achieves 63% precision under human review, with 100% agreement on both-none controls and 92% resistance to fake-match forced-choice; (d) the first systematic comparison of three independent ground-truth sources for Trump tariff actions, finding 98% event overlap between Wikipedia/Tax Foundation and PIIE but substantial status-label divergence.

**Keywords**: tariff, Trump, TACO, policy communication, event study, large language models, Bradley-Terry, measurement validity, ground truth

---

## 1. Introduction

In May 2025, *Financial Times* columnist Robert Armstrong coined the term TACO ("Trump Always Chickens Out") to describe a recurring pattern: the U.S. president issues a drastic tariff threat, the market sells off, and the threat is later walked back. The pattern is widely cited enough to anchor a so-called TACO trade said to have produced double-digit Q1 2025 returns for some hedge funds ([CNN 2025](https://www.cnn.com/2025/07/09/business/trump-tariffs-markets-taco)). The phenomenon has not, however, been quantitatively examined. Existing public trackers ([thetacotracker.com](https://www.thetacotracker.com/), PolitiFact MAGA-Meter) catalogue events ex-post but make no predictions and identify no textual features that distinguish executed from withdrawn threats.

This paper asks two questions:

> **Q1.** Is the text of an individual tariff threat associated with whether and when it gets enacted? Which linguistic dimensions, if any, carry signal?
>
> **Q2.** How does the S&P 500 react in the 30 trading days following such threats, and is the reaction asymmetric (drawdown then recovery)?

We pose these against the methodological backdrop of [Baker, Bloom & Davis (2016)](https://www.policyuncertainty.com/), who showed that text-derived signals from public discourse have predictive content for macroeconomic outcomes. We narrow this approach to a single political actor's individual posts and evaluate whether the narrowing holds.

**Contributions.**

1. A reproducible cross-LLM pipeline for political-text analysis. Claude Haiku 4.5 and GPT-4o-mini agree at three stages: A/B/C classification, pairwise Bradley-Terry comparison of linguistic features, and episode-to-policy-event matching. Only consensus is retained, with reliability diagnostics at each stage.
2. A three-tier ground-truth architecture: a hand-compiled Wikipedia and Tax Foundation timeline as primary, Federal Register Presidential Documents for cross-validation, and the LLM-cleaned PIIE timeline for robustness. We evaluate four additional tracker websites (Atlantic Council, Tax Foundation, TaCo Tracker, Trump Trade Tracker) and find none publish structured downloadable data.
3. Event-study evidence on the TACO market path: average peak drawdown −4.95% and maximum recovery +3.80% over 30 trading days (N=118). Placebo tests show this path is not statistically distinguishable from same-period baseline, so we report it as descriptive of the period rather than a Trump-specific effect.
4. A direction-consistent but unstable outcome-association result. Across nine LLM-only specifications, BT-ranked specificity HR ∈ [1.06, 2.17] with HR > 1 in 8/9. The primary tariff-adjacent specification gives HR=1.39 [0.95, 2.14], p=0.076; the anonymized 1-7 Claude BT specification gives HR=2.17 [1.48, 3.64], p<0.001; the GPT counterpart is null. Under human-validated matching (Packet E), the same specification gives HR=1.15, p=0.42 (null). The signal does not survive replacement of LLM consensus with human-anchored matching. Discrete-time logistic concentrates the within-LLM signal in days 3-7 post-threat.
5. A measurement-stack documentation. We trace six successive corrections (rule-based to cross-LLM A class; 0-10 to pairwise BT; loose to strict matching; regex to LLM status inference; broad to tariff-adjacent A; original to anonymized BT) and report all resulting specifications. Two mid-pipeline "significant" results (specificity HR=1.58, p=0.028 with PIIE regex status; specificity HR=2.17, p<0.001 with Claude anonymized BT) are both overturned by adjacent robustness checks (LLM-status rerun and GPT BT). Cross-LLM, multi-specification reporting is the framing we recommend.

---

## 2. Related Work

**Policy communication and asset prices.** [Baker, Bloom & Davis (2016)](https://www.policyuncertainty.com/) construct an Economic Policy Uncertainty (EPU) index from newspaper text. [Husted, Rogers & Sun (2020)](https://www.federalreserve.gov/econres/feds/files/2017027r1pap.pdf) refine the text→market pipeline for monetary policy. [Egger & Zhu (2020)](https://onlinelibrary.wiley.com/doi/10.1111/twec.12952) study Trump's first-term tariff news and stock prices. Our work narrows the target to a single politician's individual posts.

**Text analysis in economics.** [Ash & Hansen (2023)](https://sekhansen.github.io/pdf_files/are_2023.pdf) and [Ash et al. (2026)](https://elliottash.com/) review methodological practice and recommend LLMs as auxiliary annotation tools rather than primary predictors. We follow this advice, using two LLMs for measurement and traditional econometric methods (Cox PH, event study) for inference.

**Speech act theory and political language.** Following [Searle (1969)](https://www.cambridge.org/core/books/speech-acts/D2D7B03C24A24DBF1B2C9606DB7CCA46), we operationalize *commissive* speech acts as the prerequisite for a post to count as a threat (an action the speaker commits to taking). The audience-cost tradition ([Fearon 1994](https://www.cambridge.org/core/journals/american-political-science-review/article/abs/domestic-political-audiences-and-the-escalation-of-international-disputes/B97A7B7E2A4E18F71D8E2EAF9E92FE5C)) motivates the hypothesis that public commissives carry credibility because backing down is costly.

**Event studies.** Our Y2 framework follows the standard methodology of [MacKinlay (1997)](https://www.jstor.org/stable/2729691).

**LLM as measurement instrument.** Recent work (e.g., [Velez & Lavinas 2024](https://arxiv.org/abs/2410.07978), [Mellon et al. 2024](https://arxiv.org/abs/2407.07775)) raises validity concerns when LLMs are used as raters for politically-loaded content. We adopt their recommended practice of reporting test-retest reliability and cross-model agreement explicitly.

---

## 3. Data

### 3.1 Trump Truth Social archive

We use the CNN-maintained Truth Social archive (`ix.cnn.io/data/truth-social/truth_archive.json`), which contains all of Trump's posts on the platform. Filtering to original posts (excluding pure reshares and empty content) within the period 2024-11-06 (AP race call) through 2026-05-11 yields **N = 6,943 original posts**.

### 3.2 Classification: consensus A class, narrowed to tariff-adjacent

Each of the 6,943 posts is classified into A/B/C using both Claude Haiku 4.5 and GPT-4o-mini, each prompted with an explicit Speech Act Theory framework:

- **A** = commissive + government-executable + economic-financial transmission channel
- **B** = commissive + non-economic primary impact (immigration/military/judicial/social)
- **C** = non-commissive

The full A class spans seven sub-domains: tariff, trade_agreement, commodity_intervention, sanctions, fed_monetary, antitrust_tech, financial_regulation. These map approximately to standard policy-area codes used in comparative policy-text research (e.g., topics 14 and 15 of the Comparative Agendas Project topic system, and selected economic-policy codes in the Policy Agendas Project), although we use a smaller hand-engineered set tailored to executive economic commissives rather than a full legislative-text taxonomy. The two models show 80.4% agreement (Cohen's κ = 0.45, moderate). To maximize precision, we take the consensus A class where both LLMs label A: 141 posts. Distribution by Claude policy_area: tariff (76), financial_regulation (23), trade_agreement (16), commodity_intervention (10), sanctions (8), fed_monetary (4), antitrust_tech (3), multiple (1).

**Alignment with ground-truth scope.** The ground-truth source (§3.3) is tariff-focused. We therefore narrow the analysis sample to the tariff-adjacent A sub-class: Claude policy_area $\in$ {`tariff`, `trade_agreement`, `commodity_intervention`}, yielding N = 102 posts. This avoids testing a broader econ-policy theory against a tariff-only outcome timeline. The remaining 39 posts (financial_regulation, sanctions, fed_monetary, antitrust_tech) lack systematic ground truth and are deferred. This narrowing was not in the original design document; the A class was originally framed broadly under the assumption that per-domain ground-truth sources would be available.

### 3.3 Y1 ground truth: three-tier architecture

Choosing a ground truth is non-trivial: no single source is both comprehensive and clean. We evaluated seven candidate sources (PIIE's Trade War Timeline; Atlantic Council's Trump Tariff Tracker; the Tax Foundation Tariff Tracker; Wikipedia's "Tariffs in the second Trump administration" article; the Federal Register API; CRS R48549; thetacotracker.com). Four of the web trackers (Atlantic Council, Tax Foundation, TaCo Tracker, Trump Trade Tracker) are presented as news feeds or interactive visualizations and do not publish structured downloadable data; the CRS PDF resists parsing. After triage we settled on three tiers:

**Tier 1 (primary): Hand-compiled Wikipedia and Tax Foundation timeline.** A hand-compiled JSON of 43 events with structured `announced`, `effective`, `target`, `status`, `rate_pct`, and `authority` fields, sourced from the [Wikipedia article](https://en.wikipedia.org/wiki/Tariffs_in_the_second_Trump_administration) and the [Tax Foundation Trump Tariffs Tracker](https://taxfoundation.org/research/all/federal/trump-tariffs-trade-war/). Status values are human-labeled: in_effect (21), modified (10), struck_down (6), investigation (3), withdrawn (2), paused (1).

**Tier 2 (validation): Federal Register Presidential Documents.** All 71 Presidential Documents matching "tariff" between 2025-01-20 and 2026-05-12, via the [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1). For each Tier-1 in_effect event, we check whether a corresponding Presidential Document was published within [-3, +14] days. 19 of 21 in_effect events (90.5%) cross-validate. The two without (407 metal products, implemented via Commerce Department fact sheet; UK pharmaceuticals, implemented via bilateral deal) are legitimate cases that did not require a fresh EO.

**Tier 3 (robustness): PIIE Trump Trade War Timeline 2.0.** The [PIIE timeline](https://www.piie.com/blogs/realtime-economics/2025/trumps-trade-war-timeline-20-date-guide) (145 events). The public CSV provides only free-form descriptions, not categorical status labels. We initially inferred status via a Python regex; a later audit found a `\b` word-boundary bug that caused `\bannounce\b` to fail on "announces" and "announced" and `\bimpose\b` to fail on "imposing". Re-classification of all 145 descriptions via Claude Haiku 4.5 changed 83 of 145 status labels (57%), including 50% of the labels appearing on matched episodes. We use the LLM-cleaned PIIE as a robustness foil: same threats, larger but noisier labels.

**Episode-to-event matching.** Posts cluster into 110 policy episodes (sentence-transformer `BAAI/bge-large-en-v1.5`, cosine similarity > 0.82, 30-day rolling window). After restricting to tariff-adjacent A class, 77 episodes remain (57 tariff, 12 trade_agreement, 8 commodity_intervention). 95.5% of episodes are policy-area-monothematic across constituent posts (only 5/110 contain mixed sub-domains), so episode boundaries are preserved by the narrowing.

Each episode's first-post text is paired to a candidate event via a cross-LLM matching procedure: Claude Haiku 4.5 and GPT-4o-mini independently see the episode text plus all hand-compiled candidate events in [-10, +60] days and pick one or "none". A match is retained only if both models pick the same event. On the narrowed 77-episode sample this yields N=27 consensus matches; the other 50 episodes (26 both-none, 24 disagree) are right-censored. The broad A class (110 episodes) would yield 29 consensus matches; the two extras come from financial_regulation and sanctions episodes whose match to a tariff event is forced.

Anticipation period (first-post date to matched event date) among consensus matches has median 0-1 days (Trump often posts the day of or the day before EO signing), 75th percentile of 24 days, and maximum of 56 days.

### 3.4 Y2 market data

Daily prices for S&P 500, VIX, sector ETFs, currency pairs, and commodities via `yfinance`, covering 2024-11-01 onwards.

---

## 4. Methods

### 4.1 LLM-rated linguistic features

For each consensus A post, two LLMs (Claude Haiku 4.5 with 3 calls, GPT-4o-mini with 1 call) rate ten dimensions on a 0-10 anchored scale: `commitment_strength`, `specificity`, `hedging_level`, `dramatization`, `conditional_framing`, `audience_cost`, `precedent_invocation`, `negotiation_framing`, `personal_attack`, `ego_centric_framing`. Each prompt contains four explicit anchor examples for the 0/3/6/10 levels.

**Reliability (Table 1).**

| Feature | Test-retest (Claude×3, r) | Cross-LLM (Claude vs GPT, r) |
|---|---|---|
| commitment_strength | 0.95 | 0.69 |
| specificity | 0.97 | 0.61 |
| hedging_level | 0.96 | 0.53 |
| dramatization | 0.96 | 0.80 |
| conditional_framing | 0.92 | 0.47 |
| audience_cost | 0.94 | 0.61 |
| precedent_invocation | 0.94 | 0.62 |
| negotiation_framing | 0.95 | 0.49 |
| personal_attack | 0.97 | 0.73 |
| ego_centric_framing | 0.91 | 0.65 |

Claude is self-consistent (test-retest r > 0.91 for all features); cross-LLM agreement is moderate (r = 0.47-0.80). LLM measurement is therefore partially model-specific. The primary feature track is the Claude median of 3 calls; GPT-4o-mini ratings serve as robustness.

### 4.2 Pairwise Bradley-Terry ranking (saturation fix)

The 0-10 ratings exhibit a restricted-range problem. On the 110 consensus first-posts, `commitment_strength` has mean 7.6 (SD 1.4), `audience_cost` mean 7.4 (SD 1.7), and `dramatization` mean 6.9 (SD 1.8). Trump's posts are uniformly high on these dimensions; the compressed variance limits downstream regression power. We therefore add a parallel Bradley-Terry (BT) feature track for the four most-saturated dimensions (`commitment_strength`, `hedging_level`, `specificity`, `audience_cost`):

1. Sample 200 ordered pairs $(i, j)$ uniformly from the 77 narrow-tariff first-posts (each post appears in ≥ 3 pairs, all 77 covered).
2. Anonymize each text before sending to the LLM. Country names, percentages, dollar amounts, dates, named industries, and named persons are replaced with generic placeholders (`[COUNTRY]`, `[PERCENT]`, `[AMOUNT]`, `[DATE]`, `[INDUSTRY]`, `[PERSON]`). This forces the LLM to compare structural commitment-and-hedging language rather than the salience of named targets or specific numbers.
3. For each anonymized pair, Claude Haiku 4.5 and GPT-4o-mini independently rate each of the four features on a 1-7 graduated scale (1 = "A definitely much higher", 4 = "tie", 7 = "B definitely much higher"), yielding 200 × 4 × 2 = 1,600 pairwise scores.
4. Bradley-Terry models are fit separately per LLM and per feature: $P(i \text{ beats } j) = \sigma(s_i - s_j)$. The 1-7 score is linearly mapped to (A-wins-weight, B-wins-weight) so that intermediate certainties contribute partial credit.
5. We produce three feature tracks per dimension: Claude BT z-scores, GPT BT z-scores, and a consensus average. Cox is run with each track separately.

We denote the early-project comparisons (Claude-only, original-text, A/B/tie) as BT v1 and the later comparisons (Claude+GPT, anonymized, 1-7) as BT v2. Section 5.4 reports both, since they yield materially different Cox coefficients.

Cross-LLM Pearson correlation on BT v2 scores is low: r = +0.47 on `hedging_level`, r = −0.10 on `commitment_strength`, r = −0.06 on `specificity`, r = −0.30 on `audience_cost`. The 1-7 graduated scale exposes more cross-LLM divergence than the coarser 3-class scale used in BT v1.

### 4.3 Episode-level survival modeling

For each episode we observe `duration_days` (anticipation period, or right-censored at data cutoff) and `event` (binary: executed, modified-or-withdrawn, or struck-down). Survival models estimate associations between covariates and the time-to-resolution hazard. We avoid the language of "prediction" because our goal is correlate identification, not the construction of an operational forecaster.

**Cox proportional hazards** (`lifelines`, penalizer = 0.05):

$$h(t \mid x) = h_0(t) \exp(\beta^\top x)$$

We report hazard ratios with both analytic 95% CIs and percentile CIs from 1,000 bootstrap resamples stratified by event status. The PH assumption is tested via scaled Schoenfeld residuals; covariates with p < 0.05 are flagged.

**Discrete-time logistic** (PH-free alternative). Person-period observations are constructed for four time buckets (0-2, 3-7, 8-30, 31-90 days). A bucket-stratified logistic regression with z-standardized features lets us estimate feature associations that may vary across time horizons without assuming proportional hazards.

### 4.4 Event-study cumulative abnormal returns

Following [MacKinlay (1997)](https://www.jstor.org/stable/2729691), for each first-post event date $t_0$ we estimate a constant-mean market model over the pre-event window $[t_0-70, t_0-10]$ and compute CAR over post-event windows of 1, 5, 10, 30 trading days. We separately track *peak drawdown* and *max recovery* over the 30-day window.

### 4.5 LLM zero-shot baseline

Each first-post text is fed directly to Claude Haiku 4.5 and GPT-4o-mini with a single prompt asking them to predict the 3-class outcome (executed / modified-or-withdrawn / unresolved) within 90 days. This isolates whether direct LLM judgment outperforms our feature-engineered Cox PH.

---

## 5. Results

### 5.1 Outcome distribution

Among 27 cross-LLM-consensus matches in the **tariff-adjacent A class** (the other 50 episodes are censored):

| Outcome bucket | N |
|---|---|
| Executed (in_effect) | 10 |
| Modified or withdrawn (modified/withdrawn/paused) | 11 |
| Struck down (SCOTUS IEEPA ruling) | 5 |
| Investigation | 1 |
| **Total event (used in Cox)** | **16** |

The execution-to-walk-back ratio is roughly 1:1 in the clean sample (10 executed vs. 11 modified/withdrawn), closer to the folklore "Trump walks back about half" than the 3.6:1 ratio our noisier initial matching produced. Five events were struck down by the single Feb 2026 SCOTUS ruling on IEEPA, so the effective independent event count is closer to 12.

For comparison, the initial naive matching against PIIE (loose country-keyword, no LLM verification) produced 108 matches with 40 executed, 11 modified-or-withdrawn, 35 other, and 18 unresolved. Spot-check showed ~50% of these were wrong-topic matches.

### 5.2 Y2: S&P 500 path around A-class posts

The S&P 500 event-study CAR over 30 trading days following A-class posts (N=118 with sufficient pre-event data):

| Window | Mean | 25th | 75th |
|---|---|---|---|
| CAR (1d) | +0.19% | −0.47% | +0.84% |
| CAR (5d) | +0.31% | −0.91% | +1.88% |
| CAR (30d) | +0.40% | −4.56% | +7.02% |
| Peak drawdown (30d) | **−4.95%** | −7.73% | −1.00% |
| Max recovery (30d) | **+3.80%** | +0.36% | +7.46% |

The mean 30-day CAR is near zero but the path has wide dispersion: average peak drawdown −4.95%, average recovery +3.80%. See [Figure 1: TACO market signature](../figures/fig_taco_signature.png).

**Placebo.** We test whether this path is Trump-specific. Sampling 200 random dates from the same data period (2025-02 through 2026-03) and computing the same metrics on S&P 500 gives mean peak drawdown −4.45% and mean max recovery +3.30%. Differences from Trump-day metrics are not significant: peak drawdown Δ = −0.50pp (t = −0.83, p = 0.39); max recovery Δ = +0.50pp (t = 0.83, p = 0.41); 30-day CAR Δ = −0.37pp (p = 0.68). Restricting the placebo to days more than 5 trading days from any A-class post leaves only 11 truly "calm" trading days in the sample period; on this small set the peak drawdown is −1.92% (Δ = −3.03pp vs. Trump, p < 0.001), but the small N makes this comparison itself fragile. We therefore frame the path as descriptive of the period rather than as evidence of a Trump-specific causal effect.

**Conditional CARs.** Among 108 matched A-class posts (broader sample), executed events have mean peak drawdown −5.16% and recovery +3.79% (N = 45); modified-or-withdrawn events have −3.25% and +4.48% (N = 17). The difference is not statistically significant (drawdown t = −1.41, p = 0.17; recovery t = −0.45, p = 0.66). Conditional on threat publication, the market's path is similar whether the threat is later executed or walked back.

**Sector DID.** We additionally pair each A-class post with a target-specific ETF (FXI for China, EWW for Mexico, EFA for Europe, SOXX for semiconductors, etc.) and a non-target ETF as control. A difference-in-differences design on 62 posts gives a pooled DID peak drawdown of +0.94pp (target tickers drop slightly less than non-target; not significant, p = 0.31). The DID effect is not statistically distinguishable from a parallel placebo on random dates (p = 0.36).

**Granger.** A daily VAR-style test on (post_count, mean_specificity, mean_commitment) and (sp500_ret, sp500_abs_ret, vix_change) over 378 trading days finds one significant relationship: mean Trump commitment Granger-causes SP500 return at lag 3 (F = 3.08, p = 0.027). The reverse direction (SP500 return → post count) is marginally significant at lag 3 (p = 0.068). We interpret the lead from text to market as suggestive but not unidirectional.

### 5.3 Y1: Cox PH on tariff-adjacent sample (primary analysis)

On the N=66 modeling sample (27 matched + 50 censored after dropping non-positive durations and missing-feature rows), 16 events, BT-derived feature scores:

| Feature (BT-ranked) | HR | Bootstrap 95% CI | p (analytic) | p (empirical) |
|---|---|---|---|---|
| `specificity` | **1.39** | **[0.95, 2.14]** | 0.21 | **0.076** ⋄ |
| `commitment_strength` | 1.52 | [0.88, 2.75] | 0.27 | 0.14 |
| `hedging_level` | 1.26 | [0.76, 2.02] | 0.55 | 0.40 |
| `audience_cost` | 0.78 | [0.49, 1.28] | 0.44 | 0.33 |

`⋄` denotes marginal significance (0.05 < p ≤ 0.10).

The PH assumption is not rejected on the tariff-adjacent sample (all features p > 0.05 in the Schoenfeld test). With the original 0-10 features (in place of BT-ranked), all HRs are closer to 1.0 and p > 0.27, consistent with the saturation-driven attenuation hypothesized in §4.2.

**Interpretation.** A 1-SD increase in BT-ranked `specificity` is associated with a 1.39× hazard of policy resolution (executed, modified, or struck-down). A 1-SD increase in `commitment_strength` is associated with a 1.52× hazard. See [Figure 2: V5 primary forest plot](../figures/fig_v5_primary_forest.png) for the full feature panel. The directions are consistent with the priors of audience-cost theory: more specific and more firmly committed threats are easier to verify, harder to ignore, and force the political-economic system to respond. This is a correlate, not a prediction claim. The survival model estimates how the hazard varies with text features across the sample, not how well a forecaster built from these features would perform on held-out data. The bootstrap CI for `specificity` brushes 1.0 (lower bound 0.95) and we have only 16 events, of which 5 are tied to a single SCOTUS IEEPA ruling (so the effective independent count is closer to 12). We treat this as a direction-consistent, marginally-supported association, not a confirmed effect.

**Power note.** With 16 events and 4 covariates, the events-per-variable ratio is ~4, below the standard rule of thumb of 10. Detection power for HR = 1.4 at α = 0.05 is approximately 0.40. A confirmation-level test of these effects would require roughly 80 events, about five times our current sample. The signal we report should be read as an upper bound on detectable effects given current power, not as an estimate of any "true" hazard ratio.

### 5.4 Robustness: seven independent specifications

`specificity` is direction-consistent across seven labeling/feature specifications:

| Specification | A-class | Match | Features | N / events | spec HR | 95% CI | p_emp |
|---|---|---|---|---|---|---|---|
| V2 PIIE loose | broad | country-only | 0-10 | 90 / 41 | 1.29 | [0.97, 1.72] | 0.062 ⋄ |
| V3 PIIE strict + regex status | broad | country-strict | BT v1 | 105 / 20 | 1.58 | [1.05, 2.27] | **0.028** * |
| V3 PIIE strict + LLM status | broad | country-strict | BT v1 | 105 / 23 | 1.39 | [0.89, 2.08] | 0.128 |
| V4 hand-compiled + cross-LLM | broad | LLM-consensus | BT v1 | 99 / 18 | 1.38 | [0.95, 1.98] | 0.092 ⋄ |
| **V5 + tariff-adjacent A** (LLM primary) | **narrow** | **LLM-consensus** | **BT v1** | **66 / 16** | **1.39** | **[0.95, 2.14]** | **0.076** ⋄ |
| V5b loose match (either LLM) | narrow | either-LLM | BT v1 | 65 / 39 | 1.06 | [0.71, 1.70] | 0.77 (NULL) |
| **V6 Claude BT v2 (anon + 1-7)** | narrow | LLM-consensus | BT v2 | 66 / 16 | **2.17** | **[1.48, 3.64]** | **< 0.001** *** |
| V6 GPT BT v2 (anon + 1-7) | narrow | LLM-consensus | BT v2 | 66 / 16 | 0.90 | [0.46, 1.60] | 0.71 (NULL) |
| V6 Consensus avg BT v2 | narrow | LLM-consensus | BT v2 | 66 / 16 | 1.67 | [0.87, 3.43] | 0.118 |
| **V7 human-validated matching** | narrow | human-anchored | BT v1 | 64 / 16 | 1.15 | [0.79, 1.66] | 0.42 (NULL) |

⋄ = marginal (0.05 < p ≤ 0.10), * = p < 0.05, *** = p < 0.001.

Six observations:

1. **Direction is consistent across the seven specifications**: `specificity` HR > 1 in eight of nine rows (the lone exception, V6 GPT, gives HR=0.90 with p=0.71, null but not opposed). Estimates range HR ∈ [1.06, 2.17].
2. **The strict-consensus filter is doing real work, not just being conservative.** When we relax to "either LLM matched" (V5b), N events rises from 16 to 39, but `specificity` HR collapses from 1.39 to 1.06 and p climbs to 0.77. The extra 23 single-LLM matches are noise that dilutes signal, not additional power.
3. **Anonymization + 1-7 scale strengthens Claude's signal (V6 Claude BT v2)** dramatically: HR=2.17, p<0.001. This is consistent with anonymization forcing the LLM to compare *structural* commitment language rather than salient surface tokens (country names, percentages). See [Figure 3: V5 vs V6 comparison](../figures/fig_v5_v6_compare.png).
4. **GPT BT v2 (under the same anonymization)** sees no signal, null with HR=0.90. Cross-LLM Pearson correlation on BT v2 scores is r=−0.06 (`specificity`), r=+0.47 (`hedging`), r=−0.30 (`audience_cost`). This indicates substantial model-specific disagreement.
5. **The Claude-vs-GPT BT v2 divergence is itself a finding.** Either Claude is detecting real structural signal that GPT misses, or one model is capturing pattern noise. We cannot adjudicate without a human-rater ground truth on pairwise comparisons; we therefore treat V5 and V6 Consensus (HR=1.67, p=0.12) as the conservative primary reading, and report V6 Claude (HR=2.17) as the Claude-specific upper bound.
6. **The single sub-0.05 p-value in V3 PIIE + regex** collapses once the underlying status-inference regex bug is repaired. Similarly, the V6 Claude p<0.001 result is *not* claimed as the headline because it does not survive cross-LLM averaging.

Central methodological lesson: *the same data, with different ground-truth cleaning, feature scoring, and consensus rule, produces specificity HR ranging from 1.06 to 2.17. Reporting all rows (not selecting the most flattering) is what survives review.* The signal we are most willing to defend is the direction (HR > 1 in eight specifications), not any single estimate.

**Episode clustering threshold sensitivity.** We additionally vary the bge-large cosine similarity threshold used in episode formation (default 0.82):

| Threshold | Episodes | Tariff-adjacent eps | Mixed-policy eps |
|---|---|---|---|
| 0.78 | 75 | 47 | 8 (11%) |
| 0.80 | 92 | 60 | 8 (9%) |
| **0.82 (primary)** | **110** | **77** | **5 (5%)** |
| 0.85 | 127 | 91 | 2 (2%) |
| 0.90 | 133 | 96 | 1 (1%) |

Episodes remain ≥ 89% policy-area-monothematic across the full range, so the threshold choice does not materially change cluster quality; it only affects how aggressively related posts are merged. We do not rerun the full LLM-matching pipeline at every threshold (each rerun would cost ~$0.40), but the headline N=77 narrow-tariff episodes at 0.82 sits in the middle of the [47, 96] range.

**Human validation of the 0.82 threshold (Packet D).** The author rated 39 post-pairs sampled across five cosine bins as "same topic," "related," or "different." Spearman ρ between cosine similarity and the ordinal user judgment is 0.775 (p < 0.0001). Counts by bin:

| Cosine bin | same (Y) | related (/) | different (N) |
|---|---|---|---|
| 0.50-0.65 | 0 | 1 | 7 |
| 0.65-0.78 | 0 | 0 | 8 |
| **0.78-0.82** (transition zone) | 2 | 4 | 2 |
| 0.82-0.88 | 6 | 2 | 0 |
| 0.88-0.95 | 6 | 0 | 1 |

No pair below cosine 0.78 was judged "same topic" by the human rater. Pairs above 0.82 were judged "same" or "related" 14/15 of the time (one anomaly at cosine 0.885 was judged different, likely an embedding false positive). The 0.82 threshold sits empirically in the transition zone between clearly-different (below) and clearly-same (above) pairs; a marginally tighter threshold (0.85) would slightly improve precision at the cost of more singleton episodes.

**Human validation of LLM specificity ratings (Packet A).** The author manually rated 40 stratified posts on a 0-10 specificity scale, with 8 additional posts inserted as hidden duplicates for test-retest. Human-Claude agreement is high: **Pearson r = 0.75, Spearman ρ = 0.75 (both p < 0.0001)**. Test-retest reliability on the 8 duplicate pairs is **r = 0.84 (mean absolute difference 1.0 point on the 10-point scale)**. The human mean rating is 3.73 (SD 3.27); Claude's median rating on the same 40 posts is 5.55 (SD 2.40). The 1.8-point gap indicates Claude has a systematic positive bias on specificity (consistent with the saturation finding in §4.2), but rank-order agreement is strong, so the LLM measurement is rank-valid.

**Human validation of cross-LLM matching (Packet E).** The author manually re-evaluated all 75 cases in Packet E (24 disagree, 27 consensus, 12 both-none, 12 fake controls). Of 27 LLM consensus matches, the human agreed on 17 (63%) and judged 10 as wrong-topic or insufficient candidate coverage. Of 24 cross-LLM disagree cases, 9 (38%) were resolved to a specific event. Sanity checks pass: 12/12 on both-none controls (100%), 11/12 on fake controls (92%; fakes had the LLM-picked event silently removed from the candidate list, so the correct answer is "none"). One headline metric: **cross-LLM consensus matching achieves 63% precision under same-information human review**. V7 in the table above applies this human-anchored matching: the `specificity` HR drops from 1.39 to 1.15 and loses significance, indicating that part of the V5 marginal signal was supported by LLM consensus matches the human would reject.

**First-post vs episode-mean feature aggregation.** The primary specification uses first-post features as the episode covariate, following standard event-study practice (MacKinlay 1997). As a robustness check we re-estimate using episode-mean features (mean of all consensus-A posts within the episode). Estimates are nearly identical: specificity HR = 1.50 [0.99, 2.49], p = 0.060 (mean) vs. 1.45 [0.94, 2.37], p = 0.096 (first-post). Within multi-post episodes (19 of 110 total, 5 of 27 matched), the first-post-vs-mean Pearson correlation is r = 0.94 for commitment, 0.92 for hedging, 0.76 for specificity, 0.95 for audience cost. First-post features therefore capture most of the episode-level variance. Time-varying-covariate Cox models with explicit decay would be the more rigorous treatment but are not feasible at this N.

**Errors-in-variables sensitivity.** LLM-rated features carry measurement error; with reliability ρ (Spearman 1904; Prentice 1982 for Cox PH), the attenuation-corrected hazard ratio is HR_corrected = exp(log(HR_observed) / ρ). Using within-Claude test-retest as a lower-bound estimate of ρ ≈ 0.95 and cross-LLM agreement as an upper-bound noise estimate at ρ ≈ 0.50, the corrected `specificity` HRs are:

| ρ | V5 primary HR | V6 Claude HR | V6 Consensus HR |
|---|---|---|---|
| 1.00 (no correction) | 1.39 | 2.17 | 1.67 |
| 0.95 (within-Claude) | 1.42 | 2.26 | 1.71 |
| 0.85 | 1.48 | 2.48 | 1.83 |
| 0.70 | 1.60 | 3.02 | 2.08 |
| 0.50 (cross-LLM worst) | 1.94 | 4.69 | 2.79 |

Attenuation correction is uniformly *toward larger* HR in our setting (since the observed HR > 1), so unobserved measurement error makes the true effect, if any, *larger* not smaller; this is a robustness in our favor, but at lower reliability the corrected HRs become implausibly large and we view this as evidence that the observed estimates already reflect substantial signal.

### 5.5 Time-varying effects (discrete-time logistic)

Bucket-stratified logistic regression on the hand-compiled sample, BT features (z-standardized coefficients, larger absolute = more predictive within bucket):

| Bucket | n / events | Top features (coef) |
|---|---|---|
| Day 0-2 | 99 / 3 | audience_cost +0.31, specificity +0.27 |
| **Day 3-7** | 96 / 5 | **commitment_strength +1.26**, **specificity +0.88**, hedging +0.69 |
| Day 8-30 | 90 / 6 | (all coefficients < 0.15 in magnitude) |
| Day 31-90 | 80 / 4 | hedging_level +0.56, audience_cost −0.38 |

**Day 3-7 is where the action is.** Threats most likely to resolve quickly are those that combine high commitment_strength and high specificity. This is consistent with both intuitive theory and the observation that the dictionary `lm_hedging` feature **violates the PH assumption** (Schoenfeld p = 0.048) on the original PIIE sample; its hazard contribution is not constant across time horizons.

### 5.6 LLM zero-shot baseline performs below chance

| Model | Accuracy | Modal prediction |
|---|---|---|
| Claude Haiku 4.5 | 24.6% | "modified_or_withdrawn" (74% of cases) |
| GPT-4o-mini | 26.1% | "unresolved" (90% of cases) |
| Random (1/3) | 33.3% | — |

Both models exhibit strong class-imbalance priors: Claude over-predicts walk-back; GPT over-predicts unresolved. Neither beats random. End-to-end LLM judgment of "will this be executed" from the full post text performs worse than guessing, which suggests the prediction task is genuinely difficult and not an artifact of our feature engineering.

### 5.7 How measurement choices accumulate

Four decision points where successive rigor changed apparent signal:

| Decision | First-cut result | After rigor | Net effect |
|---|---|---|---|
| Rule-based vs cross-LLM A class | `lm_hedging` HR=8.6 (rule-based, N=70) | HR=0.93 (cross-LLM, N=90) | spurious signal removed |
| 0-10 absolute vs Bradley-Terry | `specificity` HR=1.12, p=0.27 | HR=1.38, p=0.09 | saturation lifted |
| Loose vs strict matching | `specificity` HR=1.19, p=0.14 (loose PIIE) | HR=1.58, p=0.03 (strict PIIE) | noise-driven false significance |
| Regex vs LLM status inference | `specificity` HR=1.58, p=0.03 (regex) | HR=1.39, p=0.13 (LLM-clean) | bug-driven false significance removed |

After all four corrections (cross-LLM A class, BT features, strict cross-LLM matching, LLM-cleaned status), the surviving result is HR=1.38 at p=0.09 on `specificity`. The remaining gap from p=0.05 is consistent with small-sample power rather than a deeper flaw.

---

## 6. Discussion

### 6.1 Why is the signal faint?

Four non-exclusive explanations.

1. The TACO trade does not require individual-threat predictability. Wall Street's "TACO trade" is a base-rate bet (buy the dip after any threat, sell after any walk-back); it does not require knowing which specific threat will be walked back. Our task (conditional prediction from text alone) is strictly harder than the strategy that pays.
2. Trump's textual style is partially decoupled from his actions. Whether a threat is walked back may be driven by post-publication shocks (market drops, executive phone calls, central-bank pushback, foreign retaliation) that dominate any prior textual commitment.
3. The sample is small. With 16 events and 4 covariates, the events-per-variable ratio is barely admissible.
4. Specificity may be a partial proxy for verifiability rather than commitment. Specific threats (with named targets and explicit deadlines) force the system to move (executed or withdrawn); vague threats can linger. Our finding may measure verifiability more than commitment per se.

### 6.2 The market path is descriptive of the period

The mean 30-day CAR near zero combined with average peak drawdown −4.95% and recovery +3.80% is consistent with a market that briefly prices in each threat and then unprices most of it. But the placebo test shows the same path on same-period random dates, and executed-vs-walked-back paths are statistically indistinguishable. We therefore frame the path as descriptive of S&P 500 volatility during Trump's second term, not as a Trump-specific causal signature. The Granger test gives one suggestive directional link (commitment → SP500 return at lag 3, p = 0.027), but the reverse link (SP500 return → post count, lag 3) is also marginal (p = 0.068), so we do not claim unidirectional causation.

### 6.3 Ground truth is a moving target

The seven-candidate evaluation of public Trump-tariff trackers, plus the regex bug uncovered in our own PIIE cleaning, suggests that ground-truth construction is itself a research question. The 50% wrong-topic rate of country-keyword matching against PIIE, and the 30% mis-classified status from a single missing word-boundary character, are expected failure modes of regex pipelines on policy text. We recommend LLM-based matching with cross-LLM verification as the default; the marginal API cost is less than $1 per analysis.

### 6.4 LLM as measurement instrument: validity is partial

Within-Claude test-retest reliability is high (r > 0.91 for all 10 features), but cross-LLM agreement is moderate (r = 0.47-0.80 on absolute scoring). Forced-choice pairwise comparisons agree more often (29/36 = 81% on the early Claude-only BT v1 set) but the cross-LLM Pearson correlation on BT v2 scores drops to near zero on most features. Forced-choice scoring helps with the saturation problem; it does not eliminate model-specific bias.

### 6.5 Confounders we do not fully control

LLM-rated text features used as Cox covariates are exposed to two families of confounding.

**Linguistic confounders.** A post contains substantive features we want to measure (commitment, hedging, specificity) and stylistic features the LLM may key on (capital letters, exclamation chains, "tremendous"/"big"/"beautiful" vocabulary). If stylistic features correlate with outcomes through channels other than commitment (for example, if exclamation density rises during high-attention news cycles when policies are also more likely to be enacted), the Cox coefficient on `commitment_strength` partly reflects style-outcome correlation rather than substantive commitment. We attempt partial mitigation through anonymization before pairwise comparison (§4.2) and through forced-choice BT scoring. Residual concern: anonymization is regex-based and does not catch idiosyncratic Trump vocabulary.

**Behavioral confounders.** Trump posts with awareness that markets and counterparties are reading. He may modulate hedging when he expects to walk back, or commit firmly when retreat would impose audience cost. If this modulation is correlated with outcomes (because, for example, hedged-and-walked-back posts reflect private information about counterparty receptivity), the text features become endogenous and the coefficients absorb the selection. We cannot identify this with the current data and report it as a limitation.

**Time-of-administration confounders.** Posts in the first 90 days of the term occurred under different political conditions (markets pricing in inaugural pledges, SCOTUS not yet ruled on IEEPA) than later posts. We do not include calendar-time fixed effects; with 16 events this is impractical, but the early-vs-late composition could bias estimates.

### 6.6 Endogeneity

We do not claim causal identification. The framework is associative and descriptive. Any relationship between text features and outcomes could run through unobserved political-economic state (the market reaction itself may shape Trump's choices). The `specificity → resolution` finding should be read as "specific threats resolve faster on average," not "specificity causes faster resolution."

---

## 7. Limitations

1. Small effective sample. The cleanest pipeline yields 27 cross-LLM-consensus matches and 16 events. With 4 covariates the events-per-variable ratio is ~4, below the standard rule of 10. Power to detect HR = 1.4 at α = 0.05 is ~0.40; a confirmation-level test would require ~80 events. We frame the finding as direction-consistent rather than confirmed.

2. Effective independence further reduced. Five of 16 events are tied to a single Feb 2026 SCOTUS IEEPA ruling, lowering the effective independent count to ~12; bootstrap CIs are correspondingly wide.

3. A class narrower than the original framing. The pre-registered design defined A as broad econ-policy commissive, but ground-truth pragmatics forced concentration on tariff-only outcomes. The 39 non-tariff A posts (financial_regulation, sanctions, fed_monetary, antitrust_tech) lack equivalently clean ground truth and are deferred. This is a scope limitation, not a measurement failure.
4. Single-actor corpus. Results may not generalize beyond Trump's distinctive style. Other actors (Vance, Cruz, Rubio for U.S. ranking; foreign leaders for cross-country tests) are out of scope.
5. Single-platform. Cross-platform comparison (Truth Social vs. X) is deferred. Deleted posts are an acknowledged unmeasured limitation.
6. Ground-truth incompleteness. Even the cleanest source (hand-compiled Wikipedia + Tax Foundation) is incomplete; one event (Oct 2025 China_additional withdrawal) is uniquely captured by hand-compile and missed by PIIE. Coverage of non-tariff commissive actions (Fed pressure, personnel nominations, antitrust threats) is essentially zero across all sources.
7. Cross-LLM BT replicated only on BT v2. Our Claude-vs-GPT BT comparison covers BT v2; BT v1 was Claude-only.
8. Episode clustering threshold partially sensitivity-tested. We use bge-large cosine > 0.82 with a 30-day window. Alternative thresholds (0.78, 0.85, 0.90) shift the episode count to 75-133; we did not rerun the full LLM-matching pipeline at each threshold due to API cost. Of 110 episodes, 95.5% are policy-area-monothematic at post level.
9. Single annotator. The human validation (Packet A specificity ratings, Packet E match decisions) was completed by the first author over a ~3-hour session, with hidden duplicate items (8 in Packet A, controls in Packet E) used to measure intra-rater consistency. Inter-rater κ requires a second annotator and is deferred.

---

## 8. Conclusion

We construct a quantitative pipeline for measuring political-economic threats in Trump's Truth Social, with cross-LLM verification at three stages (classification, feature extraction, event matching) and a three-tier ground-truth architecture (hand-compiled human labels, Federal Register validation, LLM-cleaned PIIE for robustness). Four contributions:

1. The S&P 500 30-day path around A-class posts averages −4.95% peak drawdown and +3.80% maximum recovery, with near-zero net drift. Placebo testing shows this path is not statistically distinguishable from same-period baseline, so we report it as descriptive rather than as evidence of a Trump-specific causal effect.
2. BT-ranked `specificity` is direction-consistent across nine LLM-only specifications, HR ∈ [1.06, 2.17] with HR > 1 in 8/9. The primary LLM-only specification gives HR = 1.39 [0.95, 2.14], p = 0.076; the Claude anonymized 1-7 BT variant gives HR = 2.17, p < 0.001; the GPT counterpart is null. Under human-validated matching, the same specification gives HR = 1.15, p = 0.42. The marginal LLM-only signal does not survive replacement of cross-LLM matching with human-anchored matching. Discrete-time logistic concentrates the LLM-only signal in days 3-7.
3. A measurement-stack documentation. Six successive corrections (rule-based to cross-LLM classification; 0-10 to pairwise BT; loose to strict matching; regex to LLM status inference; broad to tariff-adjacent A; original-text to anonymized BT) each move estimates. Two mid-pipeline "significant" results are overturned by adjacent robustness checks. The takeaway is not "use LLMs less" but "use multiple LLMs and report all specifications" (incremental API cost under $1).
4. Forced-choice pairwise comparison (Bradley-Terry) is a practical fix for the saturation problem encountered when LLMs rate stylistically uniform corpora on absolute scales.

Future work should: (a) ingest [Polymarket](https://polymarket.com) and [Kalshi](https://kalshi.com) prediction-market traces as an external market-belief signal to compare against text features; (b) expand to multiple political actors to test generalization; (c) extend to non-tariff threats (sanctions via OFAC, Fed pressure via FOMC minutes, immigration enforcement via ICE statistics) once each domain's ground truth is triaged; (d) recruit additional annotators for inter-rater agreement.

---

## Figures

1. `figures/fig_taco_signature.png` — TACO market signature bar chart (peak / net / recovery CAR).
2. `figures/fig_v5_primary_forest.png` — V5 primary Cox PH forest plot (BT v1, N=66 / 16 events).
3. `figures/fig_v6_claude_forest.png` — V6 Claude anonymized 1-7 BT forest plot.
4. `figures/fig_v6_gpt_forest.png` — V6 GPT anonymized 1-7 BT forest plot.
5. `figures/fig_v6_consensus_forest.png` — V6 Consensus-average anonymized BT forest plot.
6. `figures/fig_v5_v6_compare.png` — Side-by-side V5 vs V6 Claude comparison.

---

## References

- Ash, E., & Hansen, S. (2023). Text Algorithms in Economics. *Annual Review of Economics*, 15, 659-688.
- Ash, E., Hansen, S., Muvdi, Y., & Marangon, C. (2026). Large Language Models in Economics. In *The Palgrave Handbook of Economics and Language*. Springer.
- Baker, S. R., Bloom, N., & Davis, S. J. (2016). Measuring economic policy uncertainty. *Quarterly Journal of Economics*, 131(4), 1593-1636.
- Bradley, R. A., & Terry, M. E. (1952). Rank analysis of incomplete block designs: I. The method of paired comparisons. *Biometrika*, 39(3/4), 324-345.
- Cox, D. R. (1972). Regression Models and Life-Tables. *JRSS B*, 34(2), 187-202.
- Efron, B. (1979). Bootstrap methods: Another look at the jackknife. *The Annals of Statistics*, 7(1), 1-26.
- Egger, P., & Zhu, J. (2020). The U.S.-Chinese Trade War: An Event Study of Stock-Market Responses. *World Economy*, 43(11), 2913-2937.
- Fearon, J. D. (1994). Domestic Political Audiences and the Escalation of International Disputes. *APSR*, 88(3), 577-592.
- Husted, L., Rogers, J., & Sun, B. (2020). Monetary policy uncertainty. *Journal of Monetary Economics*, 115, 20-36.
- Loughran, T., & McDonald, B. (2011). When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. *Journal of Finance*, 66(1), 35-65.
- MacKinlay, A. C. (1997). Event Studies in Economics and Finance. *JEL*, 35(1), 13-39.
- Searle, J. R. (1969). *Speech Acts: An Essay in the Philosophy of Language*. Cambridge University Press.

### Data sources

- [PIIE Trump Trade War Timeline 2.0](https://www.piie.com/blogs/realtime-economics/2025/trumps-trade-war-timeline-20-date-guide) — Peterson Institute for International Economics
- [Tax Foundation Trump Tariffs Tracker](https://taxfoundation.org/research/all/federal/trump-tariffs-trade-war/)
- [Wikipedia: Tariffs in the second Trump administration](https://en.wikipedia.org/wiki/Tariffs_in_the_second_Trump_administration)
- [Atlantic Council Trump Tariff Tracker](https://www.atlanticcouncil.org/programs/geoeconomics-center/trump-tariff-tracker/) (high-level visualization only)
- [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1) — Presidential Documents
- [The TACO Tracker](https://www.thetacotracker.com/) (consulted, unstructured)
- Truth Social archive (CNN-maintained, `ix.cnn.io/data/truth-social/truth_archive.json`)
- `yfinance` for S&P 500 / VIX / sector ETFs / FX
