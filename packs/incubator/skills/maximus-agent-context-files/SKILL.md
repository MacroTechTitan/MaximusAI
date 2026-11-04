---
name: maximus-agent-context-files
description: "Write AGENTS.md and CLAUDE.md rules coding agents actually follow, measure compliance per harness and model, and move must-hold rules into hooks, deny rules, or CI. Covers wording (direct beats conditional), size, path-scoped rules, and checks on real session diffs. Use for 'agents ignore AGENTS.md', 'write CLAUDE.md', 'make rules stick'."
metadata: {"openclaw": {"emoji": "📏", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Agent Context Files

An agent context file (AGENTS.md, CLAUDE.md, rules files) is advice the model weighs, not configuration the harness enforces. A November 2026 study added one rule in four wordings to 86 benchmark tasks: one model followed the direct wording in 71.6% of sessions and the prohibitive wording in 17.3%; another followed no wording more than 1.5% of the time. Wording matters, the model matters more, and neither is a guarantee. This skill is about writing the file so the rules that can be advice work well, and getting the rules that must hold out of the file.

## Purpose

Produce context files that are short, concrete, and worded for compliance; measure whether agents follow them on your stack; and move every rule with zero exceptions into a mechanism the harness or CI enforces. Study numbers, file limits, and hook formats are in `references/agent-context-files-2026-11.md`.

## Scope boundary

| Need | Use |
|---|---|
| Writing context-file rules, measuring compliance, choosing what becomes a hook | this skill |
| Which instruction files load, whether they are trustworthy, config drift | maximus-agent-instruction-audit (incubator) |
| OS-level containment of the agent | maximus-coding-agent-sandbox (incubator) |
| Protecting monitors and alerts from agent edits | maximus-agent-oversight-integrity (incubator) |
| System prompts and few-shot design for LLM products | maximus-prompt-engineering |

## Core workflow

1. **Sort every rule into guideline or invariant.** A guideline has exceptions the agent may judge (naming, structure, preferred libraries). An invariant has none (never read `.env`, never touch migrations, always run the formatter). Invariants do not stay in the file alone.
2. **Enforce invariants outside the model.** Use deny rules for reads and commands, `command` hooks (not `prompt` or `agent` hooks, which ask another model) for checks before and after tool calls, managed settings for organization policy, and CI or branch protection for anything that must be true at merge. Keep a one-line note in the context file saying what is enforced and how to ask for an exception.
3. **Write guidelines as direct instructions.** State what to do, as a plain imperative. In the study, conditional phrasing ("If you add a function, ...") lost to direct and explained phrasing in every model where wording made a difference. Prohibitive phrasing ("Never ... without ...") was erratic. Add a reason when it helps; test which works better on your model.
4. **Make every line concrete and checkable.** "Run `npm test` before committing", not "test your changes". If you cannot tell from a diff whether a rule was followed, rewrite it or drop it.
5. **Keep the file short.** Claude Code's docs target under 200 lines per CLAUDE.md, and Codex stops adding files once the combined size reaches `project_doc_max_bytes` (32 KiB by default). Move multi-step procedures to skills, and rules that apply to one part of the tree to path-scoped rules or nested files.
6. **Remove conflicts.** Nested files are concatenated, so contradictory lines both load and the agent may follow either one. Review the merged view, not each file on its own.
7. **Measure on your own stack.** Pick the checkable rules, collect the diffs of 20 or more real sessions per harness and model, and run `examples/rule_compliance.py`. A rule below your threshold either gets reworded and re-measured or becomes a hook or CI check.
8. **Re-measure when anything changes.** A model upgrade, a harness upgrade, or a file rewrite can move compliance by tens of points. Treat the compliance table as a dated artifact.

## Anti-patterns

- **Adding emphasis instead of enforcement.** If a line keeps being missed after ALL CAPS and "IMPORTANT", it belongs in a hook.
- **Security rules in prose only.** Injected text, a misread task, context compaction, or an edited file can defeat them.
- **Hooks for preferences.** A hook is for a rule with zero exceptions; hooking "prefer named exports" just blocks legitimate work.
- **Assuming one model's compliance carries over.** In the study, the same harness with a different model followed the same rule half as often.
- **Imports to save space.** `@path` imports load with the file that imports them; they organize, they do not shrink.
- **Rules the agent can disable.** Hooks in a repository file the agent can edit are weaker than managed settings it cannot.

## Output

The rule inventory with each rule labeled guideline or invariant, the enforcement mechanism for each invariant, the rewritten context file (line count and byte size), the compliance table per harness and model with session counts and date, and the list of rules moved to hooks or CI with the reason.
