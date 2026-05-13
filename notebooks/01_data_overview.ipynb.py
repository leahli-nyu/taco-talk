"""Step-by-step data exploration (run as a notebook).

This is a `.py` you can convert to `.ipynb` with jupytext OR open as cells in VS Code.
Each `# %%` is a cell.
"""

# %% Setup
import pandas as pd
from pathlib import Path
import plotly.express as px
DATA = Path(__file__).resolve().parents[1] / "data"

# %% Load all data
posts = pd.read_parquet(DATA / "raw" / "trump_posts_unified.parquet")
market = pd.read_parquet(DATA / "raw" / "market_daily.parquet")
candidates = pd.read_parquet(DATA / "processed" / "tariff_threat_candidates.parquet")

# %% Quick stats
print("posts", posts.shape, posts.date.min(), posts.date.max())
print("candidates", candidates.shape)
print("market tickers", market.ticker.unique())

# %% Temporal distribution of tariff candidates
candidates["year_month"] = candidates.date.dt.to_period("M").astype(str)
counts = candidates.groupby("year_month").size().reset_index(name="n")
fig = px.bar(counts, x="year_month", y="n",
             title="Tariff threat candidates over time")
fig.show()

# %% Sample 20 random candidates to eyeball quality
sample = candidates.sample(20, random_state=1)[["date", "platform", "text"]]
for _, r in sample.iterrows():
    print(f"\n--- {r.date} [{r.platform}]")
    print(r.text[:300])
