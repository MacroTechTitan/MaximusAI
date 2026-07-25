#!/usr/bin/env python3
"""Score an email candidate using the Maximus baseline scoring model.

Illustrative reference implementation. Real production use should log every
signal to an audit trail and gate on suppression + bounce histories.

Usage:
    python score_email.py --json '{...}'

Input JSON schema (all keys optional; missing = neutral):
    {
      "exact_match_official": bool,
      "exact_match_credible_public": bool,
      "authorized_provider_match": bool,
      "dominant_pattern_match": bool,
      "pattern_examples_count": int,
      "strong_identity": bool,
      "strong_domain": bool,
      "mx_valid": bool,
      "smtp_accepted": bool,
      "prior_verification": bool,
      "catch_all": bool,
      "stale_employment": bool,
      "conflicting_employer": bool,
      "conflicting_patterns": bool,
      "single_weak_pattern_example": bool,
      "role_address": bool,
      "personal_email_not_business": bool,
      "suppression_hit": bool
    }
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass


@dataclass
class Signals:
    exact_match_official: bool = False
    exact_match_credible_public: bool = False
    authorized_provider_match: bool = False
    dominant_pattern_match: bool = False
    pattern_examples_count: int = 0
    strong_identity: bool = False
    strong_domain: bool = False
    mx_valid: bool = False
    smtp_accepted: bool = False
    prior_verification: bool = False
    catch_all: bool = False
    stale_employment: bool = False
    conflicting_employer: bool = False
    conflicting_patterns: bool = False
    single_weak_pattern_example: bool = False
    role_address: bool = False
    personal_email_not_business: bool = False
    suppression_hit: bool = False


def score(s: Signals) -> tuple[int, str, list[str]]:
    if s.suppression_hit:
        return 0, "SUPPRESSED", ["Suppression-list match — disqualified."]

    raw = 0
    reasons: list[str] = []

    def add(delta: int, why: str) -> None:
        nonlocal raw
        raw += delta
        reasons.append(f"{delta:+d}  {why}")

    if s.exact_match_official:
        add(45, "Exact match on official company source")
    if s.exact_match_credible_public:
        add(35, "Exact match on credible public source")
    if s.authorized_provider_match:
        add(30, "Authorized provider match")
    if s.dominant_pattern_match:
        add(20, "Dominant observed company pattern")
    if s.pattern_examples_count >= 3:
        add(10, "≥3 recent pattern examples")
    if s.strong_identity:
        add(10, "Strong identity match")
    if s.strong_domain:
        add(10, "Strong company-domain match")
    if s.mx_valid:
        add(5, "Valid MX records")
    if s.smtp_accepted and not s.catch_all:
        add(10, "SMTP accepted (non-catch-all)")
    if s.prior_verification:
        add(5, "Prior successful verification")

    if s.catch_all:
        add(-25, "Catch-all domain")
    if s.stale_employment:
        add(-20, "Stale employment")
    if s.conflicting_employer:
        add(-25, "Conflicting employer")
    if s.conflicting_patterns:
        add(-10, "Conflicting patterns")
    if s.single_weak_pattern_example:
        add(-10, "Only one weak pattern example")
    if s.role_address:
        add(-20, "Role address")
    if s.personal_email_not_business:
        add(-30, "Personal email instead of business email")

    normalized = max(0, min(100, raw))

    # Classify
    if s.exact_match_official:
        status = "PUBLICLY_CONFIRMED"
    elif normalized >= 80 and s.mx_valid and s.smtp_accepted and not s.catch_all:
        status = "VALID"
    elif normalized >= 65 and s.mx_valid:
        status = "LIKELY_VALID" if not s.catch_all else "LIKELY_VALID"
    elif s.catch_all:
        status = "CATCH_ALL"
    elif s.conflicting_employer or s.stale_employment:
        status = "RISKY"
    elif not s.mx_valid:
        status = "INVALID"
    else:
        status = "UNKNOWN"

    return normalized, status, reasons


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default=None, help="Signals as a JSON string. If omitted, read stdin.")
    args = ap.parse_args()

    payload = args.json or sys.stdin.read()
    data = json.loads(payload)
    s = Signals(**{k: v for k, v in data.items() if k in Signals.__annotations__})
    normalized, status, reasons = score(s)

    print(json.dumps({
        "confidence": normalized,
        "status": status,
        "reasons": reasons,
    }, indent=2))


if __name__ == "__main__":
    main()
