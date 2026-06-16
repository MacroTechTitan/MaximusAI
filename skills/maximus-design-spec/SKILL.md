---
name: maximus-design-spec
description: "Write a software design specification before code. Use when starting any non-trivial feature, system, or refactor that crosses module boundaries, when the user asks for a spec, design doc, technical design, architecture document, or RFC, or before handing work off to another engineer or agent. Translates requirements into an implementable architecture with module decomposition, data models, interfaces, non-functional constraints, and design rationale. Skip for one-file scripts and tight bug fixes."
metadata:
  pillar: planning
  source: maximus
---

# Maximus — Design Specification

A design spec is the bridge between *what* the user wants and *how* it will be built. It exists so the build phase is grinding, not guessing. The horse plows straight when the furrow is drawn first.

## When to use this skill

Use when:

- The work spans multiple modules, services, or repos.
- A non-trivial data model, API contract, or integration is involved.
- Multiple agents/engineers will touch the code (handoff incoming).
- The user explicitly asks for a "spec", "design doc", "RFC", "architecture", or "technical design".
- The work is regulated (fintech, health, science publication) and an audit trail matters.

**Skip** for: single-file changes, trivial bug fixes, throwaway scripts, or work fully covered by an existing spec.

## What a complete spec contains

1. **Purpose & scope** — one paragraph stating what this spec covers and what it does not. Reference the originating request or ticket.
2. **System context** — where this fits in the larger architecture. One diagram (Mermaid is fine) showing the components, their responsibilities, and the boundaries with anything external.
3. **Requirements (linked, not duplicated)** — list functional and non-functional requirements with stable IDs (FR-1, NFR-1, …). Reference the source document instead of rewriting.
4. **Architecture & module design** — how the system is partitioned. For each module: responsibility, public interface, internal data structures, dependencies.
5. **Data model** — entities, relationships, persistence choice, migration strategy. Include the schema in SQL/Prisma/Pydantic — text descriptions are not enough.
6. **Interfaces / API contracts** — request and response shape, status codes, errors, idempotency, timeouts. Prefer machine-readable (OpenAPI, JSON Schema, gRPC `.proto`).
7. **Non-functional constraints** — performance budgets, security controls, scalability targets, observability requirements. Every NFR pairs with a design rationale.
8. **Design rationale & alternatives** — for each significant decision, the chosen approach AND at least one rejected alternative with the reason for rejection.
9. **Risks, assumptions, open questions** — explicit list. Open questions block sign-off, not work; assumptions get validated during build.
10. **Traceability matrix** — table mapping each FR/NFR to the module(s) that realize it. Catches gaps before code is written.

## Procedure

1. **Confirm the requirements before designing.** If the requirements are vague, contradictory, or missing constraints (perf, security, deadline), stop and clarify with the user. Designing on top of a guess wastes the build phase.
2. **Read the existing codebase first.** Use the repo's existing patterns. A spec that ignores the current architecture creates an integration problem the build phase has to solve under duress.
3. **Draft the spec as a Markdown file** in the project — `docs/design/<feature>.md` is a good default. Real files, not chat dumps.
4. **Lead with the diagram.** Reviewers anchor on the picture. Mermaid renders in GitHub and most viewers — prefer it over images you have to maintain separately.
5. **Be specific about contracts.** "Returns a user object" is not a contract. Give exact field names, types, nullability, and error shapes.
6. **Pair each NFR with rationale.** "p95 < 200ms" is a target; "because the call sits in the checkout hot path" is the rationale that lets the next person preserve the constraint when they refactor.
7. **Make alternatives a section, not a footnote.** The rejected paths are how the reviewer audits your reasoning.
8. **End with the traceability matrix.** Visually obvious gaps surface here that you missed in prose.
9. **Mark open questions inline with `> [!QUESTION]`** so reviewers can grep for them, and resolve before sign-off.

## Domain-specific spec checklists

- **Web service**: auth model, rate limits, CORS, idempotency keys on mutations, pagination strategy, error envelope, multi-tenant isolation if applicable.
- **Fintech**: PCI scope (what the system touches), money-handling precision (use integer minor units, never floats), webhook signing, idempotency, audit log of every mutation, regulatory residency (data location).
- **Scientific computing**: input data provenance + checksum, pinned dependency versions, random-seed strategy, deterministic mode where feasible, output reproducibility test (single command must regenerate all figures/tables).
- **DevOps/infra**: blast radius (what fails if this service fails), SLO targets, dependencies on other internal services, runbook references, IaC module ownership, rollback procedure.

## Gotchas

- **Designing without reading the code first** is the #1 failure mode — your spec will contradict the codebase.
- **Skipping rationale** makes the spec un-reviewable; reviewers can only nod or reject without it.
- **Vague NFRs** ("fast", "secure", "scalable") are non-functional fiction. Give numbers or skip the bullet.
- **Specs go stale.** Date the spec, version it, and update it when reality diverges. A wrong spec is worse than no spec.
- **Open questions are not optional.** If you're uncertain, write it down — it's a sign of rigor, not weakness.

## Output

A Markdown design spec file in the project (default path: `docs/design/<feature>.md`), produced via the file-write tool, then shared with the user. End the chat reply with a 3-bullet summary: scope, key decisions, open questions.
