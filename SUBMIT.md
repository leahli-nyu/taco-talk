# Submission checklist · TACO Talk · DS-GA 1015 · Spring 2026

> Verified against the official Course Project Instructions
> (https://eash.cc/projects, exported May 12 2026).

## 📋 Three required deliverables (verbatim from instructions)

> "All final submissions must include:
> - A publicly accessible website (clickable URL)
> - A comprehensive report
> - A replication package containing data, code, and documentation"

| Deliverable | Our file | Status |
|---|---|---|
| 1. Public website (clickable URL) | `app/index.html` → GitHub Pages | ⏳ Ready, needs deploy |
| 2. Comprehensive report | `paper/draft.md` (7,555 words, 8 sections) | ✅ Complete |
| 3. Replication package | `src/` + `data/` + `README.md` + `DECISIONS.md` + `requirements.txt` | ✅ Complete |

## 🎯 Quality standards (verbatim)

> "Because students work with AI assistants, deliverables face higher standards:
> - Research papers should meet publication quality and contribute meaningful research findings
> - Apps must address genuine user needs and include documentation explaining functionality"

Our paper contributes:
- 9-specification robustness analysis (most papers report 1)
- Cross-LLM consensus pipeline + cross-LLM matching
- 3-tier ground-truth architecture
- Human validation on 3 packets (specificity rating, matching, clustering threshold)
- Methodological cautionary tale (regex bug, BT-vs-0-10, Claude-vs-GPT divergence)

Our web app:
- Genuine reader-facing essay (newspaper format)
- Visualizes the 4 key results
- Documented (DEPLOY.md + README.md)

---

## 🚀 Publish web app (5 minutes)

```bash
cd /Users/leahli/Documents/26Spring-TextasData/final_proj

# 1. Init repo + commit everything
git init
git add app/ paper/ src/ data/raw/ figures/ annotation/ \
        README.md DECISIONS.md SUBMIT.md requirements.txt \
        data/processed/cox_*.parquet data/processed/episodes_*.parquet \
        data/processed/all_features.parquet data/processed/consensus_a.parquet \
        data/processed/event_study_v2.parquet data/processed/sector_did_summary.parquet \
        data/processed/granger_results.parquet data/processed/packet_*_user_*.txt \
        data/processed/packet_*_summary.json data/processed/_archive/
git commit -m "Final · TACO Talk · DS-GA 1015 Spring 2026"

# 2. Create GitHub repo
gh repo create taco-talk --public --source=. --remote=origin --push

# 3. Enable Pages from /app
gh api repos/$(gh api user -q .login)/taco-talk/pages -X POST \
  -f source[branch]=main -f source[path]=/app

# 4. Wait ~60 seconds, get URL
echo "Site: https://$(gh api user -q .login).github.io/taco-talk/"
```

**No gh CLI?** Manual:
1. Create public repo on github.com
2. `git push origin main`
3. Settings → Pages → Source: branch `main`, folder `/app` → Save

---

## 📤 Brightspace submission

According to the syllabus, "Due May 12th" → submit on Brightspace.
Items to upload / paste:

1. **Paper** → `paper/draft.md` (as PDF if Brightspace requires it; pandoc command below)
2. **Web URL** → `https://USERNAME.github.io/taco-talk/`
3. **Repo URL** → `https://github.com/USERNAME/taco-talk` (= "replication package")

### Convert paper to PDF if needed

```bash
# Install pandoc if missing
brew install pandoc basictex

# Convert
cd /Users/leahli/Documents/26Spring-TextasData/final_proj
pandoc paper/draft.md -o paper/draft.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Charter" \
  -V monofont="IBM Plex Mono" \
  -V geometry:margin=1in
```

---

## 🧪 30-second pre-submission sanity check

```bash
cd app && python3 -m http.server 8000
# Open http://localhost:8000 — verify:
#   ✓ Title renders in Fraunces serif (not flat)
#   ✓ 6 figures load
#   ✓ "By the numbers" stats populate (8 numbers)
#   ✓ Footer "paper" link works
#   ✓ Mobile view OK (resize browser <640px)
```

---

## 📂 Final repo structure

```
final_proj/                        ← Public repo root
├── README.md                      ← Project overview, headline findings
├── SUBMIT.md                      ← This file
├── DECISIONS.md                   ← Locked research-design decisions
├── requirements.txt
├── paper/
│   └── draft.md                   ← 7,555 words, 8 sections
├── app/                           ← Web app (publishes to Pages)
│   ├── index.html
│   ├── styles.css                 ← Newspaper aesthetic + Fraunces serif
│   ├── app.js
│   ├── data.json / data.js
│   ├── figures/                   ← Copy of paper figures
│   └── DEPLOY.md
├── figures/                       ← 6 paper figures
├── src/                           ← 33 active pipeline scripts
├── annotation/
│   ├── RUBRIC.md
│   ├── README_PACKETS.md
│   ├── packet_A,B,D,E *.md
│   ├── annotation_corpus.json
│   └── *_key.parquet
├── data/
│   ├── raw/                       ← Public source data
│   │   ├── tariff_timeline_ground_truth.json
│   │   ├── federal_register_tariff_eos.json
│   │   ├── Trump's trade war timeline 2.0...csv
│   │   └── market_daily.parquet
│   └── processed/                 ← Pipeline outputs
└── _archive/                      ← Earlier iterations (kept for traceability)
```

---

## 📊 Paper section map (for grader speed)

- §1 Intro + 5 contributions
- §2 Related work
- §3 Data (3-tier ground truth, cross-LLM matching)
- §4 Methods (cross-LLM, BT, Cox + bootstrap, event study, discrete-time logistic)
- §5 Results
  - §5.1 Outcome distribution
  - §5.2 S&P 500 path + placebo + DID + Granger
  - §5.3 Cox primary (V5)
  - §5.4 10 specifications + human validation (Packets A/E/D) + EIV + episode-mean
  - §5.5 Time-varying effects
  - §5.6 LLM zero-shot baseline (below chance)
  - §5.7 Measurement-stack table
- §6 Discussion (6 sub-sections)
- §7 9 limitations
- §8 4-contribution conclusion

**Word count**: 7,555. Reasonable for a "comprehensive report."
