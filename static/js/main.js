/* Prajin S — Portfolio interactivity. Vanilla JS, no dependencies. */
(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- Loader ---------------- */
  function initLoader() {
    var loader = document.getElementById("loader");
    if (!loader) return;
    var bar = loader.querySelector(".loader-bar span");
    document.body.classList.add("is-loading");
    requestAnimationFrame(function () {
      if (bar) bar.style.width = "100%";
    });
    var hide = function () {
      loader.classList.add("is-hidden");
      document.body.classList.remove("is-loading");
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

  /* ---------------- Theme toggle ---------------- */
  function initTheme() {
    var root = document.documentElement;
    var toggles = document.querySelectorAll("[data-theme-toggle]");
    var stored = null;
    try {
      stored = localStorage.getItem("portfolio-theme");
    } catch (e) {
      /* storage unavailable — fall back to default dark theme */
    }
    if (stored === "light" || stored === "dark") {
      root.setAttribute("data-theme", stored);
    }
    function currentTheme() {
      return root.getAttribute("data-theme") === "light" ? "light" : "dark";
    }
    function apply(theme) {
      root.setAttribute("data-theme", theme);
      toggles.forEach(function (btn) {
        btn.textContent = theme === "light" ? "🌙" : "☀️";
        btn.setAttribute("aria-label", theme === "light" ? "Switch to dark mode" : "Switch to light mode");
      });
      try {
        localStorage.setItem("portfolio-theme", theme);
      } catch (e) {
        /* ignore */
      }
    }
    apply(currentTheme());
    toggles.forEach(function (btn) {
      btn.addEventListener("click", function () {
        apply(currentTheme() === "light" ? "dark" : "light");
      });
    });
  }

  /* ---------------- Sticky nav + active section ---------------- */
  function initNav() {
    var nav = document.querySelector(".nav");
    if (!nav) return;
    var onScroll = function () {
      nav.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    var links = document.querySelectorAll(".nav-link[href^='#'], .mobile-menu a[href^='#']");
    var sections = [];
    links.forEach(function (link) {
      var id = link.getAttribute("href").slice(1);
      var section = document.getElementById(id);
      if (section) sections.push({ link: link, section: section });
    });
    if (sections.length && "IntersectionObserver" in window) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            sections.forEach(function (item) {
              item.link.classList.toggle("is-active", item.section === entry.target);
            });
          });
        },
        { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
      );
      sections.forEach(function (item) {
        observer.observe(item.section);
      });
    }
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

  /* ---------------- Smooth anchor scroll (offset for fixed nav) --------- */
  function initSmoothAnchors() {
    var navHeight = 84;
    document.querySelectorAll("a[href^='#']").forEach(function (link) {
      link.addEventListener("click", function (e) {
        var id = link.getAttribute("href");
        if (id.length < 2) return;
        var target = document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        var top = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
        window.scrollTo({ top: top, behavior: prefersReducedMotion ? "auto" : "smooth" });
        history.pushState(null, "", id);
      });
    });
  }

  /* ---------------- Scroll reveal ---------------- */
  function initReveal() {
    var items = document.querySelectorAll(".reveal");
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

  /* ---------------- Custom cursor (desktop, fine pointer only) --------- */
  function initCursor() {
    var isFinePointer = window.matchMedia("(pointer: fine)").matches;
    if (!isFinePointer || prefersReducedMotion) return;
    var dot = document.createElement("div");
    var ring = document.createElement("div");
    dot.className = "cursor-dot";
    ring.className = "cursor-ring";
    document.body.append(dot, ring);
    document.body.classList.add("has-custom-cursor");

    var mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;
    window.addEventListener("mousemove", function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.transform = "translate(" + mouseX + "px," + mouseY + "px) translate(-50%,-50%)";
    });
    (function loop() {
      ringX += (mouseX - ringX) * 0.18;
      ringY += (mouseY - ringY) * 0.18;
      ring.style.transform = "translate(" + ringX + "px," + ringY + "px) translate(-50%,-50%)";
      requestAnimationFrame(loop);
    })();

    var hoverables = "a, button, .filter-btn, .skills-tab, input, textarea";
    document.addEventListener("mouseover", function (e) {
      if (e.target.closest && e.target.closest(hoverables)) ring.classList.add("is-active");
    });
    document.addEventListener("mouseout", function (e) {
      if (e.target.closest && e.target.closest(hoverables)) ring.classList.remove("is-active");
    });
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
    initTheme();
    initNav();
    initMobileMenu();
    initSmoothAnchors();
    initReveal();
    initCursor();
    initProjectFilter();
    initSkillTabs();
    initContactForm();
    initHeroCanvas();
    initCounters();
  });
})();
