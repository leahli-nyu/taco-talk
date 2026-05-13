# Deploy this web app to a public URL

The `app/` directory is a static site — no build step, no server. Three ways to host it.

## Option 1: GitHub Pages (recommended, free, ~3 minutes)

```bash
# from final_proj root
cd /Users/leahli/Documents/26Spring-TextasData/final_proj

git init
git add app/ src/ data/raw/*.json data/raw/*.csv data/processed/*.parquet paper/ MORNING_REPORT.md DECISIONS.md README.md requirements.txt
# Note: .env is gitignored

git commit -m "Initial commit"

# Create new repo on github.com (e.g., "tariff-talk-tracker"), then:
git remote add origin git@github.com:<your-username>/<repo-name>.git
git branch -M main
git push -u origin main

# In GitHub repo settings:
#   Settings → Pages → Source: "Deploy from a branch"
#   Branch: main / folder: /app
#   Save.
# Wait ~1 minute. Site live at:
#   https://<your-username>.github.io/<repo-name>/
```

## Option 2: Vercel (also free, even faster ~1 minute)

```bash
npm i -g vercel
cd app/
vercel --prod
# follow prompts; pick "static site"
```

URL gets printed at the end.

## Option 3: Local preview (for testing)

```bash
cd /Users/leahli/Documents/26Spring-TextasData/final_proj/app
python3 -m http.server 8000
# open http://localhost:8000
```

## When you update the data

After running `src/build_app_data.py`, the file `app/data.json` is regenerated.
For GitHub Pages: just commit + push. For Vercel: re-run `vercel --prod`.

## Customizing

- **Colors**: edit CSS variables in `styles.css` at the top (`:root { ... }`)
- **Sections**: edit `index.html`
- **Logic**: edit `app.js`

## What loads

- `index.html` — layout
- `styles.css` — TACO Tracker-inspired theme
- `app.js` — fetches `data.json`, renders cards + filters
- `data.json` — generated from your analysis pipeline
