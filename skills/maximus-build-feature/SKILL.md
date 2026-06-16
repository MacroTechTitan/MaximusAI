---
name: maximus-build-feature
description: "Execute a feature implementation with read-before-edit, minimum-change discipline. Use when implementing a feature in an existing codebase, applying an approved implementation plan, or any time the user says 'build this', 'implement', 'ship the feature', 'add X to the repo'. Encodes the workhorse rule: read the file before editing, change the minimum, preserve unrelated code, run tests after every meaningful step, and never blind-overwrite. Works for Python, JavaScript/TypeScript, Go, and similar languages."
metadata:
  pillar: build
  source: maximus
---

# Maximus — Build Feature

The build phase is execution, not invention. A plan and a design tell you what to do; this skill is the discipline of *how* you do it without breaking things on the way through.

## When to use

- Implementing a feature, fix, or refactor in an existing repository.
- Applying an approved implementation plan (see `maximus-plan-implementation`).
- The user says "build", "implement", "ship", "add X", "wire up Y".

If there's no plan and the work is non-trivial, stop and plan first.

## Core rules (non-negotiable)

1. **Read before edit.** Always read the file you're editing — and the files that import or are imported by it — before changing a line. Blind overwriting loses work; mis-imports break builds.
2. **Minimum change.** Edit only what the task requires. Do not reformat, rename, reorder imports, or "clean up while I'm here" unless that *is* the task. Unrelated diffs make review impossible and revert risky.
3. **Preserve invariants.** Existing tests pass before you start. They still pass after every step. If a test legitimately needs updating, that's a deliberate change in the plan, not a side effect.
4. **Verify after every meaningful step.** Run the relevant tests (or, at minimum, the file's typecheck/lint) after each task. A green build is the unit of progress.
5. **Commit in small steps.** One task → one commit (or one PR for a coherent slice). Commit messages explain *why*, not *what* the diff already shows.
6. **Never invent APIs.** If you're not sure a function or library method exists, read the docs or the source — do not guess from training data. Hallucinated APIs are the most common AI-coding failure.

## Procedure

1. **Confirm the plan and the branch.** Working on the right branch? Plan loaded? If no plan and the work is more than one file, load `maximus-plan-implementation` first.
2. **Read the surface area.** Open every file the plan touches. Note: naming conventions, error handling pattern, logging pattern, test pattern. New code conforms to existing patterns unless the plan explicitly says otherwise.
3. **Execute task by task.** For each plan task:
   1. Read the target file(s).
   2. Apply the minimum edit.
   3. Run the task's verify step.
   4. If green: commit with a message tying it to the plan task ("plan-task-3: validate webhook signature").
   5. If red: stop and diagnose before continuing. Don't pile changes on top of a broken state.
4. **Run the full test suite at major milestones.** End of each module. Before opening a PR. Before merging.
5. **Update the plan when reality diverges.** Discovered a missing dependency? A wrong assumption? Edit the plan file before continuing. Future-you and reviewers depend on it.
6. **Surface deviations explicitly.** When you change scope ("had to touch file X that wasn't in the plan"), note it in the PR description.

## File-edit discipline (Computer's native tools)

- Use the `read` tool to load a file before editing.
- Use the `edit` tool (exact string replacement) for surgical changes. Prefer this over rewriting the whole file.
- Use the `write` tool only for new files or when the rewrite *is* the task.
- Use `grep`/`glob` to confirm an identifier or pattern's true usage across the repo before renaming, removing, or refactoring it.

## Language-specific notes

- **Python**: respect `pyproject.toml`/`setup.cfg` formatting (`black`, `ruff`). Add tests in `tests/` matching existing structure. Use type hints if the project uses them. Never `pip install` globally — work inside the project's venv/uv/poetry setup.
- **JavaScript / TypeScript**: respect `tsconfig.json`, `eslint`, `prettier`. Use the project's package manager (npm/pnpm/yarn/bun — `lockfile` tells you). Keep new code TS if the project is TS; don't smuggle in JS.
- **Go**: match the module layout; `go fmt` is non-negotiable; new packages get a `doc.go` if the project has them elsewhere.

## Gotchas

- **Blind overwriting** is the catastrophic failure: a `write` to an existing file without reading first wipes work that wasn't in your context.
- **Scope creep** ("while I was in there I also …") makes PRs un-reviewable and reverts dangerous. Refactors get their own plan.
- **Hallucinated APIs** — verify any non-trivial library call against actual docs or source. The cost of a 30-second check beats a 30-minute debug.
- **Skipping tests because they're slow** — find the targeted subset (`pytest tests/test_x.py -k case`, `vitest --filter`). Run the slow full suite at milestones.
- **Committing a broken state to "fix later"** — don't. Land green commits or stash and diagnose.
- **Reformatting on save** changing files you didn't mean to touch. Disable format-on-save for the session, or commit format changes separately and first.

## Output

Commits on the working branch, each tied to a plan task. A final chat summary lists: files changed (count), tests added (count), plan tasks completed / deferred, anything to flag to the reviewer.
