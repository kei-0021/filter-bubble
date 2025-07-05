// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: '/filter-bubble/', // ← GitHubリポジトリ名に必ず合わせる！
  plugins: [react()],
});
