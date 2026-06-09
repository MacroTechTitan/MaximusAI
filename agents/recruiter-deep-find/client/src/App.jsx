import React, { useState, useMemo, useEffect } from 'react'

const AGENCY_TYPES = [
  'DevOps agency', 'Software dev agency', 'Outsourcing firm', 'MSP',
  'Staffing agency', 'Nearshore', 'Offshore', 'Cloud consultancy', 'Security consultancy',
]
const SENIORITIES = ['Junior', 'Mid', 'Senior', 'Staff', 'Principal', 'Director', 'VP']
const COMPLIANCE = ['SOC2', 'HIPAA', 'FedRAMP', 'PCI-DSS', 'ISO 27001', 'Security clearance']

function TagInput({ value, onChange, placeholder }) {
  const [draft, setDraft] = useState('')
  const add = (raw) => {
    const v = raw.trim().replace(/,$/, '').trim()
    if (!v || value.includes(v)) { setDraft(''); return }
    onChange([...value, v]); setDraft('')
  }
  return (
    <div className="tag-input">
      {value.map((t) => (
        <span className="tag" key={t}>{t}
          <button type="button" onClick={() => onChange(value.filter((x) => x !== t))}>×</button>
        </span>
      ))}
      <input
        value={draft}
        placeholder={value.length ? '' : placeholder}
        onChange={(e) => { const v = e.target.value; if (v.endsWith(',')) { add(v); return } setDraft(v) }}
        onKeyDown={(e) => {
          if (e.key === 'Enter') { e.preventDefault(); add(draft) }
          if (e.key === 'Backspace' && !draft && value.length) onChange(value.slice(0, -1))
        }}
        onBlur={() => add(draft)}
      />
    </div>
  )
}

function Chips({ options, value, onChange, multi = true }) {
  const toggle = (opt) => {
    if (multi) onChange(value.includes(opt) ? value.filter((x) => x !== opt) : [...value, opt])
    else onChange(opt)
  }
  return (
    <div className="chips">
      {options.map((o) => {
        const active = multi ? value.includes(o) : value === o
        return <span key={o} className={`chip ${active ? 'active' : ''}`} onClick={() => toggle(o)}>{o}</span>
      })}
    </div>
  )
}

