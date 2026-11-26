# Accel Financial — marketing site

The website for **Accel Financial**, a group of four businesses built around one AI research engine:

1. **Accel Trading** (live): AI strategies trading only the founders' capital for 24 months, with a
   daily trade-log fingerprint and independent verification. Page: `trading.html`.
2. **Research Flow 360** (launching, by Accel Financial Solutions): a free weekday market newsletter paid
   for by sponsors, plus a monthly Inside Accel Trading section. Page: `research.html`; standalone site for
   researchflow360.com in `researchflow360/` (see its README for hosting).
3. **Accel Signals** (in development): the signal engine in `signals/` fingerprints each day's
   signals before the open. Licensing to institutions opens only after verification. Page: `signals.html`.
4. **Accel Fund** (gated): a private fund, only after verification.

`index.html` is the group home page.

Plain HTML, CSS and JavaScript. No build step, no dependencies.

```
index.html          group home page (built)
trading.html        1 · Accel Trading (built)
research.html       2 · Research Flow 360 (built)
researchflow360/    standalone Research Flow 360 site for researchflow360.com (built)
signals.html        3 · Accel Signals (built)
signals/            the Accel Signals engine (Python, stdlib only); see signals/README.md
404.html            not-found page
src/build.py        builds the three pages from src/*.body.html with a shared head,
                    group switcher, header and footer
src/*.body.html     the page contents; edit these, then run: python3 src/build.py
assets/styles.css   all styles (light + dark theme tokens at the top)
assets/app.js       interactions shared by every page
.github/workflows/pages.yml   deploys to GitHub Pages on every push
```

## Run locally

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
```

## Publish on GitHub Pages

1. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Push to `main` (or re-run the "Deploy site to GitHub Pages" workflow).
3. The site goes live at `https://<owner>.github.io/<repo>/`.

## Before going live

- **Sample data.** The day counter, chart, fingerprints, letter and figures are placeholders.
  Wire them to the real daily log once trading starts, or keep the "Sample" labels.
- **No offers.** While trading only your own capital, the site must not offer a fund or
  investment. If you later raise a fund under Rule 506(c), have counsel review the site first.
- **Fingerprints.** Publish each day's SHA-256 of the full trade log (and keep the log itself)
  so the verifier can match them later.
- **Signup form.** The email form validates and confirms in the browser only. To collect leads,
  point it at a form backend (Formspree, HubSpot, Basin, your own API) in `assets/app.js`.
- **Links.** Log in, Careers, Press, Form CRS, Privacy, Terms and Disclosures currently
  point to the top of the page.

## Brand

| Token | Light | Use |
|---|---|---|
| Pine | `#0F3B32` | brand blocks, dashboard, featured plan |
| Signal | `#FF5B23` | accent: highlights, primary CTA on dark, chart line |
| Paper | `#F5F6F1` | page background |
| Ink | `#0C1F1B` | text, primary buttons |
| Mint / Sky | `#D3EEDF` / `#DCE7FB` | secondary product cards |

Type: **Bricolage Grotesque** (display), **Geist** (body), **Geist Mono** (numbers and labels),
all from Google Fonts. Dark mode follows the visitor's system setting.
