# Prajin S — Portfolio

A full-stack personal portfolio built with **Python + Django**, presenting Prajin S
as a fresher Python Developer / Junior AI Engineer. Every piece of professional
content (projects, experience, education, skills, certifications) is stored in
the database and editable from the Django admin — nothing is hardcoded into the
templates. Content is sourced entirely from the resume; see
[`PORTFOLIO_PLAN.md`](PORTFOLIO_PLAN.md) for the content map.

## Features

- Django-templated, server-rendered site (no SPA build step) with a hand-built
  dark-first design system, light mode toggle (persisted in `localStorage`),
  and a restrained motion system (loader, scroll-reveal, magnetic-ish hover,
  custom cursor on desktop) — all respecting `prefers-reduced-motion`.
- Content-managed via Django models: `Profile`, `SocialLink`, `Experience`,
  `Project` (+ features/screenshots), `Skill`, `Education`, `Certification`,
  `CurrentlyLearning`, `ContactMessage`.
- Project detail pages (`/projects/<slug>/`) with problem → solution →
  architecture → challenges → future improvements, generated from real project
  data.
- Contact form with server-side validation, DB storage, and a JS `fetch()`
  submission (graceful HTML-form fallback without JS).
- Optional read-only JSON API (`/api/projects/`, `/api/skills/`,
  `/api/experience/`, `/api/contact/`) — no DRF, just `JsonResponse`.
- SEO: per-page meta/Open Graph/Twitter tags, JSON-LD (`Person`, `WebSite`,
  `SoftwareApplication` on project pages), `sitemap.xml`, `robots.txt`.
- GitHub activity section that only renders if `GITHUB_USERNAME` is set, and
  fails silently (hides itself) if the GitHub API is unreachable.
- Custom, on-brand `404.html` / `500.html` (only used when `DEBUG=False`).
- Environment-driven settings (`.env`), WhiteNoise for production static
  files, security hardening that activates automatically when `DEBUG=False`.

## Tech stack

