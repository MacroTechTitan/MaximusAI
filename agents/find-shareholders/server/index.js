// find-shareholders — Express API
// Endpoints:
//   GET  /api/health           liveness probe
//   POST /api/find-shareholders  run the shareholder-discovery workflow against Perplexity Sonar
//
// Input:  { companies: ["Figure AI", "Anduril", ...], options?: { include_private, max_funds_per_company, max_people_per_fund } }
// Output: { funds: [...], people: [...], by_company: {...}, citations: [...] }

import 'dotenv/config'
import express from 'express'
import cors from 'cors'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import fs from 'node:fs'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const PORT = process.env.PORT || 3001
const PPLX_KEY = process.env.PERPLEXITY_API_KEY || process.env.PPLX_API_KEY
const PPLX_MODEL = process.env.PERPLEXITY_MODEL || 'sonar-pro'

const app = express()
app.use(cors())
app.use(express.json({ limit: '1mb' }))

// ---------------------------------------------------------------------------
// Health
// ---------------------------------------------------------------------------
app.get('/api/health', (_req, res) => {
  res.json({
    ok: true,
    has_api_key: Boolean(PPLX_KEY),
    model: PPLX_MODEL,
    ts: new Date().toISOString(),
  })
})

// ---------------------------------------------------------------------------
// Prompt builders
// ---------------------------------------------------------------------------
function buildSystemPrompt() {
  return `You are an investment research analyst specializing in cap-table and shareholder discovery.

For each company the user names you must:

1. Identify whether the company is PUBLIC (has a ticker) or PRIVATE.
2. Find its INSTITUTIONAL SHAREHOLDERS — venture funds, growth funds, hedge funds, mutual funds, sovereign wealth, family offices, strategics.
   - PUBLIC: pull from latest 13F filings (Whalewisdom, fintel, sec.gov), proxy statements (DEF 14A), Yahoo/Nasdaq institutional holdings pages.
   - PRIVATE: pull from announced funding rounds (Crunchbase, PitchBook public summaries, TechCrunch, Forbes, company press releases, SEC Form D filings).
3. For each FUND surface 1-3 specific NAMED INDIVIDUALS connected to that position:
   - The investing Partner / Principal who led or sits on the board
   - The fund's Managing Partner / GP if no specific deal lead is public
   - Investor Relations / Head of Capital Formation as a fallback
4. NEVER invent emails. If you can identify the fund's standard email pattern (e.g. firstname@fund.com from public press), output it as email_guess and note the pattern source. Otherwise leave email_guess blank.
5. Cite EVERY claim with a source URL. Prefer primary sources (SEC, fund's own site, signed press release) over aggregators.

Return STRICT JSON matching this schema (no markdown, no prose outside JSON):

{
  "results": [
    {
      "company": "Figure AI",
      "company_type": "private|public",
      "ticker": null,
      "stage_or_market_cap": "Series C $675M (Feb 2024)",
      "as_of": "2026-06",
      "funds": [
        {
          "fund_name": "Microsoft",
          "fund_type": "Strategic|VC|Growth|Hedge|Mutual|Sovereign|Family Office",
          "stake_type": "Equity (Series C)",
          "position_size": "$95M",
          "ownership_pct": null,
          "source_date": "2024-02-29",
          "fund_website": "https://microsoft.com",
          "fund_linkedin": "https://linkedin.com/company/microsoft",
          "fund_hq": "Redmond, WA",
          "source_urls": ["https://..."],
          "people": [
            {
              "first_name": "Brad",
              "last_name": "Smith",
              "full_name": "Brad Smith",
              "title": "Vice Chair & President",
              "fund_role": "Strategic investment sponsor",
              "linkedin_url": "https://linkedin.com/in/...",
              "twitter_url": null,
              "location": "Redmond, WA",
              "seniority": "C-Suite",
              "email_guess": null,
              "email_pattern_source": null,
              "source_urls": ["https://..."]
            }
          ]
        }
      ]
    }
  ],
  "citations": ["url1", "url2"],
  "notes": "Any caveats about staleness, partial coverage, or private-company limits."
}`
}

