---
name: file-ops
description: Create, edit, or reorganize files in the workspace. Use when the user wants a real artifact they can keep or when modifying existing files, rather than printing content into chat.
metadata: { "openclaw": { "emoji": "📁" } }
---

# File Operations

When the user wants something they'll keep, edit, or run — a document, a script,
a config — produce a real file, not a wall of text in chat.

## When to use

- The output is a standalone artifact (a script, doc, config, dataset).
- The output is long (more than a screen) or the user will edit/reuse it.
- The user said "save", "write a file", "create", or named a path/format.

When the answer is something they'll just read once, keep it in chat instead.

## Procedure

1. **Confirm the target.** Know the path and format before writing. If editing an
   existing file, read it first — never blind-overwrite.
2. **Write to a working location, verify, then place the final artifact** where
   the user expects it.
3. **For edits, change the minimum.** Preserve everything you weren't asked to
   touch. Don't reformat or rewrite unrelated sections.
4. **Report what changed.** One line: what file, what you did.

## Gotchas

- Reading before editing is non-negotiable — overwriting unseen content loses
  work.
- Before deleting or overwriting, confirm unless the user gave standing approval.
- Don't write secrets into committed files.
