# Accel Financial — marketing site

The public site for **Accel Financial Services**, an AI trading firm that proves its strategies
before taking outside money. The plan has four steps: trade only our own capital for 24 months
in public, have the record independently verified, then open a private fund for accredited
investors and license the signals to hedge funds. Every trading day's log is fingerprinted
(SHA-256) and published at the close, so the record can't be cherry-picked later.

Plain HTML, CSS and JavaScript. No build step, no dependencies.

```
index.html          the landing page
404.html            not-found page
assets/styles.css   all styles (light + dark theme tokens at the top)
assets/app.js       interactions: mobile menu, skill-vs-luck calculator, letter replies,
                    daily log ticker, email form
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

## Page sections

Announcement bar · header · hero with public track record (day X of 730, own capital vs
benchmark, daily log fingerprints) · log ticker · the 4-step plan · three proof rules (own capital,
daily fingerprints, independent verification) · three strategies with benchmarks and loss limits ·
skill-vs-luck calculator (confidence = Φ(Sharpe × √years)) · monthly letters · risk control ·
commitments · FAQ · follow-along signup · footer.

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
