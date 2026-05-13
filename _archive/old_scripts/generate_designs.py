"""Generate 3 web design directions using Claude Opus 4.7 / Sonnet 4.6.

Each design is output as a single self-contained HTML file with inline CSS + JS,
saved to app/designs/{a,b,c}/index.html.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

ROOT = Path(__file__).resolve().parents[1]

# Load .env
_env = ROOT / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip().strip('"').strip("'")

from anthropic import Anthropic

DATA_JSON = json.load(open(ROOT / "app" / "data.json"))
DATA_SCHEMA_DOC = """
window.__APP_DATA__ shape (already injected globally — do NOT use fetch):

{
  "summary": {
    "n_threats": int,         // ~149 A-class commissive economic threats
    "n_threats_matched": int, // matched to PIIE timeline
    "n_eos": int,             // Federal Register executive orders
    "match_rate": float,      // 0.0-1.0
    "data_through": str,      // "YYYY-MM-DD"
    "n_episodes": int         // policy-episode clusters (~70)
  },
  "outcome_counts": {
    "executed": int, "modified_or_withdrawn": int, "struck_down": int,
    "announced_unresolved": int, "investigation": int, "other": int, "unmatched": int
  },
  "ticker": {
    "avg_car_30d": float,            // mean S&P 500 CAR over 30 trading days, e.g. -0.0012
    "median_anticipation_days": float, // median days from threat to formal event
    "taco_rate": float,              // fraction modified_or_withdrawn
    "execution_rate": float,         // fraction executed
    "avg_peak_drawdown_30d": float,  // mean trough CAR over event window
    "avg_max_recovery_30d": float    // mean peak rebound
  },
  "threats": [  // up to ~149 entries
    {
      "id": str,
      "date": "YYYY-MM-DD HH:MM",
      "text_preview": str,           // first 240 chars of Trump's post
      "target": str|null,            // "China", "Mexico", "EU", etc.
      "y1_outcome": str,             // one of outcome categories above
      "y1_status": str|null,
      "matched_category": str|null,  // PIIE event category
      "matched_date": str|null,
      "car_1d": float|null,          // S&P 1-day cumulative abnormal return (e.g. -0.012 = -1.2%)
      "car_5d": float|null,
      "car_30d": float|null,
      "days_threat_to_event": int|null
    }
  ]
}
"""

PROJECT_CONTEXT = """
PROJECT: "Tariff Talk" — a quantitative analysis of every tariff-relevant Trump
Truth Social post in his second term (Nov 2024 – present). Each post is classified
by speech-act type (commissive vs not), then for actual threats we match each to a
formal policy event in the PIIE Trade War Timeline, and measure market reactions
in S&P 500 over various windows.

KEY FINDINGS to feature:
- ~26% of threats end in TACO (modified/withdrawn) — confirming the "Trump Always
  Chickens Out" Wall Street folklore
- ~25% are executed as announced
- Median lead time from threat to formal event is ~4 days
- Average path: peak drawdown -4.5%, max recovery +3.5% over 30 days
  (net near zero, but path swings wide)
- Cox PH model found Loughran-McDonald hedging language predicts faster resolution
  (HR 8.6, p=0.003) — controversial preliminary finding

