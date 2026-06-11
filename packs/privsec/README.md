# Pack: privsec

Private-securities sourcing skills — finding and reaching shareholders/sellers of
private companies. **Off by default**; opt in per skill.

## Skills

- **find-shareholders** — given a company name, find its investors (firms, funds,
  individuals) from public funding data, enrich contacts via a user-connected
  provider, log to a configurable store (default Google Sheet), and **queue**
  personalized outreach for human approval. Includes optional 3-day follow-up and
  7-day re-discovery cron flows. Maximus drafts and schedules; the rider approves
  every send.

## Enable

```bash
ln -sfn "$(pwd)/packs/privsec/skills/find-shareholders" "$HOME/.openclaw/workspace/skills/find-shareholders"
```

## Config

Set in `openclaw.json`:

```json
{
  "privsec": {
    "store": "sheet",                  // sheet | supabase | csv
    "enrichment_provider": "apollo"    // apollo | clay | hunter | ...
  }
}
```

The skill prompts the user to connect an enrichment provider if none is set, and
falls back to local CSV if no store connector is available.

## A note on responsibility

This pack assembles public data and **drafts** outreach. It does not send
autonomously. Cold outreach to individuals is legally regulated (CAN-SPAM, GDPR,
CASL); the operator is responsible for sending lawfully. The skill surfaces the
relevant rules and includes a compliance footer in templates — but the rider
decides what ships. The horse plows; it doesn't sign the contracts.
