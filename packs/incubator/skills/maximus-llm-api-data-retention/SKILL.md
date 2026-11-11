---
name: maximus-llm-api-data-retention
description: "Audit and set what LLM providers keep from your API traffic: per-provider defaults (stored responses, request logs, abuse-monitoring copies, uploaded files), project vs request settings, store=false, zero data retention, and a retention inventory. Use for 'does OpenAI store my prompts', 'Gemini logging', 'store=false', 'LLM data retention'."
metadata: {"openclaw": {"emoji": "🗄️", "pillar": "ai-engineering", "source": "maximus-scout"}}
---

# Maximus — LLM API Data Retention

On October 26, 2026, Google changed a default: new paid Gemini projects now store Generate Content API requests unless told not to, and those logs can be kept for up to 55 days. Existing projects kept their setting. OpenAI's Responses API already stores application state for at least 30 days unless `store` is false, and OpenAI and Google also keep abuse-monitoring copies separate from anything you control in code. Whether your prompts and outputs persist at a provider depends on the provider, the endpoint, the project's creation date, project settings, and per-request flags, and those can change between releases.

## Purpose

Produce an accurate inventory of what each provider keeps from your traffic and for how long, set the shortest retention your product needs, and re-check whenever a provider changes a default. Provider figures are in `references/llm-api-retention-2026-11.md`; recheck them before relying on them.

## Scope boundary

| Need | Use |
|---|---|
| What LLM providers store from your API calls, and setting it | this skill |
| Redacting PII before it reaches a model, audit logs in your own system | maximus-ai-safety-governance |
| Deleting user data from training sets | maximus-ai-data-pipeline |
| Choosing a provider or model | maximus-llm-model-selection |
| Cutting token spend | maximus-ai-cost-control |

## Core workflow

1. **List every provider, project, and endpoint you call.** Include SDK wrappers, agent frameworks, and staging projects. Run `examples/retention_scan.py` over the codebase to find calls that will be stored unless they opt out.
2. **Record the four kinds of retention for each.** Application state you can reuse (stored responses, conversation state), request logs in a dashboard, abuse-monitoring copies, and files or datasets you uploaded. Each has its own default, control, and period.
3. **Check project-level settings, not only code.** Gemini logging is a project setting in AI Studio with a 7, 14, 28, or 55-day window, and its default depends on when the project was created. OpenAI zero data retention is an organization setting that overrides `store=true`. These are invisible in code.
4. **Set the request flag where you do not need state.** Send `store=false` on OpenAI Responses and Gemini Generate Content calls unless the feature depends on stored state (for example, chaining responses by ID). Write down which features need storage and why.
5. **Delete what you upload.** Files, vector stores, containers, and datasets are retained under your control, which means they stay until you delete them. Add a delete step to every upload path, and keep in mind that Gemini datasets have no retention period of their own.
6. **Apply for zero data retention where it matters.** OpenAI and Anthropic offer it by agreement or approval; check which endpoints are eligible, because ineligible features can still store state.
7. **Write the inventory down.** One row per provider and endpoint: what is kept, where, for how long, the control, its current value, and the date checked. Share it with whoever answers security questionnaires.
8. **Watch for default changes.** Subscribe to each provider's changelog and re-run steps 1 to 3 after any announcement about data or logging, and after creating a new project, since new projects may get different defaults.

## Anti-patterns

- **Assuming "not used for training" means "not stored".** They are separate; providers can keep data for monitoring or features without training on it.
- **Checking one project and assuming the rest match.** Project creation date can change the default.
- **Setting `store=false` everywhere without checking features**, then breaking anything that retrieves earlier responses.
- **Uploading files and never deleting them.**
- **Answering a customer's data question from memory.** Cite the dated inventory.
- **Sending sensitive data to datasets you share with the provider.** Google's docs warn against contributing personal, sensitive, or confidential data.

## Output

The retention inventory (provider, project, endpoint, kind of retention, period, control, current value, date checked), the scan results with each flagged call fixed or justified, the list of features that need stored state, the delete steps added for uploads, any zero-data-retention status, and the changelogs being watched.
