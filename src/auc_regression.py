"""EXPLORATORY (decided after seeing results, so not a finding): the regression's AUC for high-vs-rest,
so Jev's 0.757 can be compared on the same footing. Free: no API calls.
Same 5-fold x 5 repeat cross-validation as baselines.py; each dataset is scored only by models that never saw it."""
import json, math, sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
sys.path.insert(0, "src"); from features import card_features

TIERS = ["low", "medium", "high"]
sample = json.load(open("data/sample.json"))
rows = []
for s in sample:
    card = open("data/cards/" + s["id"].replace("/", "__") + ".md").read()
    f = card_features(card); f["log_followers"] = math.log1p(s["followers"]); f["is_org"] = int(s["is_org"])
    rows.append(f)
y = np.array([TIERS.index(s["tier"]) for s in sample])
high = (y == 2).astype(int)

FEATURE_SETS = {
    "fame only":            ["log_followers", "is_org"],
    "card features (no fame)": [k for k in rows[0] if k not in ("log_followers", "is_org", "checklist")],
    "card features + fame": [k for k in rows[0] if k != "checklist"],
}
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=1)   # same seed as baselines.py
for name, cols in FEATURE_SETS.items():
    X = np.array([[f[c] for c in cols] for f in rows], float)
    aucs = []
    score = np.zeros((5, len(y)))
    for i, (tr, te) in enumerate(cv.split(X, y)):
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X[tr], y[tr])
        score[i // 5, te] = m.predict_proba(X[te])[:, 2]      # chance of the "high" tier
    for r in range(5):
        aucs.append(roc_auc_score(high, score[r]))
    print(f"{name:26s} AUC high-vs-rest {np.mean(aucs):.3f} ± {np.std(aucs):.3f}")
