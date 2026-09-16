# Pack: devops

Domain-specific skills for development and delivery workflows. **Off by
default** — Maximus core stays generic; you opt into packs.

## Skills

- **mtt-claude-cursor** — the operating model for development work driven by
  Claude Code inside Cursor. Pre-authorizes routine reversible in-repo work
  (reads, searches, edits, tests, builds, lint, typecheck, read-only git) so the
  operator stops clearing approval prompts, and draws hard stops at destructive
  actions, secrets, production mutations, migrations, and shared-history
  rewrites. Also covers recovery from interrupted Claude responses (the
  filesystem and `git diff` are authoritative — never redo completed work),
  approval-prompt triage across the Cursor and Claude Code permission layers,
  and the `**Claude**` + single fenced block prompt format.

  Project-specific by design: it names Macro Tech Titan repositories, which is
  exactly why it lives in a pack rather than in `skills/`. See non-negotiable #2
  in [`CLAUDE.md`](../../CLAUDE.md).

## Enable

Link the skills you want into your workspace:

```bash
ln -sfn "$(pwd)/packs/devops/skills/mtt-claude-cursor" "$HOME/.openclaw/workspace/skills/mtt-claude-cursor"
```

To add a new skill to this pack, create
`packs/devops/skills/<skill-name>/SKILL.md` using the same format as core
skills (see [`skills/_template`](../../skills/_template)).

## Operating notes for mtt-claude-cursor

- **Two permission layers, not one.** Cursor Agent approvals
  (Settings > Agents > Approvals & Execution) and Claude Code permissions are
  independent. Relaxing one does not relax the other, and neither makes a
  destructive action safe — they only reduce confirmation prompts.
- **Prefer command shape over weaker protections.** When approvals keep firing,
  identify the layer that produced the prompt first. Replacing inline Python,
  dynamic shell strings, command substitution, and complex pipelines with simple
  literal commands (`rg`, `grep`, `find`, `cat`, `head`, `tail`, `sed`) usually
  fixes it without touching configuration.
- **Interruptions are not cancellations.** API errors, dropped streams, and
  truncated assistant messages mean "resume," not "restart." Read repository
  instructions, inspect `git status` / `git diff`, and continue from the first
  incomplete step through the originally required verification gates.
- **Scope stays per-repository.** A development pause on one Macro Tech Titan
  project does not freeze the others. Apply scope controls only to the active
  repository unless told otherwise.

## The point of packs

Core knows nothing about any domain. A pack turns Maximus into a specialist by
adding skills. Same free layer + devops pack = a delivery assistant; swap the
pack and it specializes elsewhere. Compose what you need, ship packs into other
projects independently.
