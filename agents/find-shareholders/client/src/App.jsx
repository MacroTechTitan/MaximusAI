import React, { useState, useEffect, useMemo } from 'react'

const PRESETS = ['Figure AI', 'Anthropic', 'OpenAI', 'Anduril', 'SpaceX', 'Stripe']

const FUND_COLUMNS = [
  { key: 'company',       label: 'Portfolio Co' },
  { key: 'fund_name',     label: 'Fund' },
  { key: 'fund_type',     label: 'Type' },
  { key: 'stake_type',    label: 'Stake' },
  { key: 'position_size', label: 'Position' },
  { key: 'ownership_pct', label: 'Own %' },
  { key: 'source_date',   label: 'As of' },
  { key: 'fund_hq',       label: 'HQ' },
  { key: 'fund_website',  label: 'Website',  isLink: true },
  { key: 'fund_linkedin', label: 'LinkedIn', isLink: true },
]

// Apollo / Folk-friendly people columns. These match Apollo's "Person" CSV
// import field names where possible (first_name, last_name, title, company,
// linkedin_url, twitter_url, location) so the file imports cleanly.
const PEOPLE_COLUMNS = [
  { key: 'first_name',                label: 'First' },
  { key: 'last_name',                 label: 'Last' },
  { key: 'title',                     label: 'Title' },
  { key: 'company',                   label: 'Company (Fund)' },
  { key: 'fund_role',                 label: 'Role on deal' },
  { key: 'related_portfolio_company', label: 'Portfolio Co' },
  { key: 'seniority',                 label: 'Seniority' },
  { key: 'location',                  label: 'Location' },
  { key: 'linkedin_url',              label: 'LinkedIn', isLink: true },
  { key: 'twitter_url',               label: 'Twitter',  isLink: true },
  { key: 'email_guess',               label: 'Email (guess)' },
]

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

