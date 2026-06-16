---
name: maximus-fintech-payments
description: "Build payment, billing, and fintech features with PCI awareness and production-grade safety. Use when integrating Stripe (Checkout, Connect, Billing, webhooks), implementing payouts, subscriptions, invoicing, refunds, or any money-handling code; when the user mentions payments, charges, payouts, PCI, KYC, AML, idempotency, webhooks, audit log, or compliance. Enforces idempotency keys, integer minor units, webhook signature verification, immutable audit logs, test-mode verification before live, and least-privilege key handling. Skip for non-financial CRUD."
metadata:
  pillar: build
  source: maximus
---

# Maximus — Fintech & Payments

Money code fails differently from other code: a silent bug becomes a chargeback, a duplicate, or a regulatory incident. This skill is the discipline that keeps that from happening. The horse does not carry cash on the road without a saddle and reins.

## When to use

- Integrating Stripe (Checkout, Billing, Connect, Issuing, Treasury, webhooks) or any payment processor.
- Implementing subscriptions, invoicing, refunds, disputes, payouts, marketplace splits, or wallets.
- Writing code that touches an amount of money — even read-only reporting that will be cited in a customer-facing receipt.
- The user mentions: payments, Stripe, charges, payouts, PCI, KYC, AML, SOC 2, audit log, reconciliation, idempotency, webhooks.

## Non-negotiable rules

1. **Integer minor units only.** Store and compute money as integer cents (or smallest currency unit). Never floats. Currency is a separate field (`amount: 1299`, `currency: "usd"`).
2. **Idempotency on every mutation.** Every `POST` that creates or charges *must* accept an `Idempotency-Key`. Stripe's SDK takes one; your own API should require one from clients.
3. **Verify webhook signatures.** Every webhook handler verifies the signature before parsing the body. No exceptions, no "we'll add it later". An unverified webhook endpoint is an open back door.
4. **Immutable audit log of every state change.** Append-only table: who, what, when, before, after, request_id. Required for SOC 2 CC7.x and indispensable for support investigations.
5. **Least-privilege keys.** Restricted API keys for backend; publishable keys only in client; never commit either to git. Rotate on leak.
6. **PCI scope minimization.** Never accept, transmit, or store raw PANs through your servers — use Stripe Elements / Payment Element / Checkout so the card data goes browser→Stripe directly. Your servers hold tokens, not numbers.
7. **Test mode before live.** Every code path runs against test keys with realistic fixtures before a single live key touches it.

## Procedure

### 1. Scope the work

- What money flow is moving (one-time charge / subscription / payout / refund)?
- Who is the payer, payee, and platform? For marketplaces this is the Connect model question: Standard, Express, or Custom account?
- What are the regulatory edges: which countries, which currencies, which industries (high-risk?)?
- Where does PCI scope land — confirm card data never crosses your servers.

### 2. Design the contract

- Document the request, response, and error envelope. Specify the idempotency-key header.
- Define the webhook events you'll consume and the action each triggers. Make the handler idempotent — Stripe retries.
- Sketch the data model: `payments`, `payment_attempts`, `webhook_events`, `audit_log`. Webhook events get stored before processing so duplicate deliveries can be deduped on event id.

### 3. Build with safety first

- **Stripe SDK config**: use the latest version pinned in the lockfile, set `apiVersion` explicitly. Pinning prevents silent API behavior changes.
- **Server holds tokens, not cards**: front end uses Stripe Elements / Payment Element / Checkout. Your endpoint receives a `payment_method` or `payment_intent` id, never a card number.
- **Idempotency**:
  ```python
  stripe.PaymentIntent.create(
      amount=1299, currency="usd",
      customer=customer_id,
      idempotency_key=f"order-{order_id}-attempt-{attempt}",
  )
  ```
- **Webhook handler**:
  ```python
  sig = request.headers["Stripe-Signature"]
  try:
      event = stripe.Webhook.construct_event(payload, sig, WEBHOOK_SECRET)
  except (ValueError, stripe.error.SignatureVerificationError):
      return 400
  # Dedup on event.id BEFORE processing
  if already_processed(event.id): return 200
  process(event); mark_processed(event.id)
  ```
- **Currency handling**: never `float`. Use `int` cents in code and `numeric(precision, scale)` in the DB if you must store a derived monetary number; never `float`/`real`.
- **Refunds and disputes** get the same audit trail as charges.

### 4. Audit log

Every create / update / delete on a money-bearing entity writes a row:
```
audit_log(id, ts, actor, action, entity, entity_id, before_json, after_json, request_id)
```
Append-only. No `UPDATE` or `DELETE` permissions on this table for app users. Tested.

### 5. Test mode verification (mandatory before live)

- All flows pass against Stripe test keys with the [test cards](https://stripe.com/docs/testing): success, 3DS challenge, decline, insufficient funds, network error.
- Webhook flows tested with `stripe trigger` / `stripe listen` locally, and with replayed events from the Stripe dashboard.
- A scripted end-to-end test that hits your real test-mode Stripe account and verifies the audit log row appears.

### 6. Go live

- Live key set as a secret (Vercel/Replit/Doppler env), never in code or committed config.
- Live webhook endpoint configured in the Stripe dashboard with HTTPS and a separate signing secret from test.
- Restricted live key with the minimum permissions for the workload (no `secret_key` if a `restricted_key` covers it).
- Verify the first live transaction end-to-end with a low-value real charge, then refund it.
- Set up dashboards/alerts for: failed payments rate, webhook delivery failure rate, dispute rate, account balance.

### 7. Reconciliation

- Daily job pulls the Stripe BalanceTransaction feed and matches each row to your internal audit log. Mismatches are alerts. Reconciliation that runs once a quarter is reconciliation theatre.

## Compliance edges (know which apply)

- **PCI-DSS**: minimize scope by tokenizing card data on Stripe. With Elements + your backend never seeing PAN, you qualify for SAQ-A (the lightest level). Document it.
- **SOC 2**: tool-layer access controls, audit log of agent/human actions, change management — already covered above if you implemented audit log + restricted keys + IaC for infra changes.
- **GDPR / CCPA**: payment data is personal data. Honor deletion requests by erasing your records and either calling Stripe's `Customer.delete` or relying on Stripe's retention policy.
- **KYC / AML**: Stripe Connect Standard handles most of this for you; Express/Custom pushes more responsibility back. Know which model you chose and what it makes you responsible for.
- **State money transmission**: most platforms avoid this by using Stripe Connect (Stripe is the money transmitter, not you). Don't accidentally exit that model by holding funds yourself.

## Gotchas

- **Float math on money** — the silent killer. Always integer cents.
- **Unverified webhooks** — anyone can `POST` to your endpoint and trigger account changes.
- **Webhook handlers that aren't idempotent** — Stripe retries; you'll double-process.
- **Hard-coded amounts in code** — promotions, taxes, and fees belong in data or config, not in source.
- **PANs landing on your server** — even briefly. Use Elements; your scope tradeoff depends on it.
- **Test key committed to git** — get it out and rotate immediately. Test keys are still keys.
- **One key for everything** — restricted keys exist for a reason; least-privilege limits blast radius on leak.
- **No reconciliation** — small drift becomes a customer-impacting discrepancy.

## Output

A PR or branch implementing the payment flow with: idempotency keys on writes, signature-verified webhook handler with dedupe, audit log table + writes, integer-cents storage, test-mode end-to-end test, and a reconciliation hook stubbed. Final chat summary lists: PCI posture (which SAQ level), key permissions used, audit log table name, test coverage.
