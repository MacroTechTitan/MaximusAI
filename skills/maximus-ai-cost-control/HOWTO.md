# HOWTO — maximus-ai-cost-control

Recipes for controlling AI inference costs. Each recipe is a complete, runnable procedure.

---

## Recipe 1: How to set up prompt caching

**Goal**: Reduce costs for repeated system prompt or few-shot prefix calls by 80–90%.

**Steps**:
1. Identify which part of your prompt is stable across requests: typically the system prompt, role definition, and any fixed few-shot examples. This is your cache-eligible prefix.
2. Audit the prefix for dynamic content: timestamps, user IDs, session tokens, request-specific data. Move any dynamic content *out* of the prefix and into the user turn. A single dynamic character in the prefix defeats caching.
3. Enable provider caching:
   - **Anthropic**: Mark the cache boundary with `"cache_control": {"type": "ephemeral"}` on the last content block of the prefix. Cached prefixes must be ≥1,024 tokens for Claude Haiku, ≥2,048 for Sonnet/Opus. Cache TTL is 5 minutes (refreshed on each hit).
   - **OpenAI**: Prompt caching is automatic for prompts ≥1,024 tokens. No explicit marker needed. The cached prefix is the longest matching prefix across requests.
4. Verify caching is working: check `usage.cache_read_input_tokens` in the API response. A non-zero value confirms a cache hit.
5. Monitor cache hit rate over 24 hours. If hit rate < 50%, the prefix likely has hidden dynamism — audit again.

**Verification**: `cache_read_input_tokens` is non-zero in >80% of API responses for the targeted endpoint.

**Common pitfalls**:
- Putting a timestamp in the system prompt ("Current date: {{date}}"). Move it to the user turn.
- Prefix too short: Anthropic requires ≥1,024 tokens (Haiku) or ≥2,048 tokens (Sonnet/Opus) for caching to activate.
- Assuming OpenAI caching is free: cached reads are ~50% of full input price, not free (as of 2025).

---

## Recipe 2: How to build a model routing table

**Goal**: Route each request class to the cheapest model that meets quality requirements.

**Steps**:
1. Enumerate your task classes. Example: simple Q&A, multi-step reasoning, code generation, summarization, classification, extraction.
2. Run offline evals on each task class across model tiers. Use your eval suite from `maximus-eval-and-test`. Capture: accuracy, latency p50/p95, cost/call.
3. For each task class, find the cheapest model that meets the quality bar. Common result: classification and extraction → small models (Claude Haiku, GPT-4o mini); complex reasoning, code → frontier models (Claude Sonnet/Opus, GPT-4o).
4. Define escalation conditions: user requests "best answer", confidence score from a classifier is below threshold, task type is explicitly in the "frontier-only" set.
5. Implement the router. See `examples/routing-config.md` for a YAML-based routing config and a Python dispatcher. The router reads task class from a lightweight classifier or from explicit request metadata.
6. Add routing decision logging: log which model handled each request. This is your audit trail for cost and quality debugging.
7. Run the eval suite against the routed system (not just individual models) to confirm end-to-end quality.

**Verification**: The routing table has eval-backed quality floors for every task class. Routing logs show the expected distribution of model usage. Cost/request is reduced relative to using the frontier model for all calls.

**Common pitfalls**:
- Routing without evals: a routing bug that sends all traffic to the frontier model is a silent cost explosion.
- Classifying task class with a frontier model (defeating the cost saving before it starts). Use a cheap embedding-based classifier or keyword routing for the task-class step.
- Forgetting to version the routing table. A routing config change is a model change — log it.

---

## Recipe 3: How to set $/user budgets and alerts

**Goal**: Prevent any single user or runaway job from creating an unexpected bill.

**Steps**:
1. Define the token budget per user per day (or per month, depending on your billing cycle). Example: 100,000 input tokens + 20,000 output tokens/day for the free tier.
2. Implement budget tracking in your application layer: increment a counter (Redis or your DB) on each LLM call. Counter key: `budget:{user_id}:{date}`. TTL: 24 hours.
3. Before each LLM call, check the counter. If it would exceed the budget, return a budget-exceeded response (with a graceful message — see `maximus-ai-ux-patterns`) instead of making the call.
4. Set provider-level hard limits as a backstop:
   - **Anthropic**: Workspace spend limits in the Anthropic console.
   - **OpenAI**: Hard limits in the OpenAI billing settings.
   - **AWS Bedrock**: AWS Budgets with an SNS alert.
