import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // The app reads the pipeline's output straight from ../data/processed.
  server: { fs: { allow: ['..'] } },
})
