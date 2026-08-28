# Vendored third-party JS

Self-hosted (not loaded from a CDN) so the site has no runtime dependency on
an external host and keeps working offline/behind restrictive networks.

- **lenis.min.js** — [Lenis](https://github.com/darkroomengineering/lenis) v1.3.26, MIT License,
  © darkroom.engineering. Provides the smooth-scroll physics used site-wide;
  disabled automatically when the visitor has `prefers-reduced-motion` set
  (see `initSmoothScroll()` in `static/js/main.js`).
