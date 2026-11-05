"""Builds the preview page (index.html) and the Shopify section from src/.
Run: python3 build.py"""
import json, pathlib
H = pathlib.Path(__file__).parent
css = (H/'src/yl3d.css').read_text(); js = (H/'src/yl3d.js').read_text()
ETSY = 'https://yalegendco.etsy.com'
TEES = [
  dict(name='Ho Ho Hooroo', tag='An Aussie Christmas farewell.', img='assets/ho-ho-hooroo.webp', tee='#16181d', colour='Black', accent='#e2453c'),
  dict(name='Drop Bear Christmas', tag="He's not here for the pressies.", img='assets/drop-bear-christmas.webp', tee='#16181d', colour='Black', accent='#f0663f'),
  dict(name='Bin Chicken Christmas Club', tag='Members only. Bins welcome.', img='assets/bin-chicken-christmas-club.webp', tee='#16181d', colour='Black', accent='#e9a83a'),
  dict(name='Professional Snag Flipper', tag='Qualified at every backyard barbie.', img='assets/professional-snag-flipper.webp', tee='#16181d', colour='Black', accent='#f2b544'),
  dict(name='Christmas in Thongs', tag='The dress code for a 35 degree December.', img='assets/christmas-in-thongs.webp', tee='#16181d', colour='Black', accent='#ef5b52'),
  dict(name="Santa's Sleigh Has Aircon", tag='Too hot for reindeer.', img='assets/santas-sleigh-has-aircon.webp', tee='#1a2238', colour='Navy', accent='#5fb2e6'),
  dict(name='Swooping Into Christmas', tag='Magpie season never takes a day off.', img='assets/swooping-into-christmas-magpie.webp', tee='#16181d', colour='Black', accent='#e2453c'),
  dict(name='Christmas Arvo Swim Club', tag="Pool's open straight after lunch.", img='assets/christmas-arvo-swim-club.webp', tee='#1a2238', colour='Navy', accent='#f2b544'),
]
for t in TEES: t['url'] = ETSY

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@800;900&family=Figtree:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap">'
MARQ = ''.join(f'<span>{w}</span>' for w in ['Aussie Christmas','Printed on demand','Free delivery in Australia','Sizes S to 3XL','Bin chickens welcome','Thongs optional'])

def body(data_json, first, n, eyebrow, h1a, h1b, btn, shop, range_on=True):
    rng = f'''
  <section class="yl-range yl-wrap" aria-labelledby="yl-range-h">
    <div class="yl-eyebrow">The summer Christmas range</div>
    <h2 id="yl-range-h">Pick your legend</h2>
    <p class="yl-lede">Soft Gildan cotton crewnecks in black and navy. Each tee is printed when you order it, so nothing sits in a warehouse.</p>
    <div class="yl-grid"></div>
  </section>
  <div class="yl-wrap"><div class="yl-facts">
    <div><strong>Made to order</strong><span>Printed after you buy, usually shipped within a few days.</span></div>
    <div><strong>Free AU delivery</strong><span>No delivery fee anywhere in Australia.</span></div>
    <div><strong>S to 3XL</strong><span>Unisex fit, with roomy 2XL and 3XL sizes.</span></div>
  </div></div>''' if range_on else ''
    return f'''<div class="yl">
  <script type="application/json" class="yl-data">{data_json}</script>
  <section class="yl-show" aria-label="Featured tees">
    <div class="yl-stage">
      <div class="yl-top yl-wrap"><a class="yl-brand" href="{shop}">Ya<b>Legend</b>Co</a><div class="yl-count" aria-hidden="true"><strong class="yl-cur">01</strong> / <span class="yl-tot">{n:02d}</span></div></div>
      <div class="yl-head"><div class="yl-eyebrow">{eyebrow}</div><h1>{h1a}<span>{h1b}</span></h1></div>
      <div class="yl-ring"><div class="yl-plinth"></div></div>
      <div class="yl-cap yl-wrap">
        <p class="yl-name" aria-live="polite">{first['name']}</p>
        <p class="yl-tag">{first['tag']}</p>
        <div class="yl-bar"><i></i></div>
        <a class="yl-btn yl-buy" href="{first['url']}">{btn} &rarr;</a>
        <span class="yl-hint">Scroll to spin the rack</span>
      </div>
    </div>
  </section>
  <div class="yl-strip" aria-hidden="true"><div>{MARQ}</div><div>{MARQ}</div></div>{rng}
  <section class="yl-end yl-wrap">
    <div class="yl-eyebrow">Christmas orders</div>
    <h2>Be the legend<br>at <em>Chrissy lunch</em></h2>
    <div class="yl-btns"><a class="yl-btn" href="{shop}">Shop all tees &rarr;</a></div>
  </section>
  <div class="yl-foot yl-wrap">YaLegendCo &middot; Aussie humour tees &middot; Printed on demand</div>
</div>'''

