# How Jev works here, and why it scored low

Written 26 Oct 2026, after the pilot Jev run (25 Oct, `jev-1.13.0`, 501 cards, 38.3% accuracy).

> **Status: exploratory.** Everything under "Why it scored low" was decided *after* seeing the results. It is a set of explanations to test, not a finding. The pre-registered result stands: **H3 is supported**: Jev did no better than the regression. Re-run the numbers with `.venv/bin/python src/explore_jev.py` (free, no API calls).

## In one sentence

Jev isn't blind. It mostly expects any new dataset to be ignored, which is true in real life but a losing bet on our evenly split test, and it can't see some of the information the simple methods use.

## What Jev reads

Each call (one per dataset) sends three things:

1. **The card text** (`state`): the dataset's documentation page as it was 7 days after publication, cut at 8,000 characters (26 of 501 cards were cut). For the 77 datasets with no card, it gets the sentence "The dataset has no documentation card at all."
2. **Our question:** "This is the documentation card of a newly published open dataset. About 16 to 21 months after release, how much attention will the dataset have attracted from the community?"
3. **Three answer descriptions**, in words, with no mention of "likes" (decision D13):
   - low: "Nobody has endorsed it; it is essentially ignored."
   - medium: "A handful of people (1 to 4) have endorsed it."
   - high: "Five or more people have endorsed it; it is clearly noticed."

**What it does not see:** the dataset's name, the publisher's identity or follower count, the publication date, or anything after day 7. The regression *does* get the follower count.

## What Jev returns

A probability for each answer (for example low 0.83, medium 0.15, high 0.02), the highest one as its choice, and a separate "confidence" number.

## How it calculates: unknown

TypeSafe's official API docs (docs.typesafe.ai/api, checked 26 Oct 2026) describe only what goes in and what comes out. They do not say:

- what kind of model Jev is,
- how the probabilities are produced,
- whether they are calibrated (whether "80% sure" means right 80% of the time),
- how "confidence" relates to the probabilities. In our answers it is *not* the top probability: one answer had confidence 0.74 with a top probability of 0.83.

From the outside it behaves like an AI language model that reads the text and spreads probability across the answers we offer. It also used about 1.7 times the tokens we estimated. Possible causes are hidden instructions Jev adds, or a rough estimating rule on our side. Neither is confirmed.

## What it actually did

| Actual tier | Jev: low | Jev: medium | Jev: high |
|---|---|---|---|
| low (167) | 164 | 0 | 3 |
| medium (167) | 162 | 0 | 5 |
| high (167) | 138 | 1 | 28 |

Accuracy 38.3% (chance 33.3%; regression 54.0%; fame alone 42.0%). Full table and calibration: `RESULTS_PILOT.md`.

## Why it scored low: hypotheses, strongest evidence first

### 1. It predicts for the real world; our sample isn't the real world (strong evidence)

| | low | medium | high |
|---|---|---|---|
| All 158,567 datasets (real world) | 90.5% | 7.6% | 1.9% |
| Our sample (by design) | 33.3% | 33.3% | 33.3% |
| Jev's average probabilities | 73.9% | 15.9% | 10.3% |

- Jev leans towards reality, which is sensible for a question that says "a newly published open dataset". On the full population, always saying "low" would be right about 90% of the time.
- Our balanced design (chosen so each tier has enough examples) makes that same habit look bad.
- The regression learned the one-third split during training. Jev was never told it.

**Test:** divide out Jev's average lean so every tier starts on equal footing. This uses only Jev's own numbers, never the true tiers. Accuracy rises from **38.3% to 47.3%**. That's still below the regression (54.0%) and near the checklist (51.7%). So this explains much of the gap, **not all of it**.

### 2. It is missing information the regression has

- **No fame.** It never sees the publisher's follower count, which alone gives 42%.
- **Empty cards.** 77 datasets had no card. Jev said "low" for all 77, which is all it reasonably can, but 12 were actually high and 33 medium.

### 3. It rates the documentation, not the popularity

- Jev's "high" probability moves with card length (correlation 0.50) and checklist score (0.40) more than with follower count (0.25).
- The 28 high-tier datasets it caught had long cards: median 421 words, checklist 3.3 out of 6.
- The 138 it missed were thinner: median 123 words, checklist 2.0.
- Many datasets get noticed for reasons outside the card: who released them, a linked paper, timing.

### 4. "Medium" is nearly impossible for it

Jev's probability for medium never went above 0.41, so medium almost never came out on top (1 of 501). The line between 0 likes and 1-4 likes is probably partly luck, which makes the middle tier hard for any method.

### 5. Its probabilities are not calibrated

It is on average about 38 points more confident than it is right (expected calibration error 0.376). The docs make no calibration claims.

### Ruled out: a broken setup

All 501 replies were complete and came from the pinned version (`jev-1.13.0`). Only 26 cards were cut short. The first 20 were checked by hand before the full run (D17).

## The silver lining: ranking versus placing

Jev is decent at **ranking** but bad at **placing** datasets into tiers.

Take one high-tier dataset and one other at random. How often does each measure score the high one higher? (This is the "AUC": 50% is chance, 100% is perfect.)

| Measure | AUC (high vs rest) |
|---|---|
| Jev's "high" probability | **75.7%** |
| Checklist score | 71.3% |
| Card length | 70.2% |
| Publisher followers | 66.6% |

**Not yet checked:** the regression's AUC. Until it is computed, we can't say whether Jev ranks better than the best simple method.

## What this means for the study

- **H3 stands as pre-registered:** under the agreed test, Jev lost.
- **The write-up should add this context:** much of the loss comes from a mismatch between Jev's real-world lean and our balanced test. Jev ranks reasonably but places datasets poorly.

## Possible next steps (not started)

Any of these must be recorded as a dated amendment, never as a replacement for the original result.

- **(a) Free:** compute the regression's AUC for a fair ranking comparison, and add a short exploratory note to `RESULTS_PILOT.md`.
- **(b) About 2 cents, pre-registered first:** a second Jev run that tells Jev the three tiers are equally common and gives it the publisher's follower count.
