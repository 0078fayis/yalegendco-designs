"""Tourney Finder: static site of football, futsal and junior sports tournaments (NSW + QLD first).

Usage: python3 build.py [site_url]  ->  dist/ and tourneyfinder.zip
Data: events.json (agents update it weekly; organisers add events through the form on /add/).
"""
import html, json, os, re, shutil, sys, zipfile
from datetime import date, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = (sys.argv[1] if len(sys.argv) > 1 else "https://tourney-finder.netlify.app").rstrip("/")
DIST = os.path.join(ROOT, "dist")
E = html.escape

CSS = """
/* Broadcast-grade tournament look: midnight navy, gold hairlines, expanded caps, fixture rows grouped by month. One deliberate dark theme. */
:root{--bg:#070b1f;--bg2:#0c1330;--panel:#101a3d;--panel2:#152150;--ink:#f3efe4;--muted:#a9b0cc;--faint:#6d76a0;--line:rgba(201,165,76,.22);--hair:rgba(243,239,228,.09);
--gold:#c9a54c;--gold2:#e6c97a;--goldink:#1a1404;
--ok:#7fd6a4;--exp:#e6c97a;--tba:#a9b0cc;
--football:#2e9e6a;--futsal:#d98b3a;--cricket:#d8cfa8;--basketball:#c8693a;--afl:#c9a54c;--badminton:#9d8ce0;--touch:#5aa9d6;--oztag:#d46a8f;
--display:"Archivo",system-ui,sans-serif;--body:"Hanken Grotesk",system-ui,-apple-system,sans-serif;color-scheme:dark}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:var(--gold2)}
.eyebrow{font-family:var(--display);font-stretch:125%;font-weight:700;font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold)}
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(7,11,31,.86);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.in{max-width:1000px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}
.top .in{padding-block:12px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink)}
.brand svg{width:38px;height:38px;flex:none}
.brand b{font-family:var(--display);font-stretch:125%;font-weight:800;font-size:17px;letter-spacing:.16em;text-transform:uppercase;line-height:1}
.brand small{display:block;font-size:10px;letter-spacing:.3em;color:var(--gold);text-transform:uppercase;margin-top:4px}
.btn-gold{font-family:var(--display);font-stretch:112%;font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:var(--gold2);border:1px solid var(--gold);padding:9px 16px;border-radius:2px;transition:background .2s,color .2s}
.btn-gold:hover{background:var(--gold);color:var(--goldink)}
.hero{position:relative;overflow:hidden;border-bottom:1px solid var(--line);background:
 radial-gradient(ellipse 70% 90% at 80% 0%,rgba(201,165,76,.18),transparent 60%),
 radial-gradient(ellipse 60% 80% at 0% 100%,rgba(46,80,200,.25),transparent 60%),
 linear-gradient(180deg,var(--bg2),var(--bg))}
.hero::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(115deg,rgba(243,239,228,.035) 0 1px,transparent 1px 28px);pointer-events:none}
.hero .in{position:relative;padding-block:64px 56px;display:grid;gap:20px}
h1,h2,h3{font-family:var(--display);margin:0;text-wrap:balance}
h1{font-stretch:125%;font-weight:800;font-size:clamp(38px,8.5vw,78px);line-height:.98;letter-spacing:-.01em;text-transform:uppercase}
h1 em{font-style:normal;color:var(--gold2)}
.lede{max-width:600px;color:var(--muted);font-size:18px}
.next{justify-self:start;max-width:100%;display:grid;gap:12px;padding:18px 20px;border:1px solid var(--line);background:linear-gradient(180deg,rgba(16,26,61,.85),rgba(12,19,48,.85));border-radius:4px}
.next a{color:var(--ink);text-decoration:none;font-weight:600;font-size:16px}
.next a:hover{color:var(--gold2)}
.digits{display:flex;gap:0;align-items:stretch}
.digits div{display:grid;justify-items:center;padding:0 18px;border-left:1px solid var(--hair)}
.digits div:first-child{border-left:0;padding-left:0}
.digits b{font-family:var(--display);font-stretch:100%;font-weight:300;font-size:46px;line-height:1;color:var(--ink);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.digits small{font-family:var(--display);font-stretch:125%;font-size:10px;letter-spacing:.24em;color:var(--gold);text-transform:uppercase;margin-top:6px}
main.in{padding-block:44px 64px;display:grid;gap:28px}
.sechead{display:flex;align-items:end;justify-content:space-between;gap:16px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:12px}
h2{font-stretch:125%;font-weight:800;font-size:clamp(24px,4vw,32px);text-transform:uppercase;letter-spacing:.02em}
.count{font-size:14px;color:var(--muted)}
.months{display:flex;overflow-x:auto;border-bottom:1px solid var(--hair);scrollbar-width:none}
.months::-webkit-scrollbar{display:none}
.mo{flex:1 0 64px;font:inherit;background:none;border:0;border-bottom:2px solid transparent;color:var(--ink);padding:10px 4px 12px;cursor:pointer;display:grid;justify-items:center;gap:2px;transition:border-color .2s,color .2s}
.mo b{font-family:var(--display);font-stretch:125%;font-weight:700;font-size:14px;letter-spacing:.14em}
.mo small{font-size:11px;color:var(--faint)}
.mo .n{font-family:var(--display);font-weight:300;font-size:22px;line-height:1.1;color:var(--gold2)}
.mo:hover{border-bottom-color:var(--hair)}
.mo[aria-pressed="true"]{border-bottom-color:var(--gold)}
.mo:disabled{opacity:.3;cursor:default}
.filters{display:flex;flex-wrap:wrap;gap:10px 22px;align-items:center}
.seg{display:flex;flex-wrap:wrap;gap:6px}
.seg-l{font-family:var(--display);font-stretch:125%;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--faint);margin-right:4px;align-self:center}
.chip{font:inherit;font-size:14px;font-weight:600;background:transparent;color:var(--muted);border:1px solid var(--hair);border-radius:999px;padding:6px 13px;cursor:pointer;display:flex;gap:7px;align-items:center;transition:all .2s}
.chip:hover{color:var(--ink);border-color:var(--line)}
.chip[aria-pressed="true"]{color:var(--goldink);background:var(--gold2);border-color:var(--gold2)}
.chip .dot{width:8px;height:8px;border-radius:50%;background:var(--c,var(--gold))}
.list{display:grid}
.mhead{font-family:var(--display);font-stretch:125%;font-weight:700;font-size:13px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);padding:26px 0 10px;border-bottom:1px solid var(--line)}
.ev{display:grid;grid-template-columns:76px 46px 1fr auto;gap:18px;align-items:center;padding:18px 6px;border-bottom:1px solid var(--hair);text-decoration:none;color:var(--ink);position:relative;transition:background .2s}
.ev::before{content:"";position:absolute;left:0;top:18px;bottom:18px;width:2px;background:var(--gold);transform:scaleY(0);transition:transform .25s}
.ev:hover{background:linear-gradient(90deg,rgba(201,165,76,.07),transparent 70%)}
.ev:hover::before{transform:scaleY(1)}
.date{display:grid;justify-items:center;line-height:1;font-family:var(--display)}
.date .d{font-weight:300;font-size:38px;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.date .m{font-stretch:125%;font-weight:700;font-size:11px;letter-spacing:.22em;color:var(--gold);margin-top:6px;text-transform:uppercase}
.date .tbc{font-weight:300;font-size:22px;color:var(--muted)}
.crest{width:46px;height:46px}
.crest circle.o{fill:none;stroke:var(--c,var(--gold));stroke-width:1.5}
.crest circle.i{fill:color-mix(in srgb,var(--c,var(--gold)) 16%,transparent)}
.crest text{font-family:var(--display);font-stretch:125%;font-weight:800;font-size:13px;letter-spacing:.06em;fill:var(--ink)}
.ev .body{min-width:0;display:grid;gap:4px}
.ev h3{font-family:var(--body);font-weight:700;font-size:18px;line-height:1.3}
.meta{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:14px;color:var(--muted)}
.meta .sp{color:var(--c,var(--gold));font-weight:700;letter-spacing:.04em}
.st{display:flex;align-items:center;gap:14px;font-size:12px;font-family:var(--display);font-stretch:112%;font-weight:600;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap}
.st .confirmed{color:var(--ok)}.st .expected{color:var(--exp)}.st .tba{color:var(--tba)}
.st i{font-style:normal;color:var(--faint);font-size:18px;transition:transform .2s,color .2s}
.ev:hover .st i{transform:translateX(4px);color:var(--gold2)}
.s-football{--c:var(--football)}.s-futsal{--c:var(--futsal)}.s-cricket{--c:var(--cricket)}.s-basketball{--c:var(--basketball)}.s-afl{--c:var(--afl)}.s-badminton{--c:var(--badminton)}.s-touch{--c:var(--touch)}.s-oztag{--c:var(--oztag)}
.panel{background:linear-gradient(180deg,var(--panel),var(--bg2));border:1px solid var(--line);border-radius:4px;padding:26px;display:grid;gap:14px}
.shop{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px}
.prod{display:grid;gap:8px;background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:10px;text-decoration:none;color:var(--ink);transition:border-color .2s,transform .2s}
.prod:hover{border-color:var(--gold);transform:translateY(-2px)}
.prod img{width:100%;height:auto;aspect-ratio:5/6;object-fit:cover;border-radius:2px;background:#141414}
.prod b{font-family:var(--display);font-stretch:112%;font-size:14px;letter-spacing:.04em;text-transform:uppercase;line-height:1.25}
.prod span{color:var(--gold2);font-weight:700;font-size:14px}
.navlink{font-family:var(--display);font-stretch:112%;font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:var(--ink);margin-right:18px}
.navlink:hover{color:var(--gold2)}
.hdr-r{display:flex;align-items:center}
.split{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.muted{color:var(--muted)}p{margin:0}
button,.button{font-family:var(--display);font-stretch:112%;font-weight:700;font-size:14px;letter-spacing:.14em;text-transform:uppercase;border:1px solid var(--gold2);border-radius:2px;padding:13px 20px;background:var(--gold2);color:var(--goldink);cursor:pointer;text-decoration:none;display:inline-block;text-align:center;transition:background .2s,color .2s}
button:hover,.button:hover{background:transparent;color:var(--gold2)}
.button.ghost{background:transparent;color:var(--gold2)}
.button.ghost:hover{background:var(--gold2);color:var(--goldink)}
input,select,textarea{font:inherit;padding:12px 14px;border-radius:2px;border:1px solid var(--hair);background:rgba(7,11,31,.6);color:var(--ink);width:100%}
input::placeholder,textarea::placeholder{color:var(--faint)}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--gold)}
label{font-family:var(--display);font-stretch:112%;font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);display:grid;gap:6px}
form{display:grid;gap:14px}.hidden{display:none!important}
.back{font-family:var(--display);font-stretch:125%;font-size:12px;letter-spacing:.22em;text-transform:uppercase;text-decoration:none;color:var(--gold)}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));border-top:1px solid var(--line)}
.facts div{padding:16px 0;border-bottom:1px solid var(--hair);display:grid;gap:4px;padding-right:16px}
.facts dt{font-family:var(--display);font-stretch:125%;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold)}
.facts dd{margin:0;font-size:17px;min-width:0}
.facts dl{display:contents}
footer{border-top:1px solid var(--line);margin-top:8px}
footer .in{padding-block:28px 40px;display:grid;gap:8px;font-size:13px;color:var(--faint)}
:focus-visible{outline:2px solid var(--gold2);outline-offset:3px}
@media (max-width:640px){.ev{grid-template-columns:58px 1fr;gap:6px 14px}.ev .crest{display:none}.top .in{flex-wrap:nowrap}.brand b{font-size:14px;letter-spacing:.12em}.brand small{letter-spacing:.2em}.navlink{font-size:11px;margin-right:10px;letter-spacing:.08em}.btn-gold{font-size:11px;padding:8px 10px;letter-spacing:.08em;white-space:nowrap}.st{grid-column:2}.date .d{font-size:32px}.digits b{font-size:36px}.digits div{padding:0 12px}.hero .in{padding-block:44px 40px}}
@media (max-width:420px){.wide{display:none}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
STATUS = {"confirmed": "Dates confirmed", "expected": "Expected (based on last year)", "tba": "Dates to be announced"}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70]


GA_ID = os.environ.get("GA_ID", "G-MR8R1Y96GP")


def ga():
    if not GA_ID:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>\n")


def head(title, desc, path):
    return f"""<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website">
