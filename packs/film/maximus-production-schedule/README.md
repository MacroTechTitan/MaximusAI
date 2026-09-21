# maximus-production-schedule

Console-first feature-film scheduling from a locked Fountain screenplay: scene breakdown, stripboard, one-liner, day-out-of-days.

## What it's for

- Generating a first-draft shoot schedule from a locked screenplay.
- Producing CSV/MD/JSON artifacts an AD or UPM can hand-tune.
- Running scheduling on indie or low-budget features where a Movie Magic Scheduling license isn't justified.
- Producing a day-out-of-days for cast contract negotiations.

## What it's not for

- Producing a locked, shootable schedule (AD's job).
- TV episodes.
- Documentaries (no fictional script to parse).
- Managing permits, insurance, SAG paperwork, or crew booking.

## Assumed tooling

- Python 3.10+ or Node.js 18+
- A locked Fountain screenplay
- Optional: Gorilla Scheduling if the AD wants a GUI layer

## What ships with this skill

- `SKILL.md` — parsing rules, stripboard rules, DOOD format
- `README.md` — this file
- `HOWTO.md` — recipes for parsing, stripboard build, one-liner, DOOD
- `examples/indie-feature-14-day-shoot.md` — worked example: 14-day indie feature schedule from a 96-page screenplay

## Where the boundary sits

The skill produces first-draft artifacts. The AD and UPM adjust for weather, cast holds, holidays, permits, and prep. Do not present the output as a shootable schedule.
