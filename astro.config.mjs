import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import node from '@astrojs/node'; // 👈 ¡ESTO ES LO QUE FALTA! Por eso decía "node is not defined"

// https://astro.build/config
export default defineConfig({
  integrations: [tailwind()],
  output: 'server', // Activa el Renderizado en el Servidor (SSR) para Supabase
  adapter: node({
    mode: 'standalone',
  }),
});