# maximus-transaction-analyst

Turn dense deal correspondence into an executive-quality two-page transaction memo.

## What this skill is for

Private-company transactions generate hundreds of emails, dozens of PDFs, term sheets, closing docs, wire instructions, brokerage forms, trust/SPV paperwork, and revised economics that shift over weeks or months. A sophisticated reader needs to understand the deal without reading the email traffic. This skill produces that memo.

Typical inputs:

- Email exports (mbox, .eml, .pst, forwarded chains)
- PDFs — term sheets, purchase agreements, transfer forms, closing statements
- Attachments — cap tables, wire receipts, KYC packets
- Spreadsheets — pricing waterfalls, fee schedules

Typical outputs:

- Approximately two pages of polished prose
- A compact economics table (tranche, shares, PPS, gross, net)
- Chronology broken into 3–5 logical phases (not email-by-email)
- Explicit separation of established facts, contested allegations, and unresolved items
- A "Bottom Line" with the specific documents or reconciliations still needed

## When to reach for it

- You have inherited a deal folder and need to brief a partner, investor, or counsel in one memo.
- You are auditing a closed transaction and need a defensible reconstruction of what actually happened.
- You are on the buy or sell side and need to reconcile numbers that changed across drafts.
- You are counsel or corporate development and need to understand a dispute's factual spine before drafting a response.

## When not to reach for it

- Public-market transactions with SEC filings as the primary evidence base — use `maximus-deep-research` or `maximus-finance` skills.
- Pure counterparty discovery (finding new potential buyers or sellers) — use `maximus-counterparty-discovery`.
- Investigative reconstruction of an event where no organized deal folder exists — use `maximus-investigative-research`.

## What ships with the skill

- `SKILL.md` — the workflow, default output structure, style rules, transaction-reasoning rules, and quality checks.
- `HOWTO.md` — recipes for common runs: first pass, reconciliation-only pass, dispute memo, appendix generation.
- `examples/` — two worked examples (secondary purchase with repricing, brokerage fee dispute).
- `references/PERPLEXITY_MAXIMUS.md` — portable standing prompt for pasting into a Maximus/Computer session.
- `agents/openai.yaml` — sidecar metadata for OpenAI Assistants integration.

## Discipline the skill enforces

- Sources over speculation — no outside knowledge unless explicitly requested.
- Reconcile, don't select — when numbers change across emails, explain the evolution.
- Attribute contested claims to the speaker (e.g. "Joseph alleged…"), never launder them as facts.
- Executed/latest closing evidence beats early indications for final economics; earlier figures preserved to explain evolution.
- Never mention file-extraction, OCR, or parsing issues in the memo itself.
- Track gross price, seller net price, buyer all-in price, and intermediary fees separately.
- Distinguish buyer of record from underlying investors or LPs; broker/dealer from placement agent from introducer from SPV/trust manager.