- **Backend:** Python, Django 5, Django ORM, SQLite (dev) / PostgreSQL-ready (prod)
- **Frontend:** Django templates, hand-written CSS (no Tailwind build step —
  see rationale in `PORTFOLIO_PLAN.md`), vanilla JavaScript (loader, theme
  toggle, mobile nav, scroll-reveal, magnetic buttons, custom cursor,
  kinetic hero text reveal, project filter, contact form) plus a single
  vendored dependency, [Lenis](https://github.com/darkroomengineering/lenis)
  (self-hosted at `static/js/vendor/`, not loaded from a CDN), for smooth-scroll
  physics — disabled automatically under `prefers-reduced-motion`
- **Static/media:** WhiteNoise (compressed, hashed static files), Pillow for
  image fields
- **Deployment:** gunicorn/uvicorn-ready WSGI/ASGI entrypoints

## Project structure

```
portfolio/
├── manage.py
├── requirements.txt
├── .env.example
├── PORTFOLIO_PLAN.md
├── config/            # settings, urls, wsgi, asgi
├── core/               # models, admin, views, urls, forms, seed command
│   └── management/commands/seed_portfolio.py
├── templates/
│   ├── base.html
│   ├── robots.txt
│   ├── 404.html / 500.html
│   └── core/ (home.html, project_detail.html)
├── static/{css,js,images,icons}
└── media/{resume,projects}
```

## Getting started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # then edit values as needed

python manage.py migrate
python manage.py seed_portfolio   # loads the real resume-driven content
python manage.py createsuperuser  # for /admin/ access

python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `/admin/` for content
management.

## Environment variables

See `.env.example` for the full list. Key ones:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key — generate a real one for production |
| `DEBUG` | `True` locally, `False` in production |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `DATABASE_URL` | Leave blank for SQLite; set `postgres://...` in production |
| `GITHUB_USERNAME` | Optional — enables the GitHub activity section |
| `RESUME_FILE_NAME` | Filename to look for in `media/resume/` |
| `EMAIL_*` | Contact form email delivery (defaults to console backend) |

Never commit `.env` — it's already in `.gitignore`.

## Replacing the resume

Drop your PDF at `media/resume/resume.pdf` (or set `RESUME_FILE_NAME` in
`.env` to a different filename). The "Download Resume" / "View Resume"
buttons detect the file automatically and hide themselves if it's missing —
nothing else to configure.

## Adding / editing content

Everything in `/admin/` is editable without touching code:

- **Projects** — add a `Project`, its `ProjectFeature` bullet points, and
  optional `ProjectScreenshot`s inline. `order` and `featured` control
  homepage placement.
- **Experience / Education / Certifications / Skills / CurrentlyLearning** —
  standard list/edit screens, with `order` fields for display order.
- **SocialLink** — add GitHub/LinkedIn/etc. rows here; the nav, hero, and
  footer render them automatically once present.
- **Profile → photo** — professional headshot, shown in the About section
  (framed portrait) and, if no `illustration` is set, centered in the hero
  inside the AI particle ring. Optional.
- **Profile → illustration** — a stylised/illustrated character image,
  shown centered in the hero between two rows of project screenshots
  (matches the current hero layout). Takes priority over `photo` in the
  hero when both are set. Optional — the hero falls back to the AI
  particle ring alone if neither is uploaded.
- **Profile → hero_background_video** — an optional looping video shown
  full-bleed beneath the hero headline, at full clarity (no dimming or
  fade treatment). Autoplays muted, loops, hidden entirely under
  `prefers-reduced-motion`. Keep it short (a few seconds), silent, and
  heavily compressed — a large file will hurt page load. `.mp4` (H.264)
  works in real browsers, but `.webm` (VP9) has broader guaranteed codec
  support (some Chromium builds, including headless/CI ones, lack a
  licensed H.264 decoder) — `.webm` is the safer choice if you're not
  sure. Uploads go through the same Cloudinary storage as your other
  images once `CLOUDINARY_URL`/the separate Cloudinary env vars are set
  (see "Deploying to Render"), using Cloudinary's video resource type.
- **Project → image / screenshots** — used on the Projects section card and
  the project detail page.
- **Project → hero_image** — a separate image field, independent of the
  main project image. Currently unused on the homepage (the hero no
  longer shows flanking project cards) — kept in case that layout comes
  back; safe to leave blank.
- **ContactMessage** — read submissions and mark them read/unread from the
  admin; use the bulk actions for multiple messages at once.

Alternatively, edit `core/management/commands/seed_portfolio.py` and re-run
`python manage.py seed_portfolio` (it's idempotent — safe to re-run).

## Running checks

```bash
python manage.py check
python manage.py check --deploy   # run with DEBUG=False env vars for real output
python manage.py makemigrations --check
python manage.py migrate
python manage.py collectstatic --noinput
```

## Deployment

### Deploying to Render (recommended — free tier)

The repo includes `render.yaml`, a Render "Blueprint" that provisions the
web service and a free Postgres database together and wires them up
automatically.

1. Push this repo to your own GitHub account (fork it, or push this branch
   to a repo you own — Render deploys from a repo you control).
2. Create a free account at [render.com](https://render.com) and connect
   your GitHub account.
3. Before clicking Apply, get two things ready — Render will prompt for
   all of the vars below during the Blueprint setup screen (or you can
   fill them in anytime after under service → **Environment**):
   - A free **Cloudinary** account at [cloudinary.com](https://cloudinary.com)
     (no card required) → dashboard → **Account Details**, where you'll
     see your **Cloud name**, **API Key**, and **API Secret** listed
     separately — use those for `CLOUDINARY_CLOUD_NAME`,
     `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` (easier and less
     error-prone than assembling the combined URL yourself). Makes
     admin-uploaded images (Profile photo/illustration, Project images)
     actually stick — see the note below for why. (If you'd rather use
     the single combined string instead, that page also shows an **API
     Environment variable** field — that's `CLOUDINARY_URL`, and it takes
     precedence over the three separate values if you set both.)
   - Your own `/admin/` login: pick a `DJANGO_SUPERUSER_USERNAME`,
     `DJANGO_SUPERUSER_EMAIL`, and a real `DJANGO_SUPERUSER_PASSWORD`.
     **The free plan has no Shell tab** to run `createsuperuser`
     interactively (that needs a paid instance type) — these three env
     vars are how the account gets created instead (see
     `ensure_superuser` in the build command). It only runs once: your
     first deploy creates the account from these, and no later deploy
     will ever reset its password again, so changing it in `/admin/`
     afterward is safe.
4. Dashboard → **New +** → **Blueprint** → pick the repo → fill in the
   vars from step 3 → **Apply**. Render creates the web service +
   database and generates a real `SECRET_KEY` automatically.
5. First deploy takes a few minutes (installs deps, runs migrations,
   collects static files, seeds the real portfolio content, creates your
   admin login). When it's done you'll have a live URL like
   `https://prajin-portfolio.onrender.com`.
6. Go to `https://<your-service>.onrender.com/admin/`, log in with the
   `DJANGO_SUPERUSER_*` credentials from step 3, and upload your real
   photo/illustration/project images there. **Uploading locally on your
   own machine only writes to your local dev database — it never
   touches the live site.** Every image has to be uploaded once through
   the live `/admin/` too.
7. (Optional) Custom domain: dashboard → **Settings** → **Custom Domains**,
   then set `SITE_DOMAIN` / `SITE_URL` env vars to match.

**Why images can disappear without Cloudinary configured:** Render's free
web service has an *ephemeral* filesystem — anything written at runtime
(any image uploaded via `/admin/`) is wiped on the next deploy or
restart. With `CLOUDINARY_URL` set (see step 3), those uploads go to
Cloudinary instead of local disk, so they survive redeploys — do this
before uploading anything you want to keep. Resume PDFs and project
images already committed to the repo (`media/resume/`, `media/projects/`
— see `.gitignore`) are unaffected either way, since those ship with the
code itself.

The free Postgres database is also time-limited (Render will show the
exact expiry when it's created) — fine to get the site live now, but
you'll want to upgrade or recreate it before it expires.

### Deploying elsewhere (manual)

1. Set real env vars (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`,
   `DATABASE_URL`, `CSRF_TRUSTED_ORIGINS`, email settings).
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py collectstatic --noinput`
5. `python manage.py seed_portfolio` (idempotent — safe to re-run)
6. Serve with a real application server — **not** `manage.py runserver`:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   # or
   uvicorn config.asgi:application --host 0.0.0.0 --port 8000
   ```
7. Put a reverse proxy (nginx, Caddy, your platform's router) in front for
   TLS termination. With `DEBUG=False`, `SECURE_SSL_REDIRECT`, HSTS, and
   secure cookies are enabled automatically (see `config/settings.py`).

## Notes on content honesty

Every project, internship, skill, education entry, and certification on this
site comes directly from the resume behind it — nothing is invented. Sections
that the resume doesn't support (e.g. hackathons/achievements, GitHub/LinkedIn
links) are simply omitted or left as easy-to-fill admin fields rather than
padded with placeholder claims.
