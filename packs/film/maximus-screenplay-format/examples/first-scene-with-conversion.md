# Example: opening scene in Fountain, converted to PDF and .fdx

## The Fountain source

`opening.fountain`:

```fountain
Title:
   NORTH OF NOWHERE
Credit: written by
Author: J. Gelet
Draft date: 2026-09-20

====

FADE IN:

EXT. TWO-LANE HIGHWAY - PRE-DAWN

Fog. A single set of HEADLIGHTS crawls east through the dark.
The road is empty. The world is not yet awake.

INT. PICKUP TRUCK (MOVING) - CONTINUOUS

MARA VESSELS (34, unshaved sleep in her eyes) grips the wheel
with both hands. A coffee thermos sweats in the cup holder. A
manila folder rides shotgun.

Her phone BUZZES on the dash. She glances. Ignores it.

The phone buzzes again. And again.

She reaches. Reads. Her jaw sets.

                    MARA
              (to no one)
          Not today.

She flips the phone screen-down and drives.

CUT TO:

EXT. GAS STATION - DAWN

The truck coasts to a stop under harsh fluorescent light. Mara
kills the engine. Sits. Does not get out.

FADE OUT.
```

## Convert to industry-standard PDF

```bash
$ afterwriting --source opening.fountain --pdf opening.pdf --overwrite
Generated: opening.pdf
```

Opening the PDF:
- Title page: `NORTH OF NOWHERE` centered ~1/3 down, "written by" beneath, "J. Gelet" beneath that, draft date bottom-left. Correct.
- Body page 1: Courier Prime 12pt. Left margin measures 1.5" with a ruler. Right and top margins measure 1.0". First slugline is `EXT. TWO-LANE HIGHWAY - PRE-DAWN` in ALL CAPS. Correct.
- Line count on the first full page: 56. Within the 55-58 target.

## Convert to Final Draft .fdx

```bash
$ afterwriting --source opening.fountain --fdx opening.fdx --overwrite
Generated: opening.fdx
```

Opening `opening.fdx` in Final Draft: scene structure preserved, transitions preserved, parenthetical `(to no one)` preserved as a Parenthetical element (not as Action), character name MARA is a Character element. All round-trip clean.

## Runtime estimate

```bash
$ pdfinfo opening.pdf | grep Pages
Pages: 3
```

3 pages → estimated runtime ~2:45-3:15 (short opening sequence). For a full 104-page draft the estimate would be 96-108 minutes.

## What we did not do

- Did not adjust the writer's dialogue.
- Did not restructure the scenes.
- Did not add or remove parentheticals.
- Did not "improve" the description lines.
- Did not offer craft notes.

The writer wrote the text. The skill formatted it. That's the boundary.