function buildUserPrompt(companies, options) {
  const maxFunds  = options?.max_funds_per_company ?? 10
  const maxPeople = options?.max_people_per_fund ?? 2
  const lines = []
  lines.push(`# Shareholder discovery brief`)
  lines.push('')
  lines.push(`Companies to research (${companies.length}):`)
  companies.forEach((c, i) => lines.push(`${i + 1}. ${c}`))
  lines.push('')
  lines.push(`Constraints:`)
  lines.push(`- Up to ${maxFunds} funds per company (largest stakes first).`)
  lines.push(`- ${maxPeople} named individuals per fund (deal lead first, then GP).`)
  lines.push(`- Include both public-market institutional holders AND private-round investors when applicable.`)
  lines.push(`- For private companies, prioritize lead investors of the most recent round.`)
  lines.push(`- Verify each fund-person tie with a public source.`)
  lines.push('')
  lines.push(`Return STRICT JSON per the schema. No prose outside the JSON.`)
  return lines.join('\n')
}

// ---------------------------------------------------------------------------
// JSON extraction (tolerant)
// ---------------------------------------------------------------------------
function extractJson(text) {
  if (!text) return null
  const fence = text.match(/```(?:json)?\s*([\s\S]*?)```/i)
  const candidate = fence ? fence[1] : text
  const start = candidate.indexOf('{')
  const end = candidate.lastIndexOf('}')
  if (start < 0 || end < 0 || end <= start) return null
  try { return JSON.parse(candidate.slice(start, end + 1)) } catch { return null }
}

// ---------------------------------------------------------------------------
// Flatten the nested response into the two table-shaped collections
// the UI + CSV exporters consume.
// ---------------------------------------------------------------------------
function flatten(result) {
  const funds = []
  const people = []
  const by_company = {}
  const companies = result?.results || []

  for (const c of companies) {
    by_company[c.company] = { funds: 0, people: 0, company_type: c.company_type, ticker: c.ticker, as_of: c.as_of, stage_or_market_cap: c.stage_or_market_cap }
    for (const f of c.funds || []) {
      funds.push({
        company:        c.company,
        company_type:   c.company_type,
        fund_name:      f.fund_name,
        fund_type:      f.fund_type,
        stake_type:     f.stake_type,
        position_size:  f.position_size,
        ownership_pct:  f.ownership_pct,
        source_date:    f.source_date,
        fund_website:   f.fund_website,
        fund_linkedin:  f.fund_linkedin,
        fund_hq:        f.fund_hq,
        source_urls:    (f.source_urls || []).join(' | '),
      })
      by_company[c.company].funds += 1
      for (const p of f.people || []) {
        const full = p.full_name || `${p.first_name || ''} ${p.last_name || ''}`.trim()
        const [first, ...rest] = full.split(/\s+/)
        people.push({
          first_name:               p.first_name || first || '',
          last_name:                p.last_name  || rest.join(' ') || '',
          full_name:                full,
          title:                    p.title,
          company:                  f.fund_name,                 // their employer = the fund
          fund_role:                p.fund_role,
          related_portfolio_company: c.company,
          email_guess:              p.email_guess || '',
          email_pattern_source:     p.email_pattern_source || '',
          linkedin_url:             p.linkedin_url || '',
          twitter_url:              p.twitter_url || '',
          location:                 p.location || '',
          seniority:                p.seniority || '',
          source_urls:              (p.source_urls || []).join(' | '),
        })
        by_company[c.company].people += 1
      }
    }
  }
  return { funds, people, by_company }
}