# ---------- preview page (artifact / any static host) ----------
page = f'''<title>YaLegendCo Floating Tees</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Aussie Christmas tees from YaLegendCo.">
{FONTS}
<style>:root{{color-scheme:dark;background:#0a0c11}} body{{background:#0a0c11;margin:0}}
{css}</style>
{body(json.dumps(TEES), TEES[0], len(TEES), 'Summer Christmas 2026', 'Aussie', 'Christmas', 'Shop this tee', ETSY)}
<script>{js}</script>
'''
(H/'index.html').write_text(page)

# ---------- Shopify section ----------
liquid = '''{%- comment -%} YaLegendCo floating tees. Add via Customize > Add section > "Floating tees (3D)". {%- endcomment -%}
''' + FONTS + '''
<style>''' + css + '''</style>
{%- capture yl_json -%}[{%- for block in section.blocks -%}{%- liquid
  assign link = block.settings.link
  if block.settings.product != blank
    assign link = block.settings.product.url
  endif
  if link == blank
    assign link = routes.all_products_collection_url
  endif
  assign img = ''
  if block.settings.print != blank
    assign img = block.settings.print | image_url: width: 700
  endif
-%}{"name":{{ block.settings.name | json }},"tag":{{ block.settings.tagline | json }},"img":{{ img | json }},"tee":{{ block.settings.tee_colour | json }},"colour":{{ block.settings.tee_label | json }},"accent":{{ block.settings.accent | json }},"url":{{ link | json }}}{%- unless forloop.last -%},{%- endunless -%}{%- endfor -%}]{%- endcapture -%}
{%- assign first = section.blocks.first -%}
'''
b = body('{{ yl_json }}', dict(name='{{ first.settings.name | escape }}', tag='{{ first.settings.tagline | escape }}', url='{{ first.settings.link | default: routes.all_products_collection_url }}'),
         0, '{{ section.settings.eyebrow | escape }}', '{{ section.settings.headline_1 | escape }}', '{{ section.settings.headline_2 | escape }}',
         '{{ section.settings.button | escape }}', '{{ routes.all_products_collection_url }}', range_on=True)
b = b.replace('<span class="yl-tot">00</span>', '<span class="yl-tot">{{ section.blocks.size }}</span>')
b = b.replace('<div class="yl-grid"></div>', '<div class="yl-grid"></div>').replace(
  '<section class="yl-range', '{%- if section.settings.show_range -%}<section class="yl-range').replace(
  '</div></div>\n  <section class="yl-end', '</div></div>{%- endif -%}\n  <section class="yl-end')
liquid += '{%- if section.blocks.size > 0 -%}\n' + b + '\n<script>' + js + '</script>\n{%- endif -%}\n'
liquid += '''
{% schema %}
{
  "name": "Floating tees (3D)",
  "tag": "section",
  "class": "yl-section",
  "settings": [
    {"type":"text","id":"eyebrow","label":"Small heading","default":"Summer Christmas 2026"},
    {"type":"text","id":"headline_1","label":"Big background word 1","default":"Aussie"},
    {"type":"text","id":"headline_2","label":"Big background word 2","default":"Christmas"},
    {"type":"text","id":"button","label":"Button text","default":"Shop this tee"},
    {"type":"checkbox","id":"show_range","label":"Show the tee grid and facts below","default":true}
  ],
  "blocks": [
    {
      "type": "tee",
      "name": "Tee",
      "settings": [
        {"type":"image_picker","id":"print","label":"Design (transparent PNG, the _print.png file)"},
        {"type":"text","id":"name","label":"Tee name","default":"Ho Ho Hooroo"},
        {"type":"text","id":"tagline","label":"One-line joke","default":"An Aussie Christmas farewell."},
        {"type":"product","id":"product","label":"Product to open"},
        {"type":"url","id":"link","label":"Or a link (used if no product)"},
        {"type":"color","id":"tee_colour","label":"Tee colour","default":"#16181d"},
        {"type":"text","id":"tee_label","label":"Tee colour name","default":"Black"},
        {"type":"color","id":"accent","label":"Glow colour","default":"#e2453c"}
      ]
    }
  ],
  "max_blocks": 10,
  "presets": [{"name":"Floating tees (3D)","blocks":[{"type":"tee"},{"type":"tee"},{"type":"tee"}]}]
}
{% endschema %}
'''
(H/'shopify').mkdir(exist_ok=True)
(H/'shopify/yalegend-floating-tees.liquid').write_text(liquid)
print('ok', len(page), len(liquid))
