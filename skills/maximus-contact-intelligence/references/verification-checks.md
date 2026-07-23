# Verification checks — what they prove and don't prove

Reference for Step 9 of the workflow. Each check has clear semantics; do not overstate what any single check demonstrates.

## Syntax validation

**What it does:** Checks that the string is a valid email per RFC 5321/5322 (local-part length, allowed characters, single @, valid domain shape).

**Proves:** Structurally parseable.
**Does not prove:** The domain exists, the mailbox exists, or the mail server accepts mail.

**Pass:** +0 (baseline). **Fail:** disqualify with status `INVALID`.

## Domain validation

**What it does:** Confirms the domain resolves via DNS.

**Proves:** The domain is registered and has DNS records.
**Does not prove:** The domain accepts mail or corresponds to the intended entity.

**Fail:** disqualify with status `INVALID`.

## MX validation

**What it does:** Confirms the domain has MX (Mail Exchange) records.

**Proves:** The domain is configured to receive mail somewhere.
**Does not prove:** The mailbox exists at that MX.

**Pass:** +5. **Fail:** disqualify (`INVALID`) — a domain with no MX cannot receive mail.

## Disposable-domain check

**What it does:** Compares the domain against known disposable-email providers (Mailinator, 10minutemail, Guerrilla, etc.).

**Proves:** The address is or is not from a disposable provider.
**Does not prove:** The person actually uses that address.

**Match:** `RISKY` or `INVALID` depending on context. Do not use for business outreach.

## Role-address check

**What it does:** Compares the local-part to known role names: `info@`, `sales@`, `support@`, `admin@`, `contact@`, `hr@`, `noreply@`, `postmaster@`, `abuse@`, etc.

**Proves:** The address is a role, not a personal mailbox.
**Does not prove:** The role is monitored or forwards to anyone specific.

**Match:** -20 and downgrade status. Roles should never be returned as the best email for a named person.

## Catch-all detection

**What it does:** Sends an SMTP `RCPT TO` for a nonsense mailbox at the domain (or looks up prior catch-all history) and checks the response.

**Proves:** The server accepts arbitrary recipients.
**Does not prove:** Any specific mailbox exists.

**Match:** -25 and cap status at `LIKELY_VALID`. Never label as `VALID` from SMTP alone.

## SMTP verification

**What it does:** Opens an SMTP session and issues `MAIL FROM` + `RCPT TO` for the candidate, then reads the server response — without sending `DATA`.

**Proves:** Nothing by itself. `250 OK` is strong on non-catch-all domains; `550` is often a real rejection but sometimes a greylist or spam-defense response.

**Semantics:**

- **250 OK on non-catch-all:** +10, status can reach `VALID`.
- **250 OK on catch-all:** +0.
- **550/551/553:** treat as evidence of invalidity if reproducible from two IPs. Single 550 → treat as `UNVERIFIABLE`.
- **421/450/451 (temp fail):** `UNVERIFIABLE`, retry later.
- **Blocked/no response:** `UNVERIFIABLE`.
- **Greylisting suspected:** retry after 15 minutes.

**Rules:**

- Never issue `DATA` — that would send a real message.
- Never verify from an untrusted IP or you'll poison future deliverability.
- Rate-limit per-domain (no more than one probe per 30 seconds).
- Log every probe attempt for audit.

## Historical verification lookup

**What it does:** Checks a prior verification cache to see if this exact address was verified in the last N days.

**Proves:** Recent evidence of validity.
**Does not prove:** Current validity if the person changed jobs.

**Match within 30 days:** +5. **Match within 90 days:** +2. **Older:** ignore.

## Bounce-history lookup

**What it does:** Checks whether this address has bounced from prior outreach.

**Hard bounce in last 90 days:** status `INVALID`, disqualify.
**Soft bounce:** flag `RISKY`, do not disqualify.
**No history:** neutral.

## Suppression-list check

**What it does:** Checks unsubscribe/opt-out lists and internal do-not-contact lists.

**Match:** status `SUPPRESSED`, disqualify from any outreach output. This overrides all other signals.

## Combined rules

- A candidate with valid MX, valid domain, catch-all=false, and SMTP 250 on a non-catch-all domain, plus a dominant pattern match with 3+ examples and strong identity → `VALID`, typically 80–95 confidence.
- A candidate with valid MX and dominant pattern but no SMTP data → `LIKELY_VALID`, typically 65–79.
- Catch-all domains cap at `LIKELY_VALID` unless the exact email appears on an official public source (then `PUBLICLY_CONFIRMED`).
- Any suppression-list match → `SUPPRESSED`, disqualified, regardless of other signals.
- Never issue verification traffic through an IP that would harm the requester's deliverability.
