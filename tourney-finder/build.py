"""Tourney Finder: static site of football, futsal and junior sports tournaments (NSW + QLD first).

Usage: python3 build.py [site_url]  ->  dist/ and tourneyfinder.zip
Data: events.json (agents update it weekly; organisers add events through the form on /add/).
"""
import html, json, os, re, shutil, sys, zipfile
from datetime import date, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = (sys.argv[1] if len(sys.argv) > 1 else "https://tourneyfinder.netlify.app").rstrip("/")
DIST = os.path.join(ROOT, "dist")
E = html.escape

CSS = """
:root{--bg:#f4f7f2;--card:#fff;--ink:#14261a;--muted:#5b6b5f;--line:#dbe4d8;--pitch:#1f7a43;--pitch-ink:#fff;--chalk:#eaf4ec;
--ok:#1f7a43;--ok-soft:#e1f2e6;--exp:#9a6a00;--exp-soft:#fff2d3;--tba:#5b6b5f;--tba-soft:#eceff0;
--display:"Barlow Condensed",system-ui,sans-serif;--body:"Barlow",system-ui,-apple-system,sans-serif;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#0e1611;--card:#16211a;--ink:#e9f2ea;--muted:#9fb2a4;--line:#26362b;--pitch:#3fbf72;--pitch-ink:#0e1611;--chalk:#1b2b20;
--ok:#5fd38f;--ok-soft:#173826;--exp:#ffc95a;--exp-soft:#3a2d0f;--tba:#a3b0a7;--tba-soft:#222c26;color-scheme:dark}}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.5}
a{color:var(--pitch)}
.top{background:var(--pitch);color:var(--pitch-ink)}
.top .in,.wrap{max-width:860px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.top .in{padding-block:14px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.logo{font-family:var(--display);font-weight:800;font-size:24px;letter-spacing:.02em;color:var(--pitch-ink);text-decoration:none;text-transform:uppercase}
.top a.btn{background:var(--pitch-ink);color:var(--pitch);text-decoration:none;font-weight:700;padding:8px 14px;border-radius:999px;font-size:14px}
.wrap{padding-block:22px 48px;display:grid;gap:20px}
h1,h2{font-family:var(--display);font-weight:800;margin:0;line-height:1.05;text-wrap:balance}
h1{font-size:clamp(34px,8vw,52px);text-transform:uppercase}
h2{font-size:24px}
p{margin:0}.muted{color:var(--muted)}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
select,input,textarea{font:inherit;padding:10px 12px;border-radius:10px;border:2px solid var(--line);background:var(--card);color:var(--ink);width:100%}
select:focus,input:focus,textarea:focus{outline:none;border-color:var(--pitch)}
label{font-size:13px;font-weight:700;color:var(--muted);display:grid;gap:4px}
.count{font-size:14px;color:var(--muted)}
.list{display:grid;gap:12px}
.ev{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;display:grid;grid-template-columns:72px 1fr;gap:14px;text-decoration:none;color:var(--ink)}
.ev:hover{border-color:var(--pitch)}
.date{background:var(--chalk);border-radius:12px;display:grid;place-items:center;text-align:center;padding:8px 4px;font-family:var(--display);font-weight:800;line-height:1}
.date .m{font-size:15px;text-transform:uppercase;color:var(--pitch)}
.date .d{font-size:28px}.date .y{font-size:13px;color:var(--muted);font-weight:600}
.ev h3{margin:0 0 4px;font-size:18px;line-height:1.25}
.meta{display:flex;flex-wrap:wrap;gap:6px 12px;font-size:14px;color:var(--muted)}
.pill{font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;white-space:nowrap}
.pill.confirmed{background:var(--ok-soft);color:var(--ok)}.pill.expected{background:var(--exp-soft);color:var(--exp)}.pill.tba{background:var(--tba-soft);color:var(--tba)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;display:grid;gap:12px}
.cta{background:var(--pitch);color:var(--pitch-ink);border-radius:16px;padding:18px;display:grid;gap:10px}
.cta a{color:var(--pitch-ink);font-weight:700}
button,.button{font:inherit;font-weight:700;border:0;border-radius:10px;padding:12px 16px;background:var(--pitch);color:var(--pitch-ink);cursor:pointer;text-decoration:none;display:inline-block;text-align:center}
.cta .button{background:var(--pitch-ink);color:var(--pitch)}
dl{display:grid;grid-template-columns:120px 1fr;gap:8px 12px;margin:0}dt{font-weight:700;color:var(--muted)}dd{margin:0;min-width:0}
form{display:grid;gap:12px}.hidden{display:none!important}
footer{font-size:13px;color:var(--muted);display:grid;gap:6px}
:focus-visible{outline:3px solid var(--pitch);outline-offset:2px}
@media (max-width:420px){.ev{grid-template-columns:60px 1fr}dl{grid-template-columns:1fr}}
"""

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
STATUS = {"confirmed": "Dates confirmed", "expected": "Expected (based on last year)", "tba": "Dates to be announced"}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70]


