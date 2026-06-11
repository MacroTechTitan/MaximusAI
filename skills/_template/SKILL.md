---
name: skill-template
description: Copy this folder to create a new skill. One sentence on exactly when this skill should fire — be specific so the model triggers it correctly.
metadata: { "openclaw": { "emoji": "🧩" } }
---

# Skill Name

> Delete this template's prose and replace it with your skill. Keep the
> frontmatter format above: `name` and `description` are single lines,
> `metadata` is a single-line JSON object. OpenClaw's parser requires this.

## When to use this

State the trigger precisely. A good description is the difference between a
skill that fires when needed and one that never does. Bad: "for research."
Good: "when the user asks for current information that isn't in the model's
training or memory."

## Procedure

Encode the *correct* way to do this task, including the steps a generic model
would skip or get wrong. This is the whole value of a skill — captured expertise,
not a restatement of the obvious.

1. First step, concretely.
2. Second step. Note the gotcha here that bites people.
3. Verify the result before reporting done.

## Gotchas

- The non-obvious failure mode and how to avoid it.
- The thing that looks right but isn't.

## Notes

- Reference the skill's own folder with `{baseDir}` if you ship scripts or
  assets alongside `SKILL.md`.
- Optional gating: add `"requires": { "bins": [...], "env": [...] }` under
  `metadata.openclaw` to only load this skill when its dependencies exist.
- Keep `description` tight — it's injected into the prompt for every session, so
  every skill costs ~24 tokens plus its field lengths.
