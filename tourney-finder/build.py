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
/* Match-night look: floodlit pitch header, LED scoreboard countdown, ticket-style cards. Deliberately one dark theme. */
:root{--bg:#0b1410;--card:#13211a;--card2:#182a21;--ink:#eef6ef;--muted:#9db3a5;--line:#24382c;
--pitch:#1d6b3c;--pitch2:#1a5f35;--chalk:rgba(255,255,255,.55);--led:#ffd84d;--accent:#3ee07f;--pitch-ink:#0b1410;
--ok:#3ee07f;--ok-soft:rgba(62,224,127,.14);--exp:#ffd84d;--exp-soft:rgba(255,216,77,.14);--tba:#9db3a5;--tba-soft:rgba(157,179,165,.14);
--football:#3ee07f;--futsal:#ff9a3d;--touch:#4dc3ff;--oztag:#ff6fae;--cricket:#f5f0c8;--basketball:#ff7b3a;--afl:#ffd84d;--badminton:#c59bff;
--display:"Barlow Condensed",system-ui,sans-serif;--body:"Barlow",system-ui,-apple-system,sans-serif;--mono:"Share Tech Mono",ui-monospace,monospace;color-scheme:dark}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.5}
a{color:var(--accent)}
.top{background:rgba(11,20,16,.92);border-bottom:1px solid var(--line);position:sticky;top:env(safe-area-inset-top,0px);z-index:5;backdrop-filter:blur(6px)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.top .in,.wrap,.hero .in{max-width:900px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.top .in{padding-block:12px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.logo{font-family:var(--display);font-weight:800;font-size:24px;letter-spacing:.04em;color:var(--ink);text-decoration:none;text-transform:uppercase}
.logo span{color:var(--accent)}
.top a.btn{background:var(--accent);color:var(--pitch-ink);text-decoration:none;font-weight:700;padding:8px 14px;border-radius:999px;font-size:14px}
.hero{position:relative;overflow:hidden;background:
 radial-gradient(ellipse 60% 70% at 15% -10%,rgba(255,255,230,.28),transparent 60%),
 radial-gradient(ellipse 60% 70% at 85% -10%,rgba(255,255,230,.22),transparent 60%),
 repeating-linear-gradient(90deg,var(--pitch) 0 70px,var(--pitch2) 70px 140px);border-bottom:3px solid var(--chalk)}
.hero::before{content:"";position:absolute;left:50%;top:50%;width:260px;height:260px;border:3px solid var(--chalk);border-radius:50%;transform:translate(-50%,-50%);opacity:.5}
.hero::after{content:"";position:absolute;left:50%;top:0;bottom:0;border-left:3px solid var(--chalk);opacity:.5}
.hero .in{position:relative;z-index:1;padding-block:40px 34px;display:grid;gap:14px}
h1,h2{font-family:var(--display);font-weight:800;margin:0;line-height:1;text-wrap:balance;text-transform:uppercase}
h1{font-size:clamp(44px,11vw,84px);letter-spacing:.01em;text-shadow:0 3px 0 rgba(0,0,0,.25)}
h2{font-size:26px;letter-spacing:.02em}
.hero p{max-width:560px;font-size:17px;color:#e3f1e6}
.board{justify-self:start;background:#050806;border:3px solid #2b2b2b;border-radius:14px;padding:12px 16px;display:grid;gap:6px;box-shadow:0 10px 30px rgba(0,0,0,.45);max-width:100%}
.board .lbl{font-family:var(--display);font-weight:800;letter-spacing:.12em;font-size:13px;color:#8fa;text-transform:uppercase}
.board .nm{font-weight:700;font-size:15px;color:#fff;min-width:0}
.digits{display:flex;gap:8px;flex-wrap:wrap}
.digits div{display:grid;justify-items:center;background:#111;border-radius:8px;padding:6px 10px;min-width:60px}
.digits b{font-family:var(--mono);font-size:34px;line-height:1;color:var(--led);text-shadow:0 0 12px rgba(255,216,77,.6);font-variant-numeric:tabular-nums}
.digits small{font-size:10px;letter-spacing:.14em;color:#889;text-transform:uppercase}
.wrap{padding-block:24px 56px;display:grid;gap:22px}
p{margin:0}.muted{color:var(--muted)}
.chips{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px;scrollbar-width:thin}
.chip{flex:none;font:inherit;font-weight:700;font-size:14px;border:2px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:7px 14px;cursor:pointer;display:flex;gap:6px;align-items:center}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.chip .dot{width:9px;height:9px;border-radius:50%;background:var(--c,var(--accent))}
.chip .n{font-size:12px;opacity:.7}
.months{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(62px,1fr);gap:6px;overflow-x:auto;padding-bottom:4px}
.mo{font:inherit;border:2px solid var(--line);background:var(--card);color:var(--ink);border-radius:12px;padding:8px 4px;cursor:pointer;display:grid;justify-items:center;gap:2px}
.mo b{font-family:var(--display);font-size:18px;text-transform:uppercase;letter-spacing:.04em}
.mo small{font-size:11px;color:var(--muted)}
.mo i{display:block;width:70%;height:6px;border-radius:3px;background:var(--line)}
.mo i span{display:block;height:100%;border-radius:3px;background:var(--accent)}
.mo[aria-pressed="true"]{border-color:var(--accent);background:var(--card2)}
.mo:disabled{opacity:.35;cursor:default}
.rowlabel{font-family:var(--display);font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:13px;color:var(--muted)}
.count{font-size:14px;color:var(--muted)}
.list{display:grid;gap:14px}
.ev{position:relative;background:var(--card);border-radius:16px;display:grid;grid-template-columns:96px 1fr;text-decoration:none;color:var(--ink);overflow:hidden;border-left:6px solid var(--c,var(--accent));transition:transform .15s ease}
.ev:hover{transform:translateY(-2px);background:var(--card2)}
.ev::before,.ev::after{content:"";position:absolute;left:84px;width:22px;height:22px;border-radius:50%;background:var(--bg)}
.ev::before{top:-11px}.ev::after{bottom:-11px}
.date{border-right:2px dashed var(--line);display:grid;place-items:center;align-content:center;text-align:center;padding:14px 6px;font-family:var(--display);font-weight:800;line-height:1}
.date .m{font-size:16px;text-transform:uppercase;color:var(--c,var(--accent));letter-spacing:.06em}
.date .d{font-size:36px}.date .y{font-size:13px;color:var(--muted);font-weight:600}
.ev .body{padding:14px 16px;min-width:0;display:grid;gap:6px}
.ev h3{margin:0;font-size:19px;line-height:1.2;font-weight:700}
.meta{display:flex;flex-wrap:wrap;gap:6px 12px;font-size:14px;color:var(--muted)}
.tag{font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--c,var(--accent))}
.pill{font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;white-space:nowrap}
.pill.confirmed{background:var(--ok-soft);color:var(--ok)}.pill.expected{background:var(--exp-soft);color:var(--exp)}.pill.tba{background:var(--tba-soft);color:var(--tba)}
.s-football{--c:var(--football)}.s-futsal{--c:var(--futsal)}.s-touch{--c:var(--touch)}.s-oztag{--c:var(--oztag)}.s-cricket{--c:var(--cricket)}.s-basketball{--c:var(--basketball)}.s-afl{--c:var(--afl)}.s-badminton{--c:var(--badminton)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;display:grid;gap:12px}
.cta{background:linear-gradient(135deg,var(--pitch),var(--pitch2));border-radius:16px;padding:20px;display:grid;gap:10px}
button,.button{font:inherit;font-weight:700;border:0;border-radius:10px;padding:12px 16px;background:var(--accent);color:var(--pitch-ink);cursor:pointer;text-decoration:none;display:inline-block;text-align:center}
.cta .button{justify-self:start;background:#fff;color:var(--pitch)}
select,input,textarea{font:inherit;padding:10px 12px;border-radius:10px;border:2px solid var(--line);background:var(--card2);color:var(--ink);width:100%}
select:focus,input:focus,textarea:focus{outline:none;border-color:var(--accent)}
label{font-size:13px;font-weight:700;color:var(--muted);display:grid;gap:4px}
dl{display:grid;grid-template-columns:120px 1fr;gap:8px 12px;margin:0}dt{font-weight:700;color:var(--muted)}dd{margin:0;min-width:0}
form{display:grid;gap:12px}.hidden{display:none!important}
footer{font-size:13px;color:var(--muted);display:grid;gap:6px}
:focus-visible{outline:3px solid var(--led);outline-offset:2px}
@media (max-width:480px){.ev{grid-template-columns:76px 1fr}.ev::before,.ev::after{left:65px}.date .d{font-size:30px}dl{grid-template-columns:1fr}.digits div{min-width:52px;padding:6px 8px}.digits b{font-size:28px}}
@media (prefers-reduced-motion:reduce){.ev{transition:none}}
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
<meta name="theme-color" content="#0b1410">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='28' fill='%231f7a43'/%3E%3Cpolygon points='32,18 44,27 39,41 25,41 20,27' fill='white'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@800&family=Barlow:wght@400;600;700&family=Share+Tech+Mono&display=swap">
<style>{CSS}</style></head><body>
<div class="top"><div class="in"><a class="logo" href="/">⚽ Tourney<span>Finder</span></a><a class="btn" href="/add/">+ Add your tournament</a></div></div>
<!--HERO-->
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
    return (f'<a class="ev s-{slugify(ev["sport"])}" href="/t/{ev["slug"]}/" data-sport="{E(ev["sport"])}" data-state="{ev["state"]}" data-month="{ev["month"]}">'
            f'{date_box(ev)}<div class="body"><span class="tag">{E(ev["sport"])} · {ev["state"]}</span><h3>{E(ev["name"])}</h3><div class="meta"><span>📍 {E(ev["place"])}</span>'
            f'<span>{E(ev["ages"])}</span></div><div><span class="pill {ev["status"]}">{STATUS[ev["status"]]}</span></div></div></a>')


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
    sport_chips = '<button class="chip" type="button" data-f="sport" data-v="" aria-pressed="true">All sports</button>' + "".join(
        f'<button class="chip s-{slugify(k)}" type="button" data-f="sport" data-v="{E(k)}" aria-pressed="false"><span class="dot"></span>{E(k)} <span class="n">{n}</span></button>'
        for k, n in sorted(sports.items(), key=lambda x: -x[1]))
    state_chips = '<button class="chip" type="button" data-f="state" data-v="" aria-pressed="true">All states</button>' + "".join(
        f'<button class="chip" type="button" data-f="state" data-v="{k}" aria-pressed="false">{k} <span class="n">{n}</span></button>'
        for k, n in sorted(states.items(), key=lambda x: -x[1]))
    month_btns = "".join(
        f'<button class="mo" type="button" data-f="month" data-v="{mo}" aria-pressed="false"{"" if mcount.get(mo) else " disabled"}>'
        f'<b>{MONTHS[int(mo[5:])-1]}</b><small>{mo[2:4]}</small><i><span style="width:{int(100*mcount.get(mo,0)/mx)}%"></span></i><small>{mcount.get(mo,0) or "–"}</small></button>'
        for mo in allm)
    board = ""
    if nxt:
        board = (f'<div class="board" id="board" data-start="{nxt["start"]}"><span class="lbl">Next kick-off</span>'
                 f'<a class="nm" href="/t/{nxt["slug"]}/" style="color:#fff;text-decoration:none">{E(nxt["name"])} · {E(nxt["place"])}</a>'
                 '<div class="digits"><div><b id="cd">--</b><small>days</small></div><div><b id="ch">--</b><small>hrs</small></div><div><b id="cm">--</b><small>min</small></div><div><b id="cs">--</b><small>sec</small></div></div></div>')
    hero = f"""<section class="hero"><div class="in"><h1>Find your<br>next tournament</h1>
<p>Football, futsal, cricket, basketball, AFL, badminton, touch and Oztag tournaments across NSW and Queensland. One place, every date, straight to the organiser.</p>{board}</div></section>"""
    s = head("Tourney Finder: football, futsal and junior sports tournaments in NSW and QLD",
             "Find football, futsal, touch and Oztag tournaments and carnivals in NSW and Queensland. Dates, age groups and official links in one place.", "/").replace("<!--HERO-->", hero)
    s += f"""<div class="rowlabel">Pick a month</div><div class="months" id="months">{month_btns}</div>
<div class="chips" id="sports">{sport_chips}</div>
<div class="chips" id="states">{state_chips}</div>
<div class="count" id="count" role="status">{len(evs)} tournaments</div>
<div class="list" id="list">{''.join(card(e) for e in evs)}</div>
<div class="cta"><h2>Running a tournament?</h2><p>List it free. Coaches and parents across NSW and Queensland use Tourney Finder to plan their season.</p><a class="button" href="/add/">Add your tournament</a></div>
<div class="card"><h2>New tournaments in your inbox</h2><p class="muted">One short email a month with new tournaments for your sport and area. Free, unsubscribe any time.</p>
<form name="tourney-alerts" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="tourney-alerts"><p class="hidden"><label>Leave empty <input name="bot-field"></label></p>
<input id="aEmail" type="email" name="email" placeholder="Your email" required aria-label="Email">
<input id="aWhat" type="text" name="interest" placeholder="Sport, age group and area, e.g. U12 football, Brisbane" aria-label="What you're looking for">
<button type="submit">Send me new tournaments</button></form></div>
<script>
(function(){{
var f={{sport:'',state:'',month:''}},c=document.getElementById('count');
var items=[].slice.call(document.querySelectorAll('#list .ev'));
function run(){{var n=0;items.forEach(function(e){{var ok=(!f.sport||e.dataset.sport===f.sport)&&(!f.state||e.dataset.state===f.state)&&(!f.month||e.dataset.month===f.month);e.classList.toggle('hidden',!ok);if(ok)n++;}});
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
    s = head(title, desc, f"/t/{ev['slug']}/").replace("<!--HERO-->", "")
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
