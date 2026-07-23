# Worked example: batch enrichment of a small CRM list

Walk-through of enriching a 5-row CRM list. Names, domains, and evidence are illustrative — the workflow is real.

## Input CSV

```csv
row_id,linkedin_url,full_name,current_company
r001,https://linkedin.com/in/janedoe-pm,Jane Doe,Acme Robotics
r002,https://linkedin.com/in/rmendez-cto,Ricardo Méndez,Northwind Data
r003,https://linkedin.com/in/aoliveira-cfo,Ana Oliveira,Northwind Data
r004,https://linkedin.com/in/mikeq-sales,Michael Quinn,Fabrikam Systems
r005,https://linkedin.com/in/lchan-ml,Lee Chan,Fabrikam Systems
```

## Step 0 — Group by company

- Acme Robotics (1 row)
- Northwind Data (2 rows)
- Fabrikam Systems (2 rows)

Domain + pattern discovery runs once per company; row-level verification runs per row.

## Domain and pattern cache

### Acme Robotics
- Domain: `acmerobotics.example` (MX = Microsoft 365, confidence 92)
- Dominant pattern: `first.last` (4 recent examples, confidence 90)
- Catch-all: false

### Northwind Data
- Domain: `northwind.example` (MX = Google Workspace, confidence 88)
- Dominant pattern: `flast` (5 recent examples, confidence 85)
- Catch-all: **true** (probe of `zzznotexist@` returned 250 OK)

### Fabrikam Systems
- Domain: `fabrikam.example` (MX = Proofpoint in front of Microsoft 365 per SPF, confidence 88)
- Dominant pattern: **conflict** — 3 examples of `first.last` (Sales, Marketing) and 3 examples of `first` (Engineering). Departmental split.
- Catch-all: false

## Per-row processing

### r001 Jane Doe @ Acme Robotics

Reuse the single-lookup trace: publicly confirmed press-release email `jane.doe@acmerobotics.example`, verified, confidence 95, status `PUBLICLY_CONFIRMED`.

### r002 Ricardo Méndez @ Northwind Data

- Name normalization: `Ricardo Méndez` → strip accent → `ricardo mendez`.
- Dominant pattern flast → local-part = `rmendez`.
- Candidate 1: `rmendez@northwind.example`
- Verification: MX pass, catch-all **true**, SMTP 250 OK (worthless due to catch-all).
- No exact public email found in a 20-minute search.
- Score: +20 (dominant pattern) +10 (≥3 examples) +10 (identity) +10 (domain) +5 (MX) −25 (catch-all) = 30 → normalized ~65.
- Status: `LIKELY_VALID` (cap on catch-all), confidence 65.
- **Below 70 threshold** — return with clear catch-all warning.

### r003 Ana Oliveira @ Northwind Data

- Same domain, same catch-all situation.
- Candidate 1: `aoliveira@northwind.example`
- No public exact match.
- Score ~65, `LIKELY_VALID`, catch-all warning.
- Below threshold.

### r004 Michael Quinn @ Fabrikam Systems (Sales)

- Department: Sales (from LinkedIn title).
- Fabrikam pattern conflict: Sales uses `first.last`.
- Weight the pattern by department → dominant for this row: `first.last`.
- Candidate 1: `michael.quinn@fabrikam.example`
- Candidate 2 (nickname): `mike.quinn@fabrikam.example` — only include because his LinkedIn headline says "Mike Quinn".
- Verification cand 1: MX pass, catch-all false, SMTP 250. Status `VALID`, confidence 85.
- Verification cand 2: MX pass, catch-all false, SMTP 550. Status `INVALID` for this variant.
- Return cand 1.

### r005 Lee Chan @ Fabrikam Systems (Engineering)

- Department: Engineering (LinkedIn title "ML Engineer").
- Engineering uses `first` at Fabrikam.
- Candidate 1: `lee@fabrikam.example`
- Verification: MX pass, catch-all false, SMTP 250. But `lee` may collide with other Lees.
- Search: Fabrikam blog post 2026-04 lists `lee@fabrikam.example` as author of an ML post. Publicly confirmed.
- Status `PUBLICLY_CONFIRMED`, confidence 92.

## Output CSV

```csv
row_id,best_email,status,confidence,domain,pattern_used,evidence_url,verification_summary,warnings,last_verified_at
r001,jane.doe@acmerobotics.example,PUBLICLY_CONFIRMED,95,acmerobotics.example,first.last,https://acmerobotics.example/press/2026-03-launch.pdf,"MX+SMTP OK, non-catch-all",,2026-07-23
r002,,LIKELY_VALID,65,northwind.example,flast,,catch-all detected — mailbox existence not confirmed,"below 70 threshold; catch-all",2026-07-23
r003,,LIKELY_VALID,65,northwind.example,flast,,catch-all detected — mailbox existence not confirmed,"below 70 threshold; catch-all",2026-07-23
r004,michael.quinn@fabrikam.example,VALID,85,fabrikam.example,first.last (Sales),,"MX+SMTP OK, non-catch-all",nickname variant tried and failed,2026-07-23
r005,lee@fabrikam.example,PUBLICLY_CONFIRMED,92,fabrikam.example,first (Engineering),https://fabrikam.example/blog/ml-2026-04,"MX+SMTP OK, non-catch-all",,2026-07-23
```

## Summary

Of 5 rows: 2 publicly confirmed, 1 valid via technical verification, 2 fall below the 70 threshold because Northwind is catch-all. The two below-threshold rows are returned with an explicit warning, not with a fake confidence score.

## Discipline points illustrated

- Domain and pattern research runs once per company, not once per row.
- Catch-all detection triggers a per-domain cap, not a per-candidate override.
- Departmental pattern splits are handled by weighting the sample by the target's department.
- Nickname candidates are only generated when the person uses the nickname publicly.
- Confidence < 70 → the "best email" cell is empty, not filled with a guess.
