# Maximus grows to 43 — adding the Transaction Analyst

*2026-08-13 · Macro Tech Titan*

Private-company transactions generate hundreds of emails, dozens of PDFs, term sheets, revised drafts, closing documents, wire receipts, brokerage forms, trust or SPV paperwork, and economics that shift over weeks or months. Somewhere in that pile is a coherent story about what actually happened. A partner, a co-investor, a piece of counsel, or a new hire on the deal team needs that story in one sitting — not a folder to read.

Today Maximus gets a skill purpose-built for that job.

## The new skill

**[`maximus-transaction-analyst`](../skills/maximus-transaction-analyst)** — turn a dense deal folder into an executive-quality two-page transaction memo.

The workflow:

1. Ingest every supplied email, attachment, PDF, term sheet, closing document, spreadsheet, and forwarded chain.
2. Deduplicate quoted email history so a forwarded copy is treated as the same underlying communication unless it adds recipients, timestamps, attachments, or new commentary.
3. Build an internal transaction map before drafting — parties, roles, share counts, prices, gross/net economics, fees, wires, key dates, diligence issues, competing bids, disputes, what closed, what didn't, what remains unresolved.
4. Reconcile numerical changes over time. When numbers differ across emails, explain the evolution rather than silently choosing one.
5. Separate established facts from assertions. Attribute contested claims explicitly ("Joseph alleged…") rather than laundering them as facts.
6. Prefer final executed or latest closing documents over earlier indications when determining final economics — while preserving earlier figures to explain how the deal evolved.
7. Never fill factual gaps with outside knowledge unless the user explicitly asks for research or verification.
8. Never mention file-extraction, OCR, PDF portfolio limitations, parsing problems, or software issues in the memo unless asked.

The output is the memo — approximately two pages of polished prose with a Title, Executive Summary, compact Economics table, "How the Transaction Developed" broken into 3–5 logical phases (not email-by-email), "Why the Transaction Became Difficult," Fee or Commercial Dispute if applicable, and a Bottom Line naming the specific documents or reconciliations still needed.

## What makes it different from summarization

A generic "summarize these files" workflow will average the record. It will pick one price, drop the fee-split dispute, and paper over the contradiction between the buyer's counsel's 2026-05-30 email and the broker's 2026-05-30 email. That's a summary. It is not a transaction memo.

`maximus-transaction-analyst` is disciplined on the shapes that matter in real deals:

- **Signed term sheet ≠ funded closing.** A wire instruction ≠ proof funds arrived. An email saying "we're closed" is strong evidence, checked against settlement or transfer evidence when available.
- **Gross price, seller net price, buyer all-in price, and intermediary fees are tracked separately.** They often diverge by tens of thousands of dollars in a mid-sized secondary.
- **Buyer of record is distinguished from underlying investors or LPs.** Broker/dealer, placement agent, introducer, SPV manager, trust manager, and legal counsel are separated when the record supports it.
- **Tranches get their own line.** If a transaction is split into tranches, the memo explains why and shows each tranche's economics separately.
- **Issuer repricing events during the process are called out explicitly.** If a primary round or a market repricing changes the economics mid-deal, the inflection point is on the page.
- **Same-block reconciliation.** If the same certificate or block is disposed across multiple tranches, the total share count is reconciled.

The skill ships with two worked examples that show these disciplines in action — a secondary purchase with mid-process repricing (2 tranches, 40k shares, blended $74 PPS from an original $80), and a brokerage fee dispute where the securities transaction closed cleanly but two intermediaries dispute the fee-split.

## The bundle

- `SKILL.md` — workflow, output structure, style rules, transaction-reasoning rules, quality checks.
- `README.md` — when to reach for it, when not to, what ships with it.
- `HOWTO.md` — six recipes: first-pass memo, reconciliation-only pass, chronology appendix, sources-and-evidence appendix, dispute memo, questions for counsel/broker/buyer.
- `examples/secondary-purchase-with-repricing.md` — worked example with a full economics table and phase-based chronology.
- `examples/brokerage-fee-dispute.md` — worked example of Recipe 5 (dispute memo), including "what evidence would resolve" analysis.
- `references/PERPLEXITY_MAXIMUS.md` — portable standing prompt for pasting into a Maximus/Computer session directly.
- `agents/openai.yaml` — sidecar metadata for OpenAI Assistants integration.

## Where it fits

The suite now has four skills in the "make sense of a lot of material" space, each shaped for a different reader:

- **`maximus-deep-research`** — aggregation across many sources.
- **`maximus-investigative-research`** — narrative reconstruction with source tiers and contradiction hunt.
- **`maximus-literature-review`** — academic synthesis with PRISMA-style flow and GRADE grading.
- **`maximus-transaction-analyst`** — executive transaction memo from a deal folder. **NEW.**

Different audiences, different rigor, same underlying discipline: the record over the guess, the contradiction surfaced not smoothed, the gap named not hidden.

## Reach for it

Load `maximus-transaction-analyst` when you have a deal folder and need to brief a partner, investor, or counsel in one memo. Load it when you have inherited a transaction mid-flight and need a defensible reconstruction of what has happened so far. Load it when you are on the buy or sell side of a private-company transaction with revised economics you need to reconcile.

Details in the [README](../README.md).

**43 skills. 5 pillars. Free forever. No gate.**

The workhorse works.
