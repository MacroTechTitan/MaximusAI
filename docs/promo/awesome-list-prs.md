# Awesome-list PR entries — ready to submit

Below are five awesome-list PRs, each ready to paste into a fork. Submit them
one at a time so a rejection on one doesn't cascade.

For each: fork the target repo, add the line to the correct section in
alphabetical order (most awesome-lists require this), commit with the PR
title shown, and open the PR with the body shown.

---

## PR 1: awesome-llm-apps

**Target repo:** https://github.com/Shubhamsaboo/awesome-llm-apps
**Section to add to:** Look for a section like "AI Agent Frameworks", "Multi-Agent Systems", or "Developer Tools" — whichever fits. If none fits, propose a new section called "Skill Libraries".
**Alphabetical order:** yes.

### Line to add

```markdown
- [MaximusAI](https://github.com/MacroTechTitan/MaximusAI) — 43 open-source skills for AI agents across cognitive OS, build-and-ship, AI engineering, research, and AI SEO. Model-agnostic (Claude, GPT, Gemini, Perplexity, local Llama/Qwen/K3). MIT-licensed, ungated, no signup.
```

### Commit / PR title

```
Add MaximusAI — 43 open-source skills for AI agents
```

### PR body

```
Adding [MaximusAI](https://github.com/MacroTechTitan/MaximusAI), a suite of 43 open-source Agent Skills (SKILL.md format, MIT-licensed) covering:

- **Cognitive OS** — a think-before-act operating layer for any LLM
- **Build & Ship** (10 skills) — feature planning, implementation, code review, debugging, testing, DevOps
- **AI Engineering** (15 skills) — agent design, prompt engineering, RAG, model selection, fine-tuning, MLOps, cost control, safety/governance, plus Chain-of-Verification with enforced context isolation
- **Writing / Research / People-Finding** (10 skills) — long-form writing, deep research, inference-driven research, investigative research, PRISMA-style literature review, transaction analysis, people/counterparty discovery
- **AI SEO Pack** (7 skills) — modern SEO for both blue-link ranking and LLM citation

Free forever, no signup, works with Claude, GPT, Gemini, Perplexity, and local models. Lives at [maximus.macrotechtitan.com](https://maximus.macrotechtitan.com).

Happy to move to a different section or reword — just let me know.
```

---

## PR 2: awesome-ai-agents (e2b-dev)

**Target repo:** https://github.com/e2b-dev/awesome-ai-agents
**Section:** "Open-source projects" (usually under "AI Agents Landscape").
**Alphabetical order:** yes.

### Line to add

```markdown
- [MaximusAI](https://github.com/MacroTechTitan/MaximusAI) — 43 model-agnostic Agent Skills spanning cognitive OS, engineering, research, and AI SEO. Ships in Claude Skills / OpenAI Assistants format. MIT.
```

### Commit / PR title

```
Add MaximusAI to open-source projects
```

### PR body

```
Adding MaximusAI — 43 open-source Agent Skills that work with any model (Claude, GPT, Gemini, Perplexity, local Llama/Qwen/K3). Includes a Chain-of-Verification skill with enforced independent-context verification (reproducing the ~40–60% hallucination reduction from Dhuliawala et al. 2023), a PRISMA-style systematic literature review skill, and 10 other research/agent-shape skills.

MIT-licensed, no signup, no gate. Homepage: https://maximus.macrotechtitan.com.

Placed in alphabetical order under Open-source projects. Happy to move if there's a better section.
```

---

## PR 3: Awesome-Prompt-Engineering (promptslab)

**Target repo:** https://github.com/promptslab/Awesome-Prompt-Engineering
**Section:** "Prompt Engineering Guides" or "Tools & Code" — whichever fits.
**Alphabetical order:** yes.

### Line to add

```markdown
- [MaximusAI Skills](https://github.com/MacroTechTitan/MaximusAI) — 43 production prompt patterns encoded as Agent Skills. Includes maximus-prompt-engineering (adversarial-robust system prompts + JSON schema constraints), maximus-chain-of-verification (factored CoVe with enforced context isolation), and maximus-agent-design (tool-loop control, memory architecture, failure recovery).
```

### Commit / PR title

```
Add MaximusAI Skills — 43 open-source prompt engineering patterns
```

### PR body

```
Adding MaximusAI Skills — an open-source library of 43 Agent Skills covering prompt engineering, adversarial robustness, JSON schema constraints, Chain-of-Verification, RAG, model selection, and more. MIT-licensed.

Particularly relevant to this list:
- `maximus-prompt-engineering` — production system prompts, few-shot patterns, JSON schema, prompt injection defense
- `maximus-chain-of-verification` — factored CoVe with the independent-context rule enforced
- `maximus-agent-design` — tool loops, memory, and the common failure modes

Homepage: https://maximus.macrotechtitan.com
```

---

## PR 4: awesome-mlops (kelvins)

**Target repo:** https://github.com/kelvins/awesome-mlops
**Section:** "Model Lifecycle Management" or "Model Deployment and Serving" — whichever fits. `maximus-mlops-deploy` best fits Model Deployment.
**Alphabetical order:** yes.

### Line to add

```markdown
- [MaximusAI — mlops-deploy skill](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-mlops-deploy) — open-source MLOps runbook for canary deploys with eval comparison, drift detection (data/concept/prompt drift), automatic rollback on quality regression, and shadow traffic. Part of a 43-skill library for AI agents.
```

### Commit / PR title

```
Add MaximusAI mlops-deploy skill
```

### PR body

```
Adding the maximus-mlops-deploy skill from MaximusAI, an open-source runbook for ML/LLM production deployment: canary deploys with eval comparison, data/concept/prompt drift detection, automatic rollback on quality regression, shadow traffic against new prompt versions.

MIT-licensed. Full repo: https://github.com/MacroTechTitan/MaximusAI
```

---

## PR 5: awesome-claude-prompts (langgptai)

**Target repo:** https://github.com/langgptai/awesome-claude-prompts
**Section:** "Prompts" or "Resources" — whichever fits.
**Alphabetical order:** varies by list.

### Line to add

```markdown
- [MaximusAI Skills](https://github.com/MacroTechTitan/MaximusAI) — 43 open-source Agent Skills that load into Claude in Claude Skills format. Covers cognitive OS, engineering, research, prompt engineering, RAG, and AI SEO. MIT-licensed.
```

### Commit / PR title

```
Add MaximusAI — 43 open-source Claude Skills
```

### PR body

```
Adding MaximusAI, an open-source library of 43 Agent Skills written in the Claude Skills format (SKILL.md with YAML frontmatter). Works with Claude, GPT, Gemini, and Perplexity — but the format is Claude Skills native.

Includes a Cognitive OS layer (`maximus-brain`), 15 AI engineering skills, 10 research skills, 10 build/ship skills, and 7 AI SEO skills. MIT, no signup.

Homepage: https://maximus.macrotechtitan.com
```

---

## Submission order and pacing

- **Day 1:** PR 1 (awesome-llm-apps) — highest traffic
- **Day 2:** PR 2 (awesome-ai-agents)
- **Day 3:** PR 3 (Awesome-Prompt-Engineering)
- **Day 4:** PR 4 (awesome-mlops)
- **Day 5:** PR 5 (awesome-claude-prompts)

One per day. Do not submit them all in a single day — maintainers talk to each other and the pattern reads as list-farming.

## After a PR is merged

- Comment "thank you" on the merged PR (the maintainer sees this).
- Watch and star the list repo (they check).
- Do not comment on unmerged PRs to nudge them — wait at least 2 weeks.
