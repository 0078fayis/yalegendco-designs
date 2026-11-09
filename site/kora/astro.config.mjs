import { defineConfig } from 'astro/config';
export default defineConfig({
  site: 'https://kora-studioo.netlify.app',
  output: 'static',
  build: { inlineStylesheets: 'always' },
  devToolbar: { enabled: false }
});
