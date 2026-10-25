# Decision log: what was decided, and why

Each entry: the decision, the options we turned down, and the reason, in plain terms. Dates are 2026.

## D1. Study dataset adoption, not AI-evaluation evidence (24 Oct)
**Chosen:** predict whether a Hugging Face dataset gets noticed, from its documentation. 
**Parked as "Checkpoint A":** studying whether published AI-model comparisons are trustworthy. 
**Why:** Checkpoint A needs a person to hand-label hundreds of examples (10-20 hours, plus a second person to check). This idea gets its answers from the passage of time, so no labelling is required. It also fits Vivek's data-commercialisation background: it asks what makes a data product get used.

## D2. Keep the project independent of the bank (24 Oct)
**Chosen:** public data only, nothing banking-related, a separate project folder and repository, personal accounts. 
**Why:** avoids any conflict of interest or confusion about who the work speaks for. Checking the bank's outside-activities policy remains a to-do before publishing.

## D3. A new folder outside the Nine Nights project
**Chosen:** `~/Documents/Projects/dataset-adoption-study`. 
**Why:** the Nine Nights repository belongs to a different project. Mixing them would clutter both and risk publishing the wrong files.

## D4. Define success before looking at results ("pre-registration")
**Chosen:** the README states outcome tiers, sample design, methods and three hypotheses, each with what would prove it wrong, **before** any results were produced. 
**Why:** it stops us (even unintentionally) bending the story to fit the numbers. It is the main thing that makes a result credible to sceptical readers.

## D5. Use likes, not downloads, as the outcome
**Chosen:** likes, in three tiers (0 / 1-4 / 5+). 
**Rejected:** downloads. 
**Why:** in the test pull, 91% of datasets had over 100 downloads, which suggests automated traffic (bots, mirrors, tools) inflates downloads. A like needs a person with an account. Likes are not perfect either (see D14).

## D6. Only datasets created January-June 2025
**Why:** every dataset has had at least 16 months to collect likes. Mixing in newer datasets would unfairly label them "low" just because they are young.

## D7. Use the card as it stood on day 7
**Chosen:** the latest version of the documentation within 7 days of creation. 
**Rejected:** today's card. 
**Why:** owners edit cards after a dataset becomes popular. Reading today's card would mix cause and effect. We tested 150 random datasets: 91% of the accessible ones had a recoverable day-7 card.

## D8. Balanced sample: 167 per tier (501 total)
**Chosen:** equal numbers from low, medium and high. 
**Rejected:** a random sample. 
**Why:** 90% of datasets have zero likes, so a random 500 would hold only about 10 "high" examples, too few to learn from. The cost: accuracy numbers are not comparable to real-world rates, and chance is 33%, not 90%. This is stated openly.

## D9. At most 3 datasets per publisher
**Why:** some accounts upload thousands of near-identical datasets (the largest has 4,485 in the period). Without a cap they would dominate the sample and the study would just measure those few accounts.

## D10. Compare against simple methods first
**Chosen:** fame only, checklist, and a plain regression before any AI model. 
**Why:** a new AI tool is only worth using if it beats cheap, simple methods. Skipping this comparison is the most common reason such claims fall apart.

## D11. Cross-validation for the baselines
**Chosen:** 5-fold, repeated 5 times. 
**Why:** the model is trained on 80% of the sample and tested on the other 20%, rotating through, so each score is on data the model never saw. Averaging 25 rounds also shows how much results wobble (the "±" values).

## D12. Jev: call the web service with plain Python, pin the version
**Chosen:** direct call to `https://api.typesafe.ai/v1/systemone`; model `jev-1.13.0`. 
**Rejected:** Jev's Python add-on (needs a newer Python than this Mac has) and the `jev-latest` alias. 
**Why:** fewer moving parts, and a pinned version means the results cannot silently change if TypeSafe upgrades the model mid-study. If the key is a Vercel AI Gateway key instead, this script needs a small change (not yet checked).

## D13. Describe the tiers in words, not numbers, to Jev, and cut cards at 8,000 characters
**Why:** Jev reads our question and answer descriptions as part of its input. We describe each tier simply and apply the same text to everyone. Capping card length keeps cost predictable (the whole pilot is about one cent); the result file records which cards were cut.

## D14. Be upfront about limits
- Likes are not quality: a popular dataset can be poor.
- Publisher follower counts are measured now, not at release; a hit dataset can raise its publisher's followers, so the "fame" method may be flattered.
- Older datasets in the window have had up to five more months to gather likes; not yet controlled for.
- 501 datasets is a pilot. Differences of a few points are within noise.
- Raw card text is not republished until Hugging Face's reuse terms are checked.

## D15. Using VEGA ML later, and treating it as unproven
**Why:** it is two weeks old with one author, and its published benchmarks are self-reported; its training script has only been smoke-tested. We will pin its version, say so in the write-up, and test it against the same baselines. Training will happen on a free cloud GPU.

## D16. Not using Claude Code's name to hide anything
The code was written with Claude Code; the write-up should say so. This is a transparency decision.

## D17. Commit Jev's raw answers; run 20 first, then the rest
**Chosen:** commit `results/jev_raw.jsonl` to Git. Before the full run, send 20 cards and check every answer is complete before sending the other 481. 
**Rejected:** keeping the answers out of Git like the cards (not needed: the file holds only dataset names and Jev's replies, no card text); sending all 501 at once (if the request format had been wrong, every call would have been wasted). 
**Why:** anyone can re-check the scoring without paying to call Jev again, and the exact answers are preserved even if TypeSafe later retires `jev-1.13.0`. The real token use was about 1.7 times the dry-run estimate (cause not documented; probably hidden instructions Jev adds, or our rough estimate rule); the total was still about two cents.

## D18. Explain Jev's low score in a separate, clearly labelled exploratory note
**Chosen:** `docs/JEV_EXPLAINED.md` plus a free script `src/explore_jev.py` that recomputes every number in it from the saved answers. 
**Rejected:** changing the headline Jev result to the "rebalanced" 47.3% (it was decided after seeing results, so it would undo the pre-registration); leaving the explanation only in chat (it would be lost and could not be re-checked). 
**Why:** the low score has a likely, partly design-driven cause (Jev leans towards the real-world rate of about 90% "no likes"; our sample is one-third per tier). That context belongs in the write-up, but kept apart from the pre-registered result and labelled as exploratory.
