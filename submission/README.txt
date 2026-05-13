TACO Talk · DS-GA 1015 Final Project · Spring 2026
====================================================

This folder contains the 4 submission items.

----------------------------------------------------------------------
1. WEB URL (PASTE IN BRIGHTSPACE TEXT FIELD)
----------------------------------------------------------------------

   After running the deploy command (see web_url.txt), paste here:

   https://__USERNAME__.github.io/taco-talk/


----------------------------------------------------------------------
2. PAPER (PDF) — paper.pdf
----------------------------------------------------------------------

   Converted from paper/draft.md.
   ~7,500 words, 8 sections (Intro, Related Work, Data, Methods,
   Results, Discussion, Limitations, Conclusion).
   Includes 9-specification robustness table and human validation
   results from Packets A, D, E.


----------------------------------------------------------------------
3. CODE PACKAGE — code.zip
----------------------------------------------------------------------

   Contents:
     src/             - 33 active pipeline scripts
     requirements.txt - Python dependencies
     README.md        - project overview + how to run

   To run:
     pip install -r requirements.txt
     # Create .env with ANTHROPIC_API_KEY + OPENAI_API_KEY
     # Then run scripts in src/ following pipeline in README.md


----------------------------------------------------------------------
4. FULL REPLICATION PACKAGE — replication_package.zip
----------------------------------------------------------------------

   Contents (everything needed to reproduce):
     README.md, DECISIONS.md, SUBMIT.md, requirements.txt
     paper/         - markdown source of the paper
     app/           - web app (deployable)
     figures/       - 6 paper figures
     src/           - 33 active scripts
     annotation/    - 4 packets + RUBRIC + user answers
     data/raw/      - public source data (CSV, JSON)
     data/processed/ - pipeline outputs (parquet)

   Excluded:
     _archive/      - earlier iterations, not needed
     .env           - API keys (gitignored)
     __pycache__/   - Python cache


----------------------------------------------------------------------
SUBMISSION INSTRUCTIONS
----------------------------------------------------------------------

   Brightspace upload:
     1. Web URL    -> paste the github.io URL in text field
     2. paper.pdf  -> upload
     3. code.zip   -> upload
     4. replication_package.zip -> upload

   Done.


----------------------------------------------------------------------
KEY FINDINGS (TL;DR for grader)
----------------------------------------------------------------------

   1. S&P 500 path around posts: -4.95% drawdown / +3.80% recovery.
      Placebo test: NOT distinguishable from same-period baseline.

   2. BT-ranked specificity is associated with faster threat
      resolution in 8/9 LLM-only specifications (HR range 1.06-2.17).
      Primary LLM-only: HR=1.39, p=0.076.
      Under HUMAN-VALIDATED matching: HR=1.15, p=0.42 (null).

   3. Human validation numbers:
      - specificity r(human, Claude) = 0.75 (N=40)
      - test-retest r = 0.84
      - LLM matching precision = 63% under human review
      - clustering threshold (cos 0.82) at empirical Y/N transition

   4. Methodological story (the real contribution):
      9 successive corrections each move HR estimates substantially.
      Two mid-pipeline "significant" results turn out to be artifacts
      (one Python regex bug, one Claude-only model effect).
