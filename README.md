# Accel Financial — marketing site

The landing page for **Accel Financial Services**: business accounts, corporate cards, treasury,
global payments, credit, and the Accel Pilot AI finance co-pilot.

Plain HTML, CSS and JavaScript. No build step, no dependencies.

```
index.html          the landing page
404.html            not-found page
assets/styles.css   all styles (light + dark theme tokens at the top)
assets/app.js       interactions: mobile menu, treasury calculator, pricing toggle,
                    Pilot chat replies, payment-rail ticker, counters, email form
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

Announcement bar · header · hero with live dashboard mockup · customer logos · live payment-rail
ticker (open/closed computed from New York time) · product bento (Operating, Card, Treasury,
Global Pay, Capital) · interactive treasury yield calculator · Accel Pilot AI chat demo ·
3-step onboarding · Accel Advisory services · security & stats · customer stories · pricing with
monthly/annual toggle · FAQ · signup CTA · footer.

## Before going live

- **Placeholder content.** Product names, rates (4.12% APY), stats, customer logos and
  testimonials are invented for this draft. Replace them with real, approved figures.
- **Compliance.** Have counsel review the disclosures in the footer and FAQ, especially anything
  about partner banks, deposit insurance and yield.
- **Signup form.** The email form validates and confirms in the browser only. To collect leads,
  point it at a form backend (Formspree, HubSpot, Basin, your own API) in `assets/app.js`.
- **Links.** Sign in, Careers, Press, API docs, Status, Privacy, Terms and Disclosures currently
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
