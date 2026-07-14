(function () {
  "use strict";

  var burger = document.getElementById("burger");
  var links = document.getElementById("topnav-links");
  var backdrop = document.getElementById("nav-backdrop");
  function closeNav() {
    if (links) links.classList.remove("is-open");
    if (backdrop) backdrop.classList.remove("is-open");
    if (burger) { burger.classList.remove("is-open"); burger.setAttribute("aria-expanded", "false"); }
    document.documentElement.style.overflow = "";
  }
  function openNav() {
    if (links) links.classList.add("is-open");
    if (backdrop) backdrop.classList.add("is-open");
    if (burger) { burger.classList.add("is-open"); burger.setAttribute("aria-expanded", "true"); }
    document.documentElement.style.overflow = "hidden";
  }
  if (burger && links) {
    burger.addEventListener("click", function () {
      if (links.classList.contains("is-open")) closeNav(); else openNav();
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeNav);
    });
  }
  if (backdrop) backdrop.addEventListener("click", closeNav);
  window.addEventListener("resize", closeNav);
  /* Pages restored from the back/forward cache (common with cross-document
     View Transitions) can otherwise keep a stale "is-open" state from
     before navigation, making the menu appear stuck or unresponsive. */
  window.addEventListener("pageshow", closeNav);

  var topbar = document.getElementById("topbar");
  if (topbar) {
    window.addEventListener("scroll", function () {
      topbar.classList.toggle("is-solid", window.scrollY > 12);
    }, { passive: true });
  }

  var revealObserver;
  function observeReveals() {
    if (!revealObserver) {
      revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    }
    document.querySelectorAll(".reveal:not(.is-visible)").forEach(function (t) { revealObserver.observe(t); });
  }
  observeReveals();

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Labradorescence sheen: gentle mouse-follow highlight ---------- */
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var card = document.querySelector(".hero__card");
  if (card && !reduceMotion && window.matchMedia("(hover: hover)").matches) {
    card.addEventListener("mouseenter", function () {
      card.style.animationPlayState = "paused";
    });
    card.addEventListener("mousemove", function (e) {
      var rect = card.getBoundingClientRect();
      var x = ((e.clientX - rect.left) / rect.width) * 100;
      var y = ((e.clientY - rect.top) / rect.height) * 100;
      card.style.setProperty("--mx", x + "%");
      card.style.setProperty("--my", y + "%");
    });
    card.addEventListener("mouseleave", function () {
      card.style.animationPlayState = "running";
    });
  }

  /* ---------- Gregorian -> Jalali (Persian) calendar conversion ----------
     Small self-contained implementation (no external library needed). */
  function gregorianToJalali(gy, gm, gd) {
    var g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
    var jy = (gy <= 1600) ? 0 : 979;
    gy -= (gy <= 1600) ? 621 : 1600;
    var gy2 = (gm > 2) ? (gy + 1) : gy;
    var days = (365 * gy) + (Math.floor((gy2 + 3) / 4)) - (Math.floor((gy2 + 99) / 100)) +
      (Math.floor((gy2 + 399) / 400)) - 80 + gd + g_d_m[gm - 1];
    jy += 33 * Math.floor(days / 12053);
    days %= 12053;
    jy += 4 * Math.floor(days / 1461);
    days %= 1461;
    if (days > 365) {
      jy += Math.floor((days - 1) / 365);
      days = (days - 1) % 365;
    }
    var jm, jd;
    if (days < 186) {
      jm = 1 + Math.floor(days / 31);
      jd = 1 + (days % 31);
    } else {
      jm = 7 + Math.floor((days - 186) / 30);
      jd = 1 + ((days - 186) % 30);
    }
    return [jy, jm, jd];
  }

  var jalaliMonths = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"];
  var faDigits = ["۰","۱","۲","۳","۴","۵","۶","۷","۸","۹"];
  function toFaDigits(n) {
    return String(n).replace(/[0-9]/g, function (d) { return faDigits[+d]; });
  }

  /* ---------- Automatic "last updated" date, from GitHub commit history ---------- */
  var updatedEl = document.getElementById("last-updated");
  if (updatedEl) {
    var repoPath = updatedEl.getAttribute("data-path") || "resume/index.html";
    var lang = document.body.classList.contains("lang-fa") ? "fa" : "en";
    var apiUrl = "https://api.github.com/repos/amini-aria/amini-aria.github.io/commits?path=" + repoPath + "&page=1&per_page=1";

    fetch(apiUrl, { headers: { Accept: "application/vnd.github+json" } })
      .then(function (res) { if (!res.ok) throw new Error("api error"); return res.json(); })
      .then(function (data) {
        if (!data || !data[0] || !data[0].commit) return;
        var iso = data[0].commit.committer.date;
        var d = new Date(iso);
        var gy = d.getFullYear(), gm = d.getMonth() + 1, gd = d.getDate();

        if (lang === "fa") {
          var j = gregorianToJalali(gy, gm, gd);
          var shamsi = toFaDigits(j[2]) + " " + jalaliMonths[j[1] - 1] + " " + toFaDigits(j[0]);
          var miladi = d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
          updatedEl.textContent = "آخرین ویرایش: " + shamsi + " (" + miladi + " میلادی)";
        } else {
          var en = d.toLocaleDateString("en-US", { day: "numeric", month: "long", year: "numeric" });
          updatedEl.textContent = "Last updated: " + en;
        }
      })
      .catch(function () {
        updatedEl.textContent = "";
      });
  }

  /* ---------- Publications page: auto-mirror sections from the resume page ----------
     Single source of truth stays the resume page. This just fetches its HTML
     (same-origin) and clones the matching .resume__block sections in place,
     so nothing has to be typed twice. */
  var mirrorMount = document.getElementById("mirror-mount");
  if (mirrorMount) {
    var sourcePath = mirrorMount.getAttribute("data-source");
    var titlesAttr = mirrorMount.getAttribute("data-titles") || "";
    var wantedTitles = titlesAttr.split("|").map(function (s) { return s.trim(); });

    fetch(sourcePath)
      .then(function (res) { if (!res.ok) throw new Error("fetch failed"); return res.text(); })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, "text/html");
        var blocks = doc.querySelectorAll(".resume__block");
        var found = 0;
        blocks.forEach(function (block) {
          var titleEl = block.querySelector(".resume__block-title");
          if (!titleEl) return;
          var title = titleEl.textContent.trim();
          if (wantedTitles.indexOf(title) !== -1) {
            var clone = block.cloneNode(true);
            clone.classList.add("reveal");
            mirrorMount.appendChild(clone);
            found++;
          }
        });
        if (found === 0) {
          mirrorMount.innerHTML = '<p class="section__text">' + mirrorMount.getAttribute("data-empty-text") + "</p>";
        } else {
          observeReveals();
        }
      })
      .catch(function () {
        mirrorMount.innerHTML = '<p class="section__text">' + mirrorMount.getAttribute("data-error-text") + "</p>";
      });
  }
  /* ---------- Contact page: cursor-follow glow on each card ---------- */
  if (!reduceMotion) {
    document.querySelectorAll(".contact-card").forEach(function (el) {
      el.addEventListener("mousemove", function (e) {
        var rect = el.getBoundingClientRect();
        el.style.setProperty("--gx", ((e.clientX - rect.left) / rect.width) * 100 + "%");
        el.style.setProperty("--gy", ((e.clientY - rect.top) / rect.height) * 100 + "%");
      });
    });
  }
  /* ---------- Spotify playlist shutter ---------- */
  var spotifyToggle = document.getElementById("spotify-toggle");
  var spotifyDropdown = document.getElementById("spotify-dropdown");
  var heroEl = document.querySelector(".hero");
  function closeSpotify() {
    if (spotifyDropdown) spotifyDropdown.classList.remove("is-open");
    if (spotifyToggle) spotifyToggle.setAttribute("aria-expanded", "false");
    if (heroEl) heroEl.classList.remove("spotify-open");
  }
  if (spotifyToggle && spotifyDropdown) {
    spotifyToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = spotifyDropdown.classList.toggle("is-open");
      spotifyToggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (heroEl) heroEl.classList.toggle("spotify-open", open);
    });
    document.addEventListener("click", function (e) {
      if (!spotifyDropdown.contains(e.target)) closeSpotify();
    });
  }
  /* ---------- Preserve scroll position across language switches ---------- */
  document.querySelectorAll(".lang-pill a").forEach(function (a) {
    a.addEventListener("click", function () {
      var docH = document.documentElement.scrollHeight - window.innerHeight;
      var ratio = docH > 0 ? window.scrollY / docH : 0;
      try { sessionStorage.setItem("scrollRatio", String(ratio)); } catch (e) {}
    });
  });
  (function restoreScroll() {
    var val;
    try { val = sessionStorage.getItem("scrollRatio"); } catch (e) { val = null; }
    if (val === null) return;
    try { sessionStorage.removeItem("scrollRatio"); } catch (e) {}
    var ratio = parseFloat(val);
    if (isNaN(ratio)) return;
    requestAnimationFrame(function () {
      var docH = document.documentElement.scrollHeight - window.innerHeight;
      window.scrollTo(0, Math.max(0, docH * ratio));
    });
  })();

})();
