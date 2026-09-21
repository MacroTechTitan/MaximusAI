# maximus-screenplay-format — recipes

## Recipe 1: Set up the toolchain (one time)

```bash
# Install Node.js if not present
brew install node       # macOS
# or: apt install nodejs npm  (Debian/Ubuntu)

# Install afterwriting
npm install -g afterwriting

# Install Courier Prime (macOS)
# Download from https://quoteunquoteapps.com/courierprime/
# Double-click each .otf to install into Font Book
```

Verify: `afterwriting --version` should print a version string.

## Recipe 2: Start a new screenplay

Create `screenplay.fountain`:

```fountain
Title:
   Your Title Here
Credit: written by
Author: Your Name
Draft date: 2026-09-20

====

FADE IN:

INT. YOUR FIRST LOCATION - DAY

Your action goes here.

                    CHARACTER
          Your dialogue goes here.

FADE OUT.
```

Write. Save. Ready for Recipe 3 whenever.

## Recipe 3: Produce a coverage-ready PDF

```bash
afterwriting --source screenplay.fountain --pdf screenplay.pdf --overwrite
```

Verify:
- Opens in Courier Prime 12pt
- 1.5" left margin visible
- Title page renders with your title, credit, author, and draft date
- Body pages show ~55-58 lines each on representative pages

If Courier Prime doesn't render, verify the font is installed system-wide and re-run.

## Recipe 4: Export .fdx for a rep or production office

```bash
afterwriting --source screenplay.fountain --fdx screenplay.fdx --overwrite
```

Open the `.fdx` in Final Draft to confirm scene structure, transitions, and dual dialogue round-tripped correctly.

## Recipe 5: Estimate runtime

```bash
afterwriting --source screenplay.fountain --pdf screenplay.pdf --overwrite
pdfinfo screenplay.pdf | grep Pages
```

Report as a range. A 104-page screenplay estimates to 96-108 minutes. Never report a single number — the heuristic isn't that tight.

## Recipe 6: Convert an existing .fdx to Fountain

On macOS, use [Highland 2](https://quoteunquoteapps.com/highland2/) (free). File → Open → your `.fdx` → File → Export as Fountain.

On other platforms, use [textplay](https://github.com/olivertaylor/Textplay):

```bash
pip install textplay
textplay --fdx-to-fountain screenplay.fdx > screenplay.fountain
```

Round-tripped Fountain will need light manual cleanup — spacing, orphan sluglines, occasional character-name casing. Once cleaned, the plain-text file is version-controllable and diffable.
