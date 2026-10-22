# Glow Wild — glowilds.com

Hugo site built on the Hugo Hero theme (included in `themes/hugo-hero-theme`).

## Run it locally
1. Install Hugo **extended** (0.133 or newer).
2. In this folder run: `hugo server`
3. Open http://localhost:1313

## Put it online (GitHub + Netlify)
1. Push this whole folder to a GitHub repo.
2. In Netlify: Add new site → Import from GitHub → pick the repo. `netlify.toml` already has the build settings.
3. In Netlify → Domain settings, add `glowilds.com` and follow the DNS steps.

## Where to edit things
| What | File |
|---|---|
| Home hero headline | `content/_index.md` |
| Home sections | `content/homepage/work.md`, `content/homepage/about.md` |
| Services (6) | `content/services/*.md` |
| Who We Help (industries) | `content/work/*.md` |
| How It Works (4 steps) | `content/pages/process/content1-4.md` |
| About | `content/pages/about/content1-3.md` |
| Phone, email, hours | `data/contact.yaml` |
| Social links | `data/social.json` |
| Brand colors | `assets/scss/_bootstrap-variables.scss` (`$primary`) and the overrides at the bottom of `assets/scss/style.scss` |
| Logo | `static/images/logo.svg`, `static/images/logo-mobile.svg` |

## Still to fill in
- Real phone number and email in `data/contact.yaml` (currently placeholders)
- Social links in `data/social.json` (empty for now)
- Swap the generated background images in `static/` for real photos whenever you have them