<link rel="canonical" href="{SITE}{path}">
{ga()}<meta name="theme-color" content="#070b1f">
<meta name="google-site-verification" content="Gwq6BwauJ3oWrqJBQLNV-pmNyu8_st0YB2Ha4SraKXQ" />
<meta name="google-site-verification" content="moVUIrIGxKMaJrlwkLTXLseoJm8-S9sDBxLsyKo_2r4" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' fill='%23070b1f'/%3E%3Cpath d='M20 4 34 9v11c0 8-6 13-14 16C12 33 6 28 6 20V9Z' fill='none' stroke='%23c9a54c' stroke-width='2'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,300..800&family=Hanken+Grotesk:wght@400;600;700&display=swap">
<style>{CSS}</style></head><body>
<header class="top"><div class="in"><a class="brand" href="/"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 2 36 8v12c0 9-7 15-16 18C11 35 4 29 4 20V8Z" fill="none" stroke="#c9a54c" stroke-width="1.5"/><path d="M20 6 32 10.5V20c0 7-5.4 11.8-12 14.2C13.4 31.8 8 27 8 20v-9.5Z" fill="#c9a54c" fill-opacity=".12"/><text x="20" y="24.5" text-anchor="middle" font-family="Archivo,sans-serif" font-weight="800" font-size="11" letter-spacing="1" fill="#e6c97a">TF</text></svg><span><b>Tourney Finder</b><small>NSW · QLD · Season 26/27</small></span></a><span class="hdr-r"><a class="navlink" href="/shop/">Shop</a><a class="btn-gold" href="/add/">List<span class="wide"> a tournament</span></a></span></div></header>
<!--HERO-->
<main class="in">"""


FOOT = """</main><footer><div class="in"><p>Tourney Finder lists football, futsal, cricket, basketball, AFL, badminton, touch and Oztag tournaments in Australia, starting with NSW and Queensland. Dates come from organisers' own websites. Always confirm with the organiser before you book travel.</p>
<p>Spotted a mistake or a missing tournament? <a href="/add/">Tell us</a>. © 2026 Tourney Finder · Made in Australia by YaLegendCo.</p></div></footer>
</body></html>"""


def date_box(ev):
    if ev["start"]:
        d = datetime.strptime(ev["start"], "%Y-%m-%d")
        return f'<div class="date"><span class="d">{d.day:02d}</span><span class="m">{MONTHS[d.month-1]}</span></div>'
    if ev["month"]:
        y, m = ev["month"].split("-")
        return f'<div class="date"><span class="tbc">TBC</span><span class="m">{MONTHS[int(m)-1]}</span></div>'
    return '<div class="date"><span class="tbc">TBA</span><span class="m">2027</span></div>'


ABBR = {"Football": "FB", "Futsal": "FS", "Cricket": "CR", "Basketball": "BB", "AFL": "AFL", "Badminton": "BD", "Touch": "TF", "Oztag": "OZ"}


def crest(sport):
    a = ABBR.get(sport, sport[:2].upper())
    return (f'<svg class="crest" viewBox="0 0 46 46" aria-hidden="true"><circle class="i" cx="23" cy="23" r="19"/><circle class="o" cx="23" cy="23" r="21"/>'
            f'<text x="23" y="27.5" text-anchor="middle">{a}</text></svg>')


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
    lab = {"confirmed": "Confirmed", "expected": "Expected", "tba": "TBA"}[ev["status"]]
    return (f'<a class="ev s-{slugify(ev["sport"])}" href="/t/{ev["slug"]}/" data-sport="{E(ev["sport"])}" data-state="{ev["state"]}" data-month="{ev["month"]}">'
            f'{date_box(ev)}{crest(ev["sport"])}<div class="body"><h3>{E(ev["name"])}</h3>'
            f'<div class="meta"><span class="sp">{E(ev["sport"])}</span><span>{E(ev["place"])}, {ev["state"]}</span><span>{E(ev["ages"])}</span></div></div>'
            f'<div class="st"><span class="{ev["status"]}">{lab}</span><i>→</i></div></a>')


def index(evs):
    from collections import Counter
    sports = Counter(e["sport"] for e in evs)
    states = Counter(e["state"] for e in evs)
    mcount = Counter(e["month"] for e in evs if e["month"])
    allm = []
    y, m = 2026, 11
    for _ in range(12):
        allm.append(f"{y}-{m:02d}")
        m += 1
        if m == 13: y, m = y + 1, 1
    mx = max(mcount.values()) if mcount else 1
    nxt = next((e for e in evs if e["start"] and e["start"] >= date.today().isoformat()), None)
    sport_chips = '<span class="seg-l">Sport</span><button class="chip" type="button" data-f="sport" data-v="" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip s-{slugify(k)}" type="button" data-f="sport" data-v="{E(k)}" aria-pressed="false"><span class="dot"></span>{E(k)}</button>'
        for k, n in sorted(sports.items(), key=lambda x: -x[1]))
    state_chips = '<span class="seg-l">State</span><button class="chip" type="button" data-f="state" data-v="" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" type="button" data-f="state" data-v="{k}" aria-pressed="false">{k}</button>'
        for k, n in sorted(states.items(), key=lambda x: -x[1]))
    month_btns = "".join(
        f'<button class="mo" type="button" data-f="month" data-v="{mo}" aria-pressed="false"{"" if mcount.get(mo) else " disabled"}>'
        f'<b>{MONTHS[int(mo[5:])-1].upper()}</b><span class="n">{mcount.get(mo,0) or "·"}</span><small>{mo[:4]}</small></button>'
        for mo in allm)
    board = ""
    if nxt:
        board = (f'<div class="next" id="board" data-start="{nxt["start"]}"><span class="eyebrow">Next fixture</span>'
                 f'<a href="/t/{nxt["slug"]}/">{E(nxt["name"])} · {E(nxt["place"])}</a>'
                 '<div class="digits"><div><b id="cd">--</b><small>Days</small></div><div><b id="ch">--</b><small>Hours</small></div><div><b id="cm">--</b><small>Mins</small></div><div><b id="cs">--</b><small>Secs</small></div></div></div>')
    hero = f"""<section class="hero"><div class="in"><span class="eyebrow">The 2026/27 season · NSW &amp; Queensland</span>