function ResultsPanel({ run }) {
  if (!run) return null
  const { mode, result, elapsed_ms, model } = run
  const isMock = mode === 'mock' || result?._mock
  const cands = Array.isArray(result?.candidates) ? result.candidates : []
  const agencies = Array.isArray(result?.agencies) ? result.agencies : []
  const cites = result?.citations || run?.raw_citations || []

  const downloadCsv = () => {
    const header = 'rank,name,current_agency,title,location,key_skills,movement_signal,non_solicit_risk,why_fit,linkedin_url,github_url'
    const rows = cands.map((c) => [
      c.rank, c.name, c.current_agency, c.title, c.location,
      (c.key_skills || []).join('|'), c.movement_signal, c.non_solicit_risk, c.why_fit,
      c.linkedin_url, c.github_url,
    ].map((v) => `"${String(v ?? '').replace(/"/g, '""')}"`).join(','))
    const blob = new Blob([[header, ...rows].join('\n')], { type: 'text/csv' })
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'shortlist.csv'; a.click()
  }

  return (
    <div className="card results">
      <h2>Results</h2>
      <div className={`run-banner ${isMock ? 'mock' : ''}`}>
        <div>
          <span className="badge">{isMock ? 'MOCK' : 'LIVE · ' + (model || 'sonar')}</span>{' '}
          {result?.brief_recap || (isMock ? 'Mock response — set PERPLEXITY_API_KEY for real results.' : 'Search complete.')}
        </div>
        {elapsed_ms != null && <div>{(elapsed_ms / 1000).toFixed(1)}s</div>}
      </div>

      {agencies.length > 0 && (
        <>
          <h3>Agencies surfaced ({agencies.length})</h3>
          <table className="agencies-table">
            <thead><tr><th>Agency</th><th>HQ</th><th>Size</th><th>Services</th></tr></thead>
            <tbody>
              {agencies.map((a, i) => (
                <tr key={i}>
                  <td>{a.url ? <a href={a.url} target="_blank" rel="noreferrer">{a.name}</a> : a.name}</td>
                  <td>{a.hq}</td><td>{a.size}</td><td>{a.services}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

      {cands.length > 0 && (
        <>
          <h3>Candidates ({cands.length})</h3>
          {cands.map((c, i) => (
            <div className="cand" key={i}>
              <div className="cand-head">
                <div><span className="cand-rank">#{c.rank ?? i + 1}</span>{' '}<span className="cand-name">{c.name}</span></div>
                <div className="cand-meta">{c.title} · {c.current_agency} · {c.location}</div>
              </div>
              {c.why_fit && <div className="cand-row"><span><b>Why fit:</b>{c.why_fit}</span></div>}
              <div className="cand-row">
                {c.key_skills?.length > 0 && <span><b>Skills:</b>{c.key_skills.join(', ')}</span>}
                {c.movement_signal && <span><b>Movement:</b>{c.movement_signal}</span>}
                {c.non_solicit_risk && <span><b>Non-solicit risk:</b><span className={`risk-${c.non_solicit_risk}`}>{c.non_solicit_risk}</span></span>}
              </div>
              <div className="cand-links">
                {c.linkedin_url && <a href={c.linkedin_url} target="_blank" rel="noreferrer">LinkedIn</a>}
                {c.github_url   && <a href={c.github_url}   target="_blank" rel="noreferrer">GitHub</a>}
                {(c.other_sources || []).map((u, j) => <a key={j} href={u} target="_blank" rel="noreferrer">Source {j + 1}</a>)}
              </div>
            </div>
          ))}
        </>
      )}

      {result?.sourcing_notes && (
        <>
          <h3>Sourcing notes</h3>
          <div className="hint" style={{ marginBottom: 0 }}>{result.sourcing_notes}</div>
        </>
      )}

      {cites.length > 0 && (
        <>
          <h3>Citations</h3>
          <div className="citations">
            {cites.map((u, i) => (
              <div key={i}>[{i + 1}] <a href={u} target="_blank" rel="noreferrer">{u}</a></div>
            ))}
          </div>
        </>
      )}

      {result?._parse_failed && (
        <>
          <h3>Raw model output</h3>
          <div className="preview">{result.raw}</div>
        </>
      )}

      <div className="actions">
        {cands.length > 0 && <button className="secondary" onClick={downloadCsv}>Download CSV</button>}
        <button className="ghost" onClick={() => navigator.clipboard.writeText(JSON.stringify(run, null, 2))}>Copy raw JSON</button>
      </div>
    </div>
  )
}

export default function App() {
  const [targetType, setTargetType] = useState('role_profile')
  const [personName, setPersonName] = useState('')
  const [roleTitle, setRoleTitle] = useState('Senior DevOps Engineer')
  const [seniority, setSeniority] = useState('Senior')
  const [skills, setSkills] = useState(['Kubernetes', 'Terraform', 'AWS'])
  const [agencyTypes, setAgencyTypes] = useState(['DevOps agency', 'Cloud consultancy'])
  const [geo, setGeo] = useState('US-remote')
  const [geoRestrictions, setGeoRestrictions] = useState('US only')
  const [languages, setLanguages] = useState(['English'])
  const [currentEmployerHint, setCurrentEmployerHint] = useState('')
  const [priorEmployerHint, setPriorEmployerHint] = useState('')
  const [industryVertical, setIndustryVertical] = useState('')
  const [clearanceOrCompliance, setClearanceOrCompliance] = useState([])
  const [shortlistSize, setShortlistSize] = useState(10)
  const [notes, setNotes] = useState('')

  const [toast, setToast] = useState(null)
  const [running, setRunning] = useState(false)
  const [run, setRun] = useState(null)
  const [health, setHealth] = useState(null)

  useEffect(() => {
    fetch('/api/health').then((r) => r.json()).then(setHealth).catch(() => setHealth({ ok: false }))
  }, [])

  const intake = useMemo(() => ({
    schema_version: '1.0',
    generated_at: new Date().toISOString(),
    target_type: targetType,
    person_name: personName || null,
    role_title: roleTitle || null,
    seniority,
    skills, agency_types: agencyTypes,
    geo: geo || null, geo_restrictions: geoRestrictions || null,
    languages,
    current_employer_hint: currentEmployerHint || null,
    prior_employer_hint: priorEmployerHint || null,
    industry_vertical: industryVertical || null,
    clearance_or_compliance: clearanceOrCompliance,
    shortlist_size: Number(shortlistSize) || 15,
    notes: notes || null,
  }), [targetType, personName, roleTitle, seniority, skills, agencyTypes, geo, geoRestrictions, languages, currentEmployerHint, priorEmployerHint, industryVertical, clearanceOrCompliance, shortlistSize, notes])

  const flash = (msg, kind = 'ok') => { setToast({ msg, kind }); setTimeout(() => setToast(null), 2400) }

  const runSearch = async () => {
    setRunning(true); setRun(null)
    try {
      const r = await fetch('/api/run-search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(intake),
      })
      const data = await r.json()
      if (!r.ok || data.error) { flash(`Search failed: ${data.error || r.status}`, 'err'); return }
      setRun(data)
      flash(data.mode === 'mock' ? 'Mock results — set PERPLEXITY_API_KEY for live' : 'Search complete')
      setTimeout(() => document.getElementById('results-anchor')?.scrollIntoView({ behavior: 'smooth' }), 100)
    } catch (e) {
      flash(`Network error: ${e.message}`, 'err')
    } finally { setRunning(false) }
  }

  const downloadJson = () => {
    const blob = new Blob([JSON.stringify(intake, null, 2)], { type: 'application/json' })
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob)
    const slug = (personName || roleTitle || 'search').toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40)
    a.download = `recruiter_intake_${slug || 'search'}.json`; a.click()
    flash('Intake downloaded')
  }

  const namedMode = targetType === 'named_person'

  return (
    <div className="app">
      <div className="header">
        <h1>Recruiter Deep-Find</h1>
        <p>Source candidates from DevOps agencies, dev shops, outsourcing firms, MSPs, and technical staffing. Fill out the brief, click <code>Run Deep Search</code> to query the agent live.</p>
        {health && (
          <p style={{ marginTop: 8, fontSize: 12 }}>
            API: <span style={{ color: health.ok ? 'var(--success)' : 'var(--danger)' }}>{health.ok ? 'online' : 'offline'}</span>
            {' · '}Mode: <span style={{ color: health.has_api_key ? 'var(--success)' : 'var(--warn)' }}>{health.has_api_key ? `Sonar (${health.model})` : 'Mock (no API key)'}</span>
          </p>
        )}
      </div>

      <div className="card">
        <h2>Search mode</h2>
        <p className="hint">Tracking a specific person, or building a shortlist?</p>
        <div className="toggle-row">
          <span className={`chip ${namedMode ? '' : 'active'}`} onClick={() => setTargetType('role_profile')}>Role shortlist</span>
          <span className={`chip ${namedMode ? 'active' : ''}`} onClick={() => setTargetType('named_person')}>Named person</span>
        </div>
        {namedMode && (
          <div className="field">
            <label>Person name <span className="sub">required</span></label>
            <input type="text" value={personName} onChange={(e) => setPersonName(e.target.value)} placeholder="e.g. Maria Schmidt" />
          </div>
        )}
      </div>

      <div className="card">
        <h2>Role & skills</h2>
        <p className="hint">What the candidate does.</p>
        <div className="row">
          <div className="field"><label>Role title</label>
            <input type="text" value={roleTitle} onChange={(e) => setRoleTitle(e.target.value)} placeholder="Senior DevOps Engineer" /></div>
          <div className="field"><label>Seniority</label>
            <Chips options={SENIORITIES} value={seniority} onChange={setSeniority} multi={false} /></div>
        </div>
        <div className="field">
          <label>Must-have skills <span className="sub">Enter or comma to add</span></label>
          <TagInput value={skills} onChange={setSkills} placeholder="Kubernetes, Terraform, AWS…" />
        </div>
      </div>

      <div className="card">
        <h2>Employer profile</h2>
        <p className="hint">Kind of company they work at.</p>
        <div className="field"><label>Agency types</label>
          <Chips options={AGENCY_TYPES} value={agencyTypes} onChange={setAgencyTypes} /></div>
        <div className="row">
          <div className="field"><label>Current employer hint <span className="sub">optional</span></label>
            <input type="text" value={currentEmployerHint} onChange={(e) => setCurrentEmployerHint(e.target.value)} placeholder="Some Berlin DevOps consultancy" /></div>
          <div className="field"><label>Prior employer hint <span className="sub">optional</span></label>
            <input type="text" value={priorEmployerHint} onChange={(e) => setPriorEmployerHint(e.target.value)} placeholder="ThoughtWorks, AWS…" /></div>
        </div>
        <div className="field"><label>Industry vertical <span className="sub">optional</span></label>
          <input type="text" value={industryVertical} onChange={(e) => setIndustryVertical(e.target.value)} placeholder="fintech, healthtech, gov…" /></div>
        <div className="field"><label>Compliance / clearances</label>
          <Chips options={COMPLIANCE} value={clearanceOrCompliance} onChange={setClearanceOrCompliance} /></div>
      </div>

      <div className="card">
        <h2>Geography & language</h2>
        <div className="row">
          <div className="field"><label>Geo target</label>
            <input type="text" value={geo} onChange={(e) => setGeo(e.target.value)} placeholder="Austin, US-remote, EU…" /></div>
          <div className="field"><label>Hard geo restrictions <span className="sub">optional</span></label>
            <input type="text" value={geoRestrictions} onChange={(e) => setGeoRestrictions(e.target.value)} placeholder="US only, EU+UK, LATAM" /></div>
        </div>
        <div className="field"><label>Languages</label>
          <TagInput value={languages} onChange={setLanguages} placeholder="English, Spanish, German…" /></div>
      </div>

      <div className="card">
        <h2>Output</h2>
        <div className="row">
          <div className="field"><label>Shortlist size</label>
            <input type="number" value={shortlistSize} min={1} max={50} onChange={(e) => setShortlistSize(e.target.value)} /></div>
        </div>
        <div className="field"><label>Notes for the agent <span className="sub">free text</span></label>
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Avoid X agency, focus on open-to-work, timezone overlap with EST…" /></div>
      </div>

      <div className="card">
        <h2>Run</h2>
        <p className="hint">Submits the intake to the backend agent. Results render below.</p>
        <div className="actions">
          <button className="primary" onClick={runSearch} disabled={running}>
            {running ? <><span className="spinner" />Searching…</> : '▶ Run Deep Search'}
          </button>
          <button className="secondary" onClick={downloadJson}>Download JSON</button>
          <button className="ghost" onClick={() => navigator.clipboard.writeText(JSON.stringify(intake, null, 2))}>Copy JSON</button>
        </div>
        <details style={{ marginTop: 16 }}>
          <summary style={{ color: 'var(--muted)', cursor: 'pointer', fontSize: 13 }}>Show intake payload</summary>
          <div className="preview" style={{ marginTop: 10 }}>{JSON.stringify(intake, null, 2)}</div>
        </details>
      </div>

      <div id="results-anchor" />
      <ResultsPanel run={run} />

      <p className="footer-note">recruiter-deep-find · standalone build · API at <code>/api/run-search</code></p>

      {toast && <div className={`toast ${toast.kind === 'err' ? 'error' : ''}`}>{toast.msg}</div>}
    </div>
  )
}
