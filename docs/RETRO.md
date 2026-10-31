# Learning retro: Judged by its card (closed 31 Oct 2026)

A personal look back at what this project taught, written when I closed it after the pilot. It is about the learning, not the findings. For the numbers and how far to trust them, see `RESULTS_PILOT.md`. The code was written with Claude Code (D16).

## What I set out to do
Find out whether the documentation a Hugging Face dataset is published with predicts whether people notice it (likes 16-21 months later), and how simple methods compare with two AI decision tools (Jev and VEGA ML). The outcome comes from what actually happened, so no hand-labelling was needed.

## Where it ended
- 501-dataset pilot, balanced across three like-tiers (chance 33%).
- Fame only 42.0%, checklist 51.7%, card + fame regression 54.0%. Jev zero-shot 38.3%.
- H1 refuted, H2 refuted, H3 supported (see `RESULTS_PILOT.md`).
- An after-the-fact check (AUC) showed Jev ranks reasonably (0.757 vs the regression's 0.773) but is badly calibrated: it answered "low" 464 times out of 501.
- Not done: VEGA ML, controls for dataset age and a better fame measure, scale-up beyond the pilot.
- **This is a pilot, not a finding.** The honest takeaway is "documentation appears to carry signal that follower count does not; the size of the effect is unknown."

## What went well
- **Deciding success before looking.** Writing the sample, tiers and hypotheses in the README first meant I could not quietly move the goalposts when Jev scored low. It was uncomfortable and it was worth it.
- **Cheap baselines first.** Fame, a checklist and a simple regression took little effort, and they set the bar that any fancier tool has to clear. Without them, Jev's 38% would have meant nothing.
- **Running small before large.** A dry run for cost, then 20 cards, then the rest (D17). The whole Jev run cost about two cents and nothing was wasted.
- **Keeping exploration labelled.** The Jev post-mortem and the AUC check were written up as exploratory, apart from the pre-registered results (D18). Both added understanding without rewriting the headline.
- **Writing decisions down.** `DECISIONS.md` made closing the project easy, because every earlier choice had its reasons attached.

## What I would do differently
- **Pick the outcome and the inputs from the start with the real-world rate in mind.** About 90% of datasets get no likes. A balanced sample made the comparison fair between my methods, but it set Jev up badly because it leans towards the real-world rate. I knew this in principle; I did not plan for it.
- **Treat the AI tools as a side question, not the headline.** The project name and framing put Jev and VEGA ML at the centre, but the interesting question was about documentation and fame. Tool results are perishable (one version, one prompt, one wording); the question was not.
- **Measure fame better, and control for age, before comparing anything.** "Fame loses" may only mean my fame measure was weak. Adoption plainly depends on many things (subject, language, format, age, publisher history); I tested a thin version of that.
- **Match the sample size to the method.** 501 cards is fine for a checklist and a simple regression and too few for the "nuanced ML" I later wanted. I should have asked what sample the better method would need before choosing the pilot size.
- **Check terms before publishing outputs.** Jev's raw answers went into the public repo before I had checked whether TypeSafe's terms allow that. I checked after closing (31 Oct, D20) and found no restriction, but that was luck as much as care; the check belongs before the first push.

## What I learned
**About the topic**
- A dataset's card is a rough but real signal of adoption; effort in the documentation shows up in the outcome even with a crude checklist.
- A tool can be good at ranking and still bad at deciding. Accuracy and AUC told different stories about Jev, and the gap pointed to calibration, not capability.
- Measuring against a clear baseline is what turns "the AI tool got 38%" from a number into a conclusion.

**About method**
- Pre-registration, even for a personal project, is a discipline about honesty with yourself. It also gave a clean way to handle changes: a dated amendment, original kept.
- Cross-validation, calibration and AUC: what each question they answer, and why accuracy alone can mislead (see `GLOSSARY.md`).
- Stopping early is a legitimate result. The pilot's job was to say whether a bigger study was worth it; the answer was "yes, but with a different design, and not from me now."

**About working this way**
- Working with Claude Code on a project where I am not a developer worked best when every step was explained first, decisions were logged, and paid actions were small tests first.
- I should still check anything surprising myself. One example: the real token use was 1.7 times the dry-run estimate and I never found out why (D17).

## If someone picks this up
The better study is: day-7 metadata (subject, language, licence, size, publisher history) with and without the card, on a much larger sample, with age controlled, comparing a regression with gradient boosting and text features. Treat likes as a noisy outcome with a low ceiling, and keep everything as of day 7 so nothing leaks the answer. The pilot code in `src/` is a reasonable starting point.

## Before anything is published
The repository is public. Both pre-publication checks are done (31 Oct 2026): the bank's outside-activities policy was confirmed OK, and TypeSafe's terms were checked (D20). Raw cards are still kept out of the repository until Hugging Face's reuse terms are checked.
