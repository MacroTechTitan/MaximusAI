---
name: maximus-film-budget
description: "Line-item feature-film budget templating using standard AICP/AMPTP account codes (1000-4700 series), console-first, CSV/XLSX for Movie Magic Budgeting round-trip or standalone. Separates above-the-line (story, producer, director, cast) from below-the-line (production, post, music, insurance, general). Handles contingency (~10%), completion bond (3-6%), fringes (payroll tax + union benefits), payroll handling. Use when building a feature budget from scratch, auditing account-code compliance, producing a top-sheet for financiers or bond company, scaling between tiers (micro/low/indie/studio), or the user says 'film budget', 'AICP budget', 'above the line', 'below the line', 'contingency', 'completion bond', 'top sheet', 'budget breakdown'. Not for TV, commercials, or as substitute for line producer/UPM judgment. Produces skeleton and math; humans set the numbers."
license: MIT
metadata:
  pack: film
  authored_by: Macro Tech Titan
---

# maximus-film-budget

Feature-film budget templating with industry-standard account-code structure. CSV/XLSX output for Movie Magic Budgeting round-trip or standalone use.

## Core operating rules

1. **Use standard AICP/AMPTP account codes.** Financiers, bond companies, guilds, and completion-bond auditors expect line items to sit in the expected accounts. A budget where cast is in the 3000 series instead of the 1100 series will get sent back for restructuring.
2. **Separate above-the-line from below-the-line.** ATL is 1000-1500 series (story, producer, director, cast). BTL is 2000-4700 series (production, post, music, insurance, general). Below-the-line-total and above-the-line-total are two separate top-sheet numbers.
3. **Fringes are separate from rate.** A cast rate of $2,000/day carries an additional ~35-40% in fringes (payroll taxes, SAG pension/health, W&V). Never bake fringes into rate — always show as a separate line or as a percentage roll-up.
4. **Contingency is a top-sheet line.** Typically 10% of below-the-line. Financiers will refuse to close on a feature without contingency shown.
5. **Completion bond is a top-sheet line.** Typically 3-6% of the strike price (total budget before bond). Required for bonded features.
6. **Payroll handling is a real line item.** Typically 0.5-1% of gross payroll. Bake it in or the payroll company invoice will surprise the producer.
7. **The skill produces the skeleton and the math.** Rates, quantities, day-counts, and vendor bids come from the line producer / UPM, not from the skill. Never invent a rate; always leave it as a `TBD` for a human to fill.
8. **Round-trip with Movie Magic Budgeting.** Output CSV with columns MMB can import. Preserve account codes exactly.

## Account-code skeleton (standard structure)

### Above-the-line (1000-1500 series)

| Code | Category |
|---|---|
| 1100 | Story & Screenplay (writer, purchase, options) |
| 1200 | Producer (producing team, exec producers) |
| 1300 | Director |
| 1400 | Cast (principal, day players, stunt) |
| 1500 | ATL Travel & Living |

### Below-the-line: Production (2000-2900 series)

| Code | Category |
|---|---|
| 2000 | Production Staff (UPM, AD, script supervisor) |
| 2100 | Extras & Stand-ins |
| 2200 | Set Design (production designer, art director, set decorator) |
| 2300 | Set Construction |
| 2400 | Set Operations (grip, electric, sound, video assist) |
| 2500 | Special Effects |
| 2600 | Set Dressing |
| 2700 | Property |
| 2800 | Wardrobe |
| 2900 | Makeup & Hair |

### Below-the-line: Production continued (3000-3900 series)

| Code | Category |
|---|---|
| 3000 | Camera |
| 3100 | Grip |
| 3200 | Electric |
| 3300 | Sound (production) |
| 3400 | Transportation |
| 3500 | Location |
| 3600 | Production Film & Lab (or Digital Media & Data Management) |
| 3700 | Second Unit |
| 3800 | Aerial & Underwater |
| 3900 | Tests |

### Below-the-line: Post-production (4000-4400 series)

| Code | Category |
|---|---|
| 4000 | Editing (picture) |
| 4100 | Music |
| 4200 | Post Sound (dialogue, foley, sound design, mix) |
| 4300 | Post Film & Lab / Post DI, VFX, Color |
| 4400 | Titles & Opticals |

### Below-the-line: Other (4500-4700 series)

| Code | Category |
|---|---|
| 4500 | Publicity, Marketing (if included in production budget) |
| 4600 | Insurance |
| 4700 | General Expenses (office, legal, accounting) |

### Top-sheet lines (below the department totals)

| Line | Typical value |
|---|---|
| Above-the-line subtotal | sum of 1000-1500 |
| Below-the-line subtotal | sum of 2000-4700 |
| Fringes | 20-40% of ATL/BTL payroll depending on union/non-union |
| Contingency | 10% of BTL (sometimes 10% of ATL+BTL) |
| Completion bond | 3-6% of strike price |
| Payroll handling | 0.5-1% of gross payroll |
| **Total budget** | sum of all above |

## Budget tiers (for scale reference only — not for setting rates)

| Tier | Range | Union status | Cast |
|---|---|---|---|
| Micro | < $250k | Non-union / SAG Ultra-Low | Unknowns |
| Low | $250k-$1M | SAG Modified Low / Low | Character actors |
| Indie | $1M-$5M | SAG Low / SAG Modified | Mix |
| Low-mid | $5M-$20M | Full SAG | Recognizable |
| Mid | $20M-$60M | Full guilds | Stars in supporting |
| Studio | $60M+ | Full guilds | Stars |

Use these to sanity-check that the requested rates and quantities are appropriate for the tier. A day rate of $50,000 for a lead in a $500k indie is a sign the budget is either wrong or aspirational.

## Fringe percentages (2026 ballpark, verify against current rates)

- **Non-union payroll:** ~15-18% (employer FICA, FUTA, SUTA, workers comp)
- **SAG-AFTRA:** ~35-40% on top of gross (pension, health, workers comp, payroll tax)
- **DGA:** ~30-35% on top of gross
- **IATSE:** ~30-38% depending on local
- **Teamsters:** ~35-40% depending on local

Always show fringes as a separate roll-up line. Bond companies audit this.

## Output format

CSV with columns:

```
account_code,description,quantity,unit,rate,subtotal,fringes,total,notes
1100.01,Screenplay Purchase,1,flat,TBD,,,TBD,TBD by producer
1400.01,Lead (Cast #1),20,days,TBD,,,TBD,SAG Modified Low
1400.02,Second Lead (Cast #2),12,days,TBD,,,TBD,SAG Modified Low
2000.01,UPM,4,weeks,TBD,,,TBD,prep + shoot + wrap
...
```

Blank rate cells are filled by the line producer / UPM. The skill never invents a rate.

## What this skill does not do

- Does not set rates. Rates come from vendor bids, guild minimums, and line-producer judgment.
- Does not book crew, negotiate contracts, or process payroll.
- Does not produce TV or commercial budgets.
- Does not offer tax-incentive advice (see a tax counsel or the state film office).
- Does not replace Movie Magic Budgeting for productions that need MMB (bonded studio features usually do).

## Quality checkpoint

- [ ] Every account code used is a standard AICP/AMPTP code.
- [ ] ATL and BTL are clearly separated with subtotals.
- [ ] Fringes are shown as a separate roll-up, not baked into rates.
- [ ] Contingency and completion bond are explicit top-sheet lines.
- [ ] Payroll handling is a line item.
- [ ] Every `TBD` is flagged for the line producer / UPM to fill.
- [ ] Output CSV is importable into Movie Magic Budgeting.
- [ ] Budget tier and requested rates are internally consistent.
