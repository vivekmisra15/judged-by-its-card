# Pilot results (501 datasets) - preliminary, not a finding

Run on 24 Oct 2026. Sample: 167 low (0 likes), 167 medium (1-4), 167 high (5+). Chance accuracy: 33.3%. "±" is the wobble across 25 test rounds.

| Method | Accuracy | Macro-F1* |
|---|---|---|
| Fame only (publisher followers) | 42.0% ± 3.7 | 0.38 |
| Card features, no fame | 48.9% ± 4.5 | 0.47 |
| Checklist only (0-6 score) | 51.7% ± 3.9 | 0.49 |
| Card features + fame | 54.0% ± 4.2 | 0.52 |
| Jev zero-shot | not run yet (needs API key) | |
| VEGA ML | not built yet | |

*Macro-F1 is accuracy that gives each tier equal weight (1.0 is perfect, about 0.33 is chance).

## What the card looks like, by tier
| Tier | Cards with no content at all | Avg checklist (0-6) | Avg publisher followers | Median words of explanation |
|---|---|---|---|---|
| low | 19.2% | 0.47 | 19 | 0 |
| medium | 19.8% | 1.41 | 95 | 0 |
| high | 7.2% | 2.20 | 2,621 | 206 |

"Median words 0" means that more than half of the low and medium cards contain only automatic technical metadata, with no human-written explanation.

## Our pre-registered hypotheses, so far
- **H1 "fame alone beats the checklist": refuted.** The checklist was 9.7 points better than fame.
- **H2 "the checklist adds little once fame is known": refuted.** Adding card features to fame improved accuracy by 12 points (42.0 to 54.0).
- **H3 "Jev zero-shot is no better than the regression": pending.**

## How far to trust this
- The card-based methods beat fame by more than the wobble, but the gaps between card-based methods (49-54%) are inside it.
- The fame measure is crude, so "fame loses" may partly reflect a weak fame measure. A better one (for example, the publisher's earlier work) is a to-do.
- Nothing is controlled yet for how old each dataset is.
- A pilot answers "is this worth doing?" Yes, it appears so: documentation carries signal that fame does not. It does not answer how strong the effect is.
