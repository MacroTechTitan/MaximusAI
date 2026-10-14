#!/usr/bin/env python3
"""ILLUSTRATIVE: not run against a live server by the scout. Request and
response shapes follow the Ollama System One docs. Set BASE to your runtime
(Ollama :11434 or llama-server :8080) and CUTOFF from calibrate_threshold.py."""
import json, os, urllib.request

BASE = os.environ.get("SYSTEMONE_BASE", "http://localhost:11434")
MODEL = os.environ.get("SYSTEMONE_MODEL", "nimble")
CUTOFF = float(os.environ.get("CUTOFF", "0.80"))

def decide(ticket: str) -> dict:
    body = {
        "model": MODEL,
        "state": ticket,
        "questions": {
            "team": {"type": "choice", "instructions": "Which team should handle this ticket?",
                     "criteria": {"billing": "Payments, charges, refunds, invoices",
                                  "bug": "Software errors and outages",
                                  "account": "Login and account access"}},
            "urgent": {"type": "noul", "instructions": "Is a critical service unavailable?"},
        },
    }
    req = urllib.request.Request(f"{BASE}/v1/systemone", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        a = json.load(r)["answers"]
    team = a["team"]
    route = team["choice"] if team["confidence"] >= CUTOFF else "human-queue"
    return {"route": route, "confidence": team["confidence"], "urgent_p": a["urgent"]["noul"]}

if __name__ == "__main__":
    print(decide("Our checkout has returned 500 errors since 9am."))
