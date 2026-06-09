// Recruiter Deep-Find — Express API
// Endpoints:
//   GET  /api/health           liveness probe
//   POST /api/run-search       run the deep-find workflow against Perplexity Sonar
//
// In production (`npm start`), this server also serves the built client from ../client/dist
// so a single Replit deployment hosts the whole app.

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
// Prompt builder
// ---------------------------------------------------------------------------
function buildSystemPrompt() {
  return `You are a senior technical recruiter's research analyst. You execute the recruiter-deep-find workflow:

1. Identify 8-15 candidate EMPLOYER agencies that match the brief (DevOps agencies, dev shops, outsourcing firms, MSPs, staffing agencies, cloud/security consultancies).
2. For each agency, surface 1-3 publicly-visible PEOPLE who plausibly match the role profile.
3. For a NAMED-PERSON search, focus on verifying identity with 2+ public signals (LinkedIn + GitHub + conference bios + personal sites).
4. For each candidate provide: name, current agency, title, location, key skills observed, public profile URLs, and a one-line "why this fits" rationale.
5. Flag movement signals (tenure, open-to-work, recent rebranding) when visible.
6. Flag non-solicit risk for large outsourcing firms (Infosys/TCS/Wipro/HCL/Cognizant/Accenture/EPAM/Globant/BairesDev).
7. Cite every claim with a source URL. Never invent contact info. Only report publicly-published info.

Return your answer as STRICT JSON matching this schema (no markdown, no prose outside JSON):
{
  "brief_recap": "1-2 sentence echo of the brief",
  "agencies": [
    {"name": "...", "hq": "...", "size": "...", "services": "...", "url": "..."}
  ],
  "candidates": [
    {
      "rank": 1,
      "name": "...",
      "current_agency": "...",
      "title": "...",
      "location": "...",
      "key_skills": ["..."],
      "movement_signal": "...",
      "non_solicit_risk": "low|moderate|high",
      "why_fit": "...",
      "linkedin_url": "...",
      "github_url": "...",
      "other_sources": ["..."]
    }
  ],
  "sourcing_notes": "Gaps, agencies that yielded nothing, suggested follow-ups",
  "citations": ["url1", "url2"]
}`
}

function buildUserPrompt(intake) {
  const named = intake.target_type === 'named_person'
  const lines = []
  lines.push(named
    ? `# Named-person search\n\nLocate and verify: **${intake.person_name || '(no name given)'}**.`
    : `# Role-profile shortlist\n\nBuild a shortlist of ${intake.shortlist_size || 15} candidates.`)
  lines.push('')
  lines.push('## Brief')
  if (intake.role_title)             lines.push(`- Role: **${intake.role_title}**`)
  if (intake.seniority)              lines.push(`- Seniority: ${intake.seniority}`)
  if (intake.skills?.length)         lines.push(`- Must-have skills: ${intake.skills.join(', ')}`)
  if (intake.agency_types?.length)   lines.push(`- Agency types: ${intake.agency_types.join(', ')}`)
  if (intake.geo)                    lines.push(`- Geo target: ${intake.geo}`)
  if (intake.geo_restrictions)       lines.push(`- Hard geo restriction: ${intake.geo_restrictions}`)
  if (intake.languages?.length)      lines.push(`- Languages: ${intake.languages.join(', ')}`)
  if (intake.industry_vertical)      lines.push(`- Industry vertical: ${intake.industry_vertical}`)
  if (intake.clearance_or_compliance?.length)
                                     lines.push(`- Compliance/clearance: ${intake.clearance_or_compliance.join(', ')}`)
  if (intake.current_employer_hint)  lines.push(`- Current employer hint: ${intake.current_employer_hint}`)
  if (intake.prior_employer_hint)    lines.push(`- Prior employer hint: ${intake.prior_employer_hint}`)
  if (intake.notes)                  lines.push(`- Notes: ${intake.notes}`)
  lines.push('')
  lines.push('Seed your agency-discovery search with: Clutch.co (DevOps + Cloud Consulting categories), The Manifest, GoodFirms, G2, AWS Partner Finder, GCP Partner Directory, Azure Solutions Partners, HashiCorp Partners, CNCF Kubernetes Certified Service Providers, Built In city pages.')
  lines.push('')
  lines.push('Return STRICT JSON per the schema. No prose outside the JSON.')
  return lines.join('\n')
}

