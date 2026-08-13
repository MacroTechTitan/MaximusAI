# Contributing to Maximus

Thanks for wanting to make Maximus better. This document tells you how to
propose changes, file issues, and — if you want — submit a new skill.

## The bar

Maximus is not a demo. Every skill in the library encodes a real procedure
the author has used in production. If you're proposing a new skill or a
material change to an existing one, expect the maintainer to ask you:

- **What specific gotcha does this skill encode that a generic model would miss?**
- **When have you personally used this procedure in real work?**
- **What's the failure mode you're guarding against?**

If you can't answer all three, the contribution isn't ready yet. That's not
a rejection — it's a signal to try the procedure on live work first, then
come back with what you learned.

## Filing an issue

Use the appropriate template:

- **Bug report** — something in an existing skill is wrong, incomplete, or
  produces bad output. Include the skill name, the model you used, and the
  input that produced the bad output.
- **Skill request** — you'd use a skill Maximus doesn't have yet. Describe
  the procedure you're currently doing manually, why a generic model can't
  do it, and what output you want back.

## Submitting a new skill

1. **Open a Skill Request issue first.** The maintainer will tell you if
   it belongs in the library, if it overlaps with an existing skill, and
   which pillar it fits.
2. **Fork the repo.**
3. **Copy `skills/_template/` to `skills/maximus-<your-skill-name>/`.**
4. **Write `SKILL.md`** following the frontmatter and structure conventions
   in `CLAUDE.md`. The description field is under 1024 characters. The name
   matches the directory name. No emoji.
5. **Bundle the skill:** `SKILL.md` (required), `README.md`, `HOWTO.md` with
   recipes, and at least one worked example under `examples/`.
6. **Validate** with `agentskills validate skills/maximus-<your-skill-name>/`.
7. **Open a PR** with a title in the form:
   `Add maximus-<your-skill-name> (<current-count> → <new-count>)`
8. **Update the README** to include your skill in the correct pillar and
   bump the total count.
9. **Update `docs/lovable-homepage-prompt.md`** to include a card for the
   new skill.

## Submitting a fix or refinement to an existing skill

1. Open a PR directly (no prior issue needed for small fixes).
2. Explain in the PR body what was wrong and how the fix changes the output.
3. If the fix changes the skill's public shape (description, workflow, or
   output structure), update all referring docs in the same PR.

## Voice and style

The library reads in one voice: workhorse. Practical. Read-before-edit,
minimum-change, verify-then-commit. No hype. No emojis. Sparing use of the
horse metaphor.

If you're not sure whether your contribution matches the voice, read three
existing skills first — `maximus-code-review`, `maximus-chain-of-verification`,
and `maximus-transaction-analyst` are good samples.

## License

By contributing, you agree that your contribution will be licensed under the
same MIT License that covers the rest of the repository.
