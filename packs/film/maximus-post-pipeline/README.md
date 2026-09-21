# maximus-post-pipeline

Technical spine of feature-film post-production. Plans the pipeline, produces the round-trip artifacts, generates the deliverables matrix.

## What it's for

- Planning offline/online resolution and codec strategy before principal photography.
- Deciding the color pipeline (ACES vs Rec.709) at prep.
- Round-tripping EDL/AAF/XML between NLE and color/sound bays.
- Planning DCP prep for theatrical or festival delivery.
- Generating a deliverables matrix per confirmed buyer.

## What it's not for

- Doing the edit, grade, mix, or VFX (that's the artists' work).
- Managing post-house schedules.
- Running a DIT station.
- Executing a DCP mastering job.

## Assumed tooling

- Familiarity with at least one NLE (Avid, Premiere, Resolve, or Final Cut)
- Access to a color bay (Resolve, Baselight, or similar)
- Access to a sound bay (Pro Tools, Nuendo)
- DCP-o-matic or professional DCP toolchain if theatrical
- `ffprobe` for spec verification (see also `maximus-filmhub-delivery`)

## What ships with this skill

- `SKILL.md` — the linear pipeline, dailies workflow, ACES/Rec.709 decision, deliverables matrix
- `README.md` — this file
- `HOWTO.md` — recipes for dailies setup, offline/online conform, DCP prep, deliverables generation
- `examples/indie-feature-post-plan.md` — worked example: post plan for a 1M indie feature with streamer + festival deliverables

## Where the boundary sits

The skill plans and coordinates. Editors edit. Colorists color. Sound designers design. This skill produces the technical framework the artists work inside.
