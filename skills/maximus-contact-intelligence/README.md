# maximus-contact-intelligence

Find the most likely professional business email address for a person, given a LinkedIn URL or equivalent identity data — with provenance, verification, and confidence scoring. Never guess-as-fact.

## What it does

Turns an input like *"LinkedIn profile of Jane Doe, VP Product at Acme"* into a structured `PROFESSIONAL EMAIL RESULT` that includes:

1. Canonical LinkedIn URL and identity resolution.
2. Current-company confirmation from independent public sources (not just LinkedIn).
3. Company email-domain resolution via website, MX records, filings, and known employee emails.
4. Public-source search for an exact email match.
5. Company email-pattern discovery from observed employee emails.
6. Name normalization (compound surnames, apostrophes, accents, nicknames, married names).
7. Up to 10 ranked candidate emails.
8. Verification: syntax, domain, MX, disposable, role, catch-all, SMTP (when available), suppression list.
9. Scored confidence 0–100.
10. Classified status: `PUBLICLY_CONFIRMED`, `VALID`, `LIKELY_VALID`, `CATCH_ALL`, `UNVERIFIABLE`, `RISKY`, `INVALID`, `SUPPRESSED`, `UNKNOWN`.

Returns a best email only when confidence ≥ 70 and identity + employer are resolved. Otherwise says so.

## When to trigger

- "Find the work email for [LinkedIn URL]"
- "What's the corporate email for [name] at [company]?"
- "Enrich this CRM row with a verified email"
- "Discover the email pattern for [company]"
- Any request that combines identity + business email + verification

## When NOT to use

- Finding a person from scratch → use `maximus-people-finder` or `maximus-people-finder-recruiter` first
- Personal, residential, or family contact data → not supported
- Counterparty due-diligence exports → use `maximus-counterparty-discovery`
- Defeating access controls, CAPTCHAs, robots directives, or auth → forbidden

## What ships in this skill

- `SKILL.md` — full instructions and workflow
- `README.md` — this file
- `HOWTO.md` — 6 recipes covering common jobs (single lookup, batch, pattern discovery, ambiguous identity, catch-all handling, list enrichment)
- `examples/single-lookup-trace.md` — one-person walkthrough end to end
- `examples/list-enrichment-trace.md` — batch enrichment of a small CRM list
- `references/email-patterns.md` — pattern taxonomy and edge cases
- `references/verification-checks.md` — what each verification check proves and does not prove
- `references/authorized-use-and-privacy.md` — legal and ethical boundaries in one place
- `scripts/generate_candidates.py` — reproducible candidate generator from name + pattern
- `scripts/score_email.py` — reproducible scoring per the baseline model

## Guardrails (short version)

- Legitimate business use only.
- No breached credentials, hidden LinkedIn content, or bypassed access controls.
- Never send a test email; verification is passive.
- Catch-all domains are never labeled as verified.
- Confidence < 70 → return "No sufficiently reliable professional email was found."
- Suppression-list match → disqualify.
- All claims cite a source URL and observation date.

Full rules in `references/authorized-use-and-privacy.md`.

## Related skills

- [`maximus-people-finder`](../maximus-people-finder) — find the person first
- [`maximus-people-finder-recruiter`](../maximus-people-finder-recruiter) — recruiter workflow
- [`maximus-counterparty-discovery`](../maximus-counterparty-discovery) — finance-grade discovery + compliance gate
- [`maximus-deep-research-pro`](../maximus-deep-research-pro) — inference-driven triangulation
- [`maximus-brain`](../maximus-brain) — depth calibration
