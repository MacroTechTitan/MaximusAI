# Worked example: single-person lookup

End-to-end trace of finding a work email from a LinkedIn URL. Names, domains, and evidence are illustrative — the workflow is real.

## Input

```
linkedin_url: https://www.linkedin.com/in/janedoe-pm?trk=...abc123
full_name: (not supplied)
current_company: (not supplied)
job_title: (not supplied)
```

## Step 1 — Normalize the LinkedIn URL

Stripped tracking params and trailing slash:

- Canonical: `https://www.linkedin.com/in/janedoe-pm`
- Original preserved for provenance.

## Step 2 — Identity

From public LinkedIn preview + a 2026 conference bio:

- Full name: Jane M. Doe
- Current title: VP Product
- Current company: Acme Robotics, Inc.
- Location: Austin, TX

Second corroborating source: [Acme Robotics — Team](https://acmerobotics.example/team) shows "Jane Doe, VP Product". Identity confidence: 90.

## Step 3 — Employment currency

- Acme team page dated 2026-06 confirms current.
- No conflicting employer in the last 6 months.

Employment currency: current, high confidence.

## Step 4 — Email domain resolution

- Website: `acmerobotics.example`.
- MX lookup returns `*.mail.protection.outlook.com` — Microsoft 365 tenant. Domain confidence: 92.
- Contact page publishes `press@acmerobotics.example` and `careers@acmerobotics.example`, which confirms `acmerobotics.example` is the mail domain.
- No alternate domain (subsidiary or acquired brand) detected.

Selected domain: `acmerobotics.example`.

## Step 5 — Exact-email search

Queries run:

```
"Jane Doe" "@acmerobotics.example"
site:acmerobotics.example "Jane Doe"
site:acmerobotics.example "jane.doe"
filetype:pdf "Jane Doe" "acmerobotics"
```

Results: A 2026-03 press release PDF from Acme lists a media contact block:

> "Media contact: Jane Doe, VP Product — jane.doe@acmerobotics.example — 512-555-0142"

**Exact email observed on an official company source.** Candidate: `jane.doe@acmerobotics.example`, evidence-tier: `PUBLICLY_CONFIRMED`.

## Step 6 — Company email format

Observed public emails at the domain (recent 12 months):

| Employee | Email | Pattern |
|---|---|---|
| Sarah Kim | sarah.kim@acmerobotics.example | first.last |
| Rahul Mehta | rahul.mehta@acmerobotics.example | first.last |
| Priya Chen | priya.chen@acmerobotics.example | first.last |
| Media contact block (Jane Doe) | jane.doe@acmerobotics.example | first.last |

Dominant pattern: `first.last`. Sample count: 4. No conflicting pattern observed. Pattern confidence: 90.

## Step 7 — Name normalization

- First: Jane
- Middle: M. (initial only, not used unless collision)
- Surname: Doe (no compounding, no accents)
- No suffix or professional alternate.

Candidate local-part from dominant pattern: `jane.doe`.

## Step 8 — Candidate generation

1. `jane.doe@acmerobotics.example` — exact public match + dominant pattern
2. `jdoe@acmerobotics.example` — common secondary
3. `jane@acmerobotics.example` — first-only variant
4. `janedoe@acmerobotics.example` — concatenated variant

No personal-domain candidates.

## Step 9 — Verification (candidate 1)

| Check | Result |
|---|---|
| Syntax | Valid |
| Domain | Resolves |
| MX | Present (Microsoft 365) |
| Disposable | No |
| Role | No |
| Catch-all | No (probed with random local-part → 550) |
| SMTP | 250 OK on `jane.doe@acmerobotics.example` |
| Historical | Not previously verified |
| Bounce | No bounce history |
| Suppression | Not on list |

## Step 10 — Scoring (candidate 1)

- Exact match on official company source: +45
- Dominant observed company pattern: +20
- ≥3 recent pattern examples: +10
- Strong identity match: +10
- Strong company-domain match: +10
- Valid MX: +5
- SMTP accepted (non-catch-all): +10

Raw total: 110 → normalized to **95**.

## Step 11 — Classification

Status: **PUBLICLY_CONFIRMED** (exact email on an official source; independently verified).

## Step 12 — Response

```
PROFESSIONAL EMAIL RESULT

Name: Jane M. Doe
LinkedIn: https://www.linkedin.com/in/janedoe-pm
Current title: VP Product
Current company: Acme Robotics, Inc.
Company domain: acmerobotics.example

Best email: jane.doe@acmerobotics.example
Status: PUBLICLY_CONFIRMED
Confidence: 95

Why this result ranked first:
- identity evidence: LinkedIn profile + Acme team page (2026-06)
- domain evidence: MX = Microsoft 365; contact page uses acmerobotics.example
- pattern evidence: 4 recent examples of first.last, no conflicts
- verification evidence: MX valid, catch-all=false, SMTP 250 on non-catch-all

Company email format: first.last
Pattern confidence: 90
Observed examples: 4 recent (Kim, Mehta, Chen, Doe)

Verification:
- Syntax: pass
- Domain: pass
- MX: pass (Microsoft 365)
- SMTP: 250 OK
- Catch-all: false
- Role account: false
- Suppression status: clear
- Last verified: 2026-07-23

Sources:
1. Acme Robotics press release (2026-03) — https://acmerobotics.example/press/2026-03-launch.pdf — verbatim media contact block with the exact email
2. Acme Robotics team page — https://acmerobotics.example/team — confirms current title and employment
3. LinkedIn profile — https://www.linkedin.com/in/janedoe-pm — identity anchor

Alternative candidates:
1. jdoe@acmerobotics.example — RISKY — 52 — no observed examples of flast pattern at this domain
2. jane@acmerobotics.example — RISKY — 40 — likely collides with other Janes; not observed

Warnings:
- None. Publicly confirmed and independently verified.
```

## Summary

The exact email `jane.doe@acmerobotics.example` is publicly confirmed on an official Acme Robotics press release and independently verified via MX + SMTP on a non-catch-all domain. Confidence 95.
