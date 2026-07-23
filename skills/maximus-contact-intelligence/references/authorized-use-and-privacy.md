# Authorized use and privacy

The rules that constrain when and how `maximus-contact-intelligence` may operate. These are not suggestions — they are the operating conditions for the skill.

## Authorized uses

Proceed only when the intended use is one of:

- Legitimate business communication (B2B outreach, partnership development)
- Recruiting and candidate outreach for open roles
- Professional networking with individuals who have public professional presence
- Investor relations, LP/GP outreach, and other capital-formation contexts (subject to relevant securities rules)
- Journalistic research and source-development
- Due diligence, KYB, and vendor evaluation
- Existing-customer support and account management
- Fraud investigation with appropriate authority

## Prohibited data

Do not search for, collect, retain, or expose:

- Private residential addresses
- Passwords, password hashes, or any authentication material
- Breached credentials from data-leak dumps (Have I Been Pwned lookups for informational counts are permissible; extracting the underlying data is not)
- Personal family information: spouse, children, parents, siblings — unless they are themselves the professional subject and the data is professionally public
- Sensitive personal information: health, sexual orientation, political affiliation, religious affiliation, immigration status, criminal history
- Protected-class information used to filter or target
- Hidden LinkedIn content behind logged-in views, InMail-only fields, or paid Recruiter/Sales Nav restricted data
- Data obtained by bypassing access controls, whether technical or contractual

## Prohibited techniques

Never:

- Defeat or attempt to defeat CAPTCHAs, LinkedIn's authentication, robots.txt-declared exclusions, or any technical safeguard
- Impersonate the person or the company to obtain data
- Send a test email to verify a mailbox — verification is passive only
- Extract data from paid data brokers whose license terms disallow the requester's use case
- Use scraped LinkedIn data that was collected in violation of LinkedIn's terms of use

## Consent and legitimacy

- Public professional presence (LinkedIn, company bio, conference bio, press mentions) creates a reasonable basis for professional outreach. It does not create consent for every downstream use.
- Suppression-list matches always win. If a person opted out, they stay out. Do not attempt to re-target them via a personal domain, alternate spelling, or "old" email address.
- GDPR, CCPA, PIPEDA, and other privacy laws apply to email addresses. Have a lawful basis (legitimate interest, contract, consent) and be prepared to honor deletion requests.
- Do not aggregate personal data across sources beyond what the professional context requires.

## Regulated contexts

- **US securities:** Do not use this skill to build lists for unregistered offerings without counsel review. Discovery of an accredited investor's email does not authorize a general solicitation.
- **Financial services:** Follow your firm's Reg BI, Reg S-P, and IA marketing rule obligations. Coordinate with compliance.
- **Health care:** HIPAA and similar rules can apply even to professional contacts in clinical roles.
- **Government contracting:** ITAR, EAR, and public-records rules can shape which contact channels are permitted.

## Data retention

- Cache verified emails with a `last_verified_at` timestamp.
- Re-verify at least every 90 days for active outreach lists.
- Purge unverified candidates that never matured to `VALID`, `LIKELY_VALID`, or `PUBLICLY_CONFIRMED` after 30 days.
- Purge all data on request from the data subject.

## Transparency

Every returned result must include:

- Source URLs for every claim (identity, employment, domain, pattern, exact-email hit)
- Observation dates
- The verification methods run and their outcomes
- Warnings about staleness, catch-all, ambiguity, or conflicting evidence

If any of the above is missing, downgrade the status. The skill's promise is "evidence with confidence," not "email at any cost."

## Escalation

Route to a human reviewer when:

- The target is a public official or reporter and the context is politically sensitive
- The identity is ambiguous after two independent checks
- The suppression-list check returns a match
- The pattern evidence conflicts (two dominant patterns, no clear winner)
- The confidence would only reach 70 by relaxing a rule

The skill can generate confident results. It cannot decide whether the outreach itself is appropriate. That decision belongs to a person.
