// Vercel serverless entry — wraps the Express app
import app from '../server/app.js'

export default function handler(req, res) {
  return app(req, res)
}
