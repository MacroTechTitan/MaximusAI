---
name: maximus-agent-dependency-vetting
description: "Vet packages an AI assistant or coding agent wants to install before anything runs: registry existence, first-publish age, publisher check, install-script blocking, release-age cooldowns, hash-pinned locks, and a human gate on new names. Use for 'slopsquatting', 'hallucinated package', 'agent npm install', 'is this package real'."
metadata: {"openclaw": {"emoji": "🔎", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — Agent Dependency Vetting

Code models name packages that do not exist, and they repeat the same invented names. Attackers register those names and wait for the install, which often runs code at install time with the developer's credentials. When the agent types `npm install` itself, there is no human between the guess and the execution. This skill puts a check there.

## Purpose

Stop hallucinated, squatted, and freshly published packages from reaching a developer machine or CI runner when the dependency came from a model, without banning new dependencies outright. Rates, versions, and dates live in `references/package-hallucination-2026-10.md`.

## Scope boundary

| Need | Use |
|---|---|
| Check that a package an agent proposes is real, old enough, and from the expected publisher | this skill |
| Contain what the agent can read, write, and reach while it runs | maximus-coding-agent-sandbox (incubator) |
| Scope and expire the tokens an install could steal | maximus-agent-access-review (incubator) |
| General code review of the diff that adds the dependency | maximus-code-review |
| CI/CD pipeline and secret handling | maximus-devops-ship |

## Core workflow

1. **Treat every model-proposed name as unverified.** That covers names in generated code, install commands, READMEs, and agent skill files. Skill files spread hallucinated names across repositories by being copied.
2. **Resolve against the registry, not memory.** Query PyPI (`/pypi/<name>/json`) or the npm registry (`/<name>`). A 404 means the model invented it: stop and find the real package, usually a near neighbour (`aws-cdk` → `aws-cdk-lib`).
3. **Check age.** If the package or the requested version was first published recently, block by default and require a person to approve. A long-registered squat passes this test, so it is a filter, not proof.
4. **Check the publisher, not the download count.** Compare the maintainer and repository link to what the real project uses. Downloads are cheap to fake and agents inflate them.
5. **Install without scripts first.** For npm, set `ignore-scripts=true` so pre- and post-install hooks do not run; enable scripts only for packages that need them, by name.
6. **Add a release-age cooldown.** npm `min-release-age` (days) or uv `exclude-newer = "7 days"`. Keep an exemption list for internal packages and urgent security fixes.
7. **Lock with hashes.** For pip, use hash-checking mode (`--require-hashes`, every requirement pinned with `==`). Hashes stop later tampering; they do not make a bad first choice safe.
8. **Gate new names on a person.** Any change that adds a new name to a manifest or lock file needs a required reviewer. Agents may update versions of approved packages; they may not introduce new ones unattended.
9. **Recheck existing locks on a schedule.** Run the existence and age check over lock files, for example quarterly, and on every new skill or template copied in from elsewhere.

## Anti-patterns

- **Letting an agent in bypass or full-auto mode run installs on the host.** Package installs are a privileged operation; run them in the sandbox with no long-lived tokens in the environment.
- **Treating "it exists" as "it is safe".** The attack works because the name exists, registered by the wrong person.
- **Trusting download counts or a polished README.** Both are easy to manufacture.
- **Copying agent skill files or templates without checking the install commands inside them.**
- **Disabling the cooldown globally because one fix was blocked.** Exempt that package by name instead.
- **Scanning only direct dependencies.** Hallucinated names can sit deeper in the tree; scan the full resolved tree.

## Output

For each proposed package: registry status (exists or 404), first-publish date and age, latest version date, maintainers and repository link, verdict (allow, hold for review, block) with the reason, and the real package to use instead when the name was invented. Plus the committed install settings (`.npmrc`, `pyproject.toml` or requirements with hashes) and the review rule for new names.
