---
name: maximus-plan-implementation
description: "Break an approved design or feature request into a concrete, minimum-change implementation plan before writing any code. Use when starting a feature build, when the user says 'plan this out', 'before you code', 'what's the approach', or after a design spec is approved and the work needs to be scheduled. Produces an ordered task list with file-level edits, dependency notes, verification steps, and rollback plan. Skip for trivial one-file changes."
metadata:
  pillar: planning
  source: maximus
---

# Maximus — Plan Implementation

A plan turns a design into a sequence of small, verifiable changes. The build phase becomes mechanical execution instead of improvisation. The horse pulls steadily when the rider has laid the route.

## When to use

- A feature, refactor, or bug fix touches more than ~3 files or more than one module.
- A design spec exists (or the work is too big to build without one) and the next step is execution.
- The work will be implemented across multiple sessions, by another agent, or by a teammate.
- The user explicitly asks for "a plan", "the approach", "steps", "tasks", or says "before you code".

**Skip** when the change is one file, well under a screen of code, and the user has indicated speed over rigor.

## Procedure

1. **Read the relevant code first.** Open every file the plan will touch. Note conventions: naming, error handling, test style, dependency injection patterns. The plan must fit the existing codebase, not the codebase the plan wishes existed.
2. **Restate the goal.** One sentence at the top. If you cannot, the requirements aren't ready — go back to clarification.
3. **List the surface area.** Every file you will create, edit, or delete. Group by module.
4. **Sequence the tasks.** Order matters: data model → backend contract → backend implementation → backend tests → frontend wiring → frontend tests → docs → migration/deploy. Each task is small enough to verify on its own.
5. **For each task, write:**
   - **What:** one-line action verb statement.
   - **Where:** file path(s).
   - **Why:** which requirement (FR/NFR ID) or design decision this realizes.
   - **Verify:** how you'll know it worked (run command, expected output, test name).
6. **Identify dependencies** between tasks explicitly. "Task 4 requires migration in Task 2." Parallelizable tasks get noted as such.
7. **Define the rollback plan.** What's the cheap revert if a step lands and breaks production? "Feature flag off", "revert migration N", "redeploy previous tag".
8. **Surface risks and unknowns.** Anything you discovered while reading the code that the design didn't anticipate. Resolve before building, or build a spike task to resolve.
9. **Estimate work bands, not hours.** "S/M/L" or "1 PR / 2-3 PRs / multi-PR". Hour estimates are theatre at this resolution.
10. **Save the plan as a file** — `docs/plans/<feature>.md` or in the relevant ticket. Plans live alongside code, not in chat history.

## Plan template

```markdown
# Implementation Plan: <feature>

**Goal:** <one sentence>
**Design spec:** <link or path>
**Estimated size:** S / M / L

## Surface area

- Create: `path/to/new_file.py`
- Edit:   `path/to/existing_file.py`
- Delete: `path/to/deprecated.py`

## Tasks

### 1. <action verb> <thing>
- **Where:** `path/to/file.py`
- **Why:** FR-3, NFR-1
- **Verify:** `pytest tests/test_<thing>.py::test_<case>` passes
- **Depends on:** —

### 2. ...

## Rollback

- Feature flag `<name>` off; revert migration `2026_06_14_add_<thing>`.

## Risks / unknowns

- <thing the design didn't address>
```

## The minimum-change rule

Every task in the plan should change the minimum amount of code required to land the requirement. Don't bundle "while I'm in there" refactors into a feature plan — they balloon scope, complicate review, and entangle revert. Refactors get their own plan.

## Gotchas

- **Plans that don't read the code first** invent file paths and patterns that don't exist. Always read first.
- **Tasks without verification steps** are guesses. If you can't say how you'll know it worked, the task is not ready.
- **Skipping rollback** is fine for a script; for anything touching prod or money, the rollback plan is the safety net the rider depends on.
- **Plans that bundle unrelated work** become un-reviewable. One feature, one plan.
- **Estimates in hours** at planning time are noise. Use size bands.

## Output

A Markdown plan saved to the project (default `docs/plans/<feature>.md`), shared with the user. The chat reply summarizes: goal, file count, task count, top risk.
