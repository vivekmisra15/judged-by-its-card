"""Ask Jev (TypeSafe AI) to predict each dataset's adoption tier from its card, zero-shot
(no training on our labels). Saves every raw answer so nothing is paid for twice.

  python src/run_jev.py --dry-run     show the first request and a cost estimate; calls nothing
  python src/run_jev.py --limit 20    try 20 cards first
  python src/run_jev.py               run all (skips cards already answered)

Needs TYPESAFE_API_KEY, from your shell or from a git-ignored file named .env containing one line:
  TYPESAFE_API_KEY=your-key-here
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"      # pinned: 'jev-latest' can change under us mid-study
MAX_CHARS = 8000          # long cards are cut here (~2,000 tokens) to bound cost; logged in the output

# The question. The criteria describe the three outcome tiers in plain words WITHOUT
# naming 'likes', so Jev judges from the card rather than from a number it cannot see.
QUESTIONS = {"adoption": {
    "type": "choice",
    "instructions": ("This is the documentation card of a newly published open dataset. About 16 to 21 months "
                     "after release, how much attention will the dataset have attracted from the community?"),
    "criteria": {"low": "Nobody has endorsed it; it is essentially ignored.",
                 "medium": "A handful of people (1 to 4) have endorsed it.",
                 "high": "Five or more people have endorsed it; it is clearly noticed."}}}

def load_key():
    if os.environ.get("TYPESAFE_API_KEY"): return os.environ["TYPESAFE_API_KEY"]
    if os.path.exists(".env"):
        for line in open(".env"):
            line = line.strip().removeprefix("export ")   # allow 'export KEY=...' so the file also works with 'source .env'
            if line.startswith("TYPESAFE_API_KEY="): return line.split("=", 1)[1].strip().strip('"\'')
    return None

def card_text(id_):
    return open("data/cards/" + id_.replace("/", "__") + ".md").read()

def build_request(card):
    state = card[:MAX_CHARS] if card.strip() else "(The dataset has no documentation card at all.)"
    return {"model": MODEL, "state": state, "questions": QUESTIONS}

def call(body, key):
    req = urllib.request.Request(URL, json.dumps(body).encode(),
          {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(5):
        try: return json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529):          # busy: wait and retry
                time.sleep(float(e.headers.get("retry-after", 2 ** attempt))); continue
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:300]}")
    raise RuntimeError("gave up after 5 retries")

ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--limit", type=int)
args = ap.parse_args()
sample = json.load(open("data/sample.json"))
if args.limit: sample = sample[:args.limit]

if args.dry_run:
    chars = sum(min(len(card_text(s["id"])), MAX_CHARS) + 400 for s in sample)
    toks = chars / 4
    print(f"cards: {len(sample)}   est. input tokens: {toks:,.0f}   est. cost: ${toks / 1e6 * 0.042:.3f} (at $0.042 per million)")
    print("first request body (state shortened):")
    b = build_request(card_text(sample[0]["id"])); b["state"] = b["state"][:300] + " ..."
    print(json.dumps(b, indent=1)); sys.exit()

key = load_key()
if not key: sys.exit("No TYPESAFE_API_KEY found (shell or .env). Nothing was sent.")
os.makedirs("results", exist_ok=True); out_path = "results/jev_raw.jsonl"
done = {json.loads(l)["id"] for l in open(out_path)} if os.path.exists(out_path) else set()
with open(out_path, "a") as out:
    for i, s in enumerate(sample):
        if s["id"] in done: continue
        card = card_text(s["id"])
        try: resp = call(build_request(card), key)
        except RuntimeError as e: print("FAILED", s["id"], e); continue
        out.write(json.dumps({"id": s["id"], "truncated": len(card) > MAX_CHARS, "response": resp}) + "\n"); out.flush()
        if (i + 1) % 25 == 0: print(i + 1, "done", flush=True)
print("finished")
