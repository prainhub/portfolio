/* Prajin S — Portfolio interactivity. Vanilla JS, no dependencies. */
(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var lenisInstance = null;

  /* ---------------- Loader ---------------- */
  function initLoader() {
    var loader = document.getElementById("loader");
    if (!loader) return;
    var bar = loader.querySelector(".loader-bar span");
    document.body.classList.add("is-loading");
    requestAnimationFrame(function () {
      if (bar) bar.style.width = "100%";
    });
    var hidden = false;
    var hide = function () {
      if (hidden) return;
      hidden = true;
      loader.classList.add("is-hidden");
      document.body.classList.remove("is-loading");
      document.dispatchEvent(new CustomEvent("portfolio:loaded"));
    };
    var minDelay = prefersReducedMotion ? 0 : 550;
    window.setTimeout(function () {
      if (document.readyState === "complete") {
        hide();
      } else {
        window.addEventListener("load", hide, { once: true });
      }
    }, minDelay);
    // Safety net so a slow asset never traps the user behind the loader.
    window.setTimeout(hide, 3500);
  }

  /* ---------------- Smooth scroll (Lenis, wheel/trackpad only) --------- */
  function initSmoothScroll() {
    if (prefersReducedMotion || typeof window.Lenis !== "function") return;
    lenisInstance = new window.Lenis({
      duration: 1.1,
      smoothWheel: true,
      syncTouch: false, // keep native touch scrolling on mobile — better feel + battery
    });
    function raf(time) {
      lenisInstance.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
  }

  /* ---------------- Sticky nav (scroll shadow only — active state is
     driven by which panel is open, see initPanels) ---------------- */
  function initNav() {
    var nav = document.querySelector(".nav");
    if (!nav) return;
    var onScroll = function () {
      nav.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------- Theme toggle (dark/light, persisted) ---------------
     The <html> element's data-theme is already set pre-paint by the
     inline script in base.html (localStorage, default dark) — this just
     wires the button to flip it and remember the choice. */
  function initThemeToggle() {
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    var root = document.documentElement;
    var metaTheme = document.querySelector('meta[name="theme-color"]');
    var themeColors = { dark: "#0a0a0d", light: "#f7f6f2" };

    function apply(theme) {
      root.setAttribute("data-theme", theme);
      btn.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
      btn.setAttribute("aria-label", theme === "light" ? "Switch to dark theme" : "Switch to light theme");
      if (metaTheme) metaTheme.setAttribute("content", themeColors[theme] || themeColors.dark);
    }

    apply(root.getAttribute("data-theme") === "light" ? "light" : "dark");

    btn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      try {
        localStorage.setItem("theme", next);
      } catch (e) {
        // Storage unavailable (private browsing etc) — theme still flips
        // for this page view, it just won't persist across reloads.
      }
      apply(next);
    });
  }

  /* ---------------- Mobile menu ---------------- */
  function initMobileMenu() {
    var toggle = document.querySelector(".nav-toggle");
    var menu = document.querySelector(".mobile-menu");
    if (!toggle || !menu) return;
    function close() {
      toggle.classList.remove("is-active");
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }
    function open() {
      toggle.classList.add("is-active");
      menu.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    }
    toggle.addEventListener("click", function () {
      if (menu.classList.contains("is-open")) close();
      else open();
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", close);
    });
    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  /* ---------------- Side panels (About/Experience/Skills/Projects/AI/
     Education/Certifications/Contact) — slide-in drawers instead of a
     long scroll. Any link whose hash matches a .side-panel id opens that
     panel; "#home" (no matching panel) just closes and scrolls to top. --- */
  function initPanels() {
    var backdrop = document.querySelector(".panel-backdrop");
    var panels = document.querySelectorAll(".side-panel");
    if (!backdrop || !panels.length) return;

    var active = null;
    var opener = null;
    var navSelectors = ".nav-link, .mobile-menu a";

    function setActiveNav(id) {
      document.querySelectorAll(navSelectors).forEach(function (link) {
        var hash = (link.getAttribute("href") || "").split("#")[1];
        link.classList.toggle("is-active", id ? hash === id : hash === "home");
      });
    }

    function trapFocus(e) {
      if (e.key !== "Tab" || !active) return;
      var focusable = active.querySelectorAll(
        'a[href], button:not([disabled]), input, textarea, select, [tabindex]:not([tabindex="-1"])'
      );
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    function closePanel() {
      if (!active) return;
      active.classList.remove("is-open");
      active.setAttribute("aria-hidden", "true");
      backdrop.classList.remove("is-open");
      document.body.classList.remove("panel-open");
      if (lenisInstance) lenisInstance.start();
      setActiveNav(null);
      if (opener && typeof opener.focus === "function") opener.focus();
      active = null;
      opener = null;
      if (location.hash) history.pushState(null, "", location.pathname + location.search);
    }

    function openPanel(id, triggerEl) {
      var panel = document.getElementById(id);
      if (!panel || !panel.classList.contains("side-panel")) return false;
      if (active === panel) return true;
      if (active) {
        active.classList.remove("is-open");
        active.setAttribute("aria-hidden", "true");
      }
      opener = triggerEl || document.activeElement;
      active = panel;
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      backdrop.classList.add("is-open");
      document.body.classList.add("panel-open");
      // Belt-and-suspenders: data-lenis-prevent (on .side-panel) already
      // tells Lenis to leave the panel's own scroll alone, but fully
      // pausing Lenis while a panel is open removes any chance of it
      // intercepting the wheel/touch event before that check runs.
      if (lenisInstance) lenisInstance.stop();
      setActiveNav(id);
      var closeBtn = panel.querySelector(".panel-close");
      if (closeBtn) closeBtn.focus();
      return true;
    }

    document.addEventListener("click", function (e) {
      var link = e.target.closest("a[href*='#']");
      if (!link) return;
      var url;
      try {
        url = new URL(link.href, location.href);
      } catch (err) {
        return;
      }
      if (url.pathname !== location.pathname || !url.hash) return;
      var id = url.hash.slice(1);
      if (document.getElementById(id) && document.getElementById(id).classList.contains("side-panel")) {
        e.preventDefault();
        openPanel(id, link);
        history.pushState(null, "", "#" + id);
      } else if (id === "home") {
        e.preventDefault();
        closePanel();
        if (lenisInstance) lenisInstance.scrollTo(0, { duration: 1 });
        else window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
        history.pushState(null, "", location.pathname + location.search);
      }
    });

    backdrop.addEventListener("click", closePanel);
    panels.forEach(function (panel) {
      var closeBtn = panel.querySelector(".panel-close");
      if (closeBtn) closeBtn.addEventListener("click", closePanel);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closePanel();
      trapFocus(e);
    });
    window.addEventListener("popstate", function () {
      var id = location.hash.slice(1);
      if (id && document.getElementById(id) && document.getElementById(id).classList.contains("side-panel")) {
        openPanel(id);
      } else {
        closePanel();
      }
    });

    if (location.hash) {
      var initialId = location.hash.slice(1);
      openPanel(initialId);
    } else if (document.body.getAttribute("data-open-panel")) {
      // Server-rendered state (e.g. a non-JS contact form fallback POST)
      // asked a specific panel to be open on load.
      var wantedId = document.body.getAttribute("data-open-panel");
      openPanel(wantedId);
      history.replaceState(null, "", "#" + wantedId);
    }
  }

  /* ---------------- Scroll reveal (text/cards + media clip-reveal) ------ */
  function initReveal() {
    var items = document.querySelectorAll(".reveal, .reveal-media");
    if (!items.length) return;
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      items.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }
    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    items.forEach(function (el, i) {
      var group = el.closest(".reveal-stagger");
      if (group) el.style.setProperty("--i", Array.prototype.indexOf.call(group.children, el));
      observer.observe(el);
    });
  }

  /* ---------------- Magnetic buttons (desktop, fine pointer) ----------- */
  function initMagnetic() {
    var isFinePointer = window.matchMedia("(pointer: fine)").matches;
    if (!isFinePointer || prefersReducedMotion) return;
    var targets = document.querySelectorAll(".btn-primary, .btn-outline");
    targets.forEach(function (el) {
      el.classList.add("is-magnetic");
      var pull = 0.35;
      var max = 12;
      el.addEventListener("mousemove", function (e) {
        var rect = el.getBoundingClientRect();
        var relX = e.clientX - (rect.left + rect.width / 2);
        var relY = e.clientY - (rect.top + rect.height / 2);
        var x = Math.max(Math.min(relX * pull, max), -max);
        var y = Math.max(Math.min(relY * pull, max), -max);
        el.style.transform = "translate(" + x + "px," + y + "px)";
      });
      el.addEventListener("mouseleave", function () {
        el.style.transform = "";
      });
    });
  }

  /* ---------------- Hero kinetic text reveal ---------------------------- */
  function initHeroReveal() {
    var heading = document.querySelector(".hero-poster-title");
    if (!heading) return;
    if (prefersReducedMotion) return;

    var text = heading.textContent.trim();
    var words = text.split(/\s+/);
    heading.textContent = "";
    heading.setAttribute("aria-label", text);
    words.forEach(function (word, i) {
      var mask = document.createElement("span");
      mask.className = "word-mask";
      var inner = document.createElement("span");
      inner.className = "word";
      inner.style.setProperty("--word-delay", i * 90 + "ms");
      inner.textContent = word;
      inner.setAttribute("aria-hidden", "true");
      mask.appendChild(inner);
      heading.appendChild(mask);
      if (i < words.length - 1) heading.appendChild(document.createTextNode(" "));
    });

    function reveal() {
      heading.querySelectorAll(".word-mask").forEach(function (mask) {
        mask.classList.add("is-revealed");
      });
    }
    if (document.body.classList.contains("is-loading")) {
      document.addEventListener("portfolio:loaded", reveal, { once: true });
    } else {
      requestAnimationFrame(reveal);
    }
  }

  /* ---------------- Project filter ---------------- */
  function initProjectFilter() {
    var buttons = document.querySelectorAll(".filter-btn");
    var cards = document.querySelectorAll(".project-card");
    if (!buttons.length) return;
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        buttons.forEach(function (b) {
          b.classList.remove("is-active");
        });
        btn.classList.add("is-active");
        var filter = btn.getAttribute("data-filter");
        cards.forEach(function (card) {
          var match = filter === "all" || card.getAttribute("data-category") === filter;
          card.classList.toggle("is-hidden", !match);
        });
      });
    });
  }

  /* ---------------- Skills tabs ---------------- */
  function initSkillTabs() {
    var tabs = document.querySelectorAll(".skills-tab");
    var panels = document.querySelectorAll(".skills-panel");
    if (!tabs.length) return;
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (t) {
          t.classList.remove("is-active");
        });
        tab.classList.add("is-active");
        var target = tab.getAttribute("data-tab");
        panels.forEach(function (panel) {
          panel.classList.toggle("is-active", panel.getAttribute("data-panel") === target);
        });
      });
    });
  }

  /* ---------------- Email links: copy to clipboard on click -------------
     mailto: only does anything if the visitor's OS/browser has a default
     mail app registered — plenty don't (webmail-only users especially).
     Leave the mailto: href alone (it still fires for anyone who does have
     one) and additionally copy the address so it's always usable. */
  function initEmailCopy() {
    var links = document.querySelectorAll('a[href^="mailto:"]');
    if (!links.length) return;

    var toast = document.createElement("div");
    toast.className = "email-copy-toast";
    toast.setAttribute("role", "status");
    toast.setAttribute("aria-live", "polite");
    document.body.appendChild(toast);
    var hideTimer = null;

    function copyText(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text);
      }
      return new Promise(function (resolve, reject) {
        try {
          var ta = document.createElement("textarea");
          ta.value = text;
          ta.style.position = "fixed";
          ta.style.opacity = "0";
          document.body.appendChild(ta);
          ta.focus();
          ta.select();
          document.execCommand("copy");
          document.body.removeChild(ta);
          resolve();
        } catch (e) {
          reject(e);
        }
      });
    }

    links.forEach(function (link) {
      link.addEventListener("click", function () {
        var email = link.getAttribute("href").replace(/^mailto:/, "").split("?")[0];
        if (!email) return;
        copyText(email)
          .then(function () {
            toast.textContent = "Copied " + email + " to clipboard";
            toast.classList.add("is-visible");
            window.clearTimeout(hideTimer);
            hideTimer = window.setTimeout(function () {
              toast.classList.remove("is-visible");
            }, 2200);
          })
          .catch(function () {
            /* Clipboard unavailable — mailto: already fired above, nothing more to do. */
          });
      });
    });
  }

  /* ---------------- Contact form (fetch, graceful fallback) ------------ */
  function initContactForm() {
    var form = document.getElementById("contact-form");
    if (!form) return;
    var status = form.querySelector(".form-status");
    var submitBtn = form.querySelector("button[type='submit']");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      form.classList.add("is-submitting");
      if (submitBtn) submitBtn.disabled = true;
      status.className = "form-status";
      status.textContent = "";
      form.querySelectorAll(".field-error").forEach(function (el) {
        el.remove();
      });

      fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          Accept: "application/json",
        },
        body: new FormData(form),
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          });
        })
        .then(function (result) {
          if (result.ok && result.data.ok) {
            status.textContent = result.data.message || "Thanks — your message has been sent.";
            status.className = "form-status is-success";
            form.reset();
          } else {
            var errors = (result.data && result.data.errors) || {};
            var messages = [];
            Object.keys(errors).forEach(function (field) {
              (errors[field] || []).forEach(function (err) {
                messages.push((err && err.message) || err);
              });
            });
            status.textContent = messages.length
              ? messages.join(" ")
              : "Something went wrong — please check the form and try again.";
            status.className = "form-status is-error";
          }
        })
        .catch(function () {
          status.textContent = "Network error — please try again in a moment.";
          status.className = "form-status is-error";
        })
        .finally(function () {
          form.classList.remove("is-submitting");
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }

  /* ---------------- Hero node network (canvas, lightweight) ------------ */
  function initHeroCanvas() {
    var canvas = document.querySelector(".node-canvas");
    if (!canvas || prefersReducedMotion) return;
    var ctx = canvas.getContext("2d");
    var nodes = [];
    var NODE_COUNT = 26;
    var width, height, dpr;

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = canvas.clientWidth;
      height = canvas.clientHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function seed() {
      nodes = [];
      for (var i = 0; i < NODE_COUNT; i++) {
        nodes.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.25,
          vy: (Math.random() - 0.5) * 0.25,
          r: Math.random() * 1.6 + 1,
        });
      }
    }

    var accent = "124, 108, 255";

    function frame() {
      ctx.clearRect(0, 0, width, height);
      nodes.forEach(function (n) {
        n.x += n.vx;
        n.y += n.vy;
        if (n.x < 0 || n.x > width) n.vx *= -1;
        if (n.y < 0 || n.y > height) n.vy *= -1;
      });
      for (var i = 0; i < nodes.length; i++) {
        for (var j = i + 1; j < nodes.length; j++) {
          var a = nodes[i], b = nodes[j];
          var dx = a.x - b.x, dy = a.y - b.y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          var maxDist = width * 0.22;
          if (dist < maxDist) {
            ctx.strokeStyle = "rgba(" + accent + "," + (1 - dist / maxDist) * 0.35 + ")";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }
      nodes.forEach(function (n) {
        ctx.fillStyle = "rgba(" + accent + ",0.85)";
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fill();
      });
      requestAnimationFrame(frame);
    }

    resize();
    seed();
    frame();
    window.addEventListener(
      "resize",
      function () {
        resize();
        seed();
      },
      { passive: true }
    );
  }

  /* ---------------- Cycling role headline (hero) ------------------------ */
  function initRoleCycle() {
    var container = document.querySelector("[data-role-cycle]");
    if (!container || prefersReducedMotion) return;
    var spans = container.querySelectorAll("span");
    if (spans.length < 2) return;
    var index = 0;
    setInterval(function () {
      spans[index].classList.remove("is-active");
      index = (index + 1) % spans.length;
      spans[index].classList.add("is-active");
    }, 2600);
  }

  /* ---------------- Snapshot counters (real DB-backed numbers only) ---- */
  function initCounters() {
    var items = document.querySelectorAll("[data-countup]");
    if (!items.length) return;
    function animate(el) {
      var target = parseInt(el.getAttribute("data-countup"), 10) || 0;
      if (prefersReducedMotion || target === 0) {
        el.textContent = target;
        return;
      }
      var start = null;
      var duration = 900;
      function step(ts) {
        if (start === null) start = ts;
        var progress = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(eased * target);
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    if (!("IntersectionObserver" in window)) {
      items.forEach(animate);
      return;
    }
    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animate(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.6 }
    );
    items.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ---------------- Init ---------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initLoader();
    initSmoothScroll();
    initNav();
    initThemeToggle();
    initMobileMenu();
    initPanels();
    initReveal();
    initMagnetic();
    initHeroReveal();
    initRoleCycle();
    initProjectFilter();
    initSkillTabs();
    initEmailCopy();
    initContactForm();
    initHeroCanvas();
    initCounters();
  });
})();
