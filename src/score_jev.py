"""Score Jev's answers against what actually happened, and add a 'abstain when unsure' view."""
import json, numpy as np
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
TIERS = ["low", "medium", "high"]
truth = {s["id"]: s["tier"] for s in json.load(open("data/sample.json"))}
rows = []
for l in open("results/jev_raw.jsonl"):
    r = json.loads(l); a = r["response"]["answers"]["adoption"]
    probs = np.array([a["probabilities"][t] for t in TIERS])
    rows.append((truth[r["id"]], TIERS[int(probs.argmax())], float(probs.max()), r["response"].get("model")))
y = np.array([TIERS.index(t) for t, *_ in rows]); p = np.array([TIERS.index(q) for _, q, *_ in rows]); c = np.array([x[2] for x in rows])
print(f"n={len(y)}  model versions seen: {sorted({x[3] for x in rows})}")
print(f"accuracy {accuracy_score(y, p):.3f}   macro-F1 {f1_score(y, p, average='macro'):.3f}   (chance 0.333)")
print("confusion (rows = truth, cols = Jev):\n", confusion_matrix(y, p, labels=[0, 1, 2]))
# Abstention: the code (not Jev) declines to answer when top probability < threshold.
print("\nthreshold  coverage  accuracy-when-answering")
for th in [0.0, 0.4, 0.5, 0.6, 0.7, 0.8]:
    keep = c >= th
    if keep.sum(): print(f"  {th:.1f}      {keep.mean():5.2f}      {accuracy_score(y[keep], p[keep]):.3f}")
# Calibration: when it says ~X% sure, is it right ~X% of the time? (ECE = average gap; 0 is perfect)
bins = np.linspace(1/3, 1, 6); ece = 0
for lo, hi in zip(bins[:-1], bins[1:]):
    m = (c >= lo) & (c <= hi if hi == 1 else c < hi)
    if m.sum(): ece += m.mean() * abs(accuracy_score(y[m], p[m]) - c[m].mean())
print(f"\nexpected calibration error: {ece:.3f}")
