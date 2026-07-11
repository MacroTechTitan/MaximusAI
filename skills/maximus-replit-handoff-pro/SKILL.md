---
name: maximus-replit-handoff-pro
description: "Generate a production-grade Replit Agent handoff for work built in Perplexity Computer. Use when the user says 'hand off to Replit', 'generate the Replit prompt', 'sync to Replit', 'paste into Replit Agent', or wants to transfer a feature from Computer to Replit. Goes beyond a basic prompt: includes git SHA + branch, exact dependency commands, environment variables required (with which scope), Vercel/Stripe-aware integration checks, smoke-test verification, and a rollback note. Produces a Markdown document Replit Agent can consume end-to-end."
metadata:
  pillar: deployment
  source: maximus
---

# Maximus — Replit Handoff Pro

A handoff is the moment your work leaves your hands. Done well, the next agent or human picks up exactly where you stopped — no re-discovery, no missing env var, no "what version of Node did you use?". This skill is the upgraded handoff format: a single Markdown document that contains everything Replit Agent needs to integrate, run, and verify the work, plus the Vercel/Stripe-aware checks that the basic handoff misses. The horse passes the reins cleanly; the next rider doesn't have to find them in the grass.

## When to use

- The user has built a feature in Perplexity Computer (likely against a GitHub repo) and now wants to continue work in Replit Agent.
- They say: "hand off to Replit", "generate the Replit prompt", "sync to Replit", "paste into Replit Agent", "get this into Replit".
- A multi-platform workflow is in play (Computer for planning/build, Replit for live iteration, Vercel for deploy).

## What the handoff document must contain

The document is the contract. If any of these is missing, the next agent has to guess — and guessing breaks the build.

1. **Header**: feature name, source thread URL, date, target repo (`owner/name`), target branch, source git SHA the handoff was produced from.
2. **One-sentence goal**: what this feature does, in plain language.
3. **Files touched**: every file created, edited, or deleted, with one-line description of what changed.
4. **Dependencies added or upgraded**: exact package name + version, with the install command for the project's package manager (`npm install`, `pnpm add`, `pip install`, `uv add`, `go get`).
5. **Environment variables**: each new env var, its purpose, example value, and Replit secret scope (Secrets / Deployment Secrets). Mark which are required vs optional.
6. **Local run commands**: the exact sequence from clone to running app, in copy-pasteable code blocks.
7. **Integration checks**: what the next agent should verify works before continuing. Includes the Vercel/Stripe/external-service hooks below.
8. **Tests added**: file paths and the command to run them.
9. **Known limitations and follow-ups**: anything left undone, intentional or otherwise.
10. **Rollback note**: how to revert the change if it breaks something.

## Procedure

1. **Confirm the work is committed and pushed.** A handoff to an unpushed commit is fiction. Verify `git status` is clean and the branch is on the remote.
2. **Capture the SHA and branch** of the current state. Include both — SHA for reproducibility, branch for discoverability.
3. **Diff against the merge-base** with `main` (or the target branch) to enumerate file changes accurately. Don't list from memory.
4. **List new dependencies from the lockfile diff**, not the manifest — manifests can claim a version that the lockfile pins differently.
5. **Inventory required env vars** by grepping for `process.env.` / `os.environ` / `os.getenv` in the new files. Don't rely on `.env.example` being current.
6. **Run the integration check list** locally one last time before writing the handoff. If any check fails for you, it'll fail for Replit Agent.
7. **Write the document** to `docs/handoffs/<feature>-<date>.md` in the repo and commit it as part of the handoff. The handoff lives alongside the code it describes.
8. **Share the document** with the user, with copy-paste-ready content ready for the Replit Agent input field.

## The integration check list

The next agent should verify these before continuing development. Tailor to the feature:

