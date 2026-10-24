"""Build the pilot sample: stratified by likes tier, max 3 per publisher,
with each card as it stood 7 days after creation, plus publisher fame."""
import json, random, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

PER_TIER, MAX_PER_AUTHOR, SEED = 167, 3, 1
API = "https://huggingface.co/api"

def tier(likes):  # the pre-registered outcome
    return "low" if likes == 0 else "medium" if likes < 5 else "high"

def fetch(url, as_json=True):
    for _ in range(3):
        try:
            body = urllib.request.urlopen(url, timeout=30).read()
            return json.loads(body) if as_json else body.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404): return None
            time.sleep(3)
        except Exception:
            time.sleep(3)
    return None

def parse(s): return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")

def first_week_card(row):
    id_, created = row["id"], parse(row["createdAt"])
    commits, p = [], 0
    while True:
        page = fetch(f"{API}/datasets/{id_}/commits/main?p={p}")
        if not page: break
        commits += page; p += 1
        if len(page) < 50 or p > 20: break
    if not commits: return None                      # inaccessible
    early = [c for c in commits if parse(c["date"]) <= created + timedelta(days=7)]
    if not early: return None                        # history does not reach back to week 1
    text = fetch(f"https://huggingface.co/datasets/{id_}/raw/{early[0]['id']}/README.md", as_json=False)
    return text or ""                                # "" = no card at all in week 1

authors = {}
def author_info(name):
    if name not in authors:
        d = fetch(f"{API}/organizations/{name}/overview")
        is_org = d is not None
        if d is None: d = fetch(f"{API}/users/{name}/overview") or {}
        authors[name] = {"followers": d.get("numFollowers", 0) or 0, "is_org": is_org}
    return authors[name]

rows = [json.loads(l) for l in open("data/h1_2025_all.jsonl")]
random.seed(SEED); random.shuffle(rows)
by_tier = {"low": [], "medium": [], "high": []}
for r in rows: by_tier[tier(r.get("likes") or 0)].append(r)
print({k: len(v) for k, v in by_tier.items()}, flush=True)

def pick(cands):
    out, per_author = [], {}
    def work(r): return r, first_week_card(r)
    # over-fetch in chunks until we have PER_TIER valid cards
    i = 0
    while len(out) < PER_TIER and i < len(cands):
        chunk = []
        while len(chunk) < 60 and i < len(cands):
            r = cands[i]; i += 1
            if per_author.get(r["author"], 0) < MAX_PER_AUTHOR:
                per_author[r["author"]] = per_author.get(r["author"], 0) + 1; chunk.append(r)
        with ThreadPoolExecutor(8) as ex:
            for r, card in ex.map(work, chunk):
                if card is None:
                    per_author[r["author"]] -= 1; continue
                if len(out) < PER_TIER: out.append((r, card))
    return out

import os; os.makedirs("data/cards", exist_ok=True)
sample = []
for t, cands in by_tier.items():
    got = pick(cands)
    print(t, len(got), flush=True)
    for r, card in got:
        open("data/cards/" + r["id"].replace("/", "__") + ".md", "w").write(card)
        sample.append({"id": r["id"], "author": r["author"], "created": r["createdAt"],
                       "likes": r["likes"], "downloads": r.get("downloadsAllTime", 0), "tier": t})
with ThreadPoolExecutor(8) as ex: list(ex.map(author_info, {s["author"] for s in sample}))
for s in sample: s.update(authors[s["author"]])
json.dump(sample, open("data/sample.json", "w"), indent=1)
print("saved", len(sample))
