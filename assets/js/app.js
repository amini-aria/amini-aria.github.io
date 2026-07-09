(function () {
  "use strict";

  var burger = document.getElementById("burger");
  var links = document.getElementById("topnav-links");
  if (burger && links) {
    burger.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", String(open));
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { links.classList.remove("is-open"); });
    });
  }

  var topbar = document.getElementById("topbar");
  if (topbar) {
    window.addEventListener("scroll", function () {
      topbar.classList.toggle("is-solid", window.scrollY > 12);
    }, { passive: true });
  }

  var revealTargets = document.querySelectorAll(".reveal");
  if (revealTargets.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealTargets.forEach(function (t) { io.observe(t); });
  }

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
})();