// ---------------------------------------------------------------------------
// Mock for no-key dev
// ---------------------------------------------------------------------------
function mockResult(companies) {
  const results = companies.map((c) => ({
    company: c,
    company_type: 'private',
    ticker: null,
    stage_or_market_cap: 'Series C (mock)',
    as_of: '2026-06',
    funds: [
      {
        fund_name: 'Microsoft', fund_type: 'Strategic', stake_type: 'Equity', position_size: '$95M', ownership_pct: null,
        source_date: '2024-02-29', fund_website: 'https://microsoft.com', fund_linkedin: 'https://linkedin.com/company/microsoft', fund_hq: 'Redmond, WA',
        source_urls: ['https://example.com/figure-series-c'],
        people: [{
          first_name: 'Brad', last_name: 'Smith', full_name: 'Brad Smith',
          title: 'Vice Chair & President', fund_role: 'Strategic investment sponsor',
          linkedin_url: 'https://linkedin.com/in/example', twitter_url: null,
          location: 'Redmond, WA', seniority: 'C-Suite',
          email_guess: '', email_pattern_source: null,
          source_urls: ['https://example.com/press'],
        }],
      },
      {
        fund_name: 'Intel Capital', fund_type: 'Strategic', stake_type: 'Equity', position_size: '$25M', ownership_pct: null,
        source_date: '2024-02-29', fund_website: 'https://intelcapital.com', fund_linkedin: 'https://linkedin.com/company/intel-capital', fund_hq: 'Santa Clara, CA',
        source_urls: ['https://example.com/figure-series-c'],
        people: [{
          first_name: 'Mark', last_name: 'Rostick', full_name: 'Mark Rostick',
          title: 'Vice President & Senior Managing Director', fund_role: 'GP',
          linkedin_url: 'https://linkedin.com/in/example', twitter_url: null,
          location: 'Santa Clara, CA', seniority: 'Partner',
          email_guess: '', email_pattern_source: null,
          source_urls: ['https://example.com/about'],
        }],
      },
    ],
  }))
  return {
    results,
    citations: ['https://example.com/figure-series-c', 'https://example.com/whalewisdom-mock'],
    notes: 'MOCK response. Set PERPLEXITY_API_KEY for live Sonar results.',
    _mock: true,
  }
}

// ---------------------------------------------------------------------------
// /api/find-shareholders
// ---------------------------------------------------------------------------
app.post('/api/find-shareholders', async (req, res) => {
  const { companies, options } = req.body || {}
  if (!Array.isArray(companies) || companies.length === 0) {
    return res.status(400).json({ error: 'companies must be a non-empty array of company names' })
  }
  const clean = companies.map((s) => String(s).trim()).filter(Boolean).slice(0, 25)

  if (!PPLX_KEY) {
    const raw = mockResult(clean)
    return res.json({ ok: true, mode: 'mock', result: raw, ...flatten(raw) })
  }

  try {
    const t0 = Date.now()
    const r = await fetch('https://api.perplexity.ai/chat/completions', {
      method: 'POST',
      headers: { Authorization: `Bearer ${PPLX_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: PPLX_MODEL,
        messages: [
          { role: 'system', content: buildSystemPrompt() },
          { role: 'user',   content: buildUserPrompt(clean, options) },
        ],
        temperature: 0.1,
        max_tokens: 6000,
      }),
    })
    if (!r.ok) {
      const errText = await r.text()
      return res.status(502).json({ error: 'sonar_api_error', status: r.status, detail: errText.slice(0, 500) })
    }
    const data = await r.json()
    const content = data?.choices?.[0]?.message?.content || ''
    const citations = data?.citations || data?.search_results?.map((s) => s.url) || []
    const parsed = extractJson(content)
    if (!parsed) {
      return res.json({
        ok: true, mode: 'sonar', model: PPLX_MODEL, elapsed_ms: Date.now() - t0,
        result: { raw: content, citations, _parse_failed: true },
        funds: [], people: [], by_company: {},
      })
    }
    return res.json({
      ok: true, mode: 'sonar', model: PPLX_MODEL, elapsed_ms: Date.now() - t0,
      result: parsed, ...flatten(parsed),
    })
  } catch (e) {
    return res.status(500).json({ error: 'server_error', message: String(e?.message || e) })
  }
})

// ---------------------------------------------------------------------------
// Static client (prod)
// ---------------------------------------------------------------------------
const clientDist = path.resolve(__dirname, '..', 'client', 'dist')
if (fs.existsSync(clientDist)) {
  app.use(express.static(clientDist))
  app.get('*', (_req, res) => res.sendFile(path.join(clientDist, 'index.html')))
}

app.listen(PORT, '0.0.0.0', () => {
  console.log(`[find-shareholders] api on :${PORT}`)
  console.log(`[find-shareholders] sonar key: ${PPLX_KEY ? 'present' : 'missing (mock mode)'}`)
})
