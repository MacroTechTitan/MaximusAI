# Pack: devops

Domain-specific skills for devops workflows. **Off by default** — Maximus core
stays generic; you opt into packs.

This is a placeholder showing the pack pattern. Add skills here as
`packs/devops/skills/<skill-name>/SKILL.md`, same format as core skills.

## Enable

Link the skills you want into your workspace:

```bash
ln -sfn "$(pwd)/packs/devops/skills/<skill>" "$HOME/.openclaw/workspace/skills/<skill>"
```

## The point of packs

Core knows nothing about any domain. A pack turns Maximus into a specialist by
adding skills. Same free layer + devops pack = a devops assistant; + devops
pack = a deploy assistant. Compose what you need, ship packs into other projects
independently.
