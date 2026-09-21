# maximus-film-budget

Line-item feature-film budget templating with standard AICP/AMPTP account codes. CSV/XLSX output for Movie Magic Budgeting round-trip.

## What it's for

- Building a feature budget from scratch with correct account structure.
- Auditing an existing budget for account-code compliance.
- Producing a top-sheet for financiers or a completion bond company.
- Scaling a budget between tiers (micro / low / indie / studio).

## What it's not for

- Setting rates (line producer's job).
- TV or commercial budgets.
- Payroll processing or contract negotiation.
- Tax-incentive planning (see tax counsel).

## Assumed tooling

- Any spreadsheet (Excel, Numbers, LibreOffice, Google Sheets)
- Optional: Movie Magic Budgeting for bonded studio features
- Python or Node.js only if the user wants to script the template generation

## What ships with this skill

- `SKILL.md` — account codes, tier reference, fringe percentages, top-sheet math
- `README.md` — this file
- `HOWTO.md` — recipes for skeleton generation, top-sheet build, tier sanity check
- `examples/indie-feature-1M-topsheet.md` — worked example: $1M indie feature top-sheet

## Where the boundary sits

The skill produces the skeleton and the math. Humans fill in every rate, quantity, and vendor bid. The skill never invents a number, and it never presents a budget as final until a line producer and UPM have signed off.
