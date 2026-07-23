# Email pattern taxonomy

A reference for classifying and comparing corporate email patterns during Step 6 of the workflow.

## Standard patterns

| Pattern key | Example (Jane Doe) | Notes |
|---|---|---|
| `first.last` | jane.doe@acme.com | Most common at enterprise, dominant at Microsoft 365 and Google Workspace tenants |
| `first_last` | jane_doe@acme.com | Common at older orgs, some consulting firms |
| `first-last` | jane-doe@acme.com | Rare, occasionally seen at agencies |
| `firstlast` | janedoe@acme.com | Common at startups |
| `first` | jane@acme.com | Small teams and early-stage startups; often has collisions |
| `flast` | jdoe@acme.com | Legacy convention, common in finance and law |
| `firstl` | janed@acme.com | Uncommon but real |
| `f.last` | j.doe@acme.com | Common at European firms |
| `last.first` | doe.jane@acme.com | Common in Japan, Korea, some German firms |
| `last` | doe@acme.com | Very rare, mostly universities and long-tenure execs |

## Middle-name variants

- `first.middle.last` — jane.marie.doe@acme.com
- `first.m.last` — jane.m.doe@acme.com
- `firstmiddlelast` — janemariedoe@acme.com

Middle-name patterns usually appear only when a first-name collision exists inside the company. Do not generate them unless you observe at least one example at the domain.

## Compound surname handling

Surnames like "van der Berg", "de la Cruz", "O'Neill", "Smith-Jones" need explicit rules.

- Hyphenated → keep the hyphen or drop it depending on observed pattern. Look for either at the same domain.
- Apostrophes → almost always dropped. `o.neill` or `oneill`, rarely `o'neill`.
- Spaces in surname → dropped. `van der Berg` → `vanderberg` or `van.der.berg` per pattern.
- Accents and diacritics → almost always stripped to ASCII. `Núñez` → `nunez`.
- Compound Spanish/Portuguese surnames → both parts often used at Latin American firms; only paternal surname at Iberian firms. Verify from observed samples.

## Nickname handling

Do not substitute a nickname for the given name unless:

- The person uses the nickname on their LinkedIn or company bio, or
- You observe the nickname as the local-part for that exact person on a public source.

Common risky substitutions:

- Robert → Bob, Rob, Bobby
- William → Will, Bill, Billy
- Elizabeth → Liz, Beth, Betty, Eliza
- Michael → Mike, Mick
- Katherine → Kate, Kathy, Katie

If both forms are plausible, generate both as candidates and let scoring decide.

## Case sensitivity

The local-part is case-insensitive on virtually all major mail servers (RFC 5321 allows case-sensitivity but virtually no provider enforces it). Always normalize candidates to lowercase.

## Departmental variants

Some companies use different patterns per department. Signals to look for:

- Engineering uses `first` while Sales uses `first.last` (common at mid-stage startups)
- Legal or Executive team uses `flast` while everyone else uses `first.last` (common in finance)
- Regional subsidiaries use `first.last@region.company.com`

When you detect departmental divergence, weight the sample by the target person's department.

## Alternate domain patterns

- Parent company acquired subsidiary → email may remain `person@subsidiary.com` for months to years post-acquisition, then migrate
- Multi-brand holding companies → each brand may have its own domain
- Consulting engagements → contractors may use `person@client.com` even though employed by consulting firm
- Government contractors → often have both `.gov` and contractor-domain addresses

Always check MX records for both the website domain and any suspected alternates.

## Provider tells

MX records can reveal the mail provider, which correlates with pattern likelihood:

| MX host | Provider | Typical default |
|---|---|---|
| `*.google.com`, `*.googlemail.com` | Google Workspace | first.last (admin-configurable) |
| `*.protection.outlook.com`, `*.mail.protection.outlook.com` | Microsoft 365 | first.last (admin-configurable) |
| `*.zoho.com` | Zoho Mail | Varies |
| `*.pphosted.com`, `*.ppe-hosted.com` | Proofpoint (filter in front of another provider) | Provider is behind — check SPF |
| `*.mimecast.com` | Mimecast (filter) | Provider is behind — check SPF |
| `*.mx.cloudflare.net` | Cloudflare Email Routing | Aliases to another provider |

Provider identity is a weak signal for pattern but a strong signal for domain confidence.

## Anti-patterns to avoid

- Generating `firstinitial+lastname@` without at least one observed example
- Assuming `first.last` because it's most common globally — verify per-domain
- Using a person's Twitter or GitHub handle as a local-part guess
- Combining a nickname with `.last` when only the formal name appears in public sources
- Guessing at role addresses (`sales@`, `info@`) for a specific person — these are role accounts, not personal mailboxes
