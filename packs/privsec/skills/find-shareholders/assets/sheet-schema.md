# Store Schema — Find Shareholders

One row per **person** (not per firm). A firm with three relevant partners is
three rows sharing the same Firm Name.

| Column               | Notes                                                        |
|----------------------|--------------------------------------------------------------|
| Firm Name            | Investing firm/fund. Blank for pure individuals/angels.      |
| Individual Full Name | The person to contact. Required to be a row at all.          |
| Title                | GP, Partner, CIO, Angel, etc.                                |
| Email                | From enrichment provider. Blank if not found — never guess.  |
| Phone                | From enrichment provider. Blank if not found.                |
| LinkedIn             | Profile URL.                                                 |
| Round                | Round + year if the source linked them (e.g. "Series D 2026").|
| Source URL           | Where this shareholder was found. Required — for verification.|
| Status               | New → Sent → Followed Up → Replied → Call → Closed.          |
| Tag                  | "<company> shareholder" (e.g. "Replit shareholder").         |
| Date Added           | ISO date the row was created.                                |

## Rules

- **Skip empty fields** — leave the cell blank, don't write "N/A" or a guess.
- **Dedup on (Individual Full Name + Firm Name + Tag)** before appending.
- **Status drives the cron flows** — the 3-day follow-up acts on "Sent", the
  7-day re-discovery appends only names not already present for that Tag.
