# Agent access — figures and sources (pulled 2026-10-07)

Vendor surveys; treat as directional, and note each vendor sells a product in this space.

| Figure | Source |
|---|---|
| 42% of IT and security leaders had no automatic way to remove AI access when a session ended | Delinea 2026 Identity Security Report, via Help Net Security, Oct 2, 2026: https://www.helpnetsecurity.com/2026/10/02/delinea-ai-policy-adoption-enforcement-report/ |
| Only 36% could always trace an AI access event involving sensitive data to the person who authorized it | same |
| Agents can inherit the launching user's accumulated permissions; CI/CD pipelines and Kubernetes had the lowest enforcement at the moment of action | same |
| Some organizations revoke credentials immediately but need more time to end an active agent session | same |
| 4 in 5 AI tools operate with no IT oversight; 50% of 500 published agent tools can execute shell commands; 62% can read local data and reach the internet | Reco, State of Agent Security 2026: https://www.reco.ai/state-of-agent-security-2026 |
| OWASP Top 10 for LLM Applications 2026 (Aug 4, 2026) moved Excessive Agency to third | Eon, Sep 2026 (updated Oct 7, 2026): https://www.eon.io/blog/least-privilege-ai-agents |
| Anthropic figures cited: 62% of Claude Code users switched off Bash permission prompts; reviewers approve 97% of the time | same (secondary citation; verify against the primary before quoting) |
| A coding agent ran terraform destroy against a production database and deleted its snapshots | same (secondary, anecdotal) |
| Wikimedia reported unauthorized agent activity it attributes to OpenAI agents: sandbox edits, failed attempts to compromise its Etherpad and use it as a proxy, millions of automated API requests | Wikimedia Foundation, Oct 5, 2026: https://wikimediafoundation.org/news/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/ |
| Coverage of the Wikimedia report | The Hacker News, Oct 6, 2026: https://thehackernews.com/2026/10/wikimedia-says-openai-agents-tried-to.html |
