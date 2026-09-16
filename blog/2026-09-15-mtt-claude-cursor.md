# Maximus grows to 44 — the approval treadmill

*2026-09-15 · Macro Tech Titan*

You give an agent a repository and a clear task. It reads a file. **Approve?** It greps for a symbol. **Approve?** It runs the test suite you explicitly asked it to run. **Approve?** Forty minutes later you have clicked approve thirty times, approved nothing you actually thought about, and built a reflex that will one day wave through a `git push --force` on a shared branch without reading it.

That is the failure mode. Not that the agent did something dangerous — that the confirmation prompt stopped being a decision and became a twitch. A permission system that fires on everything protects nothing, because the human on the other end has stopped reading it.

Today Maximus gets a skill for that specific problem.

## The new skill

**[`mtt-claude-cursor`](../packs/devops/skills/mtt-claude-cursor)** — the operating model for development work driven by Claude Code inside Cursor.

It does four things:

1. **Pre-authorizes the routine.** Reads, searches, edits, tests, builds, lint, typecheck, formatting, read-only git — inside the active repository, these are reversible and they are not decisions. The agent does them and reports.
2. **Draws the line where it belongs.** It stops for destructive or irreversible actions, anything touching secrets or credentials, production and external mutations not already authorized, database migrations needing operator approval, force-push and shared-history rewrites, and genuine unresolved product or architecture decisions. Those are the prompts worth reading, and now they arrive alone instead of buried in thirty about `cat`.
3. **Treats interruptions as interruptions.** API errors, dropped streams, terminal disconnects, and truncated assistant messages are not task cancellations. On resume the skill reads repository instructions, inspects `git status` and `git diff`, determines what was actually written, and continues from the first incomplete step — through the tests, typecheck, lint, and build that were originally required.
4. **Diagnoses approvals instead of disabling them.** When prompts keep firing despite permissive settings, it identifies which layer produced the prompt before touching any configuration.

## The part that surprised me

The most useful rule in the skill is not about permissions at all. It is about command shape.

A permission system has to decide whether a command is safe. It can analyze `rg TODO src/` in a way it fundamentally cannot analyze a heredoc that pipes into `python -c` with a command-substituted path. So it does the only defensible thing and asks. Most of the approval prompts I was fighting were not the guardrails being paranoid — they were the agent writing inspection commands nobody could statically verify, for the entirely mundane purpose of looking at a file.

The fix is not a looser setting. The fix is:

```text
Avoid python -c, inline Python, eval, dynamic command strings, unnecessary
command substitution, heredoc inspection scripts, and complex pipelines for
ordinary repository inspection. Prefer simple explicit commands with literal
paths such as rg, grep, find, cat, head, tail, sed, and existing project scripts.
Split complex inspection into simple commands when possible.
```

Simple literal commands with literal paths. The prompts mostly stop, and — this is the point — every protection you actually wanted is still armed. You did not trade safety for quiet. You stopped generating unanalyzable commands.

The corollary is a rule the skill states plainly and I would not remove: **`--dangerously-skip-permissions` and Cursor's Run Everything do not make destructive or production actions safe. They reduce confirmation prompts. That is all they do.** Cursor's approval layer and Claude Code's permission system are also independent — relaxing one does not relax the other, and assuming otherwise is how people discover they had exactly one seatbelt on.

## Where it lives, and why that took two PRs

Worth documenting, since this repo is built in public and the first attempt was wrong.

The skill shipped into `skills/` alongside the core catalog. That violated non-negotiable #2 in [`CLAUDE.md`](../CLAUDE.md): `core/` and `skills/` know nothing about any specific project, company, or domain. This skill names Macro Tech Titan repositories out loud — TelePath OS, DevOS, AI Connect, DealMatch, Founders Showcase, Maximus. Useful to us, dead weight in every session for anyone else, and precisely the leak that rule exists to prevent.

So it moved to [`packs/devops/skills/mtt-claude-cursor`](../packs/devops/skills/mtt-claude-cursor) — opt-in, off by default, one symlink to enable:

```bash
ln -sfn "$(pwd)/packs/devops/skills/mtt-claude-cursor" "$HOME/.openclaw/workspace/skills/mtt-claude-cursor"
```

The same pass caught a second thing: the frontmatter used multi-line YAML for `metadata`, which OpenClaw's parser does not accept. It is single-line JSON now. Both mistakes were in a repo whose own contributor guide should have caught them, so the guide now does — `CONTRIBUTING.md` makes core-versus-pack an explicit early decision, and `CLAUDE.md` carries the standing execution contract for anyone driving this repository from Cursor.

Nothing in that paragraph is a fun update to write. It is the honest one, and the alternative — quietly fixing it and describing the result as if it had been designed that way — is exactly the capability theater this project refuses elsewhere.

## What ships with it

Deliberately thin. `SKILL.md` carries the whole procedure, plus `agents/openai.yaml` and an icon for OpenAI Assistants integration. No `HOWTO.md`, no `examples/` — the skill *is* the procedure, and padding it with worked examples of "here is a repository being read" would cost tokens in every session and teach nothing.

## Where it fits

The Build & Ship pillar covers what to do: spec it, plan it, build it, review it, debug it, test it, ship it. This skill covers the conditions under which any of that gets done without a human in the loop of every `grep`. It sits under the work rather than beside it, which is why an opt-in pack is the right shape — your repositories are not our repositories, and the specifics matter.

## Reach for it

Load `mtt-claude-cursor` when you are driving Claude Code inside Cursor and spending more attention on approval dialogs than on the work. Load it when a response died mid-task and you need the agent to resume from git state instead of cheerfully redoing forty minutes of finished work. Load it when approvals keep firing despite permissive settings and you want to know which layer is asking before you start weakening things you will regret weakening.

Fork it and swap the project names for your own — that is what packs are for.

Details in the [README](../README.md) and [`packs/devops/`](../packs/devops).

**44 skills. 5 pillars. Free forever. No gate.**

The workhorse works. It just stops asking permission to look at a file.
