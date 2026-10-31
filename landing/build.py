"""Builds the test landing pages into landing/sites/<slug>/ (index, thanks, privacy).

Each folder is a complete static site for Netlify. Sign-ups use Netlify Forms.
Set ADS_ID (e.g. "AW-123456789") and ADS_LABEL to switch on Google Ads conversion tracking.
"""
import html, os, pathlib

ADS_ID = os.environ.get("ADS_ID", "")
ADS_LABEL = os.environ.get("ADS_LABEL", "")
OUT = pathlib.Path(__file__).parent / "sites"

SITES = [
    dict(
        slug="backyardrules", name="Backyard Rules", accent="#1f7a4d", accent2="#e8f5ee",
        title="Do I need council approval? | Backyard Rules",
        desc="Find out in 60 seconds if your shed, carport, deck or granny flat needs council approval in NSW or QLD.",
        kicker="NSW and QLD · launching soon",
        h1="Does your shed need council approval?",
        lead="Answer 4 quick questions about your block and what you want to build. Get a plain-English answer in 60 seconds, with the exact rule it comes from.",
        bullets=[
            ("Sheds, carports, decks, fences, pools, granny flats", "The projects people ask councils about most."),
            ("Based on your lot size and zone", "Not a generic blog post. The rules change with your block."),
            ("Every answer links to the official rule", "So you can check it yourself or show your council."),
        ],
        how=["Pick what you want to build", "Enter your suburb and rough lot size", "See: no approval, fast-track approval, or full council approval, and why"],
        price="Free quick check. A full approval checklist for your exact address will be about A$19.",
        q_label="What do you want to build?", q_name="project",
        q_opts=["Shed", "Carport or garage", "Deck or pergola", "Fence or retaining wall", "Pool", "Granny flat", "Something else"],
        q2_label="Which state?", q2_name="state", q2_opts=["NSW", "QLD", "Other state"],
        cta="Tell me when it's ready",
        note="Backyard Rules gives general information from published state and council rules. It is not legal or planning advice. Always confirm with your council before you build.",
    ),
    dict(
        slug="superontime", name="SuperOnTime", accent="#1d4fa8", accent2="#e9effa",
        title="Payday Super calculator and reminders for small employers | SuperOnTime",
        desc="Lost the free ATO clearing house? Work out super for each payday and get a reminder before it's due. Made for employers with 1-4 staff.",
        kicker="For employers with 1-4 staff",
        h1="Payday Super, without the payroll software",
        lead="Since 1 July 2026 super has to reach your staff's fund within days of each payday, and the ATO's free clearing house has closed. SuperOnTime works out the amount and reminds you before it's due.",
        bullets=[
            ("Super worked out for every payday", "Enter hours or gross pay. See the super amount straight away."),
            ("A reminder before the deadline", "By email or SMS, so you are never late and never hit with the charge."),
            ("A simple record of every payment", "Handy for your BAS, your accountant and any ATO question."),
        ],
        how=["Add your staff once (2 minutes)", "After each payday, enter what you paid", "Get the super amount and a reminder; you pay through your fund or bank as usual"],
        price="Planned price: A$5 a month or A$49 a year. Early list gets 3 months free.",
        q_label="How many staff do you pay?", q_name="staff",
        q_opts=["1", "2-4", "5 or more", "Just me (no staff yet)"],
        q2_label="How do you pay super now?", q2_name="current",
        q2_opts=["I used the ATO clearing house", "My super fund's website", "Payroll software", "My accountant does it", "Not sure"],
        cta="Get early access",
        note="SuperOnTime is a calculator and reminder tool. It never holds or moves your money and it is not tax or financial advice. Check your obligations at ato.gov.au or with your registered tax agent.",
    ),
    dict(
        slug="selfstrata", name="SelfStrata", accent="#8a3b12", accent2="#fbefe6",
        title="Simple app for small self-managed strata buildings | SelfStrata",
        desc="Run a small strata building of 2-10 units without a strata manager: levy notices, AGM paperwork, sinking fund and documents in one place.",
        kicker="For 2-10 unit buildings",
        h1="Run your small strata building without the spreadsheets",
        lead="Most strata buildings are small, and many owners run them themselves. Strata software is made for professional managers. SelfStrata is made for the owner who got stuck being secretary.",
        bullets=[
            ("Levy notices in two taps", "Work out each lot's share and send the notices."),
            ("AGM notices and minutes templates", "Ready for your state, with the right notice periods."),
            ("Sinking fund tracker and document store", "Insurance, by-laws, quotes and receipts, all in one place."),
        ],
        how=["Add your building and lots", "Invite the other owners", "Send levies, run the AGM and keep records from your phone"],
        price="Planned price: about A$12 a month per building (not per owner).",
        q_label="How many units in your building?", q_name="units",
        q_opts=["2-4", "5-10", "11-20", "More than 20"],
        q2_label="Which state?", q2_name="state", q2_opts=["NSW", "QLD", "VIC", "WA", "SA", "Other"],
        cta="Join the early list",
        note="SelfStrata provides templates and record-keeping tools. It is not legal advice and does not replace a licensed strata manager where your state's law requires one.",
    ),
    dict(
        slug="shortstaycheck", name="Short Stay Check", accent="#0f6e7a", accent2="#e6f4f5",
        title="Can I rent my place as a short stay? Check your address | Short Stay Check",
        desc="Check one address against state, council and strata rules for short-stay rentals in Australia: registration, night caps, levies and building bans.",
        kicker="NSW, VIC, QLD and WA · launching soon",
        h1="Can you rent your place as a short stay?",
        lead="State rules, council rules and your building's by-laws are all in different places. Enter one address and see what applies to it: registration, night limits, levies and strata bans, in plain English.",
        bullets=[
            ("State, council and strata rules in one check", "Not three websites and a phone call. One answer for your address."),
            ("The costs and limits that apply to you", "For example, NSW's 180-night cap for unhosted stays in Greater Sydney and Victoria's 7.5% short stay levy."),
            ("Every answer links to the official rule", "So you can check it yourself, and we tell you when a rule changes."),
        ],
        how=["Enter the address and the type of place", "Say if you'll live there or rent the whole place", "See what you need: register, night limits, levy, strata approval, and why"],
        price="Free quick check. A full report for your exact address will be about A$19, with optional rule-change alerts for about A$5 a month.",
        q_label="What kind of place is it?", q_name="place",
        q_opts=["Whole house", "Apartment or unit (strata)", "Granny flat", "A room in my home", "Not bought yet, still looking"],
        q2_label="Which state?", q2_name="state", q2_opts=["NSW", "VIC", "QLD", "WA", "Other state", "Outside Australia"],
        cta="Tell me when it's ready",
        note="Short Stay Check gives general information from published state, council and strata rules. It is not legal advice. Always confirm with your council and your owners corporation before you list.",
    ),
]

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#1b1f24;background:#fff;line-height:1.55}
.wrap{max-width:680px;margin:0 auto;padding:0 18px}
header{padding:18px 0;border-bottom:1px solid #eceff2}header .wrap{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px}
.dot{width:14px;height:14px;border-radius:4px;background:var(--a)}
.hero{background:var(--b);padding:34px 0 30px}.kicker{display:inline-block;font-size:13px;font-weight:600;color:var(--a);background:#fff;border-radius:99px;padding:3px 12px;margin-bottom:12px}
h1{font-size:clamp(28px,7vw,40px);line-height:1.15;margin:0 0 12px}.lead{font-size:18px;margin:0 0 22px;color:#30363d}
form{background:#fff;border:1px solid #e1e5ea;border-radius:14px;padding:18px;box-shadow:0 2px 10px rgba(0,0,0,.04)}
label{display:block;font-weight:600;font-size:15px;margin:0 0 6px}select,input[type=email]{width:100%;font-size:17px;padding:12px;border:1px solid #c9d0d8;border-radius:10px;margin:0 0 14px;background:#fff;color:#1b1f24}
button{width:100%;font-size:18px;font-weight:700;padding:14px;border:0;border-radius:10px;background:var(--a);color:#fff;cursor:pointer}
.small{font-size:13px;color:#5b6570;margin:10px 0 0}.hp{position:absolute;left:-9999px}
section{padding:30px 0}h2{font-size:22px;margin:0 0 14px}
.feat{display:grid;gap:12px}.feat div{border:1px solid #eceff2;border-radius:12px;padding:14px}.feat b{display:block;margin-bottom:2px}
ol{padding-left:20px}ol li{margin:0 0 8px}.price{background:var(--b);border-radius:12px;padding:14px;font-weight:600}
footer{border-top:1px solid #eceff2;padding:20px 0 40px;font-size:13px;color:#5b6570}footer a{color:#5b6570}
"""

def gtag(event):
    if not ADS_ID:
        return ""
    ev = f"gtag('event','conversion',{{send_to:'{ADS_ID}/{ADS_LABEL}'}});" if event else ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={ADS_ID}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}"
            f"gtag('js',new Date());gtag('config','{ADS_ID}');{ev}</script>")

def page(s, title, body, conversion=False, index=True):
    e = html.escape
    robots = "" if index else '<meta name="robots" content="noindex">'
    return f"""<!doctype html><html lang="en-AU"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title>
<meta name="description" content="{e(s['desc'])}">{robots}
<style>:root{{--a:{s['accent']};--b:{s['accent2']}}}{CSS}</style>{gtag(conversion)}</head><body>
<header><div class="wrap"><span class="dot"></span><a href="/" style="color:inherit;text-decoration:none">{e(s['name'])}</a></div></header>
{body}
<footer><div class="wrap"><p>{e(s['note'])}</p><p><a href="/privacy.html">Privacy</a> · © 2026 {e(s['name'])}</p></div></footer>
</body></html>"""

def select(name, label, opts):
    o = "".join(f"<option>{html.escape(x)}</option>" for x in opts)
    return f'<label for="{name}">{html.escape(label)}</label><select id="{name}" name="{name}" required><option value="">Choose one</option>{o}</select>'

def index(s):
    e = html.escape
    feats = "".join(f"<div><b>{e(a)}</b>{e(b)}</div>" for a, b in s["bullets"])
    steps = "".join(f"<li>{e(x)}</li>" for x in s["how"])
    form = f"""<form name="notify" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="bot-field">
<input type="hidden" name="form-name" value="notify"><p class="hp"><label>Leave empty <input name="bot-field"></label></p>
{select(s['q_name'], s['q_label'], s['q_opts'])}{select(s['q2_name'], s['q2_label'], s['q2_opts'])}
<label for="email">Your email</label><input id="email" type="email" name="email" required placeholder="you@example.com" autocomplete="email">
<button type="submit">{e(s['cta'])}</button>
<p class="small">Free. One email when it launches, nothing else. <a href="/privacy.html">Privacy</a></p></form>"""
    body = f"""<div class="hero"><div class="wrap"><span class="kicker">{e(s['kicker'])}</span>
<h1>{e(s['h1'])}</h1><p class="lead">{e(s['lead'])}</p>{form}</div></div>
<section><div class="wrap"><h2>What you get</h2><div class="feat">{feats}</div></div></section>
<section style="padding-top:0"><div class="wrap"><h2>How it works</h2><ol>{steps}</ol><p class="price">{e(s['price'])}</p>
<p><a href="#email" style="color:var(--a);font-weight:700">{e(s['cta'])} ↑</a></p></div></section>"""
    return page(s, s["title"], body)

def thanks(s):
    body = f"""<div class="hero"><div class="wrap"><h1>You're on the list</h1>
<p class="lead">Thanks. We'll email you once when {html.escape(s['name'])} is ready. Early sign-ups get first access.</p>
<p><a href="/" style="color:var(--a);font-weight:700">← Back</a></p></div></div>"""
    return page(s, f"Thanks | {s['name']}", body, conversion=True, index=False)

def privacy(s):
    n = html.escape(s["name"])
    body = f"""<section><div class="wrap"><h1>Privacy</h1>
<p>When you join the {n} early list we collect your email address and the answers you choose in the form.</p>
<p>We use them only to tell you when {n} launches and to understand what people need. We don't sell or share them, and we don't send marketing from anyone else.</p>
<p>The form is stored by our website host, Netlify. If we run ads, Google may record that a visit came from an ad.</p>
<p>To have your details deleted, reply to any email we send you and ask. We'll delete them within 7 days.</p>
<p>Last updated 30 October 2026.</p></div></section>"""
    return page(s, f"Privacy | {s['name']}", body)

for s in SITES:
    d = OUT / s["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(index(s))
    (d / "thanks.html").write_text(thanks(s))
    (d / "privacy.html").write_text(privacy(s))
    (d / "robots.txt").write_text("User-agent: *\nAllow: /\n")
    print("built", d)