def head(title, desc, path):
    return f"""<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website">
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#1f7a43">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='28' fill='%231f7a43'/%3E%3Cpolygon points='32,18 44,27 39,41 25,41 20,27' fill='white'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@800&family=Barlow:wght@400;600;700&display=swap">
<style>{CSS}</style></head><body>
<div class="top"><div class="in"><a class="logo" href="/">⚽ Tourney Finder</a><a class="btn" href="/add/">+ Add your tournament</a></div></div>
<div class="wrap">"""


FOOT = """<footer><p>Tourney Finder lists football, futsal and junior sports tournaments in Australia, starting with NSW and Queensland. Dates come from organisers' own websites. Always confirm with the organiser before you book travel.</p>
<p>Spotted a mistake or a missing tournament? <a href="/add/">Tell us</a>. Made in Australia by YaLegendCo.</p></footer>
</div></body></html>"""


def date_box(ev):
    if ev["start"]:
        d = datetime.strptime(ev["start"], "%Y-%m-%d")
        return f'<div class="date"><span class="m">{MONTHS[d.month-1]}</span><span class="d">{d.day}</span><span class="y">{d.year}</span></div>'
    if ev["month"]:
        y, m = ev["month"].split("-")
        return f'<div class="date"><span class="m">{MONTHS[int(m)-1]}</span><span class="d">~</span><span class="y">{y}</span></div>'
    return '<div class="date"><span class="m">TBA</span><span class="d">?</span><span class="y">&nbsp;</span></div>'


def when(ev):
    if ev["start"]:
        a = datetime.strptime(ev["start"], "%Y-%m-%d")
        b = datetime.strptime(ev["end"] or ev["start"], "%Y-%m-%d")
        if a == b:
            return f"{a.day} {MONTHS[a.month-1]} {a.year}"
        if a.month == b.month:
            return f"{a.day}–{b.day} {MONTHS[a.month-1]} {a.year}"
        return f"{a.day} {MONTHS[a.month-1]} – {b.day} {MONTHS[b.month-1]} {b.year}"
    if ev["month"]:
        y, m = ev["month"].split("-")
        return f"Expected {MONTHS[int(m)-1]} {y}" if ev["status"] == "expected" else f"Usually {MONTHS[int(m)-1]} · dates TBA"
    return "Dates to be announced"


def sort_key(ev):
    return (ev["start"] or (ev["month"] + "-15" if ev["month"] else "9999"), ev["name"])


def ics(ev):
    a = ev["start"].replace("-", "")
    b = datetime.strptime(ev["end"] or ev["start"], "%Y-%m-%d").date()
    b = date.fromordinal(b.toordinal() + 1).strftime("%Y%m%d")
    uid = slugify(ev["name"]) + "@tourneyfinder"
    return ("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Tourney Finder//EN\r\nBEGIN:VEVENT\r\n"
            f"UID:{uid}\r\nDTSTAMP:{date.today().strftime('%Y%m%d')}T000000Z\r\nDTSTART;VALUE=DATE:{a}\r\nDTEND;VALUE=DATE:{b}\r\n"
            f"SUMMARY:{ev['name']}\r\nLOCATION:{ev['place']}, {ev['state']}\r\nURL:{ev['src']}\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")


def card(ev):
    return (f'<a class="ev" href="/t/{ev["slug"]}/" data-sport="{E(ev["sport"])}" data-state="{ev["state"]}" data-month="{ev["month"]}">'
            f'{date_box(ev)}<div><h3>{E(ev["name"])}</h3><div class="meta"><span>{E(ev["place"])}, {ev["state"]}</span>'
            f'<span>{E(ev["sport"])}</span><span>{E(ev["ages"])}</span><span class="pill {ev["status"]}">{STATUS[ev["status"]]}</span></div></div></a>')


