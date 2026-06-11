# Outreach Templates — Find Shareholders

Merge fields: `{{first_name}}`, `{{firm}}`, `{{company}}`, `{{sender_name}}`,
`{{sender_org}}`. Maximus renders these and **queues the result for approval** —
it does not send. Edit these freely; they're starting points.

> The operator must supply a real subject, sender identity, and a compliant
> footer (physical address + opt-out) before any send. Placeholders below.

## Initial outreach

```
Subject: {{company}} — secondary interest

Dear {{first_name}},

I'm reaching out regarding {{company}}. We work with holders of private
shares and wanted to gauge whether you or {{firm}} would be open to a brief
conversation about potential liquidity options.

No obligation — happy to share specifics if useful.

Best,
{{sender_name}}
{{sender_org}}

—
{{sender_org}} · {{physical_address}}
Unsubscribe: {{unsubscribe_link}}
```

## Follow-up (3 days, no reply)

```
Subject: Re: {{company}} — secondary interest

Dear {{first_name}},

Circling back briefly in case my note got buried. If there's any interest in
discussing {{company}} share liquidity, I'm glad to find a time. If not, no
worries at all and I won't follow up further.

Best,
{{sender_name}}

—
{{sender_org}} · {{physical_address}}
Unsubscribe: {{unsubscribe_link}}
```

## Call / LinkedIn nudge

```
Subject: {{company}} — quick call?

Dear {{first_name}},

Would a short call be easier than email? Also happy to connect on LinkedIn:
{{sender_linkedin}}. Whatever's least friction for you.

Best,
{{sender_name}}

—
{{sender_org}} · {{physical_address}}
Unsubscribe: {{unsubscribe_link}}
```

## Compliance footer — required

Every sent email needs `{{physical_address}}` and a working
`{{unsubscribe_link}}` (CAN-SPAM). Don't strip the footer. If the user's send
path can't honor opt-outs, recommend exporting drafts to a compliant platform.