<h1>Every tournament.<br><em>One calendar.</em></h1>
<p class="lede">Football, futsal, cricket, basketball, AFL, badminton, touch and Oztag tournaments, with dates, age groups and the organiser's official link.</p>{board}</div></section>"""
    s = head("Tourney Finder: football, futsal and junior sports tournaments in NSW and QLD",
             "Find football, futsal, cricket, basketball, AFL, touch and Oztag tournaments in NSW and Queensland. Dates, age groups and official links in one place.", "/").replace("<!--HERO-->", hero)
    groups, cur = [], None
    for e in evs:
        key = e["month"] or "tba"
        if key != cur:
            lab = (["January","February","March","April","May","June","July","August","September","October","November","December"][int(key[5:])-1] + " " + key[:4]) if key != "tba" else "Dates to be announced"
            groups.append(f'<div class="mhead" data-g="{key}">{lab}</div>')
            cur = key
        groups.append(card(e).replace('<a class="ev', f'<a data-g="{key}" class="ev', 1))
    s += f"""<section style="display:grid;gap:22px"><div class="sechead"><h2>Fixtures</h2><div class="count" id="count" role="status">{len(evs)} tournaments</div></div>
<div class="months" id="months">{month_btns}</div>
<div class="filters"><div class="seg">{sport_chips}</div><div class="seg">{state_chips}</div></div>
<div class="list" id="list">{''.join(groups)}</div></section>
""" + shop_strip(PRODUCTS[:4]) + f"""<div class="split"><div class="panel"><span class="eyebrow">For organisers</span><h2>List your tournament</h2><p class="muted">Free listing for clubs and associations. Coaches and parents across NSW and Queensland use Tourney Finder to plan their season.</p><a class="button" href="/add/" style="justify-self:start">Add a tournament</a></div>
<div class="panel"><span class="eyebrow">Season alerts</span><h2>New fixtures, monthly</h2><p class="muted">One short email a month with new tournaments for your sport and area.</p>
<form name="tourney-alerts" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="tourney-alerts"><p class="hidden"><label>Leave empty <input name="bot-field"></label></p>
<input id="aEmail" type="email" name="email" placeholder="Your email" required aria-label="Email">
<input id="aWhat" type="text" name="interest" placeholder="e.g. U12 football, Brisbane" aria-label="Sport, age group and area">
<button type="submit">Subscribe</button></form></div></div>
"""
    s += f"""<script>
(function(){{
var f={{sport:'',state:'',month:''}},c=document.getElementById('count');
var items=[].slice.call(document.querySelectorAll('#list .ev'));
function run(){{var n=0;items.forEach(function(e){{var ok=(!f.sport||e.dataset.sport===f.sport)&&(!f.state||e.dataset.state===f.state)&&(!f.month||e.dataset.month===f.month);e.classList.toggle('hidden',!ok);if(ok)n++;}});
[].forEach.call(document.querySelectorAll('.mhead'),function(h){{var g=h.dataset.g;h.classList.toggle('hidden',!items.some(function(e){{return e.dataset.g===g&&!e.classList.contains('hidden');}}));}});
c.textContent=n+(n===1?' tournament':' tournaments')+(n===0?'. Try another filter, or add one you know about.':'');}}
[].forEach.call(document.querySelectorAll('[data-f]'),function(b){{b.addEventListener('click',function(){{
var k=b.dataset.f,v=b.dataset.v;if(k==='month'&&f.month===v)v='';f[k]=v;
[].forEach.call(document.querySelectorAll('[data-f="'+k+'"]'),function(x){{x.setAttribute('aria-pressed',String(x.dataset.v===v&&(k!=='month'||v!=='')));}});
if(k!=='month'&&v==='')document.querySelector('[data-f="'+k+'"][data-v=""]').setAttribute('aria-pressed','true');
run();}});}});
var bd=document.getElementById('board');if(bd){{var t=new Date(bd.dataset.start+'T09:00:00+10:00').getTime();
function p(x){{return (x<10?'0':'')+x;}}
function tick(){{var d=Math.max(0,t-Date.now()),s=Math.floor(d/1000);
document.getElementById('cd').textContent=Math.floor(s/86400);document.getElementById('ch').textContent=p(Math.floor(s%86400/3600));
document.getElementById('cm').textContent=p(Math.floor(s%3600/60));document.getElementById('cs').textContent=p(s%60);}}
tick();setInterval(tick,1000);}}
}})();
</script>"""
    return s + FOOT


