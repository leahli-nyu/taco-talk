# Next 3 Concrete Actions

## ✅ Done (by Claude)
- Project directory structure
- `requirements.txt`
- Scraper skeletons:
  - `src/scrape_market.py` — yfinance for S&P, sector ETFs, currencies, oil, gold
  - `src/scrape_federal_register.py` — FR API for tariff EOs/notices
  - `src/fetch_trump_posts.py` — pulls Twitter archive CSV (Truth Social needs manual download)
  - `src/filter_tariff_threats.py` — regex pre-filter to narrow to tariff candidates
- `notebooks/01_data_overview.ipynb.py` — first inspection cells

## 🧑‍🎨 What needs YOU (in this order, ~30 min total)

### Action 1 — Install env (5 min)
```bash
cd /Users/leahli/Documents/26Spring-TextasData/final_proj
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Action 2 — Run the three scrapers (15 min, mostly wait)
```bash
python src/fetch_trump_posts.py
python src/scrape_market.py
python src/scrape_federal_register.py
python src/filter_tariff_threats.py
```

If `fetch_trump_posts.py` complains Truth Social is missing, that's OK — it still
processes the Twitter archive. We can add Truth Social later by downloading
from Kaggle/GitHub manually.

### Action 3 — Eyeball ~20 random candidate threats (10 min)
Open `notebooks/01_data_overview.ipynb.py` in VS Code, run the cells, and
read 20 random candidates. Tell me:
- Do they look like real tariff threats?
- What false positives slipped through?
- Anything obviously missing?

That's all. Once you've done these 3, I will:
- Refine the filter based on your feedback
- Write the LLM first-pass labeler
- Build the feature extractor

You don't need to think about features, models, paper, or app yet.
