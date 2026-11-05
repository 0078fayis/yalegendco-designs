# YaLegendCo floating tees (3D scroll showcase)

Dark, scroll-driven page where the tees float on a curved rack and spin as you scroll. Plain CSS + JS, no libraries, no paid tools.

- `src/yl3d.css`, `src/yl3d.js`: the shared code. Edit these, then run `python3 build.py`.
- `index.html` + `assets/`: the standalone preview (works on Netlify or as an artifact).
- `shopify/yalegend-floating-tees.liquid`: the same thing as a Shopify section with tee blocks.

## Put it on Shopify (Basic plan is fine)
1. Online Store > Themes > Dawn > "..." > Duplicate (edit the copy, keep the live one safe).
2. On the copy: "..." > Edit code > Sections > Add a new section > name it `yalegend-floating-tees` > paste the .liquid file > Save.
3. Customize > Home page > Add section > "Floating tees (3D)". Add one Tee block per design: upload the transparent `_print.png` (or the .webp in `assets/`), name, joke line, pick the product.
4. Preview on your phone, then Publish the copy.
