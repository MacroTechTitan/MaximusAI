# maximus-llm-api-data-retention (incubator)

Audit and set what LLM providers keep from your API traffic: stored responses, request logs, abuse-monitoring copies, and uploaded files, with per-provider defaults, project versus request settings, `store=false`, zero data retention, and a dated retention inventory.

**Triggers:** "does OpenAI store my prompts", "Gemini logging", "store=false", "LLM data retention", "security questionnaire about AI vendors".

**Files:** `SKILL.md` (workflow), `HOWTO.md` (5 recipes), `references/llm-api-retention-2026-11.md` (provider defaults with dates and sources), `examples/retention_scan.py` (runnable code scanner, tested on synthetic Python and TypeScript files).

**Siblings:** maximus-ai-safety-governance, maximus-ai-data-pipeline, maximus-llm-model-selection, maximus-ai-cost-control.

Drafted by the skill scout on 2026-11-11. Unreviewed until promoted.