5. Set an application-level alert: if total spend/day exceeds N% of your monthly budget allocation, fire a Slack/PagerDuty alert. Don't wait for the provider invoice.
6. Test the budget enforcement path: manually hit the limit in a dev environment and confirm the graceful response fires, not an unhandled exception.

**Verification**: Exceeding the test budget returns a graceful message (not a 5xx). Provider-level limits are set and confirmed active. An alert fires when spend exceeds the threshold in a test scenario.

**Common pitfalls**:
- Setting only provider-level limits (no application-level enforcement). By the time the provider hard limit fires, the damage is done for that billing cycle.
- Not testing the budget-exceeded path. A user hitting the limit should get a helpful message, not a cryptic error.
- Using a single global counter instead of per-user counters. One heavy user should not throttle all users.

---

## Recipe 4: How to compress context safely

**Goal**: Reduce input token count without degrading output quality.

**Steps**:
1. Audit your current prompt for bloat: (a) system prompt redundancy (instructions repeated in multiple sections), (b) retrieved documents injected verbatim (with HTML/markdown formatting), (c) full conversation history instead of summarized history.
2. **System prompt compression**: Combine redundant instructions. Remove examples that can be replaced with a schema. Aim for ≤500 tokens for the system prompt in most cases.
3. **Document compression**: Before injecting retrieved chunks, strip HTML tags, navigation text, headers/footers, and markdown formatting. Keep only the prose content of the relevant passage. Use a regex or BeautifulSoup strip. Typical reduction: 20–40%.
4. **Conversation history compression**: After N turns (typically 8–12), replace the oldest turns with a rolling summary. Use a cheap model (Haiku, GPT-4o mini) for the summarization — the summary doesn't need frontier quality. Keep the last 2 turns verbatim for recency context.
5. Measure: compare input token counts before and after at p50 and p95.
6. Run evals on the compressed version vs the uncompressed version. If quality drops, you compressed too aggressively — add back the lost content selectively.

**Verification**: Input token count at p50 reduced by ≥20%. Eval quality on the compressed version matches or exceeds the uncompressed baseline within the eval's margin of error.

**Common pitfalls**:
- Truncating context instead of summarizing it. Truncation loses recent context; summarization preserves it semantically.
- Compressing the system prompt so aggressively that edge-case instructions are lost. Keep edge-case handling instructions even if they're rarely triggered.
- Not re-running evals after compression. Context compression is a model parameter change — treat it as one.

---

## Recipe 5: How to audit a sudden cost spike

**Goal**: Find the root cause of a $/request or total spend spike within 30 minutes.

**Steps**:
1. Pull the cost breakdown by: endpoint, model, user cohort, and time window. Most providers (Anthropic, OpenAI) provide usage breakdowns in the console or via API. If you have your own logging (you should), query it first.
2. Check input token trend: did input tokens/request increase? If yes: (a) was a longer document retrieval introduced? (b) did the system prompt grow? (c) did conversation history summarization stop working?
3. Check output token trend: did output tokens/request increase? If yes: (a) was a response length constraint removed? (b) is a streaming response being buffered and counted multiple times?
4. Check model distribution: did traffic shift from a cheap model to a frontier model? Check routing logs for a routing config change or a routing classifier regression.
5. Check call volume: did call volume increase (user growth, batch job, retry loop)? Retry loops with no backoff and no max-retry limit are a common cause of sudden volume spikes.
6. Check caching: did cache hit rate drop? A schema or system prompt change can invalidate all cached prefixes.
7. Fix the root cause. Redeploy. Monitor the next 1-hour window to confirm the spike resolves.

**Verification**: Cost/request has returned to the pre-spike baseline. Root cause is documented in a post-mortem note. A preventive measure (alert, test, cache audit) is added to the backlog.

**Common pitfalls**:
- Looking only at total spend without breaking down by endpoint or model. The cause is almost always in one specific call path.
- Assuming user growth is the cause without checking cost/request. If cost/request is also up, it's not just growth.
- Fixing without adding a prevention measure. The same spike will happen again.
