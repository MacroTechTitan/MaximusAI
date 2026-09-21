# Maximus grows to 49 — the Film Pack, for working filmmakers

*2026-09-20 · Macro Tech Titan*

Every AI-tool launch of the last two years has taken a run at "filmmaking." The pitch is always the same: generate the frames, generate the voice, generate the cast, generate the score, generate the poster. Then generate the audience while you're at it.

That's not filmmaking. It's slop.

Today Maximus adds a pack for the people who make films the old way — the way that involves cameras, cast, a shot list, a call sheet, a color bay, and a delivery master a distributor will actually accept. Five skills, opt-in, console-first, feature-length only. Suite total: 49.

## What's in the pack

**`packs/film/`** — five skills covering the technical spine of a feature production:

- **`maximus-screenplay-format`** — Console-first Fountain screenplay authoring. Output to industry-standard PDF (Courier Prime 12pt, 1.5" left margin, 55-58 lines per page) and Final Draft `.fdx`. Runtime estimation from page count. Because the writer's rep will not read a 92-page feature that prints as 71 pages.

- **`maximus-production-schedule`** — Turn a locked Fountain screenplay into a scene breakdown, a stripboard grouped by location, a chronological one-liner, and a day-out-of-days matrix. Console-first, no Movie Magic Scheduling license required. Flags turnaround violations, company-move-heavy days, and consecutive-night runs.

- **`maximus-film-budget`** — Line-item feature-film budget templating with standard AICP/AMPTP account codes (1000-4700 series). Above-the-line vs below-the-line. Contingency, completion bond, fringes, payroll handling. CSV/XLSX for Movie Magic Budgeting round-trip. The skill never invents a rate — every dollar figure is a `TBD` for the line producer to fill.

- **`maximus-post-pipeline`** — The technical spine of post. Dailies workflow, offline/online conform, EDL/AAF/XML round-trip, ACES vs Rec.709 color pipeline decision, DCP prep for theatrical, and a per-buyer deliverables matrix (Netflix, Amazon, Apple, A24, Sundance, TIFF).

- **`maximus-filmhub-delivery`** — Prepare, validate, and troubleshoot feature-film delivery masters. FFprobe-first diagnosis, remux-don't-re-encode discipline, attached-thumbnail cleanup, audio-format correction. Includes a WSP/OBA compliance flag for securities-industry filmmakers (yes, this is a real category — FINRA Rule 3270 and Rule 2210 both apply when a registered representative releases a film touching on brokers or investments).

## Design principles

The pack is opinionated on purpose:

1. **Feature-length only.** Anything under 40 minutes is a different craft with different economics. The pack refuses the surface.
2. **No generative video, no AI slop.** The pack does not generate frames, voice-clone actors, or hallucinate cast. It formats, validates, schedules, budgets, and delivers real filmmaker work.
3. **Plain-text source, industry-standard outputs.** Fountain for screenplays, CSV for schedules and budgets, EDL/AAF/XML for post round-trip, DCI-P3 for theatrical, Rec.709 SDR MP4 for aggregators. Every artifact opens in the next department's existing tool.
4. **CLI-first, GUI-optional.** Every skill runs from a terminal with `ffmpeg`, `python`, `node`, and free open-source tools. Named GUI apps (Movie Magic, Final Draft, Resolve) are supported for round-trip but never required.
5. **Compliance-aware.** Filmmakers in regulated industries get a compliance flag prompt baked into the delivery skill.

## The Filmhub story that started this

The pack's `maximus-filmhub-delivery` skill exists because a real film — *Ghosted*, a 4K feature — was rejected by Filmhub for "Multiple Video Streams Detected." The film was fine. Wondershare Filmora had embedded a thumbnail as a second `mjpeg` video stream, and Filmhub's validator read it as two movies.

The fix wasn't a re-render (which would have taken hours on a 4K master and introduced generational quality loss). The fix was a 30-second `ffmpeg` remux with `-c copy` that dropped the extra stream and kept the film untouched.

That's the workhorse discipline. Diagnose before you re-encode. Preserve the master. Verify the fix. Do not overwrite. Do not confuse a container problem with a picture problem.

That specific lesson — and four others from the same production — became the pack.

## What the pack is not

It's not a "make an AI film" pack. It has no text-to-video, no voice cloning, no synthetic actor generation, no auto-generated cinematography. If you want those tools, the market has them and Maximus won't compete on that surface.

It's also not a shorts pack, a social-video pack, or a TV pack. Those are different crafts. This pack is exclusively feature-length narrative work.

And it's not a creative pack. Nothing in the pack rewrites the screenplay, restructures the schedule based on artistic preference, sets a budget number, colors a frame, or mixes a track. Every skill formats, validates, and delivers the work the filmmakers already did.

## Where the pack fits in the Maximus catalog

Maximus's structure is five pillars (Cognitive OS, Build & Ship, AI Engineering, Writing/Research/People, AI SEO) plus opt-in packs. The Film Pack is the third opt-in pack, alongside `packs/ai-seo/` and `packs/devops/`.

- **Total skills:** 49 (across pillars + packs)
- **Pillars:** 5 (unchanged)
- **Opt-in packs:** 3 (AI SEO 7, Dev Workflow 1, Film 5)

The pack model is doing what packs do — letting the suite grow into new domains without contorting the core five pillars.

## For whom

- Screenwriters working on feature-length material who want plain-text authoring with correct industry-standard output.
- Producers and line producers preparing shoot schedules, day-out-of-days, and budgets for indie or low-budget features.
- Post supervisors coordinating dailies, conform, color, sound, DCP, and deliverables.
- Self-distributing directors auditing a delivery master before uploading to Filmhub, Amazon, Apple, or a festival portal.
- Filmmakers in regulated industries (securities, healthcare, legal) who need a compliance-flag prompt before public release.

## Try the pack

Everything at [`packs/film/`](https://github.com/MacroTechTitan/MaximusAI/tree/main/packs/film) on the repo. MIT, free forever, no signup, no telemetry. Same discipline as the rest of Maximus: sources over speculation, the work over the pitch, the horse over the show.

**49 skills. 5 pillars. 3 packs. One workhorse.**

The workhorse works — including where the work involves 24 frames a second and a real audience.