def index(evs):
    sports = sorted({e["sport"] for e in evs})
    states = sorted({e["state"] for e in evs})
    months = sorted({e["month"] for e in evs if e["month"]})
    opt = lambda vals, lab=lambda v: v: "".join(f'<option value="{E(v)}">{E(lab(v))}</option>' for v in vals)
    mlab = lambda v: f"{MONTHS[int(v[5:])-1]} {v[:4]}"
    s = head("Tourney Finder: football, futsal and junior sports tournaments in NSW and QLD",
             "Find football, futsal, touch and Oztag tournaments and carnivals in NSW and Queensland. Dates, age groups and official links in one place.", "/")
    s += f"""<header style="display:grid;gap:10px"><h1>Find your next tournament</h1>
<p class="muted">Football, futsal and junior sports tournaments in NSW and Queensland, in one place. Every listing links to the organiser's own page.</p></header>
<div class="filters">
<label for="fSport">Sport<select id="fSport"><option value="">All sports</option>{opt(sports)}</select></label>
<label for="fState">State<select id="fState"><option value="">All states</option>{opt(states)}</select></label>
<label for="fMonth">Month<select id="fMonth"><option value="">Any month</option>{opt(months, mlab)}</select></label>
</div>
<div class="count" id="count" role="status">{len(evs)} tournaments</div>
<div class="list" id="list">{''.join(card(e) for e in evs)}</div>
<div class="cta"><h2>Running a tournament?</h2><p>List it free. Coaches and parents across NSW and Queensland use Tourney Finder to plan their season.</p><a class="button" href="/add/">Add your tournament</a></div>
<div class="card"><h2>Get new tournaments by email</h2><p class="muted">One short email a month with new tournaments for your sport and state. Free, unsubscribe any time.</p>
<form name="tourney-alerts" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="tourney-alerts"><p class="hidden"><label>Leave empty <input name="bot-field"></label></p>
<input id="aEmail" type="email" name="email" placeholder="Your email" required aria-label="Email">
<input id="aWhat" type="text" name="interest" placeholder="Sport, age group and area, e.g. U12 football, Brisbane" aria-label="What you're looking for">
<button type="submit">Send me new tournaments</button></form></div>
<script>
(function(){{var s=document.getElementById('fSport'),t=document.getElementById('fState'),m=document.getElementById('fMonth'),c=document.getElementById('count');
var items=[].slice.call(document.querySelectorAll('#list .ev'));
function run(){{var n=0;items.forEach(function(e){{var ok=(!s.value||e.dataset.sport===s.value)&&(!t.value||e.dataset.state===t.value)&&(!m.value||e.dataset.month===m.value);e.classList.toggle('hidden',!ok);if(ok)n++;}});
c.textContent=n+(n===1?' tournament':' tournaments')+(n===0?'. Try another filter, or add one you know about.':'');}}
[s,t,m].forEach(function(x){{x.addEventListener('change',run);}});}})();
</script>"""
    return s + FOOT


def page(ev):
    st = ev["state"]
    yr = "2027" if "2027" in (ev["start"] or ev["month"]) and "2027" not in ev["name"] else ""
    title = f"{ev['name']} {yr}".strip() + f" · {ev['place']}, {st} · Tourney Finder"
    desc = f"{ev['name']} in {ev['place']}, {st}: {when(ev)}. {ev['ages']}. {ev['about']}"[:300]
    s = head(title, desc, f"/t/{ev['slug']}/")
    cal = f'<a class="button" href="/t/{ev["slug"]}/event.ics">Add to calendar</a>' if ev["start"] else ""
    s += f"""<p><a href="/">← All tournaments</a></p>
<header style="display:grid;gap:10px"><h1 style="font-size:clamp(28px,6vw,40px)">{E(ev['name'])}</h1>
<div class="meta"><span class="pill {ev['status']}">{STATUS[ev['status']]}</span></div></header>
<div class="card"><dl>
<dt>When</dt><dd>{E(when(ev))}</dd><dt>Where</dt><dd>{E(ev['place'])}, {st}</dd>
<dt>Sport</dt><dd>{E(ev['sport'])}</dd><dt>Ages</dt><dd>{E(ev['ages'])}</dd><dt>Who can enter</dt><dd>{E(ev['who'])}</dd>
<dt>About</dt><dd>{E(ev['about'])}</dd>
<dt>Official info</dt><dd><a href="{E(ev['src'])}" rel="noopener" target="_blank">{E(ev['src_name'])}</a></dd></dl>
<div style="display:flex;gap:10px;flex-wrap:wrap">{cal}<a class="button" href="{E(ev['src'])}" rel="noopener" target="_blank" style="background:var(--chalk);color:var(--ink)">Organiser's page</a></div></div>
<div class="cta"><h2>Is this your tournament?</h2><p>Send us the latest dates, entry link and fees, and we'll update this page for free.</p><a class="button" href="/add/">Update this listing</a></div>"""
    return s + FOOT


