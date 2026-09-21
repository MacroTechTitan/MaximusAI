---
name: maximus-screenplay-format
description: "Console-first feature-film screenplay authoring in Fountain plain-text format, with industry-standard PDF output (Courier Prime 12pt, 1.5 inch left margin, ~55-58 lines per page) and Final Draft .fdx export. Use when writing or converting a feature-length screenplay in plain text, needing coverage-ready formatting without opening Final Draft or WriterDuet, estimating runtime from a Fountain source, converting between Fountain and .fdx or Celtx, or the user says 'screenplay formatting', 'fountain to pdf', 'final draft export', 'script formatting', 'runtime estimate', 'coverage-ready screenplay', 'convert fdx to fountain'. Do not use for shorts under 40 minutes, stage plays, teleplay/TV formats, or treatments/outlines/pitch docs. Not a craft tool: formats the writer's text, does not write, rewrite, or 'improve' it."
license: MIT
metadata:
  pack: film
  authored_by: Macro Tech Titan
---

# maximus-screenplay-format

Console-first screenplay authoring for feature-length films. Fountain plain-text source, industry-standard PDF output, Final Draft round-trip.

## Core operating rules

1. **Source is Fountain, always.** [Fountain](https://fountain.io) is a plain-text markup for screenplays with roughly the same relationship to a script that Markdown has to a document. Version-controllable, diffable, greppable, editable in any text editor.
2. **Output is Courier Prime 12pt.** Not Courier, not Courier New — Courier Prime, the free open-source revival of Courier 12 designed specifically for screenplays. [Free download](https://quoteunquoteapps.com/courierprime/). It renders correctly at the industry-standard page count.
3. **Page geometry:** 1.5" left margin, 1.0" right margin, 1.0" top margin, 1.0" bottom margin. US Letter (8.5 × 11). Yields ~55-58 lines per page depending on scene composition.
4. **Runtime estimate: one page ≈ one minute.** This is a heuristic. Action-heavy pages run longer, dialogue-heavy pages run shorter. Give a range, not a single number: "estimated runtime 96-104 minutes."
5. **Coverage-ready means industry standard.** Studio and rep coverage readers reject scripts that don't match the format. A feature script that prints at 87 pages instead of 108 for the same word count will be flagged as "wrong format" before the reader engages with the story.
6. **Do not rewrite the writer's text.** This skill formats and outputs. It does not restructure, tighten, punch up, edit, or "improve" the writer's screenplay. If the writer wants craft feedback, that's a different conversation and a different skill.

## Fountain quick reference

```fountain
Title:
   The Working Title
Credit: written by
Author: Jane Doe
Draft date: 2026-09-20

FADE IN:

INT. DINER - NIGHT

A neon sign hums. RAIN streaks the window.

MAYA (30s, tired) slides into a booth. ANDRES (40s, watchful)
is already there.

                    MAYA
          You came.

                    ANDRES
              (quiet)
          I said I would.

They regard each other. A WAITER approaches.

                    WAITER (O.S.)
          Coffee?

MAYA nods without looking away from ANDRES.

CUT TO:
```

Key markup:
- `INT.` or `EXT.` starting a line → scene heading (slugline)
- `FADE IN:`, `CUT TO:`, `FADE OUT.` → transitions
- ALL CAPS character name → dialogue block follows
- Indented `(parenthetical)` → wryly / action inside dialogue
- Plain text between scene heading and next character → action

## Toolchain (all free, all open-source)

- **[afterwriting](https://afterwriting.com/)** — command-line Fountain → PDF converter with industry-standard formatting. Node.js. `npm install -g afterwriting`.
- **[textplay](https://github.com/olivertaylor/Textplay)** — alternative Fountain → PDF / HTML / FDX converter. Python. `pip install textplay` or clone the repo.
- **[Fountain.io reference](https://fountain.io/syntax)** — the canonical syntax spec.
- **Courier Prime font** — [free download](https://quoteunquoteapps.com/courierprime/), installed once into the OS font book.
- **Any text editor** — VS Code, Vim, Emacs, Sublime, plain TextEdit. No dedicated screenwriting app required.

## Standard workflows

### Fountain → industry-standard PDF

```bash
afterwriting --source screenplay.fountain --pdf screenplay.pdf --overwrite
```

Verify output: open the PDF, confirm Courier Prime 12pt renders, confirm 1.5" left margin, count lines per page (55-58 is correct).

### Fountain → Final Draft .fdx (for the writer's rep / production office)

```bash
afterwriting --source screenplay.fountain --fdx screenplay.fdx --overwrite
```

Open the `.fdx` in Final Draft to verify structure preserved. Scene numbers, transitions, dual dialogue, and title page should all round-trip.

### .fdx → Fountain (converting an existing script to plain text)

Use [Highland 2](https://quoteunquoteapps.com/highland2/) (free on macOS) or [textplay](https://github.com/olivertaylor/Textplay) to convert. Round-tripped Fountain will be slightly less pretty than hand-authored Fountain; clean up manually if the file will be maintained long-term.

### Runtime estimate

```bash
afterwriting --source screenplay.fountain --pdf screenplay.pdf --overwrite
# then:
pdfinfo screenplay.pdf | grep Pages
# Pages: 104
```

Report as a range: "Page count 104 → estimated runtime 96-108 minutes (page-count heuristic; action-heavy pages skew longer, dialogue-heavy pages skew shorter)."

## Feature-length page-count guidance

| Genre | Typical page count | Notes |
|---|---|---|
| Drama | 100-120 | Character-driven; dialogue-heavy |
| Comedy | 90-110 | Shorter is better; jokes compress |
| Thriller | 100-115 | Momentum matters |
| Action | 100-120 | Action lines compress into shots |
| Prestige / awards | 110-135 | Traditional latitude |
| Indie feature | 85-105 | Budget-driven brevity |

Anything under 80 pages is a long short, not a feature. Anything over 140 pages needs a specific defense.

## What this skill does not do

- Does not write, rewrite, edit, "punch up," or otherwise creatively alter the screenplay.
- Does not handle TV / teleplay formats — different act structure and different page conventions.
- Does not handle stage-play formats — different everything.
- Does not handle treatments, outlines, beat sheets, or pitch documents (a different skill).

## Quality checkpoint

- [ ] Source file is valid Fountain (no orphan sluglines, character names in ALL CAPS, no rogue Markdown).
- [ ] Output PDF renders in Courier Prime 12pt.
- [ ] Page geometry is 1.5" left / 1.0" other margins on US Letter.
- [ ] Line count per page falls in the 55-58 range on representative pages.
- [ ] Runtime estimate is reported as a range, not a single number.
- [ ] Title page (title, credit, author, draft date) is present and correct.
