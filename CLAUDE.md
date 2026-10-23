# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Marketing site for Glow Wild (glowilds.com), built with Hugo on the vendored Hugo Hero theme (`themes/hugo-hero-theme`). There is no JS build, package manager or test suite.

## Commands

- `hugo server`: local dev at http://localhost:1313. In server mode the CSS is linked with source maps; in production builds it's inlined.
- `hugo --minify`: production build, the same command CI runs. A clean build with no `ERROR` lines is the only automated check.
- `hugo --minify -d <tmpdir>`: build somewhere else for inspection. `public/` is gitignored and often stale; old dev builds there contain `localhost` URLs.
- Requires Hugo **extended**, 0.158 or newer. CI pins `HUGO_VERSION` in `.github/workflows/hugo.yml`.

## Deploy

Pushing to `main` builds the site and publishes it to GitHub Pages (the custom domain is glowilds.com). Check with `gh run list` / `gh run watch`. There is no staging environment.

## Architecture

- **Theme overrides:** files under `layouts/` shadow the same path in `themes/hugo-hero-theme/layouts/`. To change a theme template, copy it into `layouts/` and edit the copy; never edit the theme. The theme copies only exist where something was changed.
- **Headless bundles:** homepage sections come from `content/homepage/*.md`, and the About and How It Works page sections from `content/pages/{about,process}/content*.md`. They are ordered by `weight`, with a `background`, `button` and `buttonLink` in front matter, and rendered as "strips" by `layouts/index.html` and `layouts/pages/about.html`. Both pages use `layout: 'about'`.
- **Collections:** `content/services/` and `content/work/` (the "Who We Help" industries). Services marked `featured: true` show on the homepage. Each page sets `heroHeading`, `heroSubHeading` and `heroBackground`.
- **Site-wide data:** `data/contact.yaml` (email, phone, `formAction`, hours) and `data/testimonials.yaml`. Templates hide a block while its value is empty: the phone, the contact form and the testimonials section all stay hidden until filled. Keep that pattern for new optional content. Testimonials must be real quotes.
- **Booking button:** `layouts/partials/cta.html`, called as `{{ partial "cta.html" "<spacing class>" }}` from the homepage hero and the service and industry pages. The contact form's submit button has its own copy of the label.
- **Meta and SEO:** `layouts/partials/seo.html` adds the canonical link plus homepage-only JSON-LD built from `data/contact.yaml`. The homepage's `<meta>` tags come from `[params.homepage_meta_tags]` in `config.toml`. Every other page uses `layouts/partials/meta-default.html`.
- **Images:** pages load `.webp` from `static/`. The `og:image` swaps `.webp` for `.jpg` when a JPG copy exists, so a hero image should ship as both `.webp` and `.jpg`. With only a `.webp`, the preview falls back to the WebP.
- **Styles:** `assets/scss/style.scss` imports a trimmed Bootstrap (`_bootstrap-lite.scss`). Brand overrides are at the bottom of `style.scss`, and `$primary` is in `_bootstrap-variables.scss`. Sass is compiled by libsass, which Hugo has deprecated, so the build prints a deprecation `WARN`. Moving to dartsass would mean installing it in CI.
- **Page URLs:** `[permalinks] pages = "/:filename/"` makes `content/pages/about/` serve at `/about/`.
