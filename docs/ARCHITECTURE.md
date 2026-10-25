# How the project works (plain-English guide)

This guide explains what every part of the project does, how information moves through it, and why it was built this way. No programming knowledge is assumed.

## The question in one sentence
When someone publishes an open dataset on Hugging Face (a public library of AI datasets and models), can we predict, **from the dataset's documentation page alone**, whether people will end up noticing it? And how does that prediction compare across simple methods and two new AI "decision" tools (Jev and VEGA ML)?

## Why this is a fair test (the key idea)
We never ask a person to judge anything. Instead we use **what actually happened**. We look at datasets published between January and June 2025, read what their documentation looked like in the **first week**, and then compare against how many "likes" each one had collected by 24 October 2026 (16-21 months later). Time provides the answer, so there is no labelling by hand, and no method can "mark its own homework".

## The pipeline: five steps, left to right

```
 Hugging Face public API
        |
        v
 [1 COLLECT] list of 158,567 datasets made Jan-Jun 2025
        |      (id, publisher, creation date, likes, downloads)
        v
 [2 SAMPLE]  pick 501 of them: 167 'low', 167 'medium', 167 'high' outcome
        |      for each: fetch the documentation card as it stood on day 7,
        |      and the publisher's follower count
        v
 [3 FEATURES] turn each card into simple counts (has a licence? how long? ...)
        |
        +--> [4a BASELINES]  fame only / checklist / regression  (run on your laptop)
        |
        +--> [4b JEV]        send the card text to Jev's online service, get a prediction
        |
        +--> [4c VEGA ML]    (not built yet) same cards, run on a free cloud GPU
        v
 [5 SCORE]  compare every method's prediction with what really happened
```

## The files, one by one

| File | What it does | Analogy |
|---|---|---|
| `data/h1_2025_all.jsonl` | The full list of 158,567 datasets and their like/download counts (step 1). Not committed to Git (it is big and can be re-downloaded). | The phone book |
| `src/build_sample.py` | Step 2. Picks the 501 datasets, downloads each day-7 card and each publisher's follower count. Saves `data/sample.json` and the cards in `data/cards/`. | The researcher choosing and photocopying the pages |
| `data/sample.json` | The 501 chosen datasets with their outcome tier. | The study register |
| `data/cards/` | The 501 documentation pages, one text file each. **Not committed**, because we have not yet checked Hugging Face's terms for republishing card text. | The photocopies |
| `src/features.py` | Step 3. Reads a card and counts things: is there a licence line? A mention of sources, intended use, limitations, citation? How many words? Also produces the 0-6 **checklist score**. | The marker's tick-sheet |
| `src/baselines.py` | Step 4a. Runs the three simple methods and prints how often each guesses the right tier. | The control group |
| `src/run_jev.py` | Step 4b. Sends each card to Jev and saves the answers in `results/jev_raw.jsonl`. Can be stopped and restarted without paying twice. | The call to an outside expert |
| `src/score_jev.py` | Step 5 for Jev: accuracy, confusion table, "answer only when confident" view, calibration. | The marking |
| `results/` | Outputs. `pilot_baselines.json` (baseline scores) and `jev_raw.jsonl` (Jev's answer for each dataset; no card text). | The results folder |
| `docs/` | These explanatory documents. | The lab notebook |

## The three outcome tiers
Based on **likes** at 24 Oct 2026: **low** = 0 likes, **medium** = 1-4, **high** = 5 or more. We chose these cut-offs and wrote them down before looking at any results (see README).

## The methods being compared
1. **Fame only.** Looks only at who published the dataset (follower count; person or organisation). If this does well, documentation does not matter much, because name recognition does the work. This is the bar everything else must beat.
2. **Checklist.** Six yes/no questions about the card: has a licence, says where the data came from, says what it is for, mentions limitations, offers a citation, has at least 100 words of explanation. The score (0-6) is converted into a tier by a tiny statistical model.
3. **Card features + fame (regression).** A standard statistical model (logistic regression) that weighs all the card counts and the fame numbers together. A deliberately simple method; a complicated one has to beat it to be worth using.
4. **Jev.** TypeSafe AI's hosted decision model. We send the card and a question with the three answers described in words; it returns a probability for each answer. We did not train it on our data ("zero-shot").
5. **VEGA ML** (next phase). An open-source tool that does the same kind of job but can also be **trained on our own outcomes**. That gives us the interesting comparison: a tool used as-is versus the same kind of tool taught on this problem.

## How "I don't know" works
Neither tool refuses to answer on its own in the way a person would. Each returns probabilities. **Our code** chooses a confidence line (say 70%) and declines to answer below it. We then measure: of the datasets it still answered, how often was it right? And does "70% sure" really mean right about 70% of the time (calibration)?

## Where the work runs
- **On your Mac:** collecting data, building the sample, features, baselines, scoring. All free, all quick.
- **On Jev's servers:** only the card text and our question are sent over the internet. The estimate was about 270,000 tokens (small chunks of text); the real run used about 459,000 (Jev counts its own instructions too): roughly **two cents**.
- **On Kaggle/Colab (later):** training VEGA ML's small add-on needs a graphics chip your Mac does not have. These services provide one free.
