# Recruiter Deep-Find — Standalone App

A complete, self-contained recruiter intake + live deep-search tool. Find candidates at **DevOps agencies, software dev shops, programming-for-hire firms, IT outsourcing companies, MSPs, and technical staffing agencies** using the Perplexity Sonar API.

Ships ready to drop into Replit, Vercel, Render, Railway, or any Node host.

## What's in here

```
recruiter-deep-find-app/
├── package.json          monorepo orchestrator (concurrently runs both)
├── .replit               Replit run/build config
├── replit.nix            Replit Node 20 toolchain
├── .env.example          environment template
├── client/               React + Vite frontend (the form + results UI)
│   ├── package.json
│   ├── vite.config.js    proxies /api → :3001 in dev
│   ├── index.html
│   └── src/
│       ├── App.jsx       form, Run Deep Search button, ResultsPanel
│       ├── main.jsx
│       └── styles.css
└── server/               Express backend
    ├── package.json
    └── index.js          /api/health + /api/run-search (Sonar + mock fallback)
```

## Run locally

```bash
npm run install:all      # installs root, client, server
cp .env.example .env     # edit and add PERPLEXITY_API_KEY (optional)
npm run dev              # client on :5173, api on :3001
```

Open http://localhost:5173 — the form proxies `/api/*` to the Express server.

If you skip the API key, the backend returns a **mock response** so the UI is fully testable.

## Run in production (single process)

```bash
npm run install:all
npm run build            # builds client → client/dist
npm start                # Express serves API + built client on :3001
```

## Deploy to Replit

1. **Import this folder as a Replit project** (or git push and import).
2. **Add secret:** `PERPLEXITY_API_KEY` = your key from https://www.perplexity.ai/settings/api.
3. Click **Run** — Replit reads `.replit`, installs deps, builds the client, starts the Express server. The form is served at the public Replit URL.
4. For Replit Deployments: target is preconfigured as `cloudrun` in `.replit`.

## Deploy elsewhere

- **Vercel:** point at root; build = `npm run install:all && npm run build`; output = `client/dist`; serverless function for `server/index.js`.
- **Render / Railway:** Web Service, build = `npm run install:all && npm run build`, start = `npm start`, port = `$PORT`.
- **Docker:** Node 20 base, copy repo, `npm run install:all && npm run build`, `CMD ["npm","start"]`.

## API

### `GET /api/health`
```json
{ "ok": true, "has_api_key": true, "model": "sonar-pro", "ts": "..." }
```

### `POST /api/run-search`
**Body:** the intake JSON from the form.
**Response (live):**
```json
{
  "ok": true, "mode": "sonar", "model": "sonar-pro", "elapsed_ms": 4821,
  "result": {
    "brief_recap": "...",
    "agencies": [{ "name": "...", "hq": "...", "size": "...", "services": "...", "url": "..." }],
    "candidates": [{ "rank": 1, "name": "...", "current_agency": "...", "title": "...",
                     "location": "...", "key_skills": ["..."], "movement_signal": "...",
                     "non_solicit_risk": "low|moderate|high", "why_fit": "...",
                     "linkedin_url": "...", "github_url": "...", "other_sources": ["..."] }],
    "sourcing_notes": "...", "citations": ["..."]
  },
  "raw_citations": ["..."]
}
```
**Response (mock, no key):** same shape, `mode: "mock"`, `_mock: true` flag inside `result`.

## Notes

- The system prompt enforces strict-JSON output and bakes in the recruiter-deep-find workflow (agencies first, then people; non-solicit risk flagging; movement signals; public-only contact info).
- The Express server has zero external deps beyond `express`, `cors`, `dotenv` — easy audit.
- The CSV download in the UI matches the schema in the `recruiter-deep-find` agent skill.

## License
MIT
