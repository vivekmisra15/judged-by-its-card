# Pilot results (501 datasets) - preliminary, not a finding

Baselines run on 24 Oct 2026; Jev run on 25 Oct 2026. Sample: 167 low (0 likes), 167 medium (1-4), 167 high (5+). Chance accuracy: 33.3%. "±" is the wobble across 25 test rounds.

| Method | Accuracy | Macro-F1* |
|---|---|---|
| Fame only (publisher followers) | 42.0% ± 3.7 | 0.38 |
| Card features, no fame | 48.9% ± 4.5 | 0.47 |
| Checklist only (0-6 score) | 51.7% ± 3.9 | 0.49 |
| Card features + fame | 54.0% ± 4.2 | 0.52 |
| Jev zero-shot (`jev-1.13.0`) | 38.3% (single run, no ±)** | 0.27 |
| VEGA ML | not built yet | |

*Macro-F1 is accuracy that gives each tier equal weight (1.0 is perfect, about 0.33 is chance).

**Jev is not trained on our data, so it is scored once on all 501 rather than in 25 cross-validation rounds. There is no "±" for it.

## What the card looks like, by tier
| Tier | Cards with no content at all | Avg checklist (0-6) | Avg publisher followers | Median words of explanation |
|---|---|---|---|---|
| low | 19.2% | 0.47 | 19 | 0 |
| medium | 19.8% | 1.41 | 95 | 0 |
| high | 7.2% | 2.20 | 2,621 | 206 |

"Median words 0" means that more than half of the low and medium cards contain only automatic technical metadata, with no human-written explanation.

## Jev in detail

Jev answered all 501 cards (one version throughout: `jev-1.13.0`; no failures; cost about $0.02). 26 long cards were cut at 8,000 characters, as designed (D13).

**It almost always says "low".** Rows are what actually happened, columns are what Jev said:

| Actual tier | Jev: low | Jev: medium | Jev: high |
|---|---|---|---|
| low (167) | 164 | 0 | 3 |
| medium (167) | 162 | 0 | 5 |
| high (167) | 138 | 1 | 28 |

- 464 of 501 answers were "low"; "medium" was used once. Most of its accuracy comes from the low tier being right by default.
- It has a little real signal: when it said "high" it was right 28 times out of 36 (78%). But it found only 28 of the 167 high-tier datasets (17%).
- **It is overconfident.** Its stated confidence is on average about 38 points higher than its actual hit rate (expected calibration error 0.376).
- **Answering only when sure helps little.** If it answers only when its top probability is at least 0.8, accuracy rises to 46.9%, but it then answers only 52% of cards. Still below the regression.

| Answer only if top probability ≥ | Share of cards answered | Accuracy on those |
|---|---|---|
| 0.0 (always) | 100% | 38.3% |
| 0.5 | 88% | 39.5% |
| 0.6 | 77% | 42.3% |
| 0.7 | 67% | 45.6% |
| 0.8 | 52% | 46.9% |

**Why so low?** See `JEV_EXPLAINED.md` (exploratory, not a finding). The main suspect: Jev leans towards the real-world rate, where about 90% of datasets get no likes, but our sample is one-third per tier. Removing that lean lifts it to 47.3%, still below the regression.

## Exploratory: ranking quality (AUC), added 31 Oct 2026
Decided after seeing the results, so **not a finding**. Accuracy punishes Jev for always saying "low". AUC asks a different question: pick one high-tier dataset and one other at random; how often does the method score the high one higher? (0.5 = chance, 1.0 = perfect.) It ignores the "always low" habit. Script: `src/auc_regression.py` (regression, cross-validated as above) and `src/explore_jev.py` (Jev and simple scores).

| Method | AUC, high vs rest |
|---|---|
| Fame only (regression) | 0.660 |
| Followers alone | 0.666 |
| Word count alone | 0.702 |
| Checklist alone | 0.713 |
| Card features, no fame (regression) | 0.706 |
| **Jev (no training)** | **0.757** |
| **Card features + fame (regression)** | **0.773** |

- On ranking, Jev is **not poor**: it beats fame, word count and the checklist, and sits just under the regression (0.757 vs 0.773). That gap is about the size of the regression's own wobble across repeats (±0.003) plus the sampling noise of 501 cards, so I would not call them different.
- So Jev's low accuracy is mostly about its **calibration** (it says "low" far too often), not an inability to tell strong cards from weak ones. This fits the rebalancing result in `JEV_EXPLAINED.md`.
- Caveats: this covers one question (high vs rest), not all three tiers. Jev's AUC has no cross-validation error bar because it is one run with no training; the regression's ± reflects repeats of the same data, not a fresh sample. It does not change H3, which was pre-registered on accuracy and stays "supported".

## Our pre-registered hypotheses, so far
- **H1 "fame alone beats the checklist": refuted.** The checklist was 9.7 points better than fame.
- **H2 "the checklist adds little once fame is known": refuted.** Adding card features to fame improved accuracy by 12 points (42.0 to 54.0).
- **H3 "Jev zero-shot is no better than the regression": supported.** Jev scored 38.3%, 15.7 points *below* the regression (54.0%). It was also below fame alone (42.0%).

## How far to trust this
- The card-based methods beat fame by more than the wobble, but the gaps between card-based methods (49-54%) are inside it.
- The fame measure is crude, so "fame loses" may partly reflect a weak fame measure. A better one (for example, the publisher's earlier work) is a to-do.
- Nothing is controlled yet for how old each dataset is.
- **Jev was asked one question in one wording, fixed before the run (D13).** A different wording might do better, but changing it now to chase a better score would undo the pre-registration. Any re-wording must be an explicit, dated amendment and reported alongside this result.
- **The comparison is not like-for-like in training.** The regression learned from about 400 labelled examples per round; Jev saw none. That is the real choice a user faces ("use a ready-made AI tool, or fit a simple model to my own examples?"), but it should be said plainly.
- The Jev result is one run. Repeating it would show whether Jev gives the same answers each time; not yet checked.
- A pilot answers "is this worth doing?" Yes, it appears so: documentation carries signal that fame does not. It does not answer how strong the effect is.
