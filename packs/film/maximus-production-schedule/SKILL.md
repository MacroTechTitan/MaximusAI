---
name: maximus-production-schedule
description: "Turn a locked Fountain screenplay into a scene breakdown, stripboard, one-liner, and day-out-of-days for feature-film production, console-first, without a Movie Magic Scheduling license. Parses sluglines into scene records tagged INT/EXT, day/night, location, page count in 8ths, cast IDs. Groups by location for stripboard efficiency; produces a chronological one-liner and DOOD matrix. Use when preparing a shoot schedule from a locked draft, wanting a plain-text stripboard for indie/low-budget, needing a one-liner or DOOD for AD/UPM sign-off, or the user says 'production schedule', 'stripboard', 'one-liner', 'day out of days', 'DOOD', 'scene breakdown', 'movie magic alternative'. Do not use for shorts, TV episodes, docs with no script, or as a substitute for AD judgment. Produces first-draft artifacts the AD/UPM hand-tune, not a final locked schedule."
license: MIT
metadata:
  pack: film
  authored_by: Macro Tech Titan
---

# maximus-production-schedule

Feature-film scheduling artifacts from a locked Fountain screenplay: scene breakdown, stripboard, one-liner, day-out-of-days. Console-first. Free-tool stack.

## Core operating rules

1. **The screenplay must be locked before scheduling.** Scheduling from an in-flux draft wastes AD/UPM time. If the writer is still changing scenes, wait or work from the last locked draft with a written change log.
2. **Every scene gets a stable scene number.** Fountain supports `#1#`, `#1A#`, `#2#` markers; use them. Once scene numbers are assigned, they never renumber even if scenes are added or dropped.
3. **Page count is measured in 8ths.** A scene that runs 1 3/8 pages is `1 3/8` (11/8), not `1.375`. This is industry convention and every strip board reads it this way.
4. **Cast IDs are stable.** The lead is `1`, the second-billed is `2`, and so on. The IDs are assigned at breakdown time and never change. Day-out-of-days is built off these IDs.
5. **Location is the stripboard grouping axis.** Days are built by grouping all scenes at one location. If Location A has 12 scenes across the script, they all shoot in whatever shoot-day sequence keeps the location on the calendar for the fewest days.
6. **Day/night matters for turnaround.** A night scene followed by a morning day-scene the next day is a turnaround violation. The stripboard flags these; the AD resolves them.
7. **Company moves are visible.** Each strip-board day shows every location change explicitly. A day with three company moves is a red-flag day.
8. **The output is a hand-off, not a final schedule.** The AD and UPM adjust for weather holds, cast availability, prep days, holidays, and permits. This skill produces the first-draft artifacts, not the shootable schedule.

## Fountain scene parsing

The skill reads a Fountain source and extracts every scene heading. A scene heading in Fountain looks like:

```
INT. DINER - NIGHT
EXT. TWO-LANE HIGHWAY - PRE-DAWN
INT./EXT. PICKUP TRUCK (MOVING) - CONTINUOUS
```

The parser produces one record per scene:

| Field | Extraction rule |
|---|---|
| `scene_number` | From Fountain `#N#` marker, else assigned in slug order |
| `int_ext` | `INT`, `EXT`, or `INT/EXT` before the first period |
| `location` | Between the `INT./EXT.` and the ` - ` day/night marker |
| `day_night` | After the ` - ` — normalized to DAY / NIGHT / DAWN / DUSK / CONTINUOUS |
| `page_count_eighths` | Measured against a Courier-Prime 12pt render, in 8ths of a page |
| `cast_ids` | Character IDs speaking or physically present (from parsing dialogue + action) |
| `synopsis` | One-line action summary from the first non-blank action line |

## Stripboard rules

Stripboard is a per-day plan grouped by location. Rules:

1. **Group by location.** All scenes at one location are candidates to shoot on the same day.
2. **Order within a day: day scenes first, then night.** Reduces lighting setup complexity.
3. **Respect cast availability windows** if provided (e.g., "Cast #3 unavailable Sept 21-24").
4. **Cap page count per day** at the AD's specified maximum, typically 4-8 pages/day for indie, 3-5 for prestige.
5. **Flag turnaround violations** — night wrap → next-morning call. Standard union turnaround is 12 hours from wrap to call.
6. **Flag company-move-heavy days** — more than one location change in a day.
7. **Flag consecutive night days** — more than three in a row.

## One-liner

The one-liner is a chronological (shoot-day-ordered) list showing:

- Scene number
- Slugline
- Page count in 8ths
- Cast present (by ID)
- One-line synopsis

Format:

```
DAY 1 — Monday, Oct 5
  Sc 12   INT. DINER - NIGHT             2 3/8   1, 3, 8      Mara confronts Andres over coffee.
  Sc 13   INT. DINER - NIGHT (LATER)     1 5/8   1, 3         Mara leaves alone. Andres watches.
  Sc 47   INT. DINER - NIGHT (FLASHBACK) 7/8     1, 3, 8      Fragment of the night that started it.

DAY 2 — Tuesday, Oct 6
  ...
```

Page-count sum for a day is shown at the bottom of each day block.

## Day-out-of-days (DOOD)

The DOOD is a matrix: rows = cast IDs, columns = shoot days, cell = one of:

- `SW` — Start Work (first day this cast member is on set)
- `W`  — Work day (mid-run)
- `WF` — Work Finish (last day)
- `H`  — Hold (cast contracted but not on set that day)
- `T`  — Travel
- `R`  — Rehearsal
- (blank) — not yet started or already wrapped

Example:

```
Cast    Role         D1  D2  D3  D4  D5  D6  D7  D8  D9  D10  Total
 1      MARA         SW  W   W   H   W   W   W   W   W   WF   9 work / 1 hold
 2      ANDRES               SW  W   H   W   WF                4 work / 1 hold
 3      WAITER       SW  WF                                    2 work
```

Producers use the DOOD to negotiate cast contracts (a hold day is billed differently from a work day) and to sequence pickup weeks.

## Toolchain

- **[Fountain-Tools](https://github.com/fountain-tools)** — Python libraries for parsing Fountain
- **[fountain-parser](https://www.npmjs.com/package/fountain)** — Node.js Fountain parser
- **Custom Python or Node.js scripts** — the skill provides templates in `HOWTO.md`
- **Output formats:** CSV (for spreadsheet import), Markdown (for readable one-liner), and JSON (for downstream tools)

Optional: [Gorilla Scheduling](https://www.jungle.software/gorilla-scheduling) (commercial, cheaper than Movie Magic) if the AD wants a GUI on top of the generated artifacts.

## What this skill does not do

- Does not produce a shootable, locked schedule. That is the AD's judgment call.
- Does not handle TV episode scheduling — different constraints, different tools.
- Does not manage location permits, insurance, or SAG paperwork.
- Does not book crew or negotiate cast contracts.

## Quality checkpoint

- [ ] Every scene in the locked screenplay appears in the breakdown.
- [ ] Every scene has a stable scene number and page-count in 8ths.
- [ ] Cast IDs are stable across breakdown, one-liner, and DOOD.
- [ ] Stripboard respects any specified cast unavailability windows.
- [ ] Turnaround violations, company-move-heavy days, and consecutive-night runs are flagged.
- [ ] Output formats (CSV, MD, JSON) are all produced and internally consistent.
- [ ] Handoff artifact clearly states "first-draft schedule, AD/UPM to adjust."