function csvEscape(v) {
  if (v == null) return ''
  const s = String(v)
  if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`
  return s
}
function toCsv(rows, columns) {
  if (!rows.length) return ''
  const header = columns.map((c) => c.key).join(',')
  const body = rows.map((r) => columns.map((c) => csvEscape(r[c.key])).join(',')).join('\n')
  return header + '\n' + body
}
function download(filename, content, mime = 'text/csv') {
  const blob = new Blob([content], { type: mime })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob); a.download = filename; a.click()
  URL.revokeObjectURL(a.href)
}

function Cell({ row, col }) {
  const v = row[col.key]
  if (!v) return <td>—</td>
  if (col.isLink) return <td><a href={v} target="_blank" rel="noreferrer"><span className="ellip">{v.replace(/^https?:\/\//, '')}</span></a></td>
  if (typeof v === 'string' && v.length > 36) return <td><span className="ellip" title={v}>{v}</span></td>
  return <td>{v}</td>
}

function Table({ rows, columns }) {
  if (!rows.length) return <div className="empty">No rows yet — run a search.</div>
  return (
    <div className="table-wrap">
      <table>
        <thead><tr>{columns.map((c) => <th key={c.key}>{c.label}</th>)}</tr></thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>{columns.map((c) => <Cell key={c.key} row={r} col={c} />)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function ResultsPanel({ run }) {
  const [tab, setTab] = useState('funds')
  if (!run) return null
  const { mode, model, elapsed_ms, funds = [], people = [], by_company = {}, result } = run
  const isMock = mode === 'mock' || result?._mock
  const cites = result?.citations || []
  const companyCount = Object.keys(by_company).length

  return (
    <div className="card results">
      <h2>Results</h2>
      <div className={`run-banner ${isMock ? 'mock' : ''}`}>
        <div>
          <span className="badge">{isMock ? 'MOCK' : 'LIVE · ' + (model || 'sonar')}</span>{' '}
          {result?.notes || (isMock ? 'Mock response. Set PERPLEXITY_API_KEY for live.' : 'Search complete.')}
        </div>
        {elapsed_ms != null && <div>{(elapsed_ms / 1000).toFixed(1)}s</div>}
      </div>

      <div className="summary">
        <div className="stat"><b>{companyCount}</b>Companies</div>
        <div className="stat"><b>{funds.length}</b>Fund positions</div>
        <div className="stat"><b>{people.length}</b>People</div>
        <div className="stat"><b>{cites.length}</b>Citations</div>
      </div>

      <div className="tabs">
        <div className={`tab ${tab === 'funds'  ? 'active' : ''}`} onClick={() => setTab('funds')}>Funds <span className="count">{funds.length}</span></div>
        <div className={`tab ${tab === 'people' ? 'active' : ''}`} onClick={() => setTab('people')}>People <span className="count">{people.length}</span></div>
        <div className={`tab ${tab === 'cites'  ? 'active' : ''}`} onClick={() => setTab('cites')}>Citations <span className="count">{cites.length}</span></div>
      </div>

      {tab === 'funds'  && <Table rows={funds}  columns={FUND_COLUMNS} />}
      {tab === 'people' && <Table rows={people} columns={PEOPLE_COLUMNS} />}
      {tab === 'cites'  && (
        cites.length ? (
          <div className="citations">
            {cites.map((u, i) => <div key={i}>[{i + 1}] <a href={u} target="_blank" rel="noreferrer">{u}</a></div>)}
          </div>
        ) : <div className="empty">No citations.</div>
      )}

      {result?._parse_failed && (
        <>
          <h3 style={{ marginTop: 16, fontSize: 13, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: 0.06 }}>Raw model output</h3>
          <div className="preview">{result.raw}</div>
        </>
      )}

      <div className="actions">
        <button className="primary"   onClick={() => download('shareholders_funds.csv',  toCsv(funds,  FUND_COLUMNS))}   disabled={!funds.length}>Download funds.csv</button>
        <button className="primary"   onClick={() => download('shareholders_people.csv', toCsv(people, PEOPLE_COLUMNS))} disabled={!people.length}>Download people.csv (Folk/Apollo)</button>
        <button className="secondary" onClick={() => download('shareholders_raw.json',   JSON.stringify(run, null, 2), 'application/json')}>Download raw JSON</button>
        <button className="ghost"     onClick={() => navigator.clipboard.writeText(JSON.stringify(run, null, 2))}>Copy JSON</button>
      </div>
    </div>
  )
}

export default function App() {
  const [companies, setCompanies] = useState(['Figure AI'])
  const [maxFunds, setMaxFunds] = useState(10)
  const [maxPeople, setMaxPeople] = useState(2)
  const [includePrivate, setIncludePrivate] = useState(true)
  const [running, setRunning] = useState(false)
  const [run, setRun] = useState(null)
  const [toast, setToast] = useState(null)
  const [health, setHealth] = useState(null)

  useEffect(() => {
    fetch('/api/health').then((r) => r.json()).then(setHealth).catch(() => setHealth({ ok: false }))
  }, [])

  const payload = useMemo(() => ({
    companies,
    options: {
      max_funds_per_company: Number(maxFunds) || 10,
      max_people_per_fund:   Number(maxPeople) || 2,
      include_private:       includePrivate,
    },
  }), [companies, maxFunds, maxPeople, includePrivate])

  const flash = (msg, kind = 'ok') => { setToast({ msg, kind }); setTimeout(() => setToast(null), 2400) }

  const runSearch = async () => {
    if (!companies.length) { flash('Add at least one company', 'err'); return }
    setRunning(true); setRun(null)
    try {
      const r = await fetch('/api/find-shareholders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      const data = await r.json()
      if (!r.ok || data.error) { flash(`Search failed: ${data.error || r.status}`, 'err'); return }
      setRun(data)
      flash(data.mode === 'mock' ? 'Mock results — set PERPLEXITY_API_KEY for live' : 'Search complete')
      setTimeout(() => document.getElementById('results-anchor')?.scrollIntoView({ behavior: 'smooth' }), 100)
    } catch (e) { flash(`Network error: ${e.message}`, 'err') }
    finally { setRunning(false) }
  }

  return (
    <div className="app">
      <div className="header">
        <h1>Find Shareholders</h1>
        <p>Type one or more company names (e.g. <code>Figure AI</code>). Get the funds that own a stake plus the named people at those funds. Export CSVs shaped for Folk and Apollo enrichment.</p>
        {health && (
          <p style={{ marginTop: 8, fontSize: 12 }}>
            API: <span style={{ color: health.ok ? 'var(--success)' : 'var(--danger)' }}>{health.ok ? 'online' : 'offline'}</span>
            {' · '}Mode: <span style={{ color: health.has_api_key ? 'var(--success)' : 'var(--warn)' }}>{health.has_api_key ? `Sonar (${health.model})` : 'Mock (no API key)'}</span>
          </p>
        )}
      </div>

      <div className="card">
        <h2>Companies</h2>
        <p className="hint">Add companies by typing and pressing Enter (or comma). Both public and private companies supported.</p>
        <div className="field">
          <TagInput value={companies} onChange={setCompanies} placeholder="Figure AI, Anduril, Stripe…" />
        </div>
        <div className="field">
          <label style={{ marginBottom: 8 }}>Quick add</label>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {PRESETS.map((p) => (
              <button key={p} className="ghost" style={{ padding: '6px 12px', border: '1px solid var(--border)', borderRadius: 999, fontSize: 12 }}
                      onClick={() => { if (!companies.includes(p)) setCompanies([...companies, p]) }}>
                + {p}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="card">
        <h2>Search options</h2>
        <div className="row">
          <div className="field">
            <label>Max funds per company <span className="sub">{maxFunds}</span></label>
            <input type="number" min={1} max={25} value={maxFunds} onChange={(e) => setMaxFunds(e.target.value)} />
          </div>
          <div className="field">
            <label>People per fund <span className="sub">{maxPeople}</span></label>
            <input type="number" min={1} max={5} value={maxPeople} onChange={(e) => setMaxPeople(e.target.value)} />
          </div>
          <div className="field">
            <label>Include private rounds</label>
            <select value={includePrivate ? 'yes' : 'no'} onChange={(e) => setIncludePrivate(e.target.value === 'yes')}>
              <option value="yes">Yes — Crunchbase, press, Form D</option>
              <option value="no">No — public 13F only</option>
            </select>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>Run</h2>
        <p className="hint">Submits the companies list to the backend agent. Funds + people render below.</p>
        <div className="actions">
          <button className="primary" onClick={runSearch} disabled={running}>
            {running ? <><span className="spinner" />Searching…</> : '▶ Find Shareholders'}
          </button>
          <button className="ghost" onClick={() => navigator.clipboard.writeText(JSON.stringify(payload, null, 2))}>Copy intake JSON</button>
        </div>
        <details style={{ marginTop: 16 }}>
          <summary style={{ color: 'var(--muted)', cursor: 'pointer', fontSize: 13 }}>Show intake payload</summary>
          <div className="preview" style={{ marginTop: 10 }}>{JSON.stringify(payload, null, 2)}</div>
        </details>
      </div>

      <div id="results-anchor" />
      <ResultsPanel run={run} />

      <p className="footer-note">find-shareholders · part of Maximus AI · API at <code>/api/find-shareholders</code></p>

      {toast && <div className={`toast ${toast.kind === 'err' ? 'error' : ''}`}>{toast.msg}</div>}
    </div>
  )
}