DESIGN BRIEF:
- Must use the data structure above (`window.__APP_DATA__`)
- Self-contained single HTML file (inline CSS + JS, no external deps except fonts)
- Auto dark/light mode via prefers-color-scheme + manual toggle
- Mobile-responsive
- Strictly NOT a clone of TACO Tracker (https://www.thetacotracker.com/) — that uses
  taco-themed Mexican-food color names (avocado, salsa, corn), Playfair Display
  headings, JetBrains Mono numbers, paper/cream backgrounds, scrolling ticker.
  Your design must look distinctly different in palette, typography, and layout.
- Disclaimer: "Not financial advice" must appear in footer
- Show provenance: NYU DS-GA 1015 final project, attribution to PIIE timeline

You can use Google Fonts via <link> CDN, and Chart.js or D3 via CDN if you want
charts. ECharts is also acceptable. Keep total file under 25,000 tokens — prefer
Chart.js over hand-rolled SVG for size. You don't need to inline all 149 threat
records into the page; the data is already available via window.__APP_DATA__.

OUTPUT FORMAT: a single COMPLETE and FINAL HTML file. Must end with </html>.
Output ONLY the HTML — no preamble, no markdown code fences, no explanation.
Start with <!doctype html>.
"""

DIRECTION_A = """
DIRECTION: "Data-dense professional, with subtle humor"

Inspiration: Financial Times Visual Storytelling, Bloomberg Terminal, The Pudding,
Datawrapper. Heavy on charts and quantitative content. Sparse prose. Every section
should lead with a chart, not text.

Specific requirements:
1. Hero section: NOT a giant headline. Instead, a tight intro paragraph + one
   immediately-visible distinctive chart (e.g., the average CAR trajectory, or
   outcome distribution donut). The chart IS the hero.
2. Multiple chart types throughout: at least 3 distinct visualizations.
   Examples: outcome distribution chart, anticipation-period histogram, scatter
   of threats by features, time series of threat counts by month, sector breakdown.
3. Data tables with sparklines / inline mini-charts.
4. Numbers prominent, tabular monospace, financial colors (red negative / green positive).
5. Subtle humor placement: maybe a single witty caption per chart ("when Trump tweets,
   the market squints"), or a small visual joke (a tiny taco emoji or tortilla pattern
   used VERY sparingly, no more than 2 places in entire page). Otherwise straight-faced.
6. Use Chart.js or ECharts via CDN. Avoid TACO Tracker palette.
7. Suggested fonts: IBM Plex Sans / Inter for body, IBM Plex Mono / JetBrains Mono
   for numbers, no decorative serifs.

You are an aesthetically opinionated FT/Bloomberg-style data designer. Optimize
for information density, not whitespace. Show data first, explain it second.
"""

DIRECTION_B = """
DIRECTION: "Academic / scrollytelling"

Inspiration: distill.pub, Tufte essays, Nicky Case's explorables, NY Times R&D
visual essays. Long-form structure: starts with research question, builds context,
unfolds findings via embedded interactive charts woven into prose. Charts are
in-line illustrations that respond to scrolling.

Specific requirements:
1. Conclusion / TL;DR up front: a clean summary box at top stating the 2-3 key
   findings.
2. Then "Background" section explaining the research question (Trump tariff
   threats → market reactions → TACO pattern).
3. Then a sequential narrative ("Section 1: How we measure threats" → "Section 2:
   What happens after a threat" → "Section 3: When does Trump fold"), each section
   has prose + 1-2 embedded charts.
4. Each chart should ideally have a small interactive element (filter, hover detail,
   toggle to switch view).
5. Sidebar with table of contents (auto-highlights current section on scroll).
6. Citations / references at bottom (PIIE, MacKinlay event study, Loughran-McDonald
   2011, Baker-Bloom-Davis 2016).
7. Typography: prefer high-quality serif for body (Source Serif Pro / Crimson Text
   / Lora), clean sans for headers.
8. Color: muted academic palette — paper white / soft beige in light mode, deep
   warm grey in dark mode. Single accent color (avoid Mexican food palette).
9. Code blocks / equation blocks where math is relevant (Cox PH formula).

You are an academic data-essayist channeling distill.pub. Be thoughtful, precise,
and let the data unfold the argument.
"""

DIRECTION_C = """
DIRECTION: "Q&A interactive explainer"

Inspiration: The Pudding's "how y'all", FiveThirtyEight interactive articles,
Vox Card Stacks. Structured as a series of pointed questions, each answered with
data + a charts. User can click through.

Specific requirements:
1. Hero: a single provocative question on a near-blank canvas, e.g. "Does Trump
   actually follow through?". User clicks/scrolls to "answer".
2. Series of question-answer cards (5-7 questions). Each Q&A occupies a
   distinct visual block. User can navigate via prev/next or scroll.
3. Questions to use (you can rewrite):
   Q1: How many tariff threats has Trump made?
   Q2: How often does the market actually react?
   Q3: How often does Trump follow through?
   Q4: When he backs down, what does the market do?
   Q5: Which kinds of threats are more likely to be TACO'd?
4. Each answer includes 1 chart + 1 short paragraph.
5. Modern conversational tone. Some wit but not over the top.
6. End with "browse the data" — a compact table view of all threats.
7. Layout: full-bleed cards, single-column, generous whitespace per question.
8. Typography: bold display heading per question, regular body, mono for numbers.
9. Color: distinctive palette — try a navy + chartreuse + cream scheme, or deep
   purple + amber. Not Mexican food palette.

You are crafting a guided journalism explainer. Each question is a story beat.
The user feels like they are uncovering a finding, not reading a report.
"""

DESIGNS = [
    {"slug": "a-dashboard",  "model": "claude-opus-4-7",      "brief": DIRECTION_A, "out_dir": "app/designs/a"},
    {"slug": "b-academic",   "model": "claude-opus-4-7",      "brief": DIRECTION_B, "out_dir": "app/designs/b"},
    {"slug": "c-explainer",  "model": "claude-sonnet-4-6",    "brief": DIRECTION_C, "out_dir": "app/designs/c"},
]


def generate_one(design: dict) -> dict:
    client = Anthropic()
    full_prompt = (
        PROJECT_CONTEXT.strip()
        + "\n\n"
        + DATA_SCHEMA_DOC.strip()
        + "\n\n"
        + design["brief"].strip()
        + "\n\nNow output the complete single HTML file:"
    )
    t0 = time.time()
    try:
        # Use streaming for large outputs
        with client.messages.stream(
            model=design["model"],
            max_tokens=32000,
            messages=[{"role": "user", "content": full_prompt}],
        ) as stream:
            chunks = []
            for text in stream.text_stream:
                chunks.append(text)
            html = "".join(chunks)
            # final_message gets usage
            msg = stream.get_final_message()
        # Strip code fences if model added them
        if html.startswith("```"):
            html = html.split("```", 2)[1] if html.count("```") >= 2 else html[3:]
            if html.lstrip().startswith("html"):
                html = html.lstrip()[4:]
        html = html.strip()
        # Save
        out_dir = ROOT / design["out_dir"]
        out_dir.mkdir(parents=True, exist_ok=True)
        out_html = out_dir / "index.html"
        out_html.write_text(html)
        # Also copy data.js so it works standalone
        data_js_src = ROOT / "app" / "data.js"
        if data_js_src.exists():
            (out_dir / "data.js").write_text(data_js_src.read_text())
        return {
            "slug": design["slug"],
            "model": design["model"],
            "status": "ok",
            "html_bytes": len(html),
            "elapsed_s": time.time() - t0,
            "out": str(out_html.relative_to(ROOT)),
            "input_tokens": msg.usage.input_tokens,
            "output_tokens": msg.usage.output_tokens,
        }
    except Exception as e:
        return {
            "slug": design["slug"],
            "model": design["model"],
            "status": "error",
            "err": str(e)[:300],
            "elapsed_s": time.time() - t0,
        }


def main():
    print(f"[start] generating {len(DESIGNS)} designs in parallel", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=len(DESIGNS)) as ex:
        futures = {ex.submit(generate_one, d): d for d in DESIGNS}
        for f in as_completed(futures):
            r = f.result()
            results.append(r)
            print(f"  [{r['slug']}] {r['model']} -> {r['status']} ({r.get('elapsed_s', 0):.1f}s, "
                  f"in={r.get('input_tokens', '?')} out={r.get('output_tokens', '?')})",
                  flush=True)
    # Save summary
    summary_fp = ROOT / "app" / "designs" / "_summary.json"
    summary_fp.parent.mkdir(parents=True, exist_ok=True)
    summary_fp.write_text(json.dumps(results, indent=2))
    print(f"\n[saved] summary -> {summary_fp.relative_to(ROOT)}")

    # Cost estimate
    total_in = sum(r.get("input_tokens", 0) for r in results if r["status"] == "ok")
    total_out = sum(r.get("output_tokens", 0) for r in results if r["status"] == "ok")
    cost_opus_in = total_in * 15 / 1_000_000  # placeholder
    cost_opus_out = total_out * 75 / 1_000_000
    # mixed: 2 opus + 1 sonnet — rough
    print(f"\nTotal tokens: in={total_in:,} out={total_out:,}")


if __name__ == "__main__":
    main()
