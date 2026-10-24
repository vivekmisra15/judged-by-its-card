# Dataset adoption study (pilot)

**Question.** Can the documentation a Hugging Face dataset is published with predict whether anyone will like/use it? And how often does the card say too little to tell?

**Status:** pilot, ~500 datasets. Not a result. Written down BEFORE running anything:

## Pre-registered design (pilot)
- Population: public Hugging Face datasets created 2025-01-01 to 2025-06-30 (158,567 at pull date, 24 Oct 2026).
- Outcome (3 tiers, by all-time likes at pull date): `low` = 0, `medium` = 1-4, `high` = 5 or more.
- Sample: 167 per tier (stratified, so chance is ~33%), max 3 datasets per publisher. Gated/private/deleted datasets are excluded (cannot be read).
- Input: the card (README.md) as of day 7 after creation, i.e. what a would-be user saw early on.
- Methods compared: (1) fame only (publisher followers), (2) documentation checklist, (3) logistic regression on card features + fame, (4) Jev zero-shot, later (5) VEGA ML.
- Metric: accuracy, macro-F1 and, for Jev, calibration and accuracy when it abstains.

## Hypotheses (what would prove me wrong)
- H1: fame alone beats the checklist. Wrong if checklist accuracy > fame accuracy by a clear margin.
- H2: checklist adds little once fame is known. Wrong if regression(card + fame) beats fame by 5+ points.
- H3: Jev zero-shot is no better than the regression. Wrong if it beats it by 5+ points.

## Known limits
- Likes are not quality. Publisher followers are measured now, not at release (a popular dataset can raise its publisher's followers).
- Stratified sampling means accuracies are not comparable to the real population (90% of datasets have 0 likes).
- Raw cards are not committed (reuse terms unchecked); only derived features and results.

## Documentation for non-developers
- `docs/ARCHITECTURE.md`: how the project works, file by file and step by step.
- `docs/DECISIONS.md`: every decision, what was rejected and why.
- `docs/RESULTS_PILOT.md`: pilot numbers and how far to trust them.
- `docs/GLOSSARY.md`: plain-English meanings of technical terms.

## How to re-run (from this folder)
```
python3 -m venv .venv && .venv/bin/pip install scikit-learn numpy   # once
.venv/bin/python src/build_sample.py      # needs data/h1_2025_all.jsonl
.venv/bin/python src/baselines.py
.venv/bin/python src/run_jev.py --dry-run # shows cost, sends nothing
.venv/bin/python src/run_jev.py           # needs TYPESAFE_API_KEY
.venv/bin/python src/score_jev.py
```
