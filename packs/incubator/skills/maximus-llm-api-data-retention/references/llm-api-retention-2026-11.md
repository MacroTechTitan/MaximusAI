# LLM API data retention — facts and sources (pulled 2026-11-11)

| Fact | Source |
|---|---|
| Gemini API changelog, Oct 26 2026: new paid-tier projects using the Generate Content API (`generateContent`, `streamGenerateContent`, `batchGenerateContent`) store requests by default (`store=true`), matching the Interactions API; existing projects keep their setting; opt out with `store=false` per request or by turning off Generate Content logging in the Logs and Datasets settings | https://aistudio.google.com/docs/changelog |
| Gemini logs: available for billing-enabled projects; cover requests, responses, and metadata; default maximum retention 55 days, configurable to 7, 14, 28, or 55; logs saved to datasets have no set retention period; separate from abuse-monitoring logs | https://ai.google.dev/gemini-api/docs/logs-policy |
| Gemini paid service: prompts and responses in logs are not used for product improvement by default; logs in datasets shared with Google may be used to improve and train models and read by human reviewers; do not contribute personal, sensitive, or confidential data | same |
| OpenAI: API data not used for training unless you opt in (since March 1, 2023); abuse-monitoring logs kept up to 30 days by default | https://platform.openai.com/docs/guides/your-data |
| OpenAI Responses API: application state stored for at least 30 days by default or when `store=true`; with zero data retention enabled, `store` is treated as false; background mode keeps data about 10 minutes for polling; prompt-cache tensors not retained after 24 hours; ineligible endpoints may store state even with ZDR; ZDR requires approval | same |
| Anthropic API: inputs and outputs deleted within 30 days by default; exceptions include services with retention under your control (for example, the Files API), zero data retention agreements, usage-policy enforcement, and legal requirements | https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data |
| Scout run 2026-11-11: `examples/retention_scan.py` on synthetic files flagged 4 unprotected calls (OpenAI Responses, two Gemini Generate Content, one file upload) and skipped calls with `store=False` / `store: false` and commented code | local run |

Volatile: every default, period, and flag here can change. Recheck the provider pages before answering a customer or auditor.
