# Maximus Film Pack

A 5-skill opt-in pack for **working filmmakers** — screenwriters, producers, line producers, post supervisors, and self-distributing directors of feature-length films. Console-first, CLI-friendly, industry-standard formats. No shorts. No AI slop. No generative video. No hand-waving.

The pack encodes the procedures a working feature-film team runs from screenplay through delivery — the parts a generic LLM would either fake, over-simplify, or drown in Hollywood cliche.

## What's in the pack

| Skill | What it does |
|---|---|
| [`maximus-screenplay-format`](./maximus-screenplay-format) | Console-first screenplay authoring in Fountain plain-text format. Output to industry-standard PDF (Courier Prime 12pt, 1.5" left margin, 55-58 lines/page) and Final Draft `.fdx`. Runtime estimation, page count discipline, coverage-ready formatting. |
| [`maximus-production-schedule`](./maximus-production-schedule) | Turn a locked Fountain screenplay into a scene breakdown, a stripboard, a one-liner, and a day-out-of-days. INT/EXT, day/night, location, cast-ID and element tagging. Console-first — no Movie Magic dependency. |
| [`maximus-film-budget`](./maximus-film-budget) | Line-item feature-film budget templating with standard AICP/AMPTP account-code structure (2100-4700 series). Above-the-line vs below-the-line. Contingency, completion-bond, fringe, and payroll-handling math. Outputs CSV/XLSX for Movie Magic Budgeting round-trip. |
| [`maximus-post-pipeline`](./maximus-post-pipeline) | The technical spine of post-production. Dailies workflow, offline/online resolution, EDL/AAF/XML round-trip between NLE and color/sound, ACES vs Rec.709 color pipeline decisions, DCP prep, and a deliverables matrix for streamer/festival/broadcast specs. |
| [`maximus-filmhub-delivery`](./maximus-filmhub-delivery) | Prepare, validate, and troubleshoot feature-film delivery masters for Filmhub (and any downstream aggregator). FFprobe-first diagnosis, remux-don't-re-encode discipline, attached-thumbnail cleanup, WSP/OBA compliance flag for securities-industry filmmakers. Based on a proven Ghosted 4K delivery profile. |

## How the skills fit together

```
              maximus-screenplay-format
                       │
                       ▼
              (locked screenplay)
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
maximus-production-schedule    maximus-film-budget
        │                             │
        └──────────────┬──────────────┘
                       ▼
                  (production)
                       │
                       ▼
              maximus-post-pipeline
                       │
                       ▼
             (finished master)
                       │
                       ▼
             maximus-filmhub-delivery
                       │
                       ▼
                  (delivered)
```

- **Screenplay** at the top locks the source.
- **Schedule + budget** in parallel translate script into a production plan.
- **Post-pipeline** takes the shot footage through offline, online, color, sound, and mastering.
- **Filmhub delivery** validates and cleans the master for aggregator upload.

Each skill loads independently — you can bring only `maximus-filmhub-delivery` to a project where the rest was done in Movie Magic and Resolve, or you can run the entire pipeline through the pack.

## Design principles for this pack

1. **Feature-length only.** The pack is opinionated: shorts and vertical/social content are different crafts with different economics. Use a different tool. This pack targets works ≥ 40 minutes runtime.
2. **No generative video, no AI slop.** The pack does not generate frames, voice-clone actors, or hallucinate cast. It formats, validates, schedules, budgets, and delivers real filmmaker work.
3. **Plain-text source, industry-standard outputs.** Fountain for screenplays, CSV for budgets and schedules, EDL/AAF/XML for post round-trip, DCP-P3 for theatrical, Rec.709 SDR MP4 for aggregators. Everything the skills produce can be opened by the tool the next department already uses.
4. **CLI-first, GUI-optional.** Every skill can be executed from a terminal on a laptop with `ffmpeg`, `python`, `node`, and free open-source tools (afterwriting, textplay, DVD Author GUI, Fountain-to-FDX converters). GUI tools are named where they help; none are required.
5. **Compliance-aware.** Filmmakers in regulated industries (securities, healthcare, legal) get compliance-flag prompts baked into the delivery skill. Not legal advice — just "you might want to check this with your CCO before you upload."

## When to use this pack

- Post-producing a feature you shot and need to deliver to a distributor or aggregator.
- Screenwriting a feature and want clean plain-text authoring with correct industry-standard output.
- Producing or line-producing a feature and want machine-readable scheduling + budgeting artifacts.
- Auditing a delivery master before uploading to Filmhub, Amazon, Apple, or a festival submission portal.

## When not to use this pack

- Short films (< 40 min runtime). Use a lighter workflow.
- Vertical social video or ads. Different craft entirely.
- Fully AI-generated films. This pack explicitly refuses that surface.
- Live broadcast. Different technical stack.

## Installation

Nothing to install for the pack itself — every skill loads on demand like any other Maximus skill. Each skill's `README.md` names the external tools it assumes (`ffmpeg`, `ffprobe`, `python`, `node`, `afterwriting`, etc.) and how to install them on macOS/Linux/Windows.

## License

MIT, same as the rest of Maximus.
