# maximus-production-schedule — recipes

## Recipe 1: Parse a locked screenplay into a scene breakdown

Using Python + [fountain-parser](https://pypi.org/project/fountain-tools/):

```python
from fountain_tools import Parser

with open("screenplay.fountain") as f:
    script = Parser().parse(f.read())

scenes = []
for i, scene in enumerate(script.scenes, 1):
    scenes.append({
        "scene_number": scene.number or str(i),
        "int_ext": scene.heading.int_ext,
        "location": scene.heading.location,
        "day_night": scene.heading.time,
        "page_count_eighths": scene.page_length_eighths,
        "cast_ids": [c.id for c in scene.characters],
        "synopsis": scene.first_action_line[:80],
    })

# Export
import csv
with open("breakdown.csv", "w") as f:
    w = csv.DictWriter(f, fieldnames=scenes[0].keys())
    w.writeheader()
    w.writerows(scenes)
```

## Recipe 2: Build a stripboard grouped by location

```python
from collections import defaultdict

by_location = defaultdict(list)
for scene in scenes:
    by_location[scene["location"]].append(scene)

# Sort within each location: day scenes first, then night
for loc, loc_scenes in by_location.items():
    day_order = {"DAWN": 0, "DAY": 1, "DUSK": 2, "NIGHT": 3, "CONTINUOUS": 1}
    loc_scenes.sort(key=lambda s: day_order.get(s["day_night"], 1))

# Emit as first-draft stripboard
for loc in sorted(by_location):
    print(f"\n=== {loc} ===")
    for s in by_location[loc]:
        print(f"  Sc {s['scene_number']:>4}  {s['int_ext']}. {s['location']} - {s['day_night']:<12} {s['page_count_eighths']}/8   cast: {s['cast_ids']}")
```

Hand this to the AD for shoot-day assignment.

## Recipe 3: Compress into shoot days with a page cap

```python
MAX_EIGHTHS_PER_DAY = 40  # ~5 pages

shoot_days = []
current_day = {"scenes": [], "eighths": 0}

for loc, loc_scenes in by_location.items():
    for scene in loc_scenes:
        if current_day["eighths"] + scene["page_count_eighths"] > MAX_EIGHTHS_PER_DAY:
            shoot_days.append(current_day)
            current_day = {"scenes": [], "eighths": 0}
        current_day["scenes"].append(scene)
        current_day["eighths"] += scene["page_count_eighths"]

if current_day["scenes"]:
    shoot_days.append(current_day)

print(f"Estimated shoot days: {len(shoot_days)}")
```

Flag any day with > 1 location as a company-move day.

## Recipe 4: Generate a one-liner in Markdown

```python
from datetime import date, timedelta

start = date(2026, 10, 5)

for i, day in enumerate(shoot_days, 1):
    shoot_date = start + timedelta(days=i-1)
    print(f"\n## DAY {i} — {shoot_date.strftime('%A, %b %-d')}")
    for s in day["scenes"]:
        cast_str = ", ".join(str(c) for c in s["cast_ids"])
        print(f"  Sc {s['scene_number']:>4}  {s['int_ext']}. {s['location']} - {s['day_night']:<10} {s['page_count_eighths']}/8  cast: {cast_str}   {s['synopsis']}")
    print(f"  DAY TOTAL: {day['eighths']}/8 pages")
```

## Recipe 5: Generate a day-out-of-days matrix

For each cast ID, walk shoot days, mark:
- First appearance: `SW`
- Middle appearances: `W`
- Last appearance: `WF`
- Gap between first and last: `H` (Hold)
- Before first / after last: blank

```python
all_cast = sorted({c for day in shoot_days for s in day["scenes"] for c in s["cast_ids"]})

dood = {c: [""] * len(shoot_days) for c in all_cast}
for i, day in enumerate(shoot_days):
    working_today = {c for s in day["scenes"] for c in s["cast_ids"]}
    for c in working_today:
        dood[c][i] = "W"

for c in all_cast:
    first = next(i for i, v in enumerate(dood[c]) if v == "W")
    last = len(dood[c]) - 1 - next(i for i, v in enumerate(reversed(dood[c])) if v == "W")
    dood[c][first] = "SW"
    dood[c][last] = "WF" if last != first else "SWF"
    for i in range(first + 1, last):
        if dood[c][i] == "":
            dood[c][i] = "H"

# Emit
header = "Cast  " + "  ".join(f"D{i+1:>2}" for i in range(len(shoot_days)))
print(header)
for c in all_cast:
    print(f" {c:>3}  " + "  ".join(f"{v:>3}" for v in dood[c]))
```

## Recipe 6: Flag turnaround violations

For each pair of adjacent shoot days, check if the previous day contains a NIGHT scene and the next day starts with a DAY scene:

```python
for i in range(1, len(shoot_days)):
    prev_has_night = any(s["day_night"] == "NIGHT" for s in shoot_days[i-1]["scenes"])
    next_starts_day = shoot_days[i]["scenes"][0]["day_night"] in ("DAY", "DAWN")
    if prev_has_night and next_starts_day:
        print(f"WARN: turnaround risk between DAY {i} and DAY {i+1}")
```
