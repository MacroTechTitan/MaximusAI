# Maximus Incubator Pack

Experimental skills drafted by the skill scout (see [`SCOUT.md`](./SCOUT.md)),
one or two per weekday, based on what is trending in engineering, AI, and
research. **Off by default.** Nothing here is linked by `install.sh`, so it adds
zero tokens to any run until you opt in.

Incubator skills are machine-drafted and auto-merged without human review.
Treat them as drafts. They meet the structural bar (validated frontmatter,
dated and sourced references, illustrative code labeled), but nobody has
checked their judgment. Read one before relying on it.

## Enable one

```bash
ln -sfn "$PWD/packs/incubator/skills/<skill>" ~/.openclaw/workspace/skills/<skill>
```

## Promote one to core

Promotion is a human decision, made by PR: move the folder to `skills/`, tighten
the description to about 300 characters, re-verify the references, and update the
README catalog and `docs/lovable-homepage-prompt.md`. Every core skill costs
tokens on every run, so promote only what earns that.

## Retire one

Skills not promoted within 60 days, or whose references have gone stale, are
deleted by PR. Keeping the incubator small is part of the job.

## Ledger

Newest first. The scout appends one row per skill it ships.

| Date | Skill | Trend signal | Sources | Status |
|---|---|---|---|---|
| 2026-10-07 | `maximus-mcp-stateless-migration` | MCP spec 2026-07-28 removed sessions; migration and test guides Sep 28-29 | [MCP blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/), [computingforgeeks](https://computingforgeeks.com/migrate-mcp-server-stateless/), [TestMu](https://www.testmuai.com/blog/stateless-mcp-migration-testing/) | incubating |
