# Store Adapters — Find Shareholders

The skill writes to whatever `privsec.store` is set to. Default: Google Sheet.
All three use the same schema (`sheet-schema.md`).

## Google Sheet (default)

- Requires the Google Drive/Sheets MCP or connector to be connected.
- On first run for a company, create or locate a sheet/tab named for the company
  (e.g. "Replit shareholders").
- **Dedup:** read existing rows, build a set of (Name + Firm + Tag), append only
  new people.
- Append rows in schema column order; leave unknown cells blank.

## Supabase

- Requires a Supabase connection. Use a table like:

```sql
create table if not exists shareholders (
  id           bigserial primary key,
  firm_name    text,
  full_name    text not null,
  title        text,
  email        text,
  phone        text,
  linkedin     text,
  round        text,
  source_url   text not null,
  status       text default 'New',
  tag          text not null,
  date_added   date default current_date,
  unique (full_name, firm_name, tag)
);
```

- The `unique` constraint handles dedup — insert with `on conflict do nothing`.
- If the operator's Supabase MCP is read-only, output the INSERT statements for
  the user to run, rather than failing silently.

## Local CSV

- Append to `<company>-shareholders.csv` in the workspace.
- Dedup by reading the file first and skipping matching (Name + Firm + Tag).
- Simplest, no external dependency — good default when nothing's connected.

## Picking the adapter

If `privsec.store` is unset, default to Google Sheet if the Sheets connector is
present, else fall back to local CSV and tell the user. Never fail the whole run
just because the preferred store isn't wired — capture the data somewhere and
say where it went.
