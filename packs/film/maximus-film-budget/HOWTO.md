# maximus-film-budget — recipes

## Recipe 1: Generate an empty budget skeleton

```python
import csv

accounts = [
    # ATL
    (1100, "Story & Screenplay"),
    (1200, "Producer"),
    (1300, "Director"),
    (1400, "Cast"),
    (1500, "ATL Travel & Living"),
    # BTL Production
    (2000, "Production Staff"),
    (2100, "Extras & Stand-ins"),
    (2200, "Set Design"),
    (2300, "Set Construction"),
    (2400, "Set Operations"),
    (2500, "Special Effects"),
    (2600, "Set Dressing"),
    (2700, "Property"),
    (2800, "Wardrobe"),
    (2900, "Makeup & Hair"),
    (3000, "Camera"),
    (3100, "Grip"),
    (3200, "Electric"),
    (3300, "Sound (production)"),
    (3400, "Transportation"),
    (3500, "Location"),
    (3600, "Digital Media & Data Management"),
    (3700, "Second Unit"),
    (3800, "Aerial & Underwater"),
    (3900, "Tests"),
    # BTL Post
    (4000, "Editing"),
    (4100, "Music"),
    (4200, "Post Sound"),
    (4300, "Post DI, VFX, Color"),
    (4400, "Titles & Opticals"),
    # BTL Other
    (4500, "Publicity & Marketing"),
    (4600, "Insurance"),
    (4700, "General Expenses"),
]

with open("budget_skeleton.csv", "w") as f:
    w = csv.writer(f)
    w.writerow(["account_code", "description", "quantity", "unit", "rate", "subtotal", "fringes", "total", "notes"])
    for code, desc in accounts:
        w.writerow([f"{code}.00", desc, "", "", "TBD", "", "", "TBD", "category header"])
```

Hand the CSV to the line producer to fill in.

## Recipe 2: Add typical line items under an account (Camera example)

```csv
3000.00,Camera,,,,,,,category header
3000.01,Director of Photography,4,weeks,TBD,,,TBD,prep + shoot + wrap
3000.02,Camera Operator,3,weeks,TBD,,,TBD,shoot only
3000.03,1st AC,3,weeks,TBD,,,TBD,shoot + partial prep
3000.04,2nd AC,3,weeks,TBD,,,TBD,shoot only
3000.05,DIT,3,weeks,TBD,,,TBD,shoot only
3000.06,Camera Package Rental,3,weeks,TBD,,,TBD,ARRI Alexa Mini LF or similar
3000.07,Lens Package Rental,3,weeks,TBD,,,TBD,Zeiss Supreme Primes or similar
3000.08,Camera Support (dolly/crane/gimbal),as needed,,TBD,,,TBD,per day estimates
3000.09,Camera Consumables,flat,,TBD,,,TBD,batteries, media, etc.
```

## Recipe 3: Compute the top-sheet

```python
import csv
from collections import defaultdict

totals = defaultdict(float)

with open("budget_filled.csv") as f:
    for row in csv.DictReader(f):
        if row["total"] in ("", "TBD", "category header"):
            continue
        series = int(row["account_code"].split(".")[0]) // 1000
        totals[series] += float(row["total"])

atl = sum(v for k, v in totals.items() if k in (1,))  # 1000-series
btl = sum(v for k, v in totals.items() if k in (2, 3, 4))  # 2000-4700 series

fringes = (atl + btl) * 0.30  # placeholder; use actual weighted percentage
strike = atl + btl + fringes
contingency = btl * 0.10
bond = strike * 0.04
payroll_handling = (atl + btl) * 0.008

total = strike + contingency + bond + payroll_handling

print(f"ATL:              ${atl:>12,.0f}")
print(f"BTL:              ${btl:>12,.0f}")
print(f"Fringes:          ${fringes:>12,.0f}")
print(f"Strike price:     ${strike:>12,.0f}")
print(f"Contingency (10%): ${contingency:>12,.0f}")
print(f"Bond (4%):        ${bond:>12,.0f}")
print(f"Payroll handling: ${payroll_handling:>12,.0f}")
print(f"TOTAL BUDGET:     ${total:>12,.0f}")
```

## Recipe 4: Sanity-check against tier

If total budget is $1.2M but the cast rates are studio-tier ($10k/day for a lead), flag the mismatch. Cast rates for a $1.2M indie feature should sit in the SAG Modified Low range — typically $335/day for principals plus fringes.

```python
if total < 5_000_000:
    cast_rows = [r for r in rows if r["account_code"].startswith("1400")]
    for row in cast_rows:
        if row["rate"] != "TBD" and float(row["rate"]) > 5000:
            print(f"WARN: {row['description']} rate ${row['rate']}/day may exceed indie tier norms")
```

## Recipe 5: Round-trip with Movie Magic Budgeting

MMB imports CSV with the columns above. When exporting from the skill, preserve account codes exactly and keep the `subtotal`, `fringes`, and `total` columns even if empty — MMB won't create them on import.

Export back out of MMB and diff against the original to catch anything MMB re-categorized.
