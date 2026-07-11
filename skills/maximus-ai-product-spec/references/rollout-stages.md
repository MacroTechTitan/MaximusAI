# Reference: AI Feature Rollout Stages

## Why staged rollout is mandatory for AI features

AI features fail in ways that don't show up in offline evaluation:
- Production inputs diverge from the test set
- Edge cases that annotators never labeled
- Adversarial users who probe the system
- Latency and throughput that differ from load testing
- User expectations that the spec writer didn't anticipate

The cost of a failed silent launch (100% traffic from day one) is disproportionate: a safety incident or a model hallucinating confidently for 100% of users is a legal, reputational, and support burden that a 5% staged rollout would have caught and contained.

---

## Stage definitions

### Stage 0: Off (Infrastructure Live)

**Who**: Nobody.  
**Traffic**: 0%.  
**Purpose**: Deploy all infrastructure — model endpoint, prompt, feature flag, logging, monitoring dashboard, kill switch mechanism — without routing any user traffic. Verify that the kill switch works: flip the flag off, confirm the fallback appears, flip it back.

**Gate to Stage 1**:
- [ ] Feature flag deployed and toggleable by one designated person without code deployment
- [ ] Monitoring dashboard live, showing all eval rubric metrics
- [ ] Audit logging active (see `maximus-ai-safety-governance`)
- [ ] Kill switch tested (flipped off → fallback verified → flipped back on)
- [ ] Safety controls active (PII redaction, output filtering)
- [ ] Eval rubric defined and test set exists

---

### Stage 1: Internal (Dogfood)

**Who**: Internal team and designated trusted testers.  
**Traffic**: ~0.1–1% (internal users only).  
**Hold time**: Minimum 3 business days. Do not rush this stage.  
**Purpose**: Find the bugs and failure modes that didn't show up in offline eval. Internal users will probe the feature harder and more creatively than annotators did.

**What to monitor**:
- Task success rate (qualitative internal feedback)
- Any safety incidents (zero tolerance for P0/P1 safety issues)
- Latency (does it hold under low volume?)
- Kill switch readiness (on-call person briefed?)

**Gate to Stage 2**:
- [ ] 3+ business days elapsed
- [ ] Zero P1 incidents
- [ ] Task success rate ≥ Stage 1 threshold (from eval rubric)
- [ ] No systemic format compliance failures
- [ ] Monitoring dashboard confirms logging and alerting are working

---

### Stage 2: Limited (5%)

**Who**: 5% of eligible users, randomly sampled (or a specific cohort if the feature is cohort-targeted).  
**Traffic**: 5%.  
**Hold time**: Minimum 7 days OR minimum 1,000 model calls, whichever comes later.  
**Purpose**: Real user traffic reveals distribution shifts and usage patterns that internal testing misses.

**Cohort selection considerations**:
- Random is usually right.
- Exclude users who opted out of beta features.
- If the feature is high-stakes (financial, medical), exclude vulnerable populations from early cohorts.
- Ensure the cohort is large enough to give statistical power (1,000 calls minimum).

**What to monitor** (daily during this stage):
- Task success rate vs. Stage 1 target
- Safety pass rate (must stay ≥ 99%)
- Thumbs-up / thumbs-down ratio
- Rewrite rate (users deleting AI output)
- Latency P95
- Support tickets mentioning the feature

**Gate to Stage 3**:
- [ ] 7 days elapsed AND 1,000+ calls logged
- [ ] Primary task metric ≥ Stage 2 threshold
- [ ] Safety pass rate ≥ 99.5%
- [ ] Zero P1 incidents in the last 72 hours
- [ ] Thumbs-up rate ≥ target (or trending upward)
- [ ] No regression in latency

---

### Stage 3+: Ramp to Full (25% → 50% → 100%)

**Traffic increments**: 25% → 50% → 100%.  
**Hold time**: 3 days minimum at each increment.  
**Purpose**: Confirm the feature scales and the metrics hold at higher load.

**At each increment**:
- Verify latency under higher load (P95 should not degrade significantly).
- Confirm safety pass rate is stable.
- Confirm no unexpected error rate spikes.
- Promotion approval: product lead confirms metrics before each increment.

---

## Rollback triggers

Define before Stage 1. Automate alerting. Manual rollback by the flag owner.

| Condition | Action | Threshold example |
|-----------|--------|-------------------|
| Safety flag rate spike | Page on-call, consider flag flip | > 1% in any 30-min window |
| Latency P95 breach | Alert on-call | > 2× the target P95 |
| Error rate spike | Alert + page if sustained | > 2% in 15-min window |
| P1 safety incident | Immediate kill switch flip | Any confirmed P1 |
| Thumbs-down spike | Alert, investigate | > 30% in any 1-hour window |

---

## Promotion criteria summary

| Gate | Time | Task success | Safety | Incidents |
|------|------|-------------|--------|-----------|
| 0 → 1 | Infrastructure ready | — | Controls active | — |
| 1 → 2 | 3 business days | ≥ Stage 1 target | ≥ 99% | 0 P1 |
| 2 → 3 | 7 days or 1,000 calls | ≥ Stage 2 target | ≥ 99.5% | 0 P1 in 72h |
| 3 → 4 | 3 days at 25% | Stable | ≥ 99.5% | 0 P1 in 72h |
| 4 → 5 | 3 days at 50% | Stable | ≥ 99.5% | 0 P1 in 72h |

---

## Notes on percentage increments

5% → 25% → 50% → 100% is a common pattern. Adjust based on:
- **Risk level**: A high-risk EU AI Act system should move more slowly.
- **Volume**: At low absolute volume, 5% may be < 100 calls per day — extend the hold time.
- **Feature type**: A background AI feature (no user-visible output) can move faster than one where users see and judge the AI output directly.
- **Reversibility**: If the AI feature creates persistent artifacts (writes to a database, sends an email), rollback is more complex. Be more conservative.
