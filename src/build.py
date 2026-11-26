"""Build the Accel group site: shared head, group switcher, header and footer around each page body.

Run from the repo root:  python3 src/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' "
        "height='32' rx='9' fill='%230F3B32'/%3E%3Cpath d='M9 23 16 9l7 14' fill='none' stroke='%23F6F7F3' "
        "stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M12.6 18h6.8' "
        "stroke='%23FF5B23' stroke-width='3.2' stroke-linecap='round'/%3E%3C/svg%3E")

MARK = ('<svg class="brand__mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" '
        'class="mark-bg"/><path d="M9 23 16 9l7 14" class="mark-a"/><path d="M12.6 18h6.8" class="mark-bar"/></svg>')

RF_MARK = ('<svg class="brand__mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" '
           'class="mark-bg"/><path d="M23.5 16a7.5 7.5 0 1 1-2.2-5.3" class="mark-a"/><path d="M22 6.8v4.4h-4.4" '
           'class="mark-a"/><circle cx="16" cy="16" r="2.2" class="mark-dot"/></svg>')


def brand_html(p):
    if p.get("brand") == "rf360":
        return (f'{RF_MARK}\n      <span class="brand__name brand__name--rf">Research Flow 360'
                f'<span class="brand__sub">Accel Financial Solutions</span></span>')
    return f'{MARK}\n      <span class="brand__name">Accel<span class="brand__sub">{p["sub"]}</span></span>'


BUSINESSES = [("trading", "trading.html", "1 · Trading"),
              ("research", "research.html", "2 · Research Flow 360"),
              ("signals", "signals.html", "3 · Signals")]

PAGES = {
    "index": dict(
        file="index.html", title="Accel Financial", sub="Financial",
        desc="Accel Financial is a group of four businesses built around one AI research engine: Accel Trading "
             "and Research Flow 360 now, Accel Signals and Accel Fund only after a verified record.",
        nav=[("#businesses", "Businesses"), ("#engine", "How they connect"), ("#later", "Signals & Fund"), ("#rules", "Group rules"),
             ("#faq", "FAQ")],
        cta=("#start", "Follow along")),
    "trading": dict(
        file="trading.html", title="Accel Trading", sub="Trading",
        desc="Accel Trading proves its AI strategies in public with its own money: 24 months of daily "
             "fingerprinted trade logs and independent verification before any outside capital.",
        nav=[("#plan", "The plan"), ("#proof", "How we prove it"), ("#strategies", "Strategies"),
             ("#letters", "Letters"), ("#faq", "FAQ")],
        cta=("#start", "Follow the record")),
    "signals": dict(
        file="signals.html", title="Accel Signals", sub="Signals",
        desc="Accel Signals is in development: daily strategy signals fingerprinted before every market open, "
             "to be licensed to institutions only after independent verification. Not an offer.",
        nav=[("#how", "How it will work"), ("#progress", "Where we are"), ("#rules", "Our rules"),
             ("#faq", "FAQ")],
        cta=("#start", "Get updates")),
    "research": dict(
        file="research.html", title="Research Flow 360", sub="Accel Financial Solutions", brand="rf360",
        desc="Research Flow 360 by Accel Financial Solutions: the stories that move markets, from Wall Street to "
             "Washington, in plain English every weekday before 7:00 am ET. Free, sourced, never stock tips.",
        nav=[("#inside", "What's inside"), ("#rules", "How we work"), ("#faq", "FAQ")],
        cta=("#start", "Subscribe free")),
}

FOOTER_LEGAL = (
    "Accel Financial is a group of separate businesses. Accel Trading trades only its own capital and does not "
    "manage money for others. Accel Signals is in development and is not available to anyone; Accel Fund does not "
    "exist. Both will only be considered after an independent firm verifies the trading record. Research Flow 360 publishes general "
    "market news, not personalized advice or recommendations to buy or sell any "
    "security. Nothing on this site is an offer to sell, or a solicitation of an offer to buy, any security or "
    "fund. Trading involves substantial risk of loss, and past results do not guarantee future results. "
    "Figures, charts, records, logs and letters shown are sample placeholders.")


def groupbar(current):
    links = []
    for key, href, label in BUSINESSES:
        cur = ' aria-current="page"' if key == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    home_cur = ' aria-current="page"' if current == "index" else ""
    return (f'<div class="announce groupbar">\n  <div class="wrap groupbar__in">\n'
            f'    <a href="index.html" class="groupbar__home"{home_cur}>Accel Financial</a>\n'
            f'    <nav class="groupbar__links" aria-label="Accel businesses">{"".join(links)}'
            f'<a href="index.html#later" class="groupbar__soon">4 · Fund: after verification</a></nav>\n'
            f'  </div>\n</div>')


def header(p):
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in p["nav"])
    cta_h, cta_t = p["cta"]
    return f'''<header class="header" id="top">
  <div class="wrap header__in">
    <a href="{p.get("home", "index.html")}" class="brand" aria-label="{p["title"]} home">
      {brand_html(p)}
    </a>
    <nav class="nav" id="nav" aria-label="Primary">
      {nav}
      <div class="nav__mobile-cta">
        <a href="{cta_h}" class="btn btn--primary">{cta_t}</a>
      </div>
    </nav>
    <div class="header__cta">
      <a href="{cta_h}" class="btn btn--primary btn--sm">{cta_t}</a>
    </div>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="nav">
      <span></span><span></span>
    </button>
  </div>
</header>'''


def footer():
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div class="footer__brand">
        <a href="index.html" class="brand" aria-label="Accel Financial home">
          {MARK}
          <span class="brand__name">Accel<span class="brand__sub">Financial</span></span>
        </a>
        <p>One research engine. Four businesses.</p>
      </div>
      <nav class="footer__cols" aria-label="Footer">
        <div><h4>Businesses</h4><a href="trading.html">1 · Accel Trading</a><a href="research.html">2 · Research Flow 360</a><a href="signals.html">3 · Accel Signals</a><a href="index.html#later">4 · Accel Fund</a></div>
        <div><h4>Read</h4><a href="research.html">Research Flow 360</a><a href="trading.html#plan">The 4-step plan</a><a href="trading.html#calculator">Skill or luck?</a></div>
        <div><h4>Group</h4><a href="index.html#rules">Group rules</a><a href="index.html#faq">FAQ</a><a href="index.html#start">Contact</a></div>
      </nav>
    </div>
    <div class="footer__legal">
      <p>{FOOTER_LEGAL}</p>
      <p class="footer__copy"><span>© <span id="year">2026</span> Accel Financial</span><span class="footer__links"><a href="index.html">Privacy</a><a href="index.html">Terms</a><a href="index.html">Disclosures</a></span></p>
    </div>
  </div>
</footer>'''


def page(key):
    p = PAGES[key]
    body = (SRC / f"{key}.body.html").read_text()
    head_title = p["title"]
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{head_title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{p["desc"]}">
<meta name="theme-color" content="#0F3B32">
<meta property="og:title" content="{head_title}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:type" content="website">
<link rel="icon" href="{ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Geist:wght@400..600&family=Geist+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

{groupbar(key)}

{header(p)}

{body.strip()}

{footer()}

<script src="assets/app.js"></script>
</body>
</html>
'''


RF_FOOTER_LEGAL = (
    "Research Flow 360 is published by Accel Financial Solutions, part of Accel Global Holdings. It publishes general "
    "market news for everyone; it is not investment advice and never recommends buying or selling any security. "
    "Sponsored content is labelled. Accel Media Ltd is an affiliated company and its stories are labelled when cited. "
    "Accel Trading results reported in the monthly section are for information only and are not an offer of any "
    "product. Sample issues shown on this page are illustrations.")


def rf_page():
    p = dict(PAGES["research"], home="#top")
    body = (SRC / "research.body.html").read_text()
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Research Flow 360</title>
<meta name="description" content="{p["desc"]}">
<meta name="theme-color" content="#0F3B32">
<meta property="og:title" content="Research Flow 360 · Accel Financial Solutions">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:url" content="https://researchflow360.com/">
<meta property="og:type" content="website">
<link rel="canonical" href="https://researchflow360.com/">
<link rel="icon" href="{RF_ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Geist:wght@400..600&family=Geist+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

<div class="announce groupbar">
  <div class="wrap groupbar__in">
    <span class="groupbar__home">Research Flow 360</span>
    <span class="groupbar__note">A publication of Accel Financial Solutions · part of Accel Global Holdings</span>
  </div>
</div>

{header(p)}

{body.strip()}

<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div class="footer__brand">
        <a href="#top" class="brand" aria-label="Research Flow 360 home">
          {brand_html(p)}
        </a>
        <p>The market, in five minutes. Before the open.</p>
      </div>
      <nav class="footer__cols" aria-label="Footer">
        <div><h4>Read</h4><a href="#inside">What's inside</a><a href="#rules">How we work</a><a href="#faq">FAQ</a></div>
        <div><h4>Subscribe</h4><a href="#start">Get the Daily Brief</a><a href="#start">Breaking alerts</a></div>
        <div><h4>Company</h4><a href="#faq">About us</a><a href="#start">Advertise</a><a href="#top">Privacy</a></div>
      </nav>
    </div>
    <div class="footer__legal">
      <p>{RF_FOOTER_LEGAL}</p>
      <p class="footer__copy"><span>© <span id="year">2026</span> Accel Financial Solutions · researchflow360.com</span><span class="footer__links"><a href="#top">Privacy</a><a href="#top">Terms</a></span></p>
    </div>
  </div>
</footer>

<script src="assets/app.js"></script>
</body>
</html>
'''


RF_ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' "
           "height='32' rx='9' fill='%230F3B32'/%3E%3Cpath d='M23.5 16a7.5 7.5 0 1 1-2.2-5.3M22 6.8v4.4h-4.4' fill='none' "
           "stroke='%23F6F7F3' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3Ccircle cx='16' "
           "cy='16' r='2.2' fill='%23FF5B23'/%3E%3C/svg%3E")


def build_rf360():
    import shutil
    out = ROOT / "researchflow360"
    (out / "assets").mkdir(parents=True, exist_ok=True)
    for name in ("styles.css", "app.js"):
        shutil.copyfile(ROOT / "assets" / name, out / "assets" / name)
    (out / "index.html").write_text(rf_page())
    (out / "CNAME").write_text("researchflow360.com\n")
    print("built researchflow360/index.html")


if __name__ == "__main__":
    for key, p in PAGES.items():
        (ROOT / p["file"]).write_text(page(key))
        print("built", p["file"])
    build_rf360()
