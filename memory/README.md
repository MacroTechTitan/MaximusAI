# Memory

This directory is Maximus's persistent memory across sessions. The
`memory-keeper` skill defines how Maximus reads and writes it.

## How it works now (flat files)

`memory.md` is a plain Markdown file. Maximus reads it before context-dependent
tasks and appends durable facts as it learns them. Simple, inspectable, and
plenty for a single user. Edit it directly anytime — it's yours.

You can split it into more files as it grows:

```
memory/
  memory.md            # general
  preferences.md       # how you like things
  projects/<name>.md   # per-project context
```

The `memory-keeper` skill will scan the relevant files.

## When to graduate to retrieval

Flat files start costing too many tokens once they're large (roughly when the
store no longer fits comfortably in context). At that point, switch to a
retrieval-backed store so Maximus pulls back only the relevant pieces per query.
OpenClaw ships two options:

- **memory-lancedb** — vector recall (semantic search over your notes).
- **memory-wiki** — structured, linkable notes.

Enable one in `openclaw.json`, migrate the content, and the `memory-keeper`
skill's read step becomes a query instead of a full-file load. Don't reach for
this on day one — flat files are simpler and correct until they aren't.

## Rules

- Never store secrets (keys, tokens, passwords) here.
- Keep entries terse — one line each.
- Anything you want forgotten, just delete; tell Maximus and it won't re-add it.
