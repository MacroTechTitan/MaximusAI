---
name: mtt-claude-cursor
description: Standard operating instructions for Macro Tech Titan development work performed with Claude Code inside Cursor. Use when preparing Claude/Cursor prompts, resuming interrupted coding sessions, reducing routine approval prompts, configuring autonomous repo execution, or handing development work to Claude Code across MTT projects such as TelePath OS, DevOS, AI Connect, DealMatch, Founders Showcase, Maximus, and related repositories.
metadata: { "openclaw": { "emoji": "🖥️", "pillar": "build", "source": "mtt" } }
---

# MTT Claude Cursor

Apply this operating model whenever producing instructions for Claude Code or Cursor on Macro Tech Titan development work.

## Launch commands

For Claude Code with Claude permission prompts bypassed:

```bash
claude --dangerously-skip-permissions
```

To resume the most recent Claude Code conversation in the current repository with permission prompts bypassed:

```bash
claude --dangerously-skip-permissions --continue
```

To choose an older resumable Claude Code session:

```bash
claude --dangerously-skip-permissions --resume
```

For Cursor Agent, use **Run Everything** under **Settings > Agents > Approvals & Execution** when the operator explicitly wants autonomous local execution. If the installed Cursor version supports the session command, use:

```text
/run-everything on
```

Treat Cursor approvals and Claude Code approvals as separate permission layers. Enabling one does not necessarily disable the other.

Never claim these modes make destructive or production actions safe. They only reduce confirmation prompts.

## Continuous execution rule

Include a compact version of this rule in Claude/Cursor development prompts unless the operator says otherwise:

```text
Routine reversible work inside the active repository is pre-authorized.
Do not ask for routine reads, searches, edits, tests, builds, lint, typecheck,
formatting, or read-only git operations.

Avoid python -c, inline Python, eval, dynamic command strings, unnecessary
command substitution, heredoc inspection scripts, and complex pipelines for
ordinary repository inspection. Prefer simple explicit commands with literal
paths such as rg, grep, find, cat, head, tail, sed, and existing project scripts.
Split complex inspection into simple commands when possible.

Stay inside the active repository. Do not broaden filesystem access merely to
avoid an approval prompt.

Stop for destructive or irreversible actions, secrets/credential actions,
production or external mutations not already authorized, database migrations
requiring operator approval, force-push/shared-history rewrites, or genuine
unresolved product/architecture decisions.
```

## Recover from interrupted Claude responses

Treat API errors, stopped response streams, terminal disconnects, and incomplete assistant messages as interruptions rather than task cancellation.

On resume:

1. Read repository instructions such as `CLAUDE.md`.
2. Inspect `git status` and `git diff`.
3. Inspect files relevant to the active task.
4. Determine what was actually written before interruption.
5. Continue from the first incomplete step.
6. Do not recreate, overwrite, or redo completed work merely because the narrative response was cut off.
7. Finish the originally required tests, typecheck, lint, and build where applicable.

Treat the filesystem and git diff as authoritative for implementation state.

A useful resume instruction is:

```text
Continue the active task. Recover progress from git status/diff and the working
tree. Do not redo completed work. Continue from the first incomplete step
through implementation and the originally required verification gates.
```

## Diagnose repeated approval prompts

If approvals continue despite permissive settings, identify which layer produced the prompt before changing configuration:

- Cursor Agent approval/classifier/sandbox
- Claude Code permission system
- repository/workspace boundary protection
- destructive-operation protection
- external/production action protection
- a command Claude generated that the permission parser cannot safely analyze

Prefer changing Claude's command shape rather than weakening unrelated protections. In particular, replace inline Python, dynamic shell strings, command substitution, and complicated pipelines with simple literal commands when they are only being used for repository inspection.

## Prompt formatting

When giving the user content intended to paste into Claude Code or Cursor, label it exactly:

**Claude**

Then provide one copyable fenced `text` block.

Keep prompts decisive and scoped. Preserve completed acceptance work. Tell Claude not to restart unrelated tasks.

## Project safety

Do not infer that a feature-development pause in one MTT project freezes other MTT projects. Apply scope controls only to the active repository/project unless explicitly told otherwise.

Do not ask the operator to use browser DevTools or paste manual console diagnostics when automated tests, application diagnostics, server logs, or admin instrumentation can establish the result.
