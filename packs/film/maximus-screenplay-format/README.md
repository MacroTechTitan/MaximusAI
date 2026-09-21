# maximus-screenplay-format

Console-first feature screenplay authoring. Plain-text source (Fountain), industry-standard PDF and .fdx output.

## What it's for

- Writing a feature-length screenplay in plain text without opening Final Draft or WriterDuet.
- Converting an existing `.fdx` or `.celtx` to Fountain for version-controllable long-term maintenance.
- Producing coverage-ready PDFs (Courier Prime 12pt, correct margins, ~55-58 lines/page).
- Round-tripping Fountain ↔ Final Draft `.fdx` for handoff to reps or production office.
- Runtime estimation from page count.

## What it's not for

- Writing, rewriting, editing, or "improving" the screenplay itself.
- TV / teleplay formats.
- Stage plays.
- Treatments, outlines, beat sheets, pitch documents.
- Shorts under 40 minutes.

## Assumed tooling

- Node.js ≥ 18 for `afterwriting` (`npm install -g afterwriting`)
- Python 3 for `textplay` if using that instead
- Courier Prime font installed system-wide ([free download](https://quoteunquoteapps.com/courierprime/))
- Any text editor

## What ships with this skill

- `SKILL.md` — operating rules, Fountain reference, toolchain, workflows
- `README.md` — this file
- `HOWTO.md` — recipes for authoring, converting, and estimating runtime
- `examples/first-scene-with-conversion.md` — worked example: opening scene in Fountain, converted to PDF and .fdx

## Where the boundary sits

This skill is a formatting and conversion skill. It does not offer craft feedback, structural notes, character analysis, or dialogue polish. Those are separate disciplines. This skill produces industry-standard artifacts from the writer's plain-text source, and that's it.
