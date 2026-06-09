import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In dev: client on 5173, api on 3001, /api proxied.
// In prod: server serves built client at /, api at /api.
export default defineConfig({
  plugins: [react()],
  base: './',
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
})