def page(ev):
    st = ev["state"]
    yr = "2027" if "2027" in (ev["start"] or ev["month"]) and "2027" not in ev["name"] else ""
    title = f"{ev['name']} {yr}".strip() + f" · {ev['place']}, {st} · Tourney Finder"
    desc = f"{ev['name']} in {ev['place']}, {st}: {when(ev)}. {ev['ages']}. {ev['about']}"[:300]
    s = head(title, desc, f"/t/{ev['slug']}/")
    cal = f'<a class="button" href="/t/{ev["slug"]}/event.ics">Add to calendar</a>' if ev["start"] else ""
    lab = {"confirmed": "Dates confirmed", "expected": "Expected, based on last year", "tba": "Dates to be announced"}[ev["status"]]
    hero = f"""<section class="hero"><div class="in"><a class="back" href="/">← All fixtures</a>
<div style="display:flex;gap:18px;align-items:center" class="s-{slugify(ev['sport'])}">{crest(ev['sport'])}<span class="eyebrow">{E(ev['sport'])} · {st} · {lab}</span></div>
<h1 style="font-size:clamp(32px,6.5vw,60px)">{E(ev['name'])}</h1>
<p class="lede">{E(when(ev))} · {E(ev['place'])}, {st}</p>
<div style="display:flex;gap:12px;flex-wrap:wrap">{cal}<a class="button ghost" href="{E(ev['src'])}" rel="noopener" target="_blank">Organiser's page</a></div></div></section>"""
    s = s.replace("<!--HERO-->", hero)
    s += f"""<section style="display:grid;gap:18px"><div class="sechead"><h2>Tournament details</h2></div>
<dl class="facts"><div><dt>When</dt><dd>{E(when(ev))}</dd></div><div><dt>Where</dt><dd>{E(ev['place'])}, {st}</dd></div>
<div><dt>Sport</dt><dd>{E(ev['sport'])}</dd></div><div><dt>Age groups</dt><dd>{E(ev['ages'])}</dd></div>
<div><dt>Who can enter</dt><dd>{E(ev['who'])}</dd></div><div><dt>Official source</dt><dd><a href="{E(ev['src'])}" rel="noopener" target="_blank">{E(ev['src_name'])}</a></dd></div></dl>
<p class="muted" style="max-width:680px;font-size:17px">{E(ev['about'])}</p></section>
""" + shop_strip(PRODUCTS[:3], "Gear for the weekend") + """<div class="panel"><span class="eyebrow">For organisers</span><h2>Is this your tournament?</h2><p class="muted">Send the latest dates, entry link and fees, and we'll update this page for free.</p><a class="button" href="/add/" style="justify-self:start">Update this listing</a></div>
"""
    return s + FOOT


