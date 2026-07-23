/* =============================================================================
   ARIA'S LAB — single source of truth.

   HOW TO EDIT:
   - To change the section title or subtitle, edit ARIA_LAB_DATA.title /
     ARIA_LAB_DATA.subtitle below.
   - To add, remove, rename, or re-describe a tool, edit the
     ARIA_LAB_DATA.tools array below.
   - To mark a tool as live vs not-ready-yet, change its `active` flag to
     true or false. That's the only thing that controls the green "Live"
     pulse vs the grey "Inactive" label (and whether the card is a real
     clickable link at all).
   - This exact file is loaded by BOTH index.html and fa/index.html, so the
     Lab section always renders identically — and always in English — on
     both language versions of the site. There is nowhere else to edit
     this content.
   ============================================================================= */

(function () {
  "use strict";

  var ARIA_LAB_DATA = {
    title: "Aria's Lab",
    subtitle:
      "A collection of tools, web applications, and practical bots that I designed and developed from scratch\u2014perhaps they'll be useful for you too.",
    tools: [
      {
        icon: "convert",
        tag: "Web Tool",
        name: "File Converter",
        desc: "Convert files between formats, right in the browser \u2014 no upload to a server required.",
        active: true,
        href: "#"
      },
      {
        icon: "download",
        tag: "Bot",
        name: "Spotify Downloader Bot",
        desc: "Grab a track or playlist as a local file, straight from a link.",
        active: false,
        href: "#"
      },
      {
        icon: "download",
        tag: "Bot",
        name: "YouTube Downloader Bot",
        desc: "Save any YouTube video or audio track directly to your device.",
        active: false,
        href: "#"
      },
      {
        icon: "download",
        tag: "Bot",
        name: "Instagram Downloader Bot",
        desc: "Download Instagram posts, reels, and stories without watermarks.",
        active: false,
        href: "#"
      },
      {
        icon: "download",
        tag: "Bot",
        name: "Pinterest Downloader Bot",
        desc: "Save Pinterest images and videos in their original quality.",
        active: false,
        href: "#"
      }
    ]
  };

  var ICONS = {
    convert:
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h11M15 7l-3-3M15 7l-3 3"/><path d="M20 17H9M9 17l3 3M9 17l3-3"/></svg>',
    download:
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M4 19h16"/></svg>'
  };
  var ARROW_ICON =
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function renderFixedHeader() {
    var el = document.getElementById("lab-terminal-fixed");
    if (!el) return;
    el.innerHTML =
      '<p class="lab-prompt-line"><span class="lab-prompt">root@aria:~#</span> whoami</p>' +
      '<h2 class="lab-section__title">' +
      escapeHtml(ARIA_LAB_DATA.title) +
      '<span class="lab-title__cursor">|</span></h2>' +
      '<p class="lab-section__text">' +
      escapeHtml(ARIA_LAB_DATA.subtitle) +
      "</p>";
  }

  function renderCard(tool) {
    var isActive = !!tool.active;
    var cardClass = "lab-card " + (isActive ? "lab-card--active" : "lab-card--inactive");
    var statusClass = isActive ? "lab-card__status" : "lab-card__status lab-card__status--off";
    var statusLabel = isActive ? "Live" : "Inactive";
    var icon = ICONS[tool.icon] || ICONS.download;

    var inner =
      '<span class="lab-card__top">' +
      '<span class="lab-card__icon">' + icon + "</span>" +
      '<span class="lab-card__tag">' + escapeHtml(tool.tag) + "</span>" +
      "</span>" +
      '<h3 class="lab-card__name">' + escapeHtml(tool.name) + "</h3>" +
      '<p class="lab-card__desc">' + escapeHtml(tool.desc) + "</p>" +
      '<span class="lab-card__foot">' +
      '<span class="' + statusClass + '"><span class="lab-card__dot"></span>' + statusLabel + "</span>" +
      (isActive ? '<span class="lab-card__cta">Open' + ARROW_ICON + "</span>" : "") +
      "</span>";

    if (isActive) {
      return '<a class="' + cardClass + '" href="' + tool.href + '" target="_blank" rel="noopener">' + inner + "</a>";
    }
    return '<div class="' + cardClass + '">' + inner + "</div>";
  }

  function renderCards() {
    var grid = document.getElementById("lab-grid");
    if (!grid) return;
    grid.innerHTML = ARIA_LAB_DATA.tools.map(renderCard).join("");
  }

  renderFixedHeader();
  renderCards();

  /* =========================================================================
     Simulated terminal log — a lightweight, bounded "tail -f" loop.
     Real, technically-valid Linux commands and outputs relevant to running
     these tools (git, npm, pip, docker, systemd, yt-dlp, spotdl...), with
     occasional human touches: a typo that gets corrected, a command
     aborted with Ctrl+C, a command re-run, small pauses before output.
     A single setTimeout chain drives it (never more than one pending
     timer), and the DOM node count is hard-capped, so it can run
     indefinitely without leaking memory.
     ========================================================================= */
  var logEl = document.getElementById("lab-terminal-log");
  if (!logEl) return;

  var reduceMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) {
    logEl.innerHTML =
      '<div class="lab-log__line lab-log__line--cmd"><span class="lab-prompt">root@aria:~#</span> systemctl status aria-bot.service</div>' +
      '<div class="lab-log__line">\u25cf aria-bot.service - Aria Tools Worker</div>' +
      '<div class="lab-log__line">   Active: active (running)</div>';
    return;
  }

  var MAX_LOG_LINES = 40;
  var PROMPT = "root@aria:~#";
  var timer = null;

  function schedule(fn, ms) {
    timer = setTimeout(fn, ms);
  }

  function jitter(base, spread) {
    return base + Math.random() * spread;
  }

  function trimLog() {
    while (logEl.children.length > MAX_LOG_LINES) {
      logEl.removeChild(logEl.firstChild);
    }
  }

  function appendOutputLine(text) {
    var el = document.createElement("div");
    el.className = "lab-log__line";
    el.textContent = text;
    logEl.appendChild(el);
    trimLog();
  }

  /* a download that visibly progresses from 0% to 100% on its own line,
     the way a real terminal sits and waits on a download — updates one
     element in place rather than spamming a new line per tick */
  function runDownloadProgress(templateFn, done) {
    var el = document.createElement("div");
    el.className = "lab-log__line";
    logEl.appendChild(el);
    trimLog();
    var pct = 0;
    function tick() {
      pct += jitter(7, 15);
      if (pct >= 100) pct = 100;
      el.textContent = templateFn(pct);
      if (pct < 100) {
        schedule(tick, jitter(150, 180));
      } else {
        schedule(done, jitter(300, 250));
      }
    }
    tick();
  }

  function pad2(n) {
    return (n < 10 ? "0" : "") + n;
  }

  function appendPlainCmdLine(text) {
    var el = document.createElement("div");
    el.className = "lab-log__line lab-log__line--cmd";
    el.innerHTML = '<span class="lab-prompt">' + PROMPT + "</span> " + escapeHtml(text);
    logEl.appendChild(el);
    trimLog();
    return el;
  }

  var STEPS = [
    {
      cmd: "apt update",
      output: [
        "Hit:1 http://deb.debian.org/debian bookworm InRelease",
        "Reading package lists... Done",
        "Building dependency tree... Done",
        "All packages are up to date."
      ]
    },
    {
      typo: "insall",
      cmd: "apt install ffmpeg -y",
      output: [
        "Reading package lists... Done",
        "ffmpeg is already the newest version (7:5.1.6-0+deb12u1).",
        "0 upgraded, 0 newly installed, 0 to remove."
      ]
    },
    {
      cmd: "git clone https://github.com/aria-labs/yt-downloader-bot.git",
      output: [
        "Cloning into 'yt-downloader-bot'...",
        "remote: Enumerating objects: 214, done.",
        "Receiving objects: 100% (214/214), 1.42 MiB | 3.10 MiB/s, done."
      ]
    },
    {
      cmd: "cd yt-downloader-bot && npm install",
      output: ["added 182 packages in 6s"]
    },
    {
      cmd: "npm run dev",
      output: ["  VITE ready in 320 ms", "  \u2794  Local: http://localhost:5173/"],
      ctrlC: true
    },
    {
      cmd: "npm run build",
      output: ["> yt-downloader-bot@1.0.0 build", "> tsc -p .", "Build completed successfully."]
    },
    {
      cmd: "pip install yt-dlp spotdl",
      output: ["Successfully installed yt-dlp-2024.08.06 spotdl-4.2.5"]
    },
    {
      cmd: "yt-dlp -f best -o '%(title)s.%(ext)s' <url>",
      output: [
        "[youtube] Extracting URL",
        "[download] Destination: sample_video.mp4",
        { progress: "ytdlp" }
      ]
    },
    {
      cmd: "spotdl download <playlist-url>",
      output: [
        "Processing query: Playlist",
        "Found 24 songs in playlist",
        { progress: "spotdl" },
        'Downloaded "Track 01": 100%'
      ]
    },
    {
      cmd: "docker compose up -d",
      output: ["Network aria_default  Created", "Container aria-api  Started"]
    },
    {
      cmd: "systemctl status aria-bot.service",
      output: ["\u25cf aria-bot.service - Aria Tools Worker", "   Active: active (running)"]
    },
    {
      cmd: "journalctl -u aria-bot.service -n 3",
      output: ["aria systemd[1]: Started Aria Tools Worker.", "aria bot[1842]: job completed in 3.2s"]
    },
    {
      cmd: "tree -L 2",
      output: [".", "\u251c\u2500\u2500 src", "\u251c\u2500\u2500 package.json", "\u2514\u2500\u2500 README.md"]
    }
  ];

  var stepIndex = 0;

  /* types `text` into `span` one character at a time, at an irregular,
     human pace: a slower base speed, natural per-character jitter, and
     occasional short hesitation pauses (like someone reading ahead while
     they type, not a machine printing at a constant rate) */
  function typeInto(span, text, done) {
    var i = 0;
    function tick() {
      if (i >= text.length) { done(); return; }
      span.textContent += text.charAt(i);
      i++;
      var delay = jitter(65, 95);
      if (Math.random() < 0.09) delay += jitter(180, 260);
      schedule(tick, delay);
    }
    tick();
  }

  function backspaceFrom(span, count, done) {
    var removed = 0;
    function tick() {
      if (removed >= count) { done(); return; }
      span.textContent = span.textContent.slice(0, -1);
      removed++;
      schedule(tick, jitter(55, 45));
    }
    tick();
  }

  function runStep() {
    var step = STEPS[stepIndex];

    var lineEl = document.createElement("div");
    lineEl.className = "lab-log__line lab-log__line--cmd";
    var promptSpan = document.createElement("span");
    promptSpan.className = "lab-prompt";
    var typedSpan = document.createElement("span");
    var cursorSpan = document.createElement("span");
    cursorSpan.className = "lab-log__cursor";
    lineEl.appendChild(promptSpan);
    lineEl.appendChild(document.createTextNode(" "));
    lineEl.appendChild(typedSpan);
    lineEl.appendChild(cursorSpan);
    logEl.appendChild(lineEl);
    trimLog();

    // the line lands empty first (just its fade-in), then the prompt
    // itself prints after a short human beat, then another short pause
    // before typing starts — so a new command never just pops fully
    // formed out of nowhere
    schedule(function () {
      promptSpan.textContent = PROMPT;
      schedule(beginTyping, jitter(260, 260));
    }, jitter(320, 280));

    function beginTyping() {
      if (step.typo) {
        var prefix = step.cmd.split(" ")[0] + " ";
        typeInto(typedSpan, prefix + step.typo, function () {
          schedule(function () {
            backspaceFrom(typedSpan, step.typo.length, function () {
              var rest = step.cmd.slice(prefix.length);
              typeInto(typedSpan, rest, finishTyping);
            });
          }, jitter(350, 300));
        });
      } else {
        typeInto(typedSpan, step.cmd, finishTyping);
      }
    }

    function finishTyping() {
      cursorSpan.remove();

      if (step.ctrlC) {
        schedule(function () {
          printOutput(0, function () {
            schedule(function () {
              appendOutputLine("^C");
              schedule(nextStep, jitter(450, 350));
            }, jitter(550, 450));
          });
        }, jitter(200, 200));
        return;
      }

      schedule(function () { printOutput(0, nextStepDelayed); }, jitter(220, 260));
    }

    function nextStepDelayed() {
      var delay = Math.random() < 0.14 ? jitter(200, 200) : jitter(700, 900);
      schedule(nextStep, delay);
    }

    function printOutput(i, done) {
      if (!step.output || i >= step.output.length) { done(); return; }
      var item = step.output[i];
      if (item && typeof item === "object" && item.progress) {
        var tpl =
          item.progress === "ytdlp"
            ? function (pct) {
                var eta = Math.max(0, Math.round(((100 - pct) / 100) * 3));
                return (
                  "[download] " +
                  pct.toFixed(1) +
                  "% of 24.31MiB at 6.8MiB/s ETA 00:" +
                  pad2(eta)
                );
              }
            : function (pct) {
                return 'Downloading "Track 01": ' + Math.round(pct) + "%";
              };
        runDownloadProgress(tpl, function () {
          schedule(function () { printOutput(i + 1, done); }, jitter(150, 200));
        });
        return;
      }
      appendOutputLine(item);
      schedule(function () { printOutput(i + 1, done); }, jitter(140, 220));
    }
  }

  function clearAndLoop() {
    appendPlainCmdLine("clear");
    schedule(function () {
      logEl.innerHTML = "";
      stepIndex = 0;
      schedule(runStep, 500);
    }, jitter(400, 200));
  }

  function nextStep() {
    stepIndex++;
    if (stepIndex >= STEPS.length) {
      clearAndLoop();
      return;
    }
    // small chance of immediately re-running the same command again, the
    // way people sometimes double-check a result
    if (Math.random() < 0.1) {
      var repeatIdx = stepIndex - 1;
      schedule(function () {
        stepIndex = repeatIdx;
        runStep();
      }, jitter(300, 300));
      return;
    }
    schedule(runStep, jitter(350, 350));
  }

  schedule(runStep, 600);
})();
