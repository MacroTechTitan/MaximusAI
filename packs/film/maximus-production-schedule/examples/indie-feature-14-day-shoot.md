# Example: 14-day indie feature schedule from a 96-page screenplay

## Input

- Screenplay: `north_of_nowhere.fountain`, locked draft, 96 pages
- 48 total scenes across 9 unique locations
- 7 speaking cast members
- AD constraint: max 42 eighths (5 1/4 pages) per day, no consecutive nights beyond 3
- Cast constraint: Cast #4 unavailable Oct 12-14

## Breakdown output (excerpt)

```
scene_number,int_ext,location,day_night,page_count_eighths,cast_ids,synopsis
1,EXT,TWO-LANE HIGHWAY,PRE-DAWN,6,"[1]",Fog. A single set of headlights crawls east.
2,INT,PICKUP TRUCK (MOVING),CONTINUOUS,14,"[1]",Mara grips the wheel. Coffee sweats in the cup holder.
3,EXT,GAS STATION,DAWN,5,"[1,7]",The truck coasts to a stop under harsh fluorescent.
4,INT,DINER,DAY,18,"[1,3,8]",Mara slides into a booth. Andres is already there.
...
```

48 rows. Every scene tagged.

## Stripboard (grouped by location, day-scenes first)

```
=== DINER ===
  Sc  4  INT. DINER - DAY         18/8   cast: [1, 3, 8]
  Sc 12  INT. DINER - NIGHT       19/8   cast: [1, 3, 8]
  Sc 13  INT. DINER - NIGHT       13/8   cast: [1, 3]
  Sc 47  INT. DINER - NIGHT       7/8    cast: [1, 3, 8]

=== TWO-LANE HIGHWAY ===
  Sc  1  EXT. TWO-LANE HIGHWAY - PRE-DAWN   6/8    cast: [1]
  Sc 31  EXT. TWO-LANE HIGHWAY - DAY        4/8    cast: [1, 5]
  Sc 44  EXT. TWO-LANE HIGHWAY - NIGHT      9/8    cast: [1, 5, 6]
...
```

## Compressed shoot days (14-day plan)

| Day | Date | Location(s) | Scenes | Pages (8ths) | Cast | Flags |
|---|---|---|---|---|---|---|
| 1 | Mon Oct 5 | DINER (day)                    | 4                | 18 | 1,3,8      |  |
| 2 | Tue Oct 6 | DINER (night)                  | 12, 13, 47       | 39 | 1,3,8      | NIGHT — turnaround risk vs D3 |
| 3 | Wed Oct 7 | GAS STATION (day)              | 3, 15, 27        | 22 | 1,7,3      |  |
| 4 | Thu Oct 8 | MARA'S APARTMENT (day)         | 8, 9, 10         | 34 | 1,2        |  |
| 5 | Fri Oct 9 | MARA'S APARTMENT (night)       | 21, 22           | 27 | 1,2        |  |
| 6 | Sat Oct 10 | TWO-LANE HIGHWAY (day+night)  | 1, 31, 44        | 19 | 1,5,6      | 3 scene-time changes |
| 7 | Sun Oct 11 | REST DAY                      |                  |    |            |  |
| 8 | Mon Oct 12 | RIVER BEND (day)              | 18, 19, 20       | 41 | 1,3,7      | Cast 4 unavailable — none needed |
| 9 | Tue Oct 13 | RIVER BEND (night)            | 23, 24           | 22 | 1,3        | Cast 4 unavailable — none needed |
| 10 | Wed Oct 14 | POLICE STATION (day)         | 33, 34, 35, 36   | 40 | 1,2,4,9    | Cast 4 unavailable — WARN |
| 11 | Thu Oct 15 | POLICE STATION (night)       | 37, 38           | 21 | 1,2,4      |  |
| 12 | Fri Oct 16 | FUNERAL HOME (day)           | 40, 41, 42       | 32 | 1,2,3      |  |
| 13 | Sat Oct 17 | BRIDGE (day)                 | 45, 46           | 24 | 1,2,3,5    |  |
| 14 | Sun Oct 18 | BRIDGE (night)               | 48               | 8  | 1,2,3,5,6  | Final. Wrap. |

**Flags to resolve with the AD:**
- Day 10 has Cast #4 required but Cast #4 unavailable Oct 12-14. Move Sc 33-36 to Day 11 or Day 15, push subsequent days.
- Day 2 → Day 3 turnaround: Day 2 wraps at night, Day 3 calls in the morning. Standard 12-hour turnaround may be tight. Consider Day 2 wrap early or Day 3 late call.

## Day-out-of-days matrix

```
Cast   D1  D2  D3  D4  D5  D6  D7  D8  D9  D10  D11  D12  D13  D14   Work/Hold
  1    SW  W   W   W   W   W       W   W   W    W    W    W    WF    13 / 0
  2                    SW  W       H   H   W    W    W    W    WF    7 / 2
  3    SW  W   W               W                W                     4 / 0
  4                                              SW   WF               2 / 0
  5                            SW                             W   WF   3 / 0
  6                            SW                                  WF  2 / 0
  7            SW  W                            H              WF     3 / 1
  8    SW  W                                                     WF   3 / 0
  9                                              SW  WF               2 / 0
```

Cast #2 has a 2-day hold (Oct 12-13). Producer negotiates that against contract or considers whether the schedule can compress to remove hold days.

## Handoff note

**"This is a first-draft schedule generated from the locked screenplay. The AD and UPM should adjust for weather, permits, cast contract terms, and prep-day distribution. Do not present as a shootable schedule until AD and UPM have signed off."**