ETSY = "https://yalegendco.etsy.com"
PRODUCTS = [
    ("tournament-weekend-survivor", "Tournament Weekend Survivor tee", "A$42.95"),
    ("half-time-oranges", "Half-Time Oranges tee", "A$42.95"),
    ("sideline-coach", "Sideline Coach tee", "A$42.95"),
    ("match-day-taxi-service", "Match Day Taxi Service tee", "A$42.95"),
    ("nutmeg-specialist", "Nutmeg Specialist tee", "A$42.95"),
]


def shop_grid(items):
    return '<div class="shop">' + "".join(
        f'<a class="prod" href="{ETSY}" rel="noopener" target="_blank"><img src="/shop/{slug}.jpg" alt="{E(name)}" width="500" height="600"><b>{E(name)}</b><span>{price} · Buy on Etsy</span></a>'
        for slug, name, price in items) + "</div>"


def shop_strip(items, title="The Clubhouse Shop"):
    return (f'<section style="display:grid;gap:18px"><div class="sechead"><h2>{title}</h2><a class="count" href="/shop/" style="color:var(--gold2)">See all →</a></div>'
            f'<p class="muted" style="margin:0">Tees for tournament weekends, sideline parents and players. Printed to order, free delivery in Australia.</p>{shop_grid(items)}</section>\n')


