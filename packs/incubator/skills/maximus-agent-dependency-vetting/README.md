# maximus-agent-dependency-vetting (incubator)

Pre-install checks for packages that AI assistants and coding agents propose: registry existence, first-publish age, publisher check, install scripts off by default, release-age cooldowns, hash-pinned locks, and a human gate on new names.

**Triggers:** "slopsquatting", "hallucinated package", "is this package real", "agent npm install", "vet this dependency".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/package-hallucination-2026-10.md` (rates, incidents, settings, sources), `examples/vet_package.py` (runnable checker, run live against PyPI and npm on 2026-10-21), `examples/npmrc.example` (illustrative config).

**Siblings:** maximus-coding-agent-sandbox, maximus-agent-access-review, maximus-code-review, maximus-devops-ship.

Drafted by the skill scout on 2026-10-21. Unreviewed until promoted.
