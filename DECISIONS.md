# Final Project Locked Decisions (2026-05-11)

## Scope
- **Time range**: Trump 2nd term only (2025-01-20 onwards)
- **Platform**: Truth Social ONLY for v1 (CNN archive, 6,228 originals)
- **X data**: deferred to v2 / robustness section (after main analysis is done)
- **Main sample**: A class (econ-impacting policy threats)
- **B/C classes**: control variables (overlap/clustering)

## Research Question (升级版)
Trump 关税威胁的文本特征能否预测：
- (a) 政策执行的时间分布
- (b) 短期市场反应
- (c) 市场反应与真实政策之间的偏差方向（过度恐慌 / 过度麻木）？
- 这些偏差是否随时间衰减？

## A/B/C Definition (Speech Act Theory based)
- **A**: Commissive + government-executable + economic transmission (tariff, trade deals, sanctions, Fed pressure, currency, commodity ban)
- **B**: Commissive + government-executable + non-economic primary impact (immigration, military, judicial)
- **C**: Non-commissive (complaint, boast, retweet commentary, endorsement, conditional/hypothetical)

## Y1 Model
- **Main**: Cox proportional hazards (lifelines package)
- **Backup**: Discrete-time logistic on time buckets
- **Required baseline**: Claude Haiku zero-shot prompt

## Y2 Framework
- Event study + cumulative abnormal returns (CAR)
- Pre-event 60-day window = market baseline
- Event windows: 30min / 1d / 5d / 30d + data-driven repair-time window
- EO announcements as "definite execution" samples (not benchmark)
- **No "100% execution" benchmark needed** — use pre-event baseline per threat

## Index Basket
- **Required**: S&P 500, VIX
- **Target-specific** (when applicable): FXI/EWW/EFA/SOXX/XLB/etc.
- Bonus: DXY, target-country currency pairs

## Features (12 baseline)
1. Deontic 情态强度 (custom dict: will/going to/shall/should/might/may)
2. Temporal specificity (deadline phrase parsing)
3. Conditional structure dummy (if/unless/until)
4. Target NER count + type
5. % / $ number count
6. All-caps ratio
7. NRC affect words count
8. L-M Hedging score
9. L-M Uncertainty score
10. repeat_count_7d (same-topic recurrence)
11. is_first_mention dummy
12. neighbor_event_count (overlap control)

## Confound Control
- **Long window (30d CAR)**: include `neighbor_event_count` as control variable
- **Short window (30min)**: naturally minimal overlap

## Ground truth source
- **Y1 outcome**: PIIE Trump Tariff Tracker
- **Y2 outcome**: yfinance market data (deep liquid)
- **Polymarket / Kalshi**: auxiliary if time permits

## Deferred
- Bitcoin (low priority)
- Polymarket / Kalshi (time-permitting)
- Cross-platform X comparison (v2)
- White House transcripts (out of scope)
- Deleted posts (acknowledged limitation)

## Citation Plan
**Must-cite** (cite or be questioned for not citing):
- Baker, Bloom & Davis (2016) — policy uncertainty + market reaction framework
- Ash & Hansen (2023) "Text Algorithms in Economics" — econ-NLP method survey
- Ash, Hansen, Muvdi & Marangon (2026) "LLMs in Economics" — LLM-as-tool framework
- MacKinlay (1997) — event study methodology

**Conditional-cite**:
- Arold, Ash, MacLeod & Naidu (2025) "Worker Rights" — only if deontic modal analysis is featured
- Widmer, Abed Meraim, Galletta & Ash (2025) "Media Slant" — only if discriminative classifier method is featured

**Theoretical motivation** (cite to motivate features):
- Fearon (1994) "Audience Costs"
- Searle (1969) Speech Acts (for A/B/C framework)
