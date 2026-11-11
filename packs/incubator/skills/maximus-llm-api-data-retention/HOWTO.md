# HOWTO — LLM API Data Retention

## 1. Scan the code
`python examples/retention_scan.py src/`. Each hit is a call that the provider may store. Fix it with `store=False` (Python) or `store: false` (JS) if the feature does not need stored state, or note why it does. Exit 0 means no unprotected calls were found; it does not cover project settings.

## 2. Check Gemini projects
For each Google project with billing enabled, open Logs and Datasets in AI Studio, record whether Generate Content logging is on and the retention window, and note the project's creation date (on or after 2026-10-26 means storage is on by default).

## 3. Check OpenAI and Anthropic organizations
Record whether zero data retention or modified abuse monitoring is approved, which endpoints you use, and whether each is eligible. Without these agreements, expect abuse-monitoring copies for up to 30 days on OpenAI and deletion within 30 days on Anthropic.

## 4. Clean up uploads
List files, vector stores, and datasets in each provider account. Delete what no feature needs, and add a delete call after processing in every upload path.

## 5. Keep the inventory current
Store the inventory with a "checked on" date. Re-run recipes 1 to 4 after any provider changelog entry about data, logging, or storage, and when creating a new project.
