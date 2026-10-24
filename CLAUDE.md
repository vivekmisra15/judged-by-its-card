# Dataset Adoption Study

An independent research project: **can the documentation a Hugging Face dataset is published with predict whether people will notice it, and how do simple methods compare with two AI "decision" tools (Jev and VEGA ML)?** Outcomes come from what actually happened (likes 16-21 months later), so no hand-labelling is needed.

## Who I'm working with

Vivek works in AI transformation strategy at a bank, with a background in data commercialisation and a Johns Hopkins AI certification. He is **not a developer**. He builds personal projects on GitHub and is increasingly comfortable with VS Code and the terminal.

- **Explain in plain language.** Say what a step does and why before or as you do it. Avoid jargon, or define it (add to `docs/GLOSSARY.md`).
- **Keep code simple and readable.** Plain Python, small files, standard library where possible. Comment *why*, for a learner. Ask before adding any library or infrastructure.
- **Document every decision.** When you make or change a decision (tooling, design, data, rationale), add or update an entry in `docs/DECISIONS.md` with the options rejected and why. Keep `docs/ARCHITECTURE.md` current if the pipeline or files change.
- **Be honest about results.** Report weak or negative findings plainly. Never present a pilot as a finding. State what was and was not checked.

## Independence rules (important)

- This is **not** a bank project. Use public data only, nothing banking-related, no employer branding, personal accounts only.
- Before anything is published or written about publicly, Vivek must check the bank's outside-activities policy. Remind him; do not publish anything yourself.
- Be open that the code was written with Claude Code (decision D16).

## Safety rules

- **API keys:** never ask for a key in chat, print it, or write it into code, docs or commits. Vivek puts `TYPESAFE_API_KEY=...` in the git-ignored `.env` file himself. Scripts read it from the environment or `.env`.
- **Do not commit or push** unless asked. The repository is local only for now.
- **Do not commit** `data/cards/`, `data/*.jsonl` or `.env` (already in `.gitignore`). Raw card text stays out of Git until Hugging Face's reuse terms are checked.
- Run `--dry-run` or `--limit` before any paid API run, and say what it will cost.

## Pre-registered design: do not change retrospectively

The plan in `README.md` was written **before** results existed. Do not edit the outcome tiers, sample design or hypotheses H1-H3 to fit results. If something must change, add a dated "Amendment" section saying what changed and why, and keep the original.

- Population: public datasets created 2025-01-01 to 2025-06-30 (158,567 at pull date, 24 Oct 2026).
- Outcome: likes tier: low = 0, medium = 1-4, high = 5+.
- Sample: 167 per tier (501), max 3 per publisher, card as of day 7 after creation.
- Methods: fame only, checklist, logistic regression (card + fame), Jev zero-shot, VEGA ML.

## Status (as of 24 Oct 2026)

Done:
- Feasibility check (Hugging Face API, VEGA ML, Jev).
- 501-dataset pilot sample and cards in `data/`.
- Baselines: fame 42.0%, card features 48.9%, checklist 51.7%, card + fame 54.0% (chance 33.3%). H1 and H2 refuted; see `docs/RESULTS_PILOT.md`.
- Jev runner and scorer written and dry-run. **Jev has not been called**: no API key was set.

Next, in order:
1. Vivek adds his key to `.env`. Ask whether it is a direct TypeSafe key or a Vercel AI Gateway key (the script assumes direct; a gateway key needs a small change). Official API docs are at docs.typesafe.ai/api; the request format was built from third-party descriptions, so verify it with `--limit 20` first.
2. Run Jev on all 501, then `score_jev.py`. This settles H3.
3. Add controls: dataset age (created-date) and a better fame measure than follower count.
4. VEGA ML: needs Python 3.10+ (this Mac's system Python is 3.9, so install a newer one), small model on the Mac, adapter training on a free Kaggle/Colab GPU. Pin its version. It is 2 weeks old with one author, so treat it as unproven.
5. Scale beyond the pilot, add a spot-check of the checklist, then write up.

## Folder map

```
README.md            plan, pre-registered hypotheses, how to re-run
CLAUDE.md            this file
docs/                ARCHITECTURE, DECISIONS, RESULTS_PILOT, GLOSSARY
src/build_sample.py  picks the sample, downloads day-7 cards and publisher followers
src/features.py      counts things in a card; the 0-6 checklist score
src/baselines.py     fame / checklist / regression with cross-validation
src/run_jev.py       sends cards to Jev, saves raw answers (resumable)
src/score_jev.py     accuracy, calibration, abstention view for Jev
data/                sample.json (committed), cards and big files (not committed)
results/             pilot_baselines.json, later jev_raw.jsonl
.venv/               private Python tools (not committed)
```

## Commands (run from this folder)

```
python3 -m venv .venv && .venv/bin/pip install scikit-learn numpy   # once
.venv/bin/python src/build_sample.py
.venv/bin/python src/baselines.py
.venv/bin/python src/run_jev.py --dry-run     # cost estimate, sends nothing
.venv/bin/python src/run_jev.py --limit 20    # small paid test
.venv/bin/python src/run_jev.py               # all cards
.venv/bin/python src/score_jev.py
```

`data/h1_2025_all.jsonl` (the full list of 158,567 datasets) is needed by `build_sample.py`. It is not in Git; re-create it from the Hugging Face API (`/api/datasets` sorted by `createdAt`, paged through the `Link` header) if missing.

## Related

- **Checkpoint A (parked):** studying whether published AI-model comparisons are trustworthy; needs hand-labelling unless independently re-measured claims exist in enough number. Not in this repo.
- Different project: `~/Documents/Projects/nine-nights-shakti-potter` is Supriya's. Do not touch it from here.
