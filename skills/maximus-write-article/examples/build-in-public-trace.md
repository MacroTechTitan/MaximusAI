# Worked trace — Build-in-Public Technical Writeup

**Topic:** Shipping idempotent webhook handling for a billing integration
**Format:** Technical / build-in-public (problem → approach → code → tradeoffs → what's next)
**Target length:** 900 words

This trace shows the pipeline applied to a technical post, including where real code was pulled from source rather than retyped from memory.

---

## 1. Prompt (as given by the user)

> "Write a build-in-public post about the webhook idempotency bug we just fixed in the billing service. Technical audience, show the actual fix, be honest about what we tried first that didn't work."

## 2. Frame

- **Thesis / narrative spine:** Duplicate webhook deliveries were double-charging retries; the fix wasn't "add a lock," it was "make the operation itself safe to repeat."
- **Material needed:** the actual PR/diff for the fix — do not write this from a description alone.
- **Depth tier:** Standard, leaning Deep — this is a payments-adjacent claim (double-charging), so treat code accuracy and any dollar-impact claim carefully. If `maximus-fintech-payments` conventions apply to the repo, note them.

## 3. Gather real material first

`read`/`grep` run against the actual repository before drafting (illustrative paths below — in a live run these are the real files):

```
grep -n "def handle_webhook" services/billing/webhooks.py
read services/billing/webhooks.py
read services/billing/tests/test_webhooks.py
```

Confirmed from the source:
- The original handler charged a payment method inside the webhook handler with no dedup check.
- The fix adds an idempotency key check against a `processed_events` table before charging.
- A test was added that replays the same webhook payload twice and asserts only one charge occurs.

**No code below is invented.** It mirrors the structure actually read from the files above. In a live run, snippets are copied verbatim from `read` output, not retyped from memory.

## 4. Outline (shown to user before drafting)

```
Problem: retried webhooks from the payment provider were double-charging
  customers on network blips — provider retries on any non-2xx response,
  and our handler wasn't safe to run twice.

Approach considered and rejected: a distributed lock around the handler.
  Rejected because it doesn't survive a crash between "acquire lock" and
  "release lock" — a crashed process leaves the lock held and the retry
  silently drops, worse than double-charging.

Approach taken: make the operation idempotent at the data layer. Record
  the provider's event ID before charging; check for it first; if seen,
  return 200 without charging again.

Tradeoffs accepted: adds one write to a tracking table per webhook, and a
  cleanup/retention job for that table now exists as a small new
  maintenance surface — a good trade for correctness on money movement.

What's next: same pattern needs applying to the two other webhook
  consumers in the codebase that don't have it yet.
```

## 5. Draft (excerpt)

**Problem, as drafted:**

> Our payment provider retries any webhook delivery that doesn't get a fast 2xx back. That's the right behavior on their end — and it exposed that our handler wasn't safe to run twice. A slow database call under load meant our response came back late, the provider retried, and the retry landed on a handler that had no memory of the first attempt. Result: a small number of customers got charged twice for the same invoice.

**Approach rejected, as drafted:**

> The obvious fix is a lock: acquire it at the top of the handler, release it at the end, reject a second concurrent call. We built this first. It failed a chaos test in about ten minutes — kill the process between acquiring the lock and finishing the charge, and the lock never releases. The retry that was supposed to safely fail instead hangs. A lock protects against concurrency; it does nothing about a crash mid-operation, and mid-operation crashes are exactly what retries exist to recover from.

**Code snippet, pulled from the actual fix (`services/billing/webhooks.py`):**

```python
def handle_webhook(event: WebhookEvent) -> Response:
    if EventLog.exists(event.id):
        return Response(status=200)  # already processed, ack without side effects

    with transaction():
        EventLog.record(event.id)
        charge_result = charge_payment_method(event.payment_method_id, event.amount)

    return Response(status=200, body=charge_result)
```

*(Marked as: pulled from the actual PR diff during the Gather step above. In a live run, this snippet is copied from the `read` tool's output, not retyped.)*

**Tradeoffs, as drafted:**

> This adds a table and a write to every webhook, successful or not. That's a real cost — more storage, one more thing that can be slow. It's the right trade because the failure mode it prevents is a customer being charged twice, and no amount of handler cleverness beats "the operation itself can't be repeated unsafely."

**What's next, as drafted:**

> Two other webhook consumers in the codebase — subscription-cancellation and refund-processed — don't have this pattern yet. Same fix, smaller blast radius since neither moves money directly. That's next sprint, not urgent, but on the board.

## 6. Tighten pass

- Cut a paragraph explaining what "idempotency" means in general terms — the target audience already knows this; defining it read as padding.
- Shortened the "approach rejected" section by removing a second paragraph that re-explained the chaos test result a different way.
- Net cut: ~110 words.

## 7. Verify

- Function names and table names checked against the actual file read in step 3 — no invented API.
- No specific dollar figure or customer count for the double-charge incident was available with confidence, so the draft says "a small number of customers" rather than fabricating a number — same discipline as the thought-leadership trace.
- Flagged for the user: confirm before publishing whether the incident count or dollar impact can be disclosed publicly; that's a business decision, not a writing one.

## 8. Ship

Delivered: ~800-word final draft, one confirmed-real code snippet (flagged as pulled from source), and a note that the "next" webhooks (subscription-cancellation, refund-processed) should be verified as still accurate before publishing, since sprint plans shift.

**What this trace demonstrates:** the code snippet was pulled from an actual `read` of the source file, not generated to look plausible — this is the single most important discipline difference between this format and the thought-leadership one. The "approach rejected" section is not filler; it's what makes a build-in-public post read as trustworthy rather than as a highlight reel.
