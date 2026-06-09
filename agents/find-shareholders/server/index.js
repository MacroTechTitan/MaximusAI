// Local dev / Replit / Node entry — runs Express on PORT and also serves the built client.
// On Vercel this file is NOT used; the serverless function in /api/index.js imports server/app.js directly.
import 'dotenv/config'
import express from 'express'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import fs from 'node:fs'
import app from './app.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const PORT = process.env.PORT || 3001

// Static client (built bundle) — only in local/Replit, not on Vercel
const clientDist = path.resolve(__dirname, '..', 'client', 'dist')
if (fs.existsSync(clientDist)) {
  app.use(express.static(clientDist))
  app.get('*', (_req, res) => res.sendFile(path.join(clientDist, 'index.html')))
}

app.listen(PORT, '0.0.0.0', () => {
  console.log(`[find-shareholders] api on :${PORT}`)
  console.log(`[find-shareholders] sonar key: ${process.env.PERPLEXITY_API_KEY ? 'present' : 'missing (mock mode)'}`)
})
