"""Build Paw Heat Check for Netlify: home page + one page per suburb + suburbs index + sitemap.

Usage: python3 build.py [site_url]   ->  writes dist/ and pawheatcheck.zip
"""
import csv, html, json, math, os, re, shutil, sys, zipfile
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = (sys.argv[1] if len(sys.argv) > 1 else "https://pawheatcheck.netlify.app").rstrip("/")
DIST = os.path.join(ROOT, "dist")
STATES = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load_suburbs():
    out = []
    with open(os.path.join(ROOT, "suburbs.csv")) as f:
        for r in csv.DictReader(f):
            name = r["name"]
            if name.endswith(" " + r["state"]):
                name = name[: -len(r["state"]) - 1]
            out.append({"name": name, "state": r["state"], "lat": float(r["lat"]), "lon": float(r["lon"]),
                        "slug": slugify(name + "-" + r["state"])})
    return out


def dist_km(a, b):
    dx = (a["lon"] - b["lon"]) * 111 * math.cos(math.radians(a["lat"]))
    dy = (a["lat"] - b["lat"]) * 111
    return math.hypot(dx, dy)


def links_block(title, items):
    li = "".join(f'<a href="/dog-walk/{s["slug"]}/">{html.escape(s["name"])}</a>' for s in items)
    return (f'<section class="card"><h2>{title}</h2>'
            f'<div class="sublinks">{li}</div>'
            f'<p><a href="/suburbs/">All suburbs and towns</a></p></section>')


EXTRA_CSS = (".sublinks{display:flex;flex-wrap:wrap;gap:8px}"
             ".sublinks a{color:var(--ink);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:6px 12px;font-size:14px;background:var(--bg)}"
             ".card a{color:var(--ink)}")


def page(base, sub, subs):
    s = base
    n, st = sub["name"], sub["state"]
    t = f"Is it too hot to walk my dog in {n}, {st}? Paw Heat Check"
    d = (f"Hour-by-hour footpath heat for dogs in {n}, {st}. See when the pavement is too hot for paws "
         f"and the safest walk times today and tomorrow.")
    s = s.replace("<title>Paw Heat Check – Is it too hot to walk my dog?</title>", f"<title>{html.escape(t)}</title>")
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(d)}">', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(t)}">', s)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(d)}">', s)
    s = s.replace('<meta property="og:type" content="website">',
                  f'<meta property="og:type" content="website">\n<link rel="canonical" href="{SITE}/dog-walk/{sub["slug"]}/">')
    s = s.replace("<h1>Is it too hot to <span>walk the dog?</span></h1>",
                  f"<h1>Too hot to walk the dog in <span>{html.escape(n)}?</span></h1>")
    s = s.replace("Type your suburb to see the footpath heat hour by hour and the safest times to walk.",
                  f"Here's the footpath heat in {html.escape(n)}, {st}, hour by hour, with the safest times to walk. "
                  f"Somewhere else? Type another suburb.")
    place = {"name": n, "label": f"{n}, {st}", "lat": sub["lat"], "lon": sub["lon"]}
    marker = "<script>\n(function(){"
    s = s.replace(marker, "<script>window.PHC_PLACE = " + json.dumps(place) + ";</script>\n" + marker, 1)
    near = sorted((x for x in subs if x is not sub), key=lambda x: dist_km(sub, x))[:10]
    s = s.replace("  <footer>", "  " + links_block(f"Near {html.escape(n)}", near) + "\n\n  <footer>", 1)
    return s


def suburbs_index(subs):
    groups = []
    for st in STATES:
        items = sorted((x for x in subs if x["state"] == st), key=lambda x: x["name"])
        if items:
            li = "".join(f'<a href="/dog-walk/{x["slug"]}/">{html.escape(x["name"])}</a>' for x in items)
            groups.append(f'<section class="card"><h2>{st}</h2><div class="sublinks">{li}</div></section>')
    return f"""<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dog walk heat by suburb · Paw Heat Check</title>
<meta name="description" content="Check if it's too hot to walk your dog in your suburb. Footpath heat forecasts for {len(subs)} Australian suburbs and towns.">
<link rel="canonical" href="{SITE}/suburbs/">
<style>
:root{{--bg:#fbf6ef;--card:#fff;--ink:#2a1d14;--muted:#7a6656;--line:#eadfd2;--accent:#f26a1b;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1a130e;--card:#251b14;--ink:#f6ebe0;--muted:#bba796;--line:#3a2c21;--accent:#ff8a45;color-scheme:dark}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Nunito Sans",system-ui,sans-serif;line-height:1.5}}
.wrap{{max-width:760px;margin:0 auto;padding:24px max(16px,env(safe-area-inset-left,0px));display:grid;gap:16px}}
h1{{font-family:Georgia,serif;margin:0}} h2{{margin:0 0 10px;font-size:18px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px}}
{EXTRA_CSS}
.back{{color:var(--accent);font-weight:800}}
</style></head><body><div class="wrap">
<a class="back" href="/">← Paw Heat Check</a>
<h1>Dog walk heat by suburb</h1>
<p>Pick your suburb or town to see when the footpath is too hot for paws.</p>
{''.join(groups)}
</div></body></html>"""


def main():
    subs = load_suburbs()
    base = open(os.path.join(ROOT, "index.html")).read()
    base = base.replace("</style>", EXTRA_CSS + "\n</style>", 1)
    shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(DIST)
    popular = [x for x in subs if x["name"] in ("Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Hobart",
                                                "Darwin", "Canberra", "Gold Coast", "Parramatta", "Geelong", "Newcastle")]
    home = base.replace('<meta property="og:type" content="website">',
                        f'<meta property="og:type" content="website">\n<link rel="canonical" href="{SITE}/">')
    home = home.replace("  <footer>", "  " + links_block("Popular places", popular) + "\n\n  <footer>", 1)
    open(os.path.join(DIST, "index.html"), "w").write(home)
    shutil.copy(os.path.join(ROOT, "thanks.html"), DIST)
    shutil.copytree(os.path.join(ROOT, "shop"), os.path.join(DIST, "shop"))
    urls = [f"{SITE}/", f"{SITE}/suburbs/"]
    for sub in subs:
        d = os.path.join(DIST, "dog-walk", sub["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(base, sub, subs))
        urls.append(f"{SITE}/dog-walk/{sub['slug']}/")
    os.makedirs(os.path.join(DIST, "suburbs"))
    open(os.path.join(DIST, "suburbs", "index.html"), "w").write(suburbs_index(subs))
    today = date.today().isoformat()
    sm = "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    open(os.path.join(DIST, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    zp = os.path.join(ROOT, "pawheatcheck.zip")
    if os.path.exists(zp):
        os.remove(zp)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, _, fs in os.walk(DIST):
            for f in fs:
                full = os.path.join(dp, f)
                z.write(full, os.path.relpath(full, DIST))
    print(f"{len(subs)} suburb pages, {len(urls)} URLs, zip {os.path.getsize(zp)//1024} KB")


if __name__ == "__main__":
    main()
