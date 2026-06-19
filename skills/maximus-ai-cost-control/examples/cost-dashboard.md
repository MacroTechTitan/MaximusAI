# Example: Cost Dashboard

A template for tracking AI inference costs in production. Includes the cost-surface table, per-user unit economics, and monitoring query patterns.

---

## Cost-surface table

Fill this out for every LLM call in your product. Update after any model or routing change.

| Endpoint / feature | Model | Input tokens p50 | Input tokens p95 | Output tokens p50 | Output tokens p95 | Calls/user/day | $/1K input | $/1K output | $/call p50 | $/call p95 | $/user/month |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `/chat/complete` | claude-haiku-3-5 | 1,200 | 4,500 | 350 | 800 | 12 | $0.00025 | $0.00125 | $0.00044 | $0.00213 | $0.16 |
| `/summarize` | claude-haiku-3-5 | 3,800 | 12,000 | 280 | 512 | 2 | $0.00025 | $0.00125 | $0.00130 | $0.00364 | $0.08 |
| `/summarize` (legal escalation) | claude-sonnet-4-5 | 3,800 | 12,000 | 280 | 512 | 0.1 | $0.003 | $0.015 | $0.01554 | $0.04368 | $0.05 |
| `/classify` | claude-haiku-3-5 | 500 | 1,200 | 30 | 80 | 25 | $0.00025 | $0.00125 | $0.00016 | $0.00040 | $0.12 |
| `/code-gen` | claude-sonnet-4-5 | 2,000 | 8,000 | 800 | 3,000 | 3 | $0.003 | $0.015 | $0.01800 | $0.06900 | $1.62 |
| **TOTAL** | | | | | | | | | | | **$2.03** |

*Prices approximate; verify at [Anthropic pricing](https://www.anthropic.com/pricing) before budgeting.*

**Unit economics check**: At $2.03 LLM cost/user/month:
- Free tier ARPU $0: LLM cost must be covered by conversion to paid.
- Paid tier ARPU $20: LLM cost = 10.2% of ARPU. Acceptable.
- Paid tier ARPU $10: LLM cost = 20.3% of ARPU. At the edge — optimize code-gen costs.

---

## Cache hit rate tracking

Track cache hit rates by endpoint. A cache hit rate below 60% for stable-prefix endpoints suggests hidden dynamism in the prompt.

| Endpoint | Cache-eligible prefix tokens | Avg cache hit rate | Cache savings/day (est.) |
|---|---|---|---|
| `/chat/complete` | 850 (system prompt) | 82% | $0.62 |
| `/summarize` | 420 (instruction prefix) | 91% | $0.18 |
| `/classify` | 650 (few-shot examples) | 88% | $0.09 |
| `/code-gen` | 1,200 (system + style guide) | 74% | $0.34 |

**Total cache savings**: ~$1.23/day at current scale. At 10,000 DAU: ~$12,300/day.

---

## Monitoring queries (Datadog / Grafana)

### Cost per request by endpoint (Datadog)

```
sum:llm.cost.total{*} by {endpoint}.rollup(sum, 300) / 
sum:llm.requests.count{*} by {endpoint}.rollup(sum, 300)
```

### Cost per active user per day

```
sum:llm.cost.total{*}.rollup(sum, 86400) / 
count_nonzero:llm.requests.count{*} by {user_id}.rollup(sum, 86400)
```

### Cache hit rate by endpoint

```
sum:llm.cache.hits{*} by {endpoint}.rollup(sum, 3600) /
sum:llm.requests.count{*} by {endpoint}.rollup(sum, 3600)
```

### Frontier model usage percentage (alert if > baseline + 25%)

```
sum:llm.requests.count{model:claude-sonnet*}.rollup(sum, 3600) /
sum:llm.requests.count{*}.rollup(sum, 3600)
```

---

## Alert thresholds

Configure these in your monitoring system before going to production:

| Alert | Threshold | Severity | Action |
|---|---|---|---|
| Cost/request spikes > 2× baseline | p95 cost/request doubles in 1 hour | P1 | Investigate routing + context length |
| Cache hit rate drops below 50% | Any endpoint for 30 min | P2 | Audit prompt for dynamic content |
| Frontier model usage > baseline + 25% | Over 1-hour window | P2 | Check routing config |
| User budget exceeded | Any user hits 100% of daily budget | P3 | Graceful UI message (see `maximus-ai-ux-patterns`) |
| Total daily spend > 150% of budget | Day-over-day | P1 | Immediate investigation |

---

## Monthly budget worksheet

```
# Fill in your numbers

DAILY_ACTIVE_USERS = 1000
COST_PER_USER_PER_MONTH = 2.03  # from cost-surface table above

MONTHLY_LLM_COST = DAILY_ACTIVE_USERS * COST_PER_USER_PER_MONTH
# = $2,030/month

PAID_USERS_PCT = 0.15  # 15% conversion
PAID_ARPU = 20  # $/month

MONTHLY_REVENUE = DAILY_ACTIVE_USERS * PAID_USERS_PCT * PAID_ARPU
# = $3,000/month

LLM_AS_PCT_REVENUE = MONTHLY_LLM_COST / MONTHLY_REVENUE * 100
# = 67.7% — UNSUSTAINABLE at current conversion

# Decision: improve conversion rate or reduce cost per user
# Target: LLM cost < 20% of revenue
# At current cost, need ARPU > $13.5 or conversion > 34%
```

---

## Notes

- Run this worksheet before any growth push. A 10× DAU increase at current unit economics means $20,300/month in LLM costs before any engineering scaling costs.
- The code-gen endpoint dominates cost ($1.62/user/month). If usage grows, this is the first target for optimization — consider caching common patterns or fine-tuning a smaller model on your code corpus.
- Update the table after any model pricing change, routing change, or significant usage pattern shift.