def shop_page():
    s = head("Shop · Tourney Finder", "Sports tees for tournament weekends, sideline parents and players. Free delivery in Australia.", "/shop/").replace("<!--HERO-->", """<section class="hero"><div class="in"><a class="back" href="/">← All fixtures</a><span class="eyebrow">The Clubhouse Shop</span><h1 style="font-size:clamp(34px,7vw,64px)">Gear for the<br><em>long weekend</em></h1>
<p class="lede">Tees for tournament weekends, sideline parents and players. Free delivery in Australia, sizes S to 3XL.</p></div></section>""")
    s += '<section style="display:grid;gap:18px"><div class="sechead"><h2>Tees</h2></div>' + shop_grid(PRODUCTS) + "</section>\n"
    s += """<div class="panel" style="max-width:720px"><span class="eyebrow">For teams</span><h2>Custom tour shirts</h2><p class="muted">Heading to a tournament? Get matching shirts with your team name on the front and player names and numbers on the back. Minimum 10 shirts. Tell us what you need and we'll send a design and quote.</p>
<form name="team-shirts" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="team-shirts"><p class="hidden"><label>Leave empty <input name="bot-field"></label></p>
<label for="sTeam">Team or club name<input id="sTeam" name="team" required></label>
<label for="sEvent">Tournament and dates<input id="sEvent" name="event" placeholder="e.g. Under 12s, January carnival"></label>
<label for="sQty">How many shirts<input id="sQty" name="qty" type="number" min="10" placeholder="e.g. 15"></label>
<label for="sEmail">Your email<input id="sEmail" name="email" type="email" required></label>
<label for="sNotes">Colours, names, anything else<textarea id="sNotes" name="notes" rows="3"></textarea></label>
<button type="submit">Ask for a quote</button></form></div>"""
    return s + FOOT


