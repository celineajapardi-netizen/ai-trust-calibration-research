"""
Generate FAKE participant data so you can test analysis.py before real data exists.

    python analysis/make_fake_data.py        (python3 on Mac)

Writes data/responses.csv (overwrites it!). Delete the fake file before
collecting real responses.
"""
from __future__ import annotations

import csv
import os
import random
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiment"))
from questions import QUESTIONS  # noqa: E402
from app import assign_presentation  # noqa: E402  (same assignment logic as the real app)

OUT = os.path.join(ROOT, "data", "responses.csv")
N_PARTICIPANTS = 60

# Made-up tendencies so the fake graphs look plausible. Real data will be whatever it is.
DETECT_PROB = {  # chance the participant judges the answer correctly
    ("Correct", "polished"): 0.90,
    ("Correct", "plain"): 0.75,
    ("Incorrect", "polished"): 0.35,   # polished wrong answers fool people
    ("Incorrect", "plain"): 0.55,
}
BASE_TRUST = {
    ("Correct", "polished"): 4.2,
    ("Correct", "plain"): 3.2,
    ("Incorrect", "polished"): 3.9,    # over-trust
    ("Incorrect", "plain"): 2.9,
}


def clamp(x, lo=1, hi=5):
    return max(lo, min(hi, int(round(x))))


def main():
    random.seed(42)
    rows = []
    for _ in range(N_PARTICIPANTS):
        pid = f"P{random.randint(100000, 999999)}"
        pres = assign_presentation()
        order = list(QUESTIONS)
        random.shuffle(order)
        for pos, q in enumerate(order, start=1):
            cell = (q["actual"], pres[q["id"]])
            detects = random.random() < DETECT_PROB[cell]
            if detects:
                judgment = q["actual"]
            else:
                judgment = "Unsure" if random.random() < 0.3 else ("Correct" if q["actual"] == "Incorrect" else "Incorrect")
            trust = clamp(random.gauss(BASE_TRUST[cell] - (1.2 if judgment == "Incorrect" else 0), 0.8))
            confidence = clamp(random.gauss(3.5 if detects else 3.1, 0.9))
            reliance = "Yes" if trust >= 4 else ("No" if trust <= 2 else random.choice(["Yes", "No", "Unsure"]))
            rows.append(
                {
                    "participant_id": pid,
                    "position": pos,
                    "question_id": q["id"],
                    "topic": q["topic"],
                    "actual": q["actual"],
                    "presentation": pres[q["id"]],
                    "judgment": judgment,
                    "confidence": confidence,
                    "trust": trust,
                    "reliance": reliance,
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                }
            )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} fake rows for {N_PARTICIPANTS} participants to {OUT}")


if __name__ == "__main__":
    main()