def add_page():
    s = head("Add your tournament · Tourney Finder", "List your football, futsal or junior sports tournament free on Tourney Finder.", "/add/")
    s += """<p><a href="/">← All tournaments</a></p><h1>Add your tournament</h1>
<p class="muted">Free listing for clubs, associations and organisers. We check every entry and usually publish within a few days.</p>
<div class="card"><form name="add-tournament" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="add-tournament"><p class="hidden"><label>Leave empty <input name="bot-field"></label></p>
<label for="tName">Tournament name<input id="tName" name="name" required></label>
<label for="tSport">Sport<select id="tSport" name="sport"><option>Football</option><option>Futsal</option><option>Touch</option><option>Oztag</option><option>Cricket</option><option>Basketball</option><option>Netball</option><option>Other</option></select></label>
<label for="tDates">Dates<input id="tDates" name="dates" placeholder="e.g. 10-12 January 2027" required></label>
<label for="tPlace">Suburb or town, and state<input id="tPlace" name="place" placeholder="e.g. Penrith, NSW" required></label>
<label for="tAges">Age groups and divisions<input id="tAges" name="ages" placeholder="e.g. U9-U16 boys and girls"></label>
<label for="tFee">Entry fee (optional)<input id="tFee" name="fee" placeholder="e.g. A$450 per team"></label>
<label for="tLink">Website or entry link<input id="tLink" name="link" type="url" placeholder="https://"></label>
<label for="tEmail">Your email (not shown on the site)<input id="tEmail" name="email" type="email" required></label>
<label for="tNotes">Anything else<textarea id="tNotes" name="notes" rows="3"></textarea></label>
<button type="submit">Submit tournament</button></form></div>"""
    return s + FOOT


def thanks():
    s = head("Thanks · Tourney Finder", "Thanks for your submission.", "/thanks/")
    s += '<h1>Thanks!</h1><p>We\'ve got it. New tournaments are usually live within a few days.</p><p><a class="button" href="/">Back to all tournaments</a></p>'
    return s + FOOT


def main():
    evs = json.load(open(os.path.join(ROOT, "events.json")))
    for e in evs:
        e["slug"] = slugify(e["name"] + "-" + e["state"])
    evs.sort(key=sort_key)
    shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(DIST)
    w = lambda p, t: (os.makedirs(os.path.dirname(os.path.join(DIST, p)), exist_ok=True), open(os.path.join(DIST, p), "w").write(t))
    w("index.html", index(evs))
    w("add/index.html", add_page())
    w("thanks/index.html", thanks())
    urls = [f"{SITE}/", f"{SITE}/add/"]
    for e in evs:
        w(f"t/{e['slug']}/index.html", page(e))
        if e["start"]:
            w(f"t/{e['slug']}/event.ics", ics(e))
        urls.append(f"{SITE}/t/{e['slug']}/")
    today = date.today().isoformat()
    w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
      + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>")
    w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    w("_headers", "/*.ics\n  Content-Type: text/calendar; charset=utf-8\n")
    zp = os.path.join(ROOT, "tourneyfinder.zip")
    if os.path.exists(zp):
        os.remove(zp)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, _, fs in os.walk(DIST):
            for f in fs:
                z.write(os.path.join(dp, f), os.path.relpath(os.path.join(dp, f), DIST))
    print(f"{len(evs)} tournaments, {len(urls)} URLs, zip {os.path.getsize(zp)//1024} KB")


if __name__ == "__main__":
    main()
