/* =============================================================================
   ARIA'S LAB — single source of truth.

   HOW TO EDIT:
   - To add, remove, rename, or re-describe a tool, edit the TOOLS array below.
   - To mark a tool as live vs not-ready-yet, change its `status` to
     "active" or "inactive". That's the only thing that controls the
     green "Live" pulse vs the grey "Coming soon" label.
   - This exact file is loaded by BOTH index.html and fa/index.html, so the
     Lab section always renders identically on both language versions —
     there is nowhere else to edit this content.
   ============================================================================= */

(function () {
  "use strict";

  var TOOLS = [
    {
      icon: "convert",
      tag: "Web Tool",
      name: "File Converter",
      desc: "Convert files between formats, right in the browser — no upload to a server required.",
      status: "active",
      href: "#",
      slug: "file-converter",
      version: "1.0.0"
    },
    {
      icon: "spotify",
      tag: "Bot",
      name: "Spotify Downloader",
      desc: "Grab a track or playlist as a local file, straight from a link.",
      status: "inactive",
      href: "#",
      slug: "spotify-downloader-bot",
      version: "0.9.2"
    },
    {
      icon: "youtube",
      tag: "Bot",
      name: "YouTube Downloader",
      desc: "Save a YouTube video or audio track straight from its link.",
      status: "inactive",
      href: "#",
      slug: "youtube-downloader-bot",
      version: "0.4.1"
    },
    {
      icon: "instagram",
      tag: "Bot",
      name: "Instagram Downloader",
      desc: "Download Instagram posts, reels, and stories from a link.",
      status: "inactive",
      href: "#",
      slug: "instagram-downloader-bot",
      version: "0.3.0"
    },
    {
      icon: "pinterest",
      tag: "Bot",
      name: "Pinterest Downloader",
      desc: "Save a Pinterest pin or board image at full resolution.",
      status: "inactive",
      href: "#",
      slug: "pinterest-downloader-bot",
      version: "0.2.0"
    }
  ];

  var ICONS = {
    convert: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h11M15 7l-3-3M15 7l-3 3"/><path d="M20 17H9M9 17l3 3M9 17l3-3"/></svg>',
    spotify: '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm4.59 14.4a.62.62 0 01-.85.2c-2.33-1.42-5.27-1.74-8.72-.96a.62.62 0 11-.28-1.22c3.78-.86 7.02-.49 9.65 1.12.3.18.4.57.2.86zm1.22-2.72a.78.78 0 01-1.07.26c-2.67-1.64-6.73-2.12-9.88-1.16a.78.78 0 11-.46-1.49c3.6-1.09 8.08-.56 11.15 1.32.37.23.49.72.26 1.07zm.1-2.83c-3.2-1.9-8.49-2.08-11.55-1.15a.94.94 0 11-.54-1.8c3.5-1.06 9.32-.85 13 1.32a.94.94 0 11-.91 1.63z"/></svg>',
    youtube: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10.5 9.5l5 2.5-5 2.5z" fill="currentColor" stroke="none"/></svg>',
    instagram: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.6" fill="currentColor" stroke="none"/></svg>',
    pinterest: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9.5"/><path d="M9.5 18c1-3.5 1.5-6 1.5-7.5a2 2 0 114 0c0 1-.5 2.5-1 4"/><path d="M11 10.3a2.6 2.6 0 015.1.7c0 2.2-1.4 3.8-3 3.8"/></svg>',
    plus: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 5v14M5 12h14"/></svg>'
  };

  var ARROW = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

  function renderCards() {
    var grid = document.getElementById("lab-grid");
    if (!grid) return;
    var html = "";
    TOOLS.forEach(function (t) {
      var activeCls = t.status === "active" ? "lab-card--active" : "lab-card--inactive";
      var statusCls = t.status === "active" ? "" : "lab-card__status--off";
      var statusLabel = t.status === "active" ? "Live" : "Coming soon";
      var tag = "<span class=\"lab-card__icon\">" + ICONS[t.icon] + "</span><span class=\"lab-card__tag\">" + t.tag + "</span>";
      var foot = "<span class=\"lab-card__status " + statusCls + "\"><span class=\"lab-card__dot\"></span>" + statusLabel + "</span>"
        + (t.status === "active" ? "<span class=\"lab-card__cta\">Open" + ARROW + "</span>" : "");
      var tagName = t.status === "active" ? "a" : "div";
      var hrefAttr = t.status === "active" ? ' href="' + t.href + '" target="_blank" rel="noopener"' : "";
      html += "<" + tagName + " class=\"lab-card " + activeCls + "\"" + hrefAttr + ">"
        + "<span class=\"lab-card__top\">" + tag + "</span>"
        + "<h3 class=\"lab-card__name\">" + t.name + "</h3>"
        + "<p class=\"lab-card__desc\">" + t.desc + "</p>"
        + "<span class=\"lab-card__foot\">" + foot + "</span>"
        + "</" + tagName + ">";
    });
    html += '<div class="lab-card lab-card--inactive">'
      + '<span class="lab-card__top"><span class="lab-card__icon lab-card__icon--soon">' + ICONS.plus + "</span></span>"
      + '<h3 class="lab-card__name">More on the way</h3>'
      + '<p class="lab-card__desc">Whatever I build next lands here first.</p>'
      + '<span class="lab-card__foot"><span class="lab-card__status lab-card__status--off"><span class="lab-card__dot"></span>Coming soon</span></span>'
      + "</div>";
    grid.innerHTML = html;
  }

  function typewriterTitle() {
    var el = document.getElementById("lab-title-text");
    if (!el || !("IntersectionObserver" in window)) return;
    var fullText = el.getAttribute("data-text") || "";
    var typed = false;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && !typed) {
          typed = true;
          var i = 0;
          var iv = setInterval(function () {
            i++;
            el.textContent = fullText.slice(0, i);
            if (i >= fullText.length) clearInterval(iv);
          }, 65);
          io.disconnect();
        }
      });
    }, { threshold: 0.4 });
    io.observe(el);
  }

  /* Decorative boot-log that "installs" each tool above, on a loop, inside a
     fixed-height terminal body — new lines push old ones up and out; they
     never make the terminal box grow. Purely atmospheric, respects
     prefers-reduced-motion by rendering one static frame instead. */
  function terminalLog() {
    var log = document.getElementById("lab-terminal-log");
    if (!log) return;
    var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var lines = [];
    lines.push({ cmd: "apt update" }, { out: "Reading package lists... Done" });
    TOOLS.forEach(function (t) {
      lines.push({ cmd: "apt install " + t.slug });
      lines.push({ out: "Setting up " + t.slug + " (" + t.version + ") ... done." });
    });
    lines.push({ cmd: "./aria-lab --status" });
    lines.push({ out: TOOLS.filter(function (t) { return t.status === "active"; }).length + " active, " + TOOLS.filter(function (t) { return t.status !== "active"; }).length + " pending" });

    if (reduceMotion) {
      var staticHtml = "";
      lines.slice(-4).forEach(function (l) { staticHtml += lineHtml(l); });
      log.innerHTML = staticHtml;
      return;
    }

    var i = 0;
    var MAX_DOM_LINES = 30;
    function pushLine() {
      var l = lines[i % lines.length];
      var div = document.createElement("div");
      div.className = "lab-terminal__line";
      div.innerHTML = lineHtml(l);
      log.appendChild(div);
      while (log.children.length > MAX_DOM_LINES) log.removeChild(log.firstChild);
      log.scrollTop = log.scrollHeight;
      i++;
    }
    function lineHtml(l) {
      if (l.cmd) return '<span class="lab-terminal__prompt">root@aria:~#</span> <span class="lab-terminal__cmd">' + l.cmd + "</span>";
      return '<span class="lab-terminal__out">' + l.out + "</span>";
    }
    pushLine();
    setInterval(pushLine, 950);
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderCards();
    typewriterTitle();
    terminalLog();
  });
})();
