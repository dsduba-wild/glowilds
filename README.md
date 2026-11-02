# Glow Wild — glowilds.com

Hugo site built on the Hugo Hero theme (included in `themes/hugo-hero-theme`).

## Run it locally
1. Install Hugo **extended** (0.158 or newer).
   Also install [Dart Sass](https://github.com/sass/dart-sass/releases) so the `sass` command is on your PATH (CI uses 1.106.1).
2. In this folder run: `hugo server`
3. Open http://localhost:1313

## Put it online
Push to `main`. GitHub Actions (`.github/workflows/hugo.yml`) builds the site and publishes it to GitHub Pages at glowilds.com.

## Where to edit things
| What | File |
|---|---|
| Home hero headline and subline | `content/_index.md` |
| Home "One Connected System" labels | `pillar` in each `content/services/*.md` |
| Home "What This Looks Like" examples | `data/examples.yaml` (demonstrations, labeled as examples) |
| Home closing section | `content/homepage/about.md` |
| Sample check-up report | `content/sample-check-up.md` |
| How We Handle Your Data | `content/your-data.md` |
| Services page "one-time vs ongoing" | `content/services/_index.md` |
| Services (4) | `content/services/*.md` |
| Who We Help (industries) | `content/work/*.md` |
| How It Works (4 steps) | `content/pages/process/content1-4.md` |
| About | `content/pages/about/content2.md` (founder story), `content3.md` (Let’s Talk) |
| FAQ (questions and answers) | `data/faq.yaml` |
| Privacy Policy, Terms of Use | `content/privacy.md`, `content/terms.md` |
| Phone, email, hours | `data/contact.yaml` |
| Social links | `data/social.json` |
| Brand colors | `assets/scss/_bootstrap-variables.scss` (`$primary`) and the overrides at the bottom of `assets/scss/style.scss` |
| Logo | `static/images/logo.svg`, `static/images/logo-mobile.svg` |

## Still to fill in
- Google Business Profile link in `data/contact.yaml` (`googleProfile`): it goes into the business data Google reads
- Social links in `data/social.json` (empty for now): each entry needs `name`, `link` and `image` (an SVG you add under `static/social/`)
- Customer quotes in `data/testimonials.yaml` (real ones only; the homepage section is hidden until there's one)
- Photos of real people for the service pages (they all use the same drawn banner now)
- Swap the generated background images in `static/` for real photos whenever you have them
