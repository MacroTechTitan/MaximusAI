// Vercel serverless entry — wraps the Express app
// All routes in server/index.js mount at /api/* and are served from this function.
import app from '../server/app.js'

export default function handler(req, res) {
  return app(req, res)
}