// ---------------------------------------------------------------------------
// JSON extraction (tolerant of model wrapping)
// ---------------------------------------------------------------------------
function extractJson(text) {
  if (!text) return null
  const fence = text.match(/```(?:json)?\s*([\s\S]*?)```/i)
  const candidate = fence ? fence[1] : text
  // Find first { and matching last }
  const start = candidate.indexOf('{')
  const end = candidate.lastIndexOf('}')
  if (start < 0 || end < 0 || end <= start) return null
  const body = candidate.slice(start, end + 1)
  try { return JSON.parse(body) } catch { return null }
}

// ---------------------------------------------------------------------------
// Mock fallback when no API key — lets the UI be exercised end-to-end
// ---------------------------------------------------------------------------
function mockResult(intake) {
  const named = intake.target_type === 'named_person'
  return {
    brief_recap: named
      ? `Mock dossier for ${intake.person_name || 'unnamed candidate'}.`
      : `Mock shortlist for ${intake.role_title || 'a role'} (${intake.geo || 'global'}).`,
    agencies: [
      { name: 'Container Solutions', hq: 'Amsterdam, NL', size: '50-200', services: 'DevOps, Kubernetes, Cloud Native', url: 'https://container-solutions.com' },
      { name: 'Caylent',             hq: 'Irvine, CA',    size: '200-500', services: 'AWS-focused DevOps & data',         url: 'https://caylent.com' },
      { name: 'Stark & Wayne',       hq: 'Buffalo, NY',   size: '10-50',   services: 'Cloud Foundry, BOSH, K8s',          url: 'https://starkandwayne.com' },
    ],
    candidates: Array.from({ length: Math.min(5, intake.shortlist_size || 5) }).map((_, i) => ({
      rank: i + 1,
      name: `Mock Candidate ${i + 1}`,
      current_agency: ['Container Solutions', 'Caylent', 'Stark & Wayne'][i % 3],
      title: intake.role_title || 'Senior DevOps Engineer',
      location: intake.geo || 'US-remote',
      key_skills: intake.skills?.length ? intake.skills.slice(0, 4) : ['Kubernetes', 'Terraform', 'AWS'],
      movement_signal: i === 0 ? 'Open-to-work badge visible' : '24mo tenure, no movement signal',
      non_solicit_risk: 'low',
      why_fit: 'Public talks + GitHub footprint align with the brief.',
      linkedin_url: 'https://linkedin.com/in/example',
      github_url:   'https://github.com/example',
      other_sources: ['https://example.com/talk'],
    })),
    sourcing_notes: 'This is a MOCK response. Set PERPLEXITY_API_KEY in your environment to run real Sonar searches.',
    citations: ['https://clutch.co/developers/devops', 'https://kubernetes.io/partners/#kcsp'],
    _mock: true,
  }
}

// ---------------------------------------------------------------------------
// /api/run-search
// ---------------------------------------------------------------------------
app.post('/api/run-search', async (req, res) => {
  const intake = req.body || {}
  if (!intake || typeof intake !== 'object') {
    return res.status(400).json({ error: 'invalid intake body' })
  }

  if (!PPLX_KEY) {
    // No key — return mock so the UI is testable
    return res.json({ ok: true, mode: 'mock', result: mockResult(intake) })
  }

  try {
    const t0 = Date.now()
    const r = await fetch('https://api.perplexity.ai/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${PPLX_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: PPLX_MODEL,
        messages: [
          { role: 'system', content: buildSystemPrompt() },
          { role: 'user',   content: buildUserPrompt(intake) },
        ],
        temperature: 0.2,
        max_tokens: 4000,
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

    return res.json({
      ok: true,
      mode: 'sonar',
      model: PPLX_MODEL,
      elapsed_ms: Date.now() - t0,
      result: parsed || { raw: content, citations, _parse_failed: true },
      raw_citations: citations,
    })
  } catch (e) {
    return res.status(500).json({ error: 'server_error', message: String(e?.message || e) })
  }
})

export default app

