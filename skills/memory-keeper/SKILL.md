---
name: memory-keeper
description: Read and write Maximus's persistent memory. Use at the start of any context-dependent task to recall what's known about the user, and after learning a durable fact about the user, their projects, preferences, or decisions.
metadata: { "openclaw": { "emoji": "🧠", "always": true } }
---

# Memory Keeper

Maximus's memory lives in the `memory/` directory of the workspace. This skill
is the discipline for using it. It is `always` on — memory is core, not optional.

## When to READ memory

Before answering anything that depends on the user's situation:

- References to "my project", "my account", "the usual", or past decisions.
- Preferences (how they like things formatted, what tools they use).
- Anything where a generic answer would be worse than a contextual one.

Read `memory/memory.md` first. If the store has grown into multiple files (e.g.
`memory/projects/`, `memory/preferences.md`), scan the relevant ones.

## When to WRITE memory

After learning something that will still matter next session:

- A durable fact (their stack, their role, a recurring constraint).
- A decision or preference they expressed ("always use X", "never do Y").
- The state of an ongoing piece of work.

Do **not** write: transient details, secrets (keys/tokens/passwords), or
anything the user asked you to forget.

## Write procedure

1. Read the current `memory/memory.md` so you don't duplicate or contradict.
2. Append or update the relevant section. Keep entries terse — one line each.
3. Confirm to the user briefly that you noted it ("Got it, I'll remember that").

## Scaling up (when files get big)

Flat `memory.md` works until it's large enough to bloat context. When that
happens, graduate to retrieval: OpenClaw ships memory plugins
(`memory-lancedb` for vector recall, `memory-wiki` for structured notes). Switch
the store to one of those and this skill's read step becomes a query instead of
a full-file read. Until then, flat files are simpler and fine.

## Gotchas

- Don't reload the entire memory store on every trivial turn — only when the
  task is context-dependent. Memory has a token cost.
- Never write a secret into memory. If a fact includes a credential, record the
  fact and omit the credential.
