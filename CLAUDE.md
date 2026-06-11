# CLAUDE.md — Build Brief for Maximus

This file orients Claude Code (and any agent) working in this repo. Read it
before making changes. It is the contract for *how* Maximus gets built so the
project stays coherent across sessions.

## What Maximus is

Maximus is a **free, open workhorse** that runs on top of
[OpenClaw](https://github.com/openclaw/openclaw). The one-line thesis, which
governs every decision in this repo:

> **The human is the brain. Maximus is the muscle.** Human-driven, not
> human-in-the-loop. The person supplies intelligence, judgment, and intent;
> Maximus supplies the skills, tools, context, and knowledge to execute it.

It is **not** a model, not an "intelligence layer," not a brain. The AI model
underneath is just the engine that lets Maximus execute. Don't reintroduce
"Maximus is smart / decides / knows best" framing anywhere — it contradicts the
whole point.

Audience: **technical people** (engineers, builders, founders, scientists) using
tools the operator ships. **Not retail users.** No hand-holding, no concept-101,
no friction a competent user didn't ask for.

Voice: scientist-entrepreneur-engineer. Highly technical, dry sarcastic wit, deep
and tool-rich, unflappable. No performative cheerfulness, no "great question."

## Non-negotiables

1. **Free and ungated, forever.** Never add a paywall, a gate, a "pro tier," or a
   paid middleman. If a capability requires money to use, it doesn't go in core.
2. **Core stays generic.** `core/` and `skills/` know nothing about any specific
   project, company, or domain. All domain/project specifics live in `packs/`,
   which are opt-in and off by default. This is what makes Maximus reusable
   across projects — do not leak project specifics into core.
3. **Honesty over capability theater.** Never fabricate a result, path, tool, or
   citation. If a tool/permission/context is missing, say so and say what fixes it.
4. **Secrets never committed.** No keys, tokens, or passwords in any tracked file,
   in memory, or in skill content. `.gitignore` guards the obvious cases; stay
   alert for the rest.

## Repo layout

```
core/          SOUL.md · AGENTS.md · TOOLS.md   — injected into every agent run
skills/        one folder per capability         — followed when a task matches
  _template/   copy this to start a new skill
memory/        persistent context store          — flat files now, retrieval later
mcp/           external tool wiring (example)
config/        example openclaw.json (local-model + BYOM paths)
packs/         opt-in domain bundles (OFF by default)
install.sh     symlinks the bundle into ~/.openclaw/workspace
```

`install.sh` uses symlinks, so edits to this repo apply live and `git pull`
updates a user's install. Don't switch it to copies without reason.

## How to write a skill (the core deliverable)

Skills are the point of Maximus. A skill is a folder with a `SKILL.md`. The value
of a skill is **captured expertise** — the correct procedure including the
gotchas a generic model would skip. A skill that just restates the obvious ("to
search, search the web") is worse than nothing; it costs tokens and adds no
capability. Aim for complex, battle-tested procedures.

### SKILL.md format (OpenClaw / AgentSkills spec — strict)

OpenClaw's parser requires **single-line** frontmatter keys and a **single-line
JSON** `metadata` object. Multi-line YAML in frontmatter will break it.

```markdown
---
name: skill-name
description: One precise sentence on exactly when this skill should fire. Specificity here is what makes the model trigger it correctly.
metadata: { "openclaw": { "emoji": "🔧" } }
---

# Skill Name

## When to use
Precise trigger conditions. When NOT to use it, too.

## Procedure
Numbered steps that encode the right way, including the non-obvious ones.
Verify the result before reporting done.

## Gotchas
The failure modes and how to avoid them.
```

Optional `metadata.openclaw` fields: `always` (bool, always load), `os`
(platform filter), `requires.bins` / `requires.env` / `requires.config` (load-time
gating), `emoji`. Reference the skill's own folder with `{baseDir}`.

Token cost: each eligible skill adds ~24 tokens + its field lengths to every
session prompt. Keep `description` tight. Don't ship dead-weight skills.

### Skill quality bar

- Triggers reliably (description is specific, not vague).
- Encodes something better than the model does unprompted.
- Has a verify step.
- Names its gotchas.
- Generic skills go in `skills/`; project/domain skills go in a `pack/`.

## Packs

A pack is a domain bundle: `packs/<name>/skills/<skill>/SKILL.md`, plus a
`README.md` explaining what it does and how to enable it. Packs are off by
default — the user links the skills they want into their workspace. Build packs
when a capability is specific to a domain (trading, devops, a particular product)
rather than universal.

## Conventions

- Markdown files use prose and tight lists; match the existing voice in `core/`.
- Keep `core/` files (SOUL/AGENTS/TOOLS) consistent with each other — if you
  change the philosophy in one, reconcile the others.
- Test `install.sh` after changing structure: it should link core files, memory,
  and every skill except `_template`, into `~/.openclaw/workspace`.
- Validate new SKILL.md frontmatter parses (single-line keys, single-line JSON
  metadata) before committing.
- One logical change per commit; clear messages.

## When in doubt

Ask whether the change serves a **human driving the work**. If it adds capability,
removes toil, or sharpens execution — yes. If it adds friction, gates something,
makes Maximus "decide" instead of execute, or leaks project specifics into core —
no.
