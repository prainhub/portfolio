# Portfolio Plan — Prajin S

Source of truth: resume pasted in conversation (2026-08-24). No GitHub/LinkedIn URL or
resume PDF was supplied — those are wired up as easy, empty-safe configuration points
(Django admin `SocialLink` rows, `media/resume/resume.pdf` drop-in) rather than invented.

## Content map

```
PROFILE
├── Name: Prajin S
├── Title: Python Developer | Junior AI Engineer
├── Location: Coimbatore, Tamil Nadu
├── Contact: prajinrp6@gmail.com · +91 76048 65376
├── Summary: final-year B.Tech IT student, AI-powered apps, Python backends
│            (OpenAI/Gemini APIs), FastAPI/Flask, REST API design
│
├── EXPERIENCE (internships)
│   ├── Data Science Intern — Pantech IT Solutions (Virtual), Mar 2025
│   └── Cybersecurity Intern — CodTech Solutions (Virtual), Jun–Jul 2025
│
├── PROJECTS
│   ├── IoT-Based Biometric Attendance System (2025–2026) — Full Stack / IoT
│   ├── AI-Powered Resume Analyzer (Feb 2026) — AI
│   ├── AI Chatbot (Jan 2026) — AI
│   └── URL Shortener Web App (Dec 2025) — Web
│
├── SKILLS
│   ├── AI/ML: Python (AI/ML), OpenAI API, Gemini API, NLP, Prompt Engineering,
│   │         ML Model Workflows, Data Preprocessing
│   ├── Backend: Flask, FastAPI, Node.js, Express.js, REST API Design, Django (this site)
│   ├── Frontend: React.js, JavaScript, HTML5, CSS3, Responsive UI
│   ├── Database: MongoDB, SQL, CRUD Operations, JSON Handling
│   ├── Cloud/Deploy: Netlify, GitHub Pages, API Integration
│   └── Tools: Git, GitHub, VS Code, Postman
│
├── EDUCATION
│   ├── B.Tech IT — Adithya Institute of Technology, Coimbatore (2022–2026), CGPA 7.8 (sem 7)
│   ├── HSC — NCP MPL HR Sec School, Dharapuram (2020–2021), 75%
│   └── SSLC — NCP MPL HR Sec School, Dharapuram (2018–2020), 73%
│
├── CERTIFICATIONS
│   ├── Python for Data Science & AI — Udemy, Jan 2025
│   ├── Web Design Fundamentals — Udemy, Jul 2025
│   └── SQL Fundamentals — GeeksforGeeks, 2025
│
└── SOCIAL LINKS
    └── Email only from resume. GitHub/LinkedIn left empty (admin-manageable, hidden if blank).
```

No hackathons/publications/leadership items are in the resume → Achievements section is
omitted rather than padded. No GitHub username supplied → GitHub activity block renders
only if `GITHUB_USERNAME` env var is set, and fails gracefully (try/except around the API
call) if the API is unreachable.

## Architecture

Django project `config`, single app `core` (models/admin/views/urls), server-rendered
templates (no SPA framework), hand-written CSS design system (no Tailwind build step — a
CDN runtime script would hurt performance/CSP for no real gain on a template-driven site;
a compiled Tailwind needs a node build pipeline this repo doesn't otherwise need), vanilla
JS modules for nav/theme/reveal/cursor/loader/contact-form. `django.contrib.sitemaps` +
static `robots.txt` view for SEO. Lightweight JSON endpoints under `/api/` (no DRF — the
payloads are simple reads, DRF would be dead weight).

## Models (core/models.py)
`Profile` (singleton-ish, holds name/title/summary/contact/CV file), `SocialLink`,
`Experience`, `Project` (+ `ProjectFeature`, `ProjectScreenshot` inlines), `Skill`
(category choices), `Education`, `Certification`, `CurrentlyLearning`, `ContactMessage`.

## Pages
`/` home — hero + quick snapshot only; About/Experience/Skills/Projects/
Education/Certifications/Contact each open as a slide-in side panel from the
nav (see "Navigation" below), not a long scroll. `/projects/<slug>/` project
detail (separate full page), `/resume/` view redirect, custom `404.html` /
`500.html`.

## Navigation — side panels
Every nav link (`#about`, `#experience`, `#skills`, `#projects`,
`#education`, `#certifications`, `#contact`) opens a `.side-panel` drawer
that slides in from the right over a dimmed backdrop, instead of scrolling
the page. Only one panel is open at a time; switching nav links swaps the
open panel directly. The panel sits below the fixed header, so the nav
stays visible and clickable while a panel is open. Handled by `initPanels()`
in `static/js/main.js`; markup lives in `templates/core/home.html` as
`<aside class="side-panel" id="...">` elements. Deep-linking a hash (e.g.
`/#projects`) opens that panel on load. Currently Learning is folded into
the About panel (as tags); GitHub Activity is folded into the Projects
panel (as a compact stat/repo strip); the standalone Resume section was
dropped in favor of the persistent header "Resume" button plus a
View/Download action inside the About panel.

## Implementation order
1. Django project skeleton, settings (env-driven), apps, base template, static dirs
2. Models + admin + migrations
3. Management command `seed_portfolio` loading the resume content map above
4. Design system: CSS tokens, typography, buttons/cards/badges/timeline/nav/footer
5. Home template sections 1–20 wired to real querysets
6. Project detail template + architecture visualization block
7. JS: loader, sticky nav + active-section indicator, theme toggle, mobile menu,
   scroll-reveal (IntersectionObserver), custom cursor (desktop, pointer:fine only),
   smooth anchor scroll, contact form fetch()
8. Contact form (Django form + view, validation, DB storage, JSON success/error)
9. SEO: meta/OG/Twitter tags, JSON-LD (Person/WebSite), sitemap.xml, robots.txt
10. Security/production settings via env vars, `.env.example`, custom error pages
11. `manage.py check`, `check --deploy`, makemigrations, migrate, collectstatic — fix
    everything actionable
