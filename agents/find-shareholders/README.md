# find-shareholders

Standalone agent: type any company name, get the institutional shareholders (funds) and the named individuals at those funds, in CSV format ready to enrich with **Folk** or **Apollo**.

Part of [Maximus AI](https://github.com/MacroTechTitan/MaximusAI). Sibling of `recruiter-deep-find`.

## What it does

For each company you input (public or private), the agent:

1. Determines if the company is public (has a ticker) or private.
2. Surfaces the **institutional shareholders / cap-table investors**:
   - Public: latest 13F filings, proxy statements (DEF 14A), Yahoo/Nasdaq institutional holdings.
   - Private: announced rounds via Crunchbase, PitchBook public summaries, press, SEC Form D.
3. For each fund, surfaces **1–3 named individuals** (deal lead first, then Managing Partner, then IR/Cap Formation).
4. Cites every claim with a source URL.

## Outputs

**Funds tab** — one row per fund per company:
```
company, fund_name, fund_type, stake_type, position_size, ownership_pct,
source_date, fund_website, fund_linkedin, fund_hq, source_urls
```

**People tab** — Folk/Apollo-ready columns:
```
first_name, last_name, full_name, title, company (= fund), fund_role,
related_portfolio_company, email_guess, linkedin_url, twitter_url,
location, seniority, source_urls
```

The `people.csv` column names match Apollo's Person CSV import format so the file imports cleanly. Folk auto-maps any of these without ceremony.

## Run locally

```bash
npm run install:all
cp .env.example .env       # add PERPLEXITY_API_KEY (optional — mock fallback if missing)
npm run dev                # client on :5173, api on :3001
```

Or single-process production:

```bash
npm run install:all
npm run build
npm start                  # serves API + built client on :3001
```

## Deploy to Replit

1. Import this folder (or the parent `MaximusAI` repo and `cd agents/find-shareholders`).
2. Add Replit Secret: `PERPLEXITY_API_KEY` (get one at https://www.perplexity.ai/settings/api).
3. Click **Run**. `.replit` handles install + build + start.

## API

### `GET /api/health`
```json
{ "ok": true, "has_api_key": true, "model": "sonar-pro", "ts": "..." }
```

### `POST /api/find-shareholders`
**Body:**
```json
{
  "companies": ["Figure AI", "Anduril"],
  "options": {
    "max_funds_per_company": 10,
    "max_people_per_fund": 2,
    "include_private": true
  }
}
```

**Response:**
```json
{
  "ok": true,
  "mode": "sonar",
  "model": "sonar-pro",
  "elapsed_ms": 6720,
  "result": { "results": [...], "citations": [...], "notes": "..." },
  "funds":   [/* flattened, ready for funds.csv */],
  "people":  [/* flattened, ready for people.csv */],
  "by_company": { "Figure AI": { "funds": 8, "people": 14, "company_type": "private", "ticker": null, "as_of": "2026-06" } }
}
```

Without an API key, the server returns a mock with the same shape so you can exercise the UI end-to-end.

## Workflow tip

1. Run the search for your target companies.
2. Click **Download people.csv (Folk/Apollo)**.
3. Import to Folk or Apollo; both will auto-enrich emails + phones from the LinkedIn URLs and `first_name + company` rows.
4. Build sequences off the `related_portfolio_company` field (your wedge: "I noticed your firm invested in X — …").

## Notes & limits

- Private-company shareholder data is only as good as what was disclosed publicly. Expect 60–80% coverage of lead investors, much less for unannounced angels.
- 13F filings lag by ~45 days — the agent's `source_date` reflects the filing period.
- `email_guess` is left blank unless the fund's email pattern was found in a public source. **Never** send to an unverified email — pipe through Folk/Apollo verification first.
- For large 25+ company batches, expect 30–60s per Sonar call. Consider running in chunks.

## License

MIT
