# HOWTO — maximus-transaction-analyst

Six invocations you'll actually use. Copy-paste-ready.

## Recipe 1 — First-pass two-page memo

The default. Use when you're handed a deal folder and need the standing memo.

```
Maximus: load `maximus-transaction-analyst`. Analyze this transaction folder and give me the two-page executive summary. Include the compact economics table. Do not mention file-extraction, OCR, or parsing issues in the memo.
```

Expected output: title + Executive Summary + Economics table + How the Transaction Developed + Why the Transaction Became Difficult + Fee/Commercial Dispute (if applicable) + Bottom Line.

## Recipe 2 — Reconciliation-only pass

Use when the memo already exists and you need every fee, wire, and share count reconciled against the underlying evidence.

```
Maximus: load `maximus-transaction-analyst`. Skip the executive narrative. For this transaction folder, produce a reconciliation table with columns: item (share block, fee, wire), amount as first stated, amount as revised, amount as finally documented, source email/PDF (with date and sender), and my reconciliation note. Flag every number that appears in only one source.
```

## Recipe 3 — Chronology / timeline appendix

Use as a follow-up to Recipe 1 when a reader wants the email-level trail without cluttering the memo.

```
Maximus: load `maximus-transaction-analyst`. Add a one-page chronology appendix to the memo, dated bullet by dated bullet, from first contact to current status. Each bullet: date, actor(s), one-sentence description, and the source (filename or email subject).
```

## Recipe 4 — Sources-and-evidence appendix

Use when the memo is going to counsel or a partner who needs to see what's behind each claim.

```
Maximus: load `maximus-transaction-analyst`. For every material claim in the memo, produce a sources-and-evidence appendix. Table columns: claim (verbatim from memo), source (filename or email subject + date), source type (executed doc / draft / email assertion / wire receipt / third-party), and confidence (established / contested / single-sourced).
```

## Recipe 5 — Dispute memo

Use when the transaction closed (or partially closed) but there is a live fee, commission, or performance dispute.

```
Maximus: load `maximus-transaction-analyst`. Skip the deal narrative. Produce a dispute memo covering: what each side claims, what each side's stated basis is, what documents support each side, what documents contradict each side, and what specific evidence (a wire receipt, a signed engagement letter, a countersigned amendment) would resolve the dispute. Attribute every allegation to the speaker.
```

## Recipe 6 — Questions for counsel / broker / buyer

Use after the memo is drafted to generate the specific asks that would close remaining gaps.

```
Maximus: load `maximus-transaction-analyst`. Based on the memo you just produced, draft three separate question lists — for counsel, for the broker or intermediary, and for the buyer (or the buyer's counsel). Each list should target the specific unresolved items or contradictions in the record, not generic diligence questions.
```

## Discipline reminders

- Never present a contested allegation as a fact.
- Never silently pick one number when the record contains several.
- Never mention parsing, OCR, or file-extraction issues in the deliverable.
- Never introduce outside knowledge unless the user asked for research or verification.
- If the source record does not establish something, say so.
