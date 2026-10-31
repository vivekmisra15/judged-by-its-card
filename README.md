# Dataset adoption study (pilot)

**Question.** Can the documentation a Hugging Face dataset is published with predict whether anyone will like/use it? And how often does the card say too little to tell?

**Status: closed after the pilot (31 Oct 2026).** See "Project closed" below. The design that follows was written down BEFORE running anything and has not been changed:

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

## Project closed (31 Oct 2026)
**Amendment, dated 31 Oct 2026.** The project stopped after the 501-dataset pilot. The design and hypotheses above are unchanged. Methods (5), VEGA ML, and the planned controls and scale-up were **not done**. This is a pilot, not a finding: it shows what looks worth studying, not how strong the effect is.

What the pilot found (details and caveats in `docs/RESULTS_PILOT.md`):
- Accuracy, with chance at 33.3%: fame only 42.0%, checklist 51.7%, card + fame regression 54.0%, Jev zero-shot 38.3%.
- **H1 refuted** (checklist beat fame). **H2 refuted** (card features added 12 points to fame). **H3 supported** (Jev scored 15.7 points below the regression).
- Exploratory, decided after seeing results: Jev answered "low" 464 times of 501, so it was badly calibrated, but its ranking was reasonable (AUC 0.757 vs 0.773 for the regression).
- Not checked: dataset age, a better fame measure, whether Jev gives the same answers twice, whether the checklist matches a human's judgement.

Why it stopped, what I learned and what a better study would look like: `docs/RETRO.md` and decision D19 in `docs/DECISIONS.md`. The code was written with Claude Code.

Raw cards are not in this repository. Jev's raw answers are (`results/jev_raw.jsonl`); whether TypeSafe's terms allow that has not been checked.

## Documentation for non-developers
- `docs/RETRO.md`: what I learned, what went well, what I would change.
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
