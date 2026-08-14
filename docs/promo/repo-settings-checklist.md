# Repo settings checklist — do these in the GitHub UI

The changes below have to be made in the GitHub web UI (they're not
git-committable). Total time: ~10 minutes.

---

## 1. About section (top-right of the repo page)

Go to https://github.com/MacroTechTitan/MaximusAI → click the ⚙️ gear
icon next to "About" in the right sidebar.

### Description (250-char limit — this fits at 179 chars)

```
43 open-source skills that make AI agents actually work. Cognitive OS, engineering, research, AI SEO. Free forever. MIT. Works with Claude, GPT, Gemini, Perplexity, and local models.
```

### Website

```
https://maximus.macrotechtitan.com
```

### Topics (add up to 20 — paste each, comma-separated in the UI)

Paste these one by one (GitHub's UI takes them as individual tokens):

```
ai
ai-agents
agent-skills
llm
llm-tools
claude
claude-skills
openai
anthropic
perplexity
prompt-engineering
rag
mlops
ai-engineering
deep-research
open-source
chain-of-verification
hallucination-reduction
seo
generative-ai
```

That's exactly 20 (GitHub's max). If you want to swap any, drop
`hallucination-reduction` first (it's the narrowest).

### Checkbox settings

- [x] Releases — check "Use your GitHub Pages website" (leave for now if
      no Pages site)
- [x] Packages — uncheck if you don't publish npm/pypi packages here
- [x] Deployments — uncheck unless you're using GitHub Environments

Click **Save changes**.

---

## 2. Social preview image

Go to https://github.com/MacroTechTitan/MaximusAI/settings → scroll to
**Social preview** (about halfway down the page).

- Click **Edit** → **Upload an image...**
- Upload the 1280×640 PNG you generated per `docs/promo/social-preview-image.md`
- Verify by pasting the repo URL into a draft LinkedIn post — you'll see the
  preview render live.

---

## 3. Pin the repo to your profile

Go to https://github.com/MacroTechTitan (your profile) → click **Customize
your pins** (top-right of the pinned repos area).

- Uncheck any dormant/experimental repos.
- Check **MaximusAI** and drag it to position 1.
- Optional: pin 2-3 supporting repos (agent apps that use Maximus, or
  the individual skill demos if any exist as standalone repos).

Save.

---

## 4. Repo-level settings tweaks

Go to https://github.com/MacroTechTitan/MaximusAI/settings.

### Features section

Enable:
- [x] Wikis — leave disabled (README is your source of truth)
- [x] Issues — **enabled** (people file bug reports and skill requests here)
- [x] Discussions — **enable this** if not already on. This is where community
      grows. Set up 4 categories: Announcements, Show and Tell, Q&A, Ideas.
- [x] Projects — disabled unless you're using them
- [x] Sponsorships — **enable if you have GitHub Sponsors set up**

### Pull Requests section

- [x] Allow squash merging — **keep enabled** (matches your merge pattern)
- [ ] Allow merge commits — disable
- [ ] Allow rebase merging — disable
- [x] Always suggest updating pull request branches — enable
- [x] Automatically delete head branches — enable (keeps the branch list clean)

---

## 5. Branch protection for main

Go to https://github.com/MacroTechTitan/MaximusAI/settings/branches → click
**Add branch ruleset** or **Add rule** for `main`.

Enable:
- [x] Require a pull request before merging (with 0 approvals since you're
      solo — this just forces the PR discipline you're already following)
- [x] Require conversation resolution before merging
- [x] Do not allow bypassing the above settings — **leave unchecked** so you
      can still push directly for doc-sync commits

This is optional but signals a mature project to visitors who click through
to Settings → Branches (some evaluators do).

---

## 6. Community Standards checklist

Go to https://github.com/MacroTechTitan/MaximusAI/community.

GitHub shows a checklist of "healthy repo" signals. Aim for a full green
checkmark. Typical items:

- [ ] Description — done in step 1
- [ ] README — done
- [ ] Code of Conduct — add `CODE_OF_CONDUCT.md` (Contributor Covenant is
      the standard: https://www.contributor-covenant.org/)
- [ ] Contributing guide — add `CONTRIBUTING.md` (one page: how to file a
      skill request, how to submit a new skill, the SKILL.md quality bar)
- [ ] License — done (MIT)
- [ ] Issue templates — add `.github/ISSUE_TEMPLATE/bug_report.md` and
      `.github/ISSUE_TEMPLATE/skill_request.md`
- [ ] Pull request template — add `.github/pull_request_template.md`

I've included ready-to-commit versions of these in `docs/promo/community-files/`
if you want to move them into place — one commit and Community Standards
goes all green.

---

## 7. Notification hygiene

Go to https://github.com/settings/notifications.

- Set "Participating and @mentions" to email + web
- Set "Watching" to web only (otherwise your inbox floods once traffic hits)
- Under "Custom routing," if you have a work email vs personal, route
  MaximusAI notifications to the address you actually check

---

## 8. One-time verification

After all of the above:

- [ ] Paste `https://github.com/MacroTechTitan/MaximusAI` into
      https://cards-dev.twitter.com/validator — verify the card renders
      with your new social preview image, description, and title.
- [ ] Paste the same URL into a draft LinkedIn post — verify the preview.
- [ ] Search GitHub for `topic:agent-skills` — verify MaximusAI shows up
      in the results (may take 24 hours for the index to update).
- [ ] Search GitHub for `topic:chain-of-verification` — same check.

---

## Total time

- About section + topics: 5 min
- Social preview upload: 2 min
- Profile pin: 1 min
- Settings tweaks: 2 min
- Community files commit: already done in this PR (see next section)
- Verification: 3 min

**Total: ~15 minutes of manual work in the GitHub UI.**
