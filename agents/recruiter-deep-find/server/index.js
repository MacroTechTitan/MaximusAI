// Local dev / Replit entry — runs Express on PORT and serves the built client.
// On Vercel this file is NOT used; /api/index.js imports server/app.js directly.
import 'dotenv/config'
import express from 'express'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import fs from 'node:fs'
import app from './app.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const PORT = process.env.PORT || 3001

const clientDist = path.resolve(__dirname, '..', 'client', 'dist')
if (fs.existsSync(clientDist)) {
  app.use(express.static(clientDist))
  app.get('*', (_req, res) => res.sendFile(path.join(clientDist, 'index.html')))
}

app.listen(PORT, '0.0.0.0', () => {
  console.log(`[recruiter-deep-find] api on :${PORT}`)
  console.log(`[recruiter-deep-find] sonar key: ${process.env.PERPLEXITY_API_KEY ? 'present' : 'missing (mock mode)'}`)
})
