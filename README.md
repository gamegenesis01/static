# Accel Financial — marketing site

The landing page for **Accel Financial Services**, an AI-driven investment manager. Clients either
give Accel their money to manage (**Accel Managed**), or connect Accel's AI trading strategies to
their own brokerage account (**Accel AI Connect**). Institutions can license the models or a signal
API. **Accel Pilot** explains every trade in plain English.

Plain HTML, CSS and JavaScript. No build step, no dependencies.

```
index.html          the landing page
404.html            not-found page
assets/styles.css   all styles (light + dark theme tokens at the top)
assets/app.js       interactions: mobile menu, what-if calculator, Pilot chat replies,
                    market and bot ticker, counters, email form
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

Announcement bar · header · hero with AI strategy dashboard (strategy vs benchmark, bot activity) ·
social proof · market and bot ticker · two paths (Managed vs AI Connect) · three AI strategies
(Core, Momentum, Income) · what-if calculator (index vs index + edge − 1% fee) · Accel Pilot chat
demo · 3-step onboarding · risk control · safety & stats · client stories · pricing (AI Connect
$49/mo, Managed 1.0%/yr, Institutional) · FAQ · signup CTA · footer.

## Before going live

- **Performance claims.** Every return, back-test, statistic and client story is a placeholder.
  Under the SEC Marketing Rule, an adviser may only advertise performance it can substantiate,
  with standard periods and disclosures; hypothetical and back-tested results carry extra rules.
  Do not publish "our bots beat the market" until you have an audited live track record.
- **Compliance.** Investment advertising is regulated (SEC Marketing Rule, FINRA rules). Before
  launch, a compliance reviewer must approve every performance figure, testimonial and claim,
  and the footer disclosures must match the firm's real registrations.
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
