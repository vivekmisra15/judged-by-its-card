"""EXPLORATORY look at why Jev scored low. Decided after seeing results, so nothing here is a finding.
Free to run: uses the saved answers in results/jev_raw.jsonl, calls no API. Numbers feed docs/JEV_EXPLAINED.md."""
import json, math, sys, collections
import numpy as np
sys.path.insert(0, "src"); from features import card_features

TIERS = ["low", "medium", "high"]

# 1. Real-world base rate: how common each tier is among ALL datasets, not just our balanced sample.
counts = collections.Counter()
for line in open("data/h1_2025_all.jsonl"):
    likes = json.loads(line)["likes"]
    counts["low" if likes == 0 else "medium" if likes < 5 else "high"] += 1
n = sum(counts.values())
print("population (n=%d):" % n, {t: "%.1f%%" % (100 * counts[t] / n) for t in TIERS})

# 2. Jev's average lean across our 501 cards.
sample = {s["id"]: s for s in json.load(open("data/sample.json"))}
answers = [json.loads(l) for l in open("results/jev_raw.jsonl")]
P = np.array([[a["response"]["answers"]["adoption"]["probabilities"][t] for t in TIERS] for a in answers])
y = np.array([TIERS.index(sample[a["id"]]["tier"]) for a in answers])
print("Jev mean probabilities:", dict(zip(TIERS, P.mean(0).round(3))))

# 3. Rebalance: divide out Jev's own average lean so every tier starts equal.
#    Uses only Jev's numbers, never the true tiers, so it does not peek at the answers.
P_bal = P / P.mean(0)
print("accuracy raw %.3f | rebalanced %.3f" % ((P.argmax(1) == y).mean(), (P_bal.argmax(1) == y).mean()))
print("rebalanced confusion (rows = truth, cols = Jev):\n",
      np.array([[((y == i) & (P_bal.argmax(1) == j)).sum() for j in range(3)] for i in range(3)]))

# 4. Ranking (AUC): pick one high-tier and one other dataset at random; how often does the score
#    put the high one higher? 0.5 = chance, 1.0 = perfect.
def auc(score, is_pos):
    ranks = score.argsort().argsort() + 1
    n_pos = is_pos.sum()
    return (ranks[is_pos].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * (len(is_pos) - n_pos))

feats = [card_features(open("data/cards/" + a["id"].replace("/", "__") + ".md").read()) for a in answers]
checklist = np.array([f["checklist"] for f in feats], float)
log_words = np.array([f["log_words"] for f in feats])
has_card = np.array([f["has_card"] for f in feats])
log_followers = np.array([math.log1p(sample[a["id"]]["followers"]) for a in answers])
high = y == 2
print("AUC high-vs-rest: Jev %.3f | checklist %.3f | words %.3f | followers %.3f" % (
    auc(P[:, 2], high), auc(checklist + 1e-6 * log_words, high), auc(log_words, high), auc(log_followers, high)))

# 5. What Jev's 'high' probability moves with.
for name, v in [("checklist", checklist), ("log words", log_words), ("log followers", log_followers)]:
    print("corr(Jev P(high), %s) = %.2f" % (name, np.corrcoef(P[:, 2], v)[0, 1]))

# 6. Empty cards, and the high-tier datasets Jev caught versus missed.
empty = has_card == 0
print("empty cards: %d | Jev said low on %d | true tiers %s" % (
    empty.sum(), (P[empty].argmax(1) == 0).sum(), dict(collections.Counter(np.array(TIERS)[y[empty]]))))
missed, caught = high & (P.argmax(1) == 0), high & (P.argmax(1) == 2)
for name, m in [("missed", missed), ("caught", caught)]:
    print("high-tier %s: n=%d, mean checklist %.2f, median words %d" % (
        name, m.sum(), checklist[m].mean(), np.median(np.expm1(log_words[m]))))
print("P(medium): max %.2f, mean %.3f" % (P[:, 1].max(), P[:, 1].mean()))
