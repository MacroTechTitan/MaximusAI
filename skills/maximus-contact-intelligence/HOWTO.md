# How to use maximus-contact-intelligence

Six recipes for common contact-intelligence jobs. Each recipe produces a `PROFESSIONAL EMAIL RESULT` block or a clearly labeled "no reliable email" answer.

## Recipe 1: Single-person lookup from a LinkedIn URL

**Goal:** Find the work email for one person from a LinkedIn URL.

1. Normalize the LinkedIn URL (strip trackers and trailing slashes).
2. Confirm identity: name, current company, current title.
3. Confirm current employment via a second source (company team page, press release, conference bio, filing).
4. Resolve the email domain — do not assume `website.com` = `email domain`. Check MX records.
5. Search public sources for an exact email (`"Full Name" "@companydomain.com"`, `site:` and `filetype:pdf` variants).
6. If no exact hit, discover the company's email pattern from 3+ recent public employee emails.
7. Normalize the person's name and generate up to 10 candidates.
8. Verify each candidate: syntax, domain, MX, disposable check, role check, catch-all, SMTP if available, suppression list.
9. Score every candidate and select the top one only if confidence ≥ 70.
10. Return the full `PROFESSIONAL EMAIL RESULT` block with sources.

## Recipe 2: Enrich a CRM list

**Goal:** Enrich a list of 50 CRM rows with verified emails.

1. Group rows by company domain to amortize domain and pattern research.
2. For each unique domain, run pattern discovery once and cache the dominant pattern with example count and recency.
3. Loop each row through Recipe 1, reusing the cached pattern.
4. Flag rows with `CATCH_ALL`, `RISKY`, `UNVERIFIABLE`, or `UNKNOWN` status separately.
5. Export a CSV with columns: `linkedin_url`, `best_email`, `status`, `confidence`, `domain`, `pattern_used`, `evidence_url`, `verification_summary`, `warnings`, `last_verified_at`.
6. Never mark a catch-all row as verified. Suppression-list hits are disqualified from export.

See `examples/list-enrichment-trace.md` for a worked example.

## Recipe 3: Pattern discovery for a target company

**Goal:** Discover the dominant email format for a specific company before running lookups.

1. Search public sources for 5–10 credible employee emails at the domain.
2. Extract the local-part for each and normalize against the corresponding employee's name.
3. Classify each into a pattern (`first.last`, `flast`, `first`, etc.).
4. Report: dominant pattern, secondary pattern (if any), example count per pattern, recency, and whether different departments diverge (support@, sales@ vs engineering).
5. Store as a cached artifact for downstream Recipe 1/2 runs.

## Recipe 4: Ambiguous identity

**Goal:** The LinkedIn URL resolves to multiple plausible candidates, or the profile is generic.

1. Do not guess. Return "Identity requires clarification."
2. List each distinguishing signal you'd need to resolve the ambiguity (middle initial, prior employer, city, university).
3. Suggest a follow-up query to the requester.
4. Do not generate candidate emails until identity is resolved.

## Recipe 5: Catch-all domain handling

**Goal:** The company mail server accepts everything, so SMTP acceptance proves nothing.

1. Detect catch-all via a verification probe against a nonsense mailbox.
2. Mark the domain `catch_all=true` in your pattern cache.
3. Cap SMTP-based scoring: SMTP acceptance adds 0 (not +10) when catch-all is true.
4. Apply the -25 catch-all penalty.
5. Rely on: exact public matches, dominant pattern with strong evidence, and identity strength.
6. Status can only reach `LIKELY_VALID` — never `VALID` — from a catch-all domain unless the exact email appears on an official public source.

## Recipe 6: LinkedIn-only, no company domain yet

**Goal:** You have a LinkedIn URL and no known company domain.

1. Confirm identity + current company from the profile and one independent source.
2. Resolve the company's website and check MX records; also check `Sender Policy Framework (SPF)` and `DMARC` records — they often reveal the actual sending domain.
3. Check the company's Contact / About page and staff bios for exposed emails.
4. If MX points to a mail provider (Google Workspace, Microsoft 365, Zoho, Proofpoint), record that as an authorized-provider match signal.
5. Once the domain is resolved with confidence ≥ 70, proceed to Recipe 1 from Step 5.

## Cross-skill combos

- **Before this skill:** run `maximus-people-finder` or `maximus-people-finder-recruiter` when you don't yet have a LinkedIn URL.
- **After this skill:** hand off approved contacts to `maximus-fintech-payments` for onboarding, or to your outreach tool of choice.
- **When identity is thin:** delegate identity triangulation to `maximus-deep-research-pro` before returning here.
- **For compliance-heavy work:** if the person is being contacted as a financial counterparty, route through `maximus-counterparty-discovery` first — it has the compliance gate this skill assumes has already been passed.
