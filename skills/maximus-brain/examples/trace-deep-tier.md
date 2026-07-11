# Worked trace — Deep tier on a real build task

User request: **"Add Stripe Connect onboarding to the marketplace so vendors can get paid."**

Below is a sanitized trace of how brain runs the five-pass loop on this task. The user does not see the bracketed reasoning blocks — they see only the final response and the tool calls.

---

## Pass 1 — Frame

> [internal] Restate goal: "Wire Stripe Connect into the marketplace so each vendor can onboard, link their bank, and receive payouts when their products sell."
>
> Unknowns: Standard, Express, or Custom Connect? US-only or multi-country? Where do platform fees come from — a flat fee, percentage, or both? Existing Stripe account on the platform side?
>
> Assumptions: This repo already uses Stripe (verified from prior memory + repo); using Express by default — most marketplaces start there; US-only first pass; 5% platform fee placeholder.
>
> Depth tier: **Deep** (money + multi-step integration). If anything irreversible (live key, real account linking), promote to **Extreme** at that step.
>
> "Done" bar: Vendor can complete onboarding from the dashboard, link their account, see status, and the platform can issue test payouts via Stripe Connect Express.

If the assumptions about Connect type or fee structure are wrong, the work is wrong. Brain surfaces them in the response so the user can correct them in one turn rather than discovering a wrong assumption after code is written.

---

## Pass 2 — Recall

```
memory_search queries:
  - "marketplace project Stripe integration prior decisions"
  - "vendor onboarding requirements maximusai marketplace"
  - "platform fee structure marketplace"
```

Findings (illustrative):
- Prior session established the repo uses Stripe in test mode for one-time charges.
- A `vendors` table already exists with `stripe_account_id` nullable.
- User has previously preferred Express Connect for new marketplaces.

Repo reads:
- `src/lib/stripe.ts` — confirmed Stripe SDK wiring and key handling.
- `db/migrations/` — confirmed `vendors.stripe_account_id` column.
- `routes/api/stripe/` — confirmed webhook endpoint exists with signature verification.

Recall pays for itself: assumptions from Pass 1 are now grounded in fact, not guess.

---

## Pass 3 — Select

Skills loaded:
- `maximus-fintech-payments` — Stripe integration discipline (idempotency, integer cents, webhook signing, audit log).
- `maximus-plan-implementation` — turn this into a phased task list.
- `maximus-build-feature` — read-before-edit during execution.

Tool plan:
1. Open spec/plan document, draft phases.
2. Generate the new endpoints (account creation, account link, webhook handlers for `account.updated` and `payout.*`).
3. Wire the dashboard component.
4. Add tests for each path.

---

## Pass 4 — Execute

Phased execution. After each phase, a verify step:

- **Phase A — DB + types**: migration to add `vendors.onboarding_status`, types updated. Verify: `npm run build` + `npm run typecheck`.
- **Phase B — backend endpoints**: `POST /api/connect/account`, `POST /api/connect/account-link`, webhook handlers. Verify: `vitest run tests/connect/` + manual `curl` smoke.
- **Phase C — frontend onboarding flow**: dashboard component reads status, kicks off link flow. Verify: local browser walk-through.
- **Phase D — audit log + idempotency**: all account-creation calls use idempotency keys derived from `vendor_id`; every state change writes an audit row. Verify: trigger duplicate onboarding, confirm idempotent.
- **Phase E — test-mode end-to-end**: spin up a test Connect account, complete the onboarding flow, trigger a test payout, confirm webhook fires and audit log row appears.

If any phase fails verify, the loop stops and brain re-frames. No phase advances on red.

---

## Pass 5 — Self-critique

Before responding:

1. **Re-read the request.** "Add Stripe Connect onboarding so vendors can get paid." ✓ Onboarding flow built. ✓ Vendors can link account. ✓ Path to payout exists. **But**: the user said "get paid" — did we wire payouts on actual sales? Yes, the existing checkout flow already settles to platform; need to confirm the destination charge mode is set for vendor payouts. Add note.
2. **Hallucination check.** Every Stripe API call cross-checked against [Stripe Connect Express docs](https://stripe.com/docs/connect/express-accounts). `account.updated` and `account_link.created` are real events; `transfer_data[destination]` is the correct field on charges.
3. **Missed steps.** Webhook events: `account.updated`, `account.application.deauthorized`, `payout.created`, `payout.failed`. Audit log table writes confirmed. PCI scope unchanged (no PAN crossing servers). ✓
4. **Stakes check.** This is money code on Express Connect. Test-mode verification step explicitly listed. Live deploy gated behind separate task — flag the user. ✓
5. **Right-size.** Response is a phased plan with the open assumptions surfaced for confirmation, not a 40-page memo. ✓

---

## What the user sees

A response that opens with the goal restatement, the four assumptions, the depth tier, and the proposed five-phase plan — followed by a question on the two assumptions that genuinely change the work (Connect type, fee structure). The work proceeds the moment the user confirms or corrects.

The user does **not** see the bracketed internal blocks. They see a calibrated answer that fires the right skills, references real Stripe APIs, and stops short of any irreversible action without an explicit confirmation.