def add_page():
    s = head("Add your tournament · Tourney Finder", "List your football, futsal or junior sports tournament free on Tourney Finder.", "/add/").replace("<!--HERO-->", """<section class="hero"><div class="in"><a class="back" href="/">← All fixtures</a><span class="eyebrow">For organisers</span><h1 style="font-size:clamp(34px,7vw,64px)">List your<br><em>tournament</em></h1>
<p class="lede">Free for clubs, associations and organisers. We check every entry and usually publish within a few days.</p></div></section>""")
    s += """<div class="panel" style="max-width:720px"><form name="add-tournament" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="add-tournament"><p class="hidden"><label>Leave empty <input name="bot-field"></label></p>
<label for="tName">Tournament name<input id="tName" name="name" required></label>
<label for="tSport">Sport<select id="tSport" name="sport"><option>Football</option><option>Futsal</option><option>AFL</option><option>Cricket</option><option>Basketball</option><option>Badminton</option><option>Tennis</option><option>Touch</option><option>Oztag</option><option>Netball</option><option>Other</option></select></label>
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
    s = head("Thanks · Tourney Finder", "Thanks for your submission.", "/thanks/").replace("<!--HERO-->", """<section class="hero"><div class="in"><span class="eyebrow">Received</span><h1>Thank <em>you</em></h1><p class="lede">We've got it. New tournaments are usually live within a few days.</p><a class="button" href="/" style="justify-self:start">Back to all fixtures</a></div></section>""")
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
    w("shop/index.html", shop_page())
    for f in os.listdir(os.path.join(ROOT, "shop")):
        shutil.copy(os.path.join(ROOT, "shop", f), os.path.join(DIST, "shop", f))
    urls = [f"{SITE}/", f"{SITE}/shop/", f"{SITE}/add/"]
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
