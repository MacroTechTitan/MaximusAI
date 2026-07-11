---
name: maximus-eval-and-test
description: "Design the test and evaluation strategy for a project or feature \u2014 unit, integration, end-to-end, and (for AI features) the three-tier eval pyramid of PR checks, nightly LLM-as-judge regression, and production canary monitoring. Use when starting a new project, when the user asks to 'add tests', 'set up CI', 'design eval', 'measure quality', or 'evaluate the agent', or before shipping any AI-powered feature to production. Covers Python (pytest), JavaScript/TypeScript (vitest, jest, playwright), and Go (testing). For AI evals covers tool-call regression, LLM-as-judge, and error-budget canaries."
metadata:
  pillar: inspection
  source: maximus
---

# Maximus — Evaluation & Testing Strategy

Tests are not coverage; tests are evidence. The point isn't to fill a coverage bar — it's to be able to say, with a straight face, "we know this works." For AI features the bar is higher: a single-prompt unit test cannot prove a multi-step agent worked end-to-end. The horse pulls; the rider checks the load before, during, and after the haul.

## When to use

- Starting a new project or feature and deciding the testing strategy.
- The user asks: "add tests", "set up CI", "design eval", "test plan", "how do we measure quality", "evaluate the agent".
- Before shipping an AI-powered feature (agent, RAG, multi-step tool use) to production — the standard unit test is necessary but nowhere near sufficient.

## The testing pyramid (deterministic code)

Bottom to top, fast to slow, many to few:

1. **Unit tests** — pure functions, single classes. Run in milliseconds. Exercise branches, boundary conditions, error paths. The bulk of the test count.
2. **Integration tests** — multiple components together, real dependencies (DB, queue, in-process), no network. Run in seconds. Exercise the interaction points where unit tests can't see.
3. **End-to-end tests** — full stack, including the user surface. Run in tens of seconds to minutes. Few in number; cover the critical user journeys only. Playwright/Cypress for web; HTTP-driven for API-only.
4. **Smoke tests** — handful of E2E tests that run against staging or production after deploy. Tell you "the deploy didn't break the building".

Rough ratio: many units, fewer integrations, very few E2E. If the ratio is inverted, the suite is slow and brittle.

## The three-tier eval pyramid (AI features)

A single response to a single prompt cannot evaluate a multi-step agent. Use three tiers, each at the right stage of the release pipeline:

1. **PR tier — Tool-call regression (cheap, deterministic, fast)**
   - Recorded "cassettes" of the model's intended tool calls for each test case.
   - On every PR: re-run the agent against the same inputs with stubbed tools; assert the same tools were called in the same order with valid arguments.
   - No live model required for the check; runs in seconds; blocks merge on structural diff.
   - Catches the "agent now calls the wrong tool" regression that user-facing output checks would miss.
2. **Nightly tier — LLM-as-judge across a golden dataset (moderate cost)**
   - A curated dataset of ~50–200 representative tasks with expected outcomes (not exact strings — outcomes).
   - Nightly run executes the agent end-to-end against each task; an LLM judge scores correctness, completeness, and tone against a rubric.
   - Track the pass rate over time; alert on a >5-point drop.
   - Catches phrasing and reasoning regressions deterministic tests miss.
3. **Production tier — Canary + error budget (continuous)**
   - Sample live traces in production; score online with the same rubric or a lighter heuristic.
   - Define an error budget on task success and tool accuracy.
   - New versions ship at 5% canary traffic first; auto-rollback if the budget burns.

The three tiers exist because the failure modes are different and only one is cheap.

## Procedure

1. **Identify what "correct" means** before writing a single test. For a function: defined I/O. For a feature: acceptance criteria. For an agent: an outcome rubric. If you cannot articulate correct, no test will tell you it's right.
2. **Map test types to behaviors**:
   - Pure logic → unit tests.
   - Cross-module interactions, persistence, queue handling → integration tests.
   - Critical user journeys (login → purchase → confirmation) → E2E.
   - AI tool selection and ordering → tool-call regression (PR tier).
   - AI output quality → LLM-as-judge (nightly).
   - AI behavior in the wild → production canary.
3. **Build the harness early.** A project without a smoke test on day 1 will not have one on day 30. The first test is the hardest to add.
4. **Wire CI on day 1.** GitHub Actions or equivalent: install → lint → typecheck → unit + integration on every push. Nightly job for slow suites and AI nightly tier. Slow gates run after merge to main, not on PR.
5. **Set quality gates explicitly.**
   - Coverage gate (if used): minimum on changed lines, not total — total coverage is a vanity metric.
   - Lint and typecheck: zero new errors.
   - Eval pass rate (AI): defined floor; merges blocked below it.
6. **Add tests at the point of change.** New code lands with new tests in the same PR. Refactor PRs add tests for previously untested behavior they touch.
7. **Treat flaky tests as bugs.** Flake erodes signal until no one trusts the suite. Quarantine + ticket + fix; do not retry into green.

## Tooling — common stacks

- **Python**: `pytest` + `pytest-cov` + `hypothesis` (property tests) + `pytest-asyncio`; integration via testcontainers or `pytest-postgresql`; E2E via `httpx`/`playwright`.
- **JavaScript / TypeScript**: `vitest` or `jest` for unit/integration; `playwright` for E2E; `msw` for HTTP mocks.
- **Go**: stdlib `testing` + `testify`; `httptest` for HTTP handlers; testcontainers-go for integration.
- **AI evals**: Braintrust, Inspect, LangSmith, or a hand-rolled harness — anything that records traces and supports LLM-as-judge with a versioned rubric.

## Domain-specific test priorities

- **Web service**: every public endpoint has at least one happy-path and one auth-failure integration test; rate-limit behavior tested; error envelopes tested.
- **Fintech**: every money-handling code path has a test asserting correct cents and currency; webhook handler tests for valid, invalid signature, and duplicate event; reconciliation test against a fixture batch.
- **Scientific / ML**: schema validation tests on data inputs; deterministic-output test (same seed + same data → same result, byte-equal where feasible); end-to-end smoke pipeline runs on a tiny sample in CI.
- **DevOps / IaC**: `terraform validate` and `plan` in CI; policy tests via OPA/Conftest where applicable; smoke test on a deployed staging environment after every infra change.
- **AI agents**: tool-call regression for every supported task pattern; golden dataset large enough that a 5% drop is statistically meaningful (≥50 cases); production sampling rate set so daily counts are usable.

## Gotchas

- **Coverage as a goal** — high coverage with thin tests proves nothing. Tests exist to fail when behavior changes; if mutating the code under test doesn't fail any test, the test is decorative.
- **Skipping tests during a "rush"** — the bug you ship has a half-life longer than the rush.
- **Mocks all the way down** in integration tests — you're testing your mocks, not the system. Use real components for integration; reserve mocks for boundaries you don't own.
- **One enormous E2E test per feature** — slow, brittle, debug-hostile. Several focused tests beat one mega-test.
- **AI eval = "ask GPT-4 if the output is good"** without a rubric — you're measuring vibes. Versioned rubric, frozen judge model, tracked over time.
- **Flaky tests retried until green** in CI — that's how a real regression escapes for weeks.
- **Eval dataset that the model has seen** — leakage destroys the signal. Curate, hold out, refresh.

## Output

A test plan document (or PR adding tests) covering: layer-by-layer test list, CI workflow file(s), eval harness scaffold for AI features, and a defined set of quality gates. Final chat summary lists: layer counts, CI job names, gate thresholds, and the first 5 tests to write if starting from zero.