- **Build passes**: `npm run build` (or equivalent) completes without errors.
- **Tests pass**: targeted command for the new tests, plus the full suite.
- **Type/lint pass**: `tsc --noEmit`, `ruff check`, `eslint`, as applicable.
- **Local server starts**: server boots; `/api/health` (or smoke endpoint) returns 200.
- **Vercel preview deploys** (if this is a Vercel project): pushing to the branch triggers a preview build; preview URL is reachable and the new feature works there.
- **Stripe paths verified** (if this touches payments): test-mode key set; a test charge flows end-to-end; webhook receiver hits with verified signature; audit log row appears.
- **Secrets present**: every env var the handoff lists is set in Replit Secrets with the right scope. Print-and-check the names (never the values).
- **External services reachable**: any third-party API (Stripe, OpenAI, Sonar, Folk, Apollo, etc.) returns a 200 from a minimal probe.

## Handoff document template

```markdown
# Replit Handoff: <feature-name>

**Source thread:** <Perplexity Computer URL>
**Repo:** <owner>/<name>
**Branch:** <branch>
**Commit SHA:** <sha>
**Date:** <YYYY-MM-DD>
**Author:** Perplexity Computer (Maximus build skills)

## Goal

<one sentence describing what this feature does>

## What changed

### Files
- `path/to/new.ts` — <one-line purpose>
- `path/to/existing.ts` — <what changed>

### Dependencies
- `package@x.y.z` — <why added>
  - Install: `pnpm add package@x.y.z`

### Env vars
- `STRIPE_SECRET_KEY` (required, Replit Secret, prod scope) — server-side Stripe API key
- `NEXT_PUBLIC_STRIPE_PK` (required, Replit Secret, all scopes) — publishable key for Stripe Elements
- `WEBHOOK_SIGNING_SECRET` (required, Replit Secret, prod scope) — Stripe webhook signature secret

## Local run

```bash
git fetch && git checkout <branch>
pnpm install
cp .env.example .env  # fill in the values above
pnpm dev
```

App on http://localhost:5173; API on http://localhost:3001.

## Integration checks (run before continuing)

- [ ] `pnpm build` passes.
- [ ] `pnpm test` passes; new tests in `tests/<feature>.test.ts` pass.
- [ ] `pnpm typecheck && pnpm lint` pass with zero new errors.
- [ ] Local server: `curl localhost:3001/api/health` returns `{"ok":true}`.
- [ ] Vercel preview URL renders the new UI and the feature works end-to-end.
- [ ] Stripe test charge: `stripe trigger payment_intent.succeeded` → webhook handler logs an audit row.
- [ ] Replit Secrets contain every env var listed above.

## Tests added

- `tests/<feature>.test.ts` — covers happy path, validation, and webhook signature failure.
  Run: `pnpm test tests/<feature>.test.ts`

## Limitations / follow-ups

- <thing intentionally left for next iteration>
- <known edge case not yet handled>

## Rollback

To revert: `git revert <sha>` and redeploy. No data migration to undo.

## Replit Agent — start here

Pull this branch, run the local commands above, run the integration check list, and resume from "Limitations / follow-ups". Do not modify files outside the touched list without flagging it in the next handoff.
```

## Gotchas

- **Handoff to an unpushed commit**: Replit can't see what isn't on the remote. Push first.
- **Outdated `.env.example`**: don't trust it — grep the new code for env reads and list them yourself.
- **Manifest vs lockfile mismatch**: list from the lockfile, which is the truth.
- **Skipping Vercel preview verification**: a feature that "works locally" but breaks the Vercel preview will silently land broken on the next merge.
- **Stripe handoff without test-mode verification**: payments code that has only run in mocks is unverified payments code.
- **No rollback note**: the next agent doesn't know how to safely undo your change if it bites.
- **Treating the handoff as throwaway chat**: it goes in the repo (`docs/handoffs/`) and is committed. The trail outlives the session.

## Output

A Markdown handoff document, written to `docs/handoffs/<feature>-<date>.md` in the repo and committed. The chat reply provides the handoff content in a copy-paste-ready block for pasting into Replit Agent, plus a one-line summary: "Handoff for <feature> at <branch>@<sha-short> — N files, M env vars, K integration checks."
