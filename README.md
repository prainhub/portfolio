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
- **Project → image / screenshots** — used on the Projects section card and
  the project detail page.
- **Project → hero_image** — a separate image shown only in the homepage
  hero's floating side cards (first 4 projects, 2 per side), independent
  of the main project image. Falls back to a plain category label
  ("AI", "Full Stack", etc.) if left blank.
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
3. Dashboard → **New +** → **Blueprint** → pick the repo → **Apply**.
   Render reads `render.yaml`, creates the web service + database, and
   generates a real `SECRET_KEY` automatically.
4. First deploy takes a few minutes (installs deps, runs migrations,
   collects static files, seeds the real portfolio content). When it's
   done you'll have a live URL like `https://prajin-portfolio.onrender.com`.
5. (Optional, for `/admin/`) Open a shell for the service — dashboard →
   **Shell** tab — and run:
   ```bash
   python manage.py createsuperuser
   ```
6. (Optional) Custom domain: dashboard → **Settings** → **Custom Domains**,
   then set `SITE_DOMAIN` / `SITE_URL` env vars to match.

**Uploaded images will not survive a redeploy on the free plan.** Render's
free web service has an *ephemeral* filesystem — anything written at
runtime (profile photo/illustration uploaded via `/admin/`, or any project
image not already committed to `media/` in git) is wiped on the next
deploy or restart. Resume PDFs and project images already committed to
the repo (`media/resume/`, `media/projects/` — see `.gitignore`) are fine,
since those ship with the code. For photos/illustrations you upload via
admin to actually persist long-term, either re-upload them after each
redeploy, or move to persistent storage later (a Render paid disk, or an
object store like Cloudinary/S3 via `django-storages` — ask if you want
this wired up).

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
