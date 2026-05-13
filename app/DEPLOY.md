# Deploying TACO Talk to GitHub Pages

5-minute publish flow. No build step.

## Option 1: GitHub Pages from `/app` (simplest)

```bash
# from project root
cd /Users/leahli/Documents/26Spring-TextasData/final_proj

git init
git add app/ paper/draft.md README.md DECISIONS.md requirements.txt src/ data/raw/tariff_timeline_ground_truth.json
git commit -m "Final project · TACO Talk"

# create GitHub repo
gh repo create taco-talk --public --source=. --remote=origin --push

# enable Pages from /app
gh api repos/$USER/taco-talk/pages -X POST \
  -f source[branch]=main -f source[path]=/app
```

Site URL: `https://USERNAME.github.io/taco-talk/`

## Option 2: GitHub UI

1. Create new public repo.
2. Push the code.
3. Settings → Pages → Source: Deploy from branch → Branch `main`, folder `/app` → Save.
4. Wait ~1 min, visit `https://USERNAME.github.io/REPO/`.

## Option 3: Vercel (alternative)

```bash
npm i -g vercel
cd app/
vercel --prod
```

URL printed at end.

## Option 4: Local preview (before publishing)

```bash
cd app && python3 -m http.server 8000
# open http://localhost:8000
```

## Files in `/app/`

- `index.html` — newspaper-style essay
- `styles.css` — newspaper aesthetic with Fraunces serif
- `app.js` — populates "by the numbers" section
- `data.json` / `data.js` — analysis output
- `figures/` — paper figures (copy of `../figures/`)

## Pre-flight checklist

- [ ] Run local preview, verify Fraunces font loads
- [ ] All 6 figures render
- [ ] "By the numbers" section populates 8 stats
- [ ] Mobile responsive (resize browser < 640px)
- [ ] Footer "paper" link points to paper/draft.md
- [ ] Footer "github" link updated to real repo URL
