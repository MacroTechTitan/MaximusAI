# Skill Scout — procedure

The contract the daily skill-scout run follows. It lives in the repo so the
method is versioned and reviewable. Change it by PR, not by editing the
automation's prompt.

## Hard limits

1. **At most 2 skills per run.** Zero is a valid result, and better than a
   weak one.
2. **Auto-merge scope is `packs/incubator/` only.** A run may squash-merge its
   own PR only if every changed path is under `packs/incubator/`. Anything
   else — `skills/`, `core/`, `README.md`, `docs/`, `config/`, `install.sh` —
   goes in a PR that is left open for human review.
3. **Never touch core.** No promotions, no edits to existing skills outside the
   incubator, no description changes.
4. **Capacity cap.** If `packs/incubator/skills/` holds 30 or more skills,
   ship nothing. Report candidates only, until a human promotes or retires some.
5. **No force-push, no direct push to `main`.** Always branch → PR → merge.
6. **No secrets, no personal data, no paid gates** (CLAUDE.md non-negotiables).
7. **Fail closed.** If validation fails, or the overlap check is uncertain, do
   not merge. Leave the PR open and say why.

## Step 1 — Sync and inventory

- Pull `main`. List every skill name and description in `skills/` and
  `packs/*/` (including the incubator). This is the overlap baseline.
- Read the incubator ledger in `packs/incubator/README.md` for recent topics.

## Step 2 — Trend research (everything trending)

Sample broadly, then narrow. Use at least four of these per run, and rotate:

- GitHub trending (daily/weekly), new releases from widely used repos
- Hacker News front page and Show HN
- arXiv recent lists (cs.AI, cs.CL, cs.LG, cs.SE) and Papers with Code
- Release notes and changelogs: Ollama, OpenClaw, llama.cpp, vLLM, LangChain,
  LlamaIndex, major model providers
- Engineering blogs and newsletters with a track record
- Developer surveys and package-download trends where available

A trend qualifies when **at least two independent sources** show it within
roughly the last 30 days.

## Step 3 — Score candidates

Score each candidate 1-5 on:

| Criterion | Question |
|---|---|
| Demand | Will Maximus users (engineers, founders, scientists) hit this in real work? |
| Procedure | Is there a repeatable workflow with real failure modes, or just a topic? |
| Gap | Does no existing skill cover it? Name the closest skill and say why it falls short. |
| Durability | Will the core method still hold in 6 months? Volatile numbers go in a dated reference file. |
| Verifiability | Can every load-bearing claim be sourced from primary docs? |

Ship only candidates scoring **≥ 4 on Gap and Procedure, and ≥ 18 total**.
Reject news ("X launched"), vendor marketing, and anything that is really a
prompt rather than a procedure.

## Step 4 — Build to the house format

```
packs/incubator/skills/maximus-<name>/
  SKILL.md          frontmatter: name, description (≤ 350 chars, includes trigger
                    phrases), metadata (single-line JSON with
                    "openclaw": {"emoji", "pillar", "source": "maximus-scout"})
                    body: Purpose, Scope boundary table naming sibling skills,
                    Core workflow, Anti-patterns, Output
  HOWTO.md          3-5 recipes
  README.md         what it does, triggers, files, siblings
  references/<topic>-YYYY-MM.md   every number and version with a URL and pull date
  examples/         at least one worked example
```

- The name must be `maximus-<kebab-case>`, must equal the folder name, and must
  not collide with any existing skill.
- Code that was not run is labeled **illustrative**.
- Voice: technical and dry (see CLAUDE.md). No hype, no emojis in prose.

## Step 5 — Validate

Run `python packs/incubator/validate.py packs/incubator/skills/maximus-<name>`.
It must exit 0. It checks frontmatter shape, name/folder match, collisions,
description length, required files, dated references with URLs, and obvious
secret patterns.

## Step 6 — Ship

1. Branch `scout/YYYY-MM-DD-<name>`. Commit the skill folder and a new ledger
   row in `packs/incubator/README.md` (date, skill, trend signal, source URLs,
   status `incubating`).
2. Open a PR titled `Incubator: maximus-<name>`. The body holds the scorecard,
   the closest existing skill, the sources, and which code is illustrative.
3. Confirm every changed path is under `packs/incubator/`, then squash-merge
   and delete the branch. If any path is outside, leave the PR open.

## Step 7 — Friday digest

On Fridays, after shipping, open one PR (not auto-merged) proposing:

- the week's incubator skills as a short "Incubator" section for
  `docs/lovable-homepage-prompt.md` and the README catalog, and
- a promotion shortlist (at most 2) with reasons, plus any retirement
  candidates older than 60 days.

## Run report

End every run with: candidates considered (one line each, with score), skills
shipped (with PR links), skills rejected and why, and any limit that was hit.
