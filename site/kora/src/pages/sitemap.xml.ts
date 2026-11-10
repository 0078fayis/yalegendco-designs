import type { APIRoute } from 'astro';
import { P } from '../data/products';
export const GET: APIRoute = ({ site }) => {
  const base = site!.toString().replace(/\/$/, '');
  const urls = ['/', '/shop/', '/looks/', '/story/', '/help/', ...P.map((p) => `/p/${p.id}/`)];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((u) => `  <url><loc>${base}${u}</loc></url>`).join('\n')}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
};
