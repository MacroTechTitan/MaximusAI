# Worked example — DIY LLM visibility tracker (Perplexity API)

This trace builds a runnable script that queries the Perplexity Sonar API for a 30-prompt set, extracts brand mentions and citations, and appends results to a CSV time series. It follows `HOWTO.md` recipe (b).

**Status: illustrative but runnable.** The script below runs as-is against a real Perplexity API key and a real `prompts.csv`. The brand-matching logic is a simple substring/regex match, which is a reasonable starting point but will need tuning for brand names that collide with common words — see the "Known limitations" section at the end.

## Step 1 — Input file: `prompts.csv`

One row per tracked prompt, matching the structure from `examples/prompt-set-design-trace.md`:

```csv
prompt_id,prompt_text,intent_tier
AW-01,"What are the best AI recruiting tools for mid-size companies?",awareness
CM-01,"HireLogic vs ScreenSmart — which is better for mid-market hiring?",comparison
DC-01,"Does HireLogic integrate with Greenhouse?",decision
```

(Full file has all 30 rows from the worked prompt set; truncated here for readability.)

## Step 2 — The tracker script

```python
"""
llm_visibility_tracker.py

Runnable DIY tracker for maximus-llm-visibility-tracking.
Queries the Perplexity Sonar API for each prompt in prompts.csv,
extracts brand/competitor mentions and citations, and appends
one row per (prompt, run_date) to visibility_log.csv.

Requirements:
    pip install requests

Environment:
    export PERPLEXITY_API_KEY="your-api-key-here"

Usage:
    python llm_visibility_tracker.py --prompts prompts.csv --out visibility_log.csv
"""

import argparse
import csv
import os
import re
import sys
from datetime import datetime, timezone

import requests

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar"  # log the exact model string used — required for reproducibility

# Brands to track: your brand plus named competitors.
# Word-boundary regex avoids matching substrings inside unrelated words.
TRACKED_BRANDS = {
    "YourBrand": re.compile(r"\bYourBrand\b", re.IGNORECASE),
    "HireLogic": re.compile(r"\bHireLogic\b", re.IGNORECASE),
    "ScreenSmart": re.compile(r"\bScreenSmart\b", re.IGNORECASE),
    "TalentPilot": re.compile(r"\bTalentPilot\b", re.IGNORECASE),
    "RecruitIQ": re.compile(r"\bRecruitIQ\b", re.IGNORECASE),
}


def call_perplexity(prompt_text: str, api_key: str) -> dict:
    """Call the Perplexity API once for a single prompt. Returns the raw JSON response."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
    }
    resp = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def extract_answer_and_citations(response_json: dict) -> tuple[str, list[str]]:
    """Pull the answer text and citation URLs out of a Perplexity API response."""
    answer_text = response_json["choices"][0]["message"]["content"]
    citations = response_json.get("citations", [])  # list of URL strings, if present
    return answer_text, citations


def find_mentions(answer_text: str) -> dict:
    """Return {brand_name: True/False} for whether each tracked brand appears in the text."""
    return {brand: bool(pattern.search(answer_text)) for brand, pattern in TRACKED_BRANDS.items()}


def find_citations(citations: list[str], brand_domains: dict) -> dict:
    """
    Return {brand_name: True/False} for whether each brand's domain appears
    in the citation URL list. brand_domains maps brand name -> domain substring.
    """
    result = {}
    for brand, domain in brand_domains.items():
        result[brand] = any(domain.lower() in url.lower() for url in citations)
    return result


def estimate_position(answer_text: str, brand: str) -> str:
    """
    Rough position heuristic: where in the answer does the brand first appear,
    by character offset, bucketed into first-third / middle-third / last-third.
    This is a heuristic, not a definitive position label — spot-check manually
    for any prompt that drives a reporting or alerting decision.
    """
    match = TRACKED_BRANDS[brand].search(answer_text)
    if not match:
        return "not_mentioned"
    offset_ratio = match.start() / max(len(answer_text), 1)
    if offset_ratio < 0.33:
        return "first_third"
    elif offset_ratio < 0.66:
        return "middle_third"
    else:
        return "last_third"


def run_tracker(prompts_path: str, out_path: str, api_key: str) -> None:
    brand_domains = {
        "YourBrand": "yourbrand.com",
        "HireLogic": "hirelogic.com",
        "ScreenSmart": "screensmart.com",
        "TalentPilot": "talentpilot.com",
        "RecruitIQ": "recruitiq.com",
    }

    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run_timestamp = datetime.now(timezone.utc).isoformat()

    file_exists = os.path.exists(out_path)
    with open(prompts_path, newline="", encoding="utf-8") as infile, \
         open(out_path, "a", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = [
            "run_date", "run_timestamp", "model", "prompt_id", "prompt_text",
            "intent_tier", "brand", "mentioned", "cited", "position",
            "raw_answer_text",
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for row in reader:
            prompt_id = row["prompt_id"]
            prompt_text = row["prompt_text"]
            intent_tier = row["intent_tier"]

            try:
                response_json = call_perplexity(prompt_text, api_key)
            except requests.RequestException as exc:
                print(f"[WARN] API call failed for {prompt_id}: {exc}", file=sys.stderr)
                continue

            answer_text, citations = extract_answer_and_citations(response_json)
            mentions = find_mentions(answer_text)
            cited = find_citations(citations, brand_domains)

            for brand in TRACKED_BRANDS:
                position = estimate_position(answer_text, brand) if mentions[brand] else "not_mentioned"
                writer.writerow({
                    "run_date": run_date,
                    "run_timestamp": run_timestamp,
                    "model": MODEL,
                    "prompt_id": prompt_id,
                    "prompt_text": prompt_text,
                    "intent_tier": intent_tier,
                    "brand": brand,
                    "mentioned": mentions[brand],
                    "cited": cited[brand],
                    "position": position,
                    "raw_answer_text": answer_text.replace("\n", " ")[:2000],
                })

            print(f"[OK] {prompt_id} done — mentions: {[b for b, v in mentions.items() if v]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DIY LLM visibility tracker (Perplexity API)")
    parser.add_argument("--prompts", default="prompts.csv", help="Path to prompt-set CSV")
    parser.add_argument("--out", default="visibility_log.csv", help="Path to append-only output CSV")
    args = parser.parse_args()

    key = os.environ.get("PERPLEXITY_API_KEY")
    if not key:
        print("ERROR: set PERPLEXITY_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    run_tracker(args.prompts, args.out, key)
```

## Step 3 — Running it

```bash
export PERPLEXITY_API_KEY="pplx-your-key-here"
python llm_visibility_tracker.py --prompts prompts.csv --out visibility_log.csv
```

Each run appends new rows to `visibility_log.csv` — never overwrites. That file is the raw methodology log referenced in `SKILL.md`'s Methodology transparency section: it carries the model string, run timestamp, exact prompt text, and full answer text alongside the extracted metrics, so any number in a later report is traceable back to the exact API call that produced it.

## Step 4 — Turning the log into weekly metrics

A short follow-up aggregation step (pandas, a notebook, or a spreadsheet pivot) computes, per brand per week:

- `citation_rate = count(cited == True) / count(*)`
- `mention_rate = count(mentioned == True) / count(*)`
- `position distribution` = value_counts on the `position` column, mentioned rows only

This aggregation is intentionally kept out of the tracker script — keep collection and analysis as separate steps so the raw log stays a stable source of truth even as reporting logic evolves.

## Known limitations (read before relying on this in production)

- **Substring/regex brand matching** will miss mentions phrased indirectly ("the company behind X product") and can false-positive on brand names that double as common words — test the regex against a sample of real answers before trusting the numbers.
- **Position heuristic is character-offset-based**, not semantically aware of list structure (e.g., "#1 in a ranked list" vs. "mentioned in a footnote") — for any prompt that feeds an alert or a leadership report, spot-check the raw answer text manually rather than trusting the automated position label alone.
- **Sentiment is not automated in this script.** The worked pattern here only covers mention/citation/position. Add an LLM-based classification pass (a second API call asking a model to label sentiment) or manual tagging before reporting sentiment trends — do not skip this dimension per `SKILL.md`'s anti-patterns.
- **Single-engine only.** This script covers Perplexity's Sonar API. Tracking ChatGPT, Claude, Gemini, or Google AI Overviews requires separate API integrations (or manual runs for surfaces without a public API, like AI Overviews) — log each engine's results with the engine name in the `model` field, never merge them into one undifferentiated number.
