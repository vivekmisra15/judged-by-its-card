"""Pilot baselines: fame only, checklist only, logistic regression on card features + fame.
Same 5-fold cross-validation (repeated 5x) for every method so the comparison is fair."""
import json, math, sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
sys.path.insert(0, "src"); from features import card_features

TIERS = ["low", "medium", "high"]
sample = json.load(open("data/sample.json"))
rows = []
for s in sample:
    card = open("data/cards/" + s["id"].replace("/", "__") + ".md").read()
    f = card_features(card); f["log_followers"] = math.log1p(s["followers"]); f["is_org"] = int(s["is_org"])
    rows.append((s, f))
y = np.array([TIERS.index(s["tier"]) for s, _ in rows])

FEATURE_SETS = {
    "fame only":                   ["log_followers", "is_org"],
    "checklist only":              ["checklist"],
    "card features (no fame)":     [k for k in rows[0][1] if k not in ("log_followers", "is_org", "checklist")],
    "card features + fame":        [k for k in rows[0][1] if k != "checklist"],
}
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=1)
results = {"n": len(y), "chance_accuracy": 1/3, "methods": {}}
print(f"n={len(y)}  chance accuracy = 0.333")
for name, cols in FEATURE_SETS.items():
    X = np.array([[f[c] for c in cols] for _, f in rows], float)
    accs, f1s, pred_all = [], [], np.zeros((5, len(y)), int)
    for i, (tr, te) in enumerate(cv.split(X, y)):
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X[tr], y[tr])
        p = m.predict(X[te]); accs.append(accuracy_score(y[te], p)); f1s.append(f1_score(y[te], p, average="macro"))
        pred_all[i // 5, te] = p     # repeat i//5 covers each dataset exactly once
    cm = sum(confusion_matrix(y, pred_all[r], labels=[0, 1, 2]) for r in range(5)) / 5
    results["methods"][name] = {"accuracy": float(np.mean(accs)), "accuracy_sd": float(np.std(accs)),
                                "macro_f1": float(np.mean(f1s)), "confusion_rows_true_cols_pred": cm.round(1).tolist()}
    print(f"{name:26s} acc {np.mean(accs):.3f} ± {np.std(accs):.3f}   macro-F1 {np.mean(f1s):.3f}")

# descriptive facts for the write-up
by = {t: [f for (s, f) in rows if s["tier"] == t] for t in TIERS}
desc = {t: {"empty_card_%": round(100 * (1 - np.mean([f["has_card"] for f in v])), 1),
            "mean_checklist": round(float(np.mean([f["checklist"] for f in v])), 2),
            "mean_followers": round(float(np.mean([math.expm1(f["log_followers"]) for f in v])), 1),
            "median_words": round(float(np.median([math.expm1(f["log_words"]) for f in v])))} for t, v in by.items()}
results["by_tier"] = desc
for t, d in desc.items(): print(t, d)
json.dump(results, open("results/pilot_baselines.json", "w"), indent=1)
