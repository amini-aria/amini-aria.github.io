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
      "A collection of tools, web applications, and practical bots that I designed and developed from scratch, perhaps they'll be useful for you too.",
    tools: [
      {
        icon: "convert",
        tag: "Web Tool",
        name: "File Converter",
        desc: "Convert files between different formats, with no restrictions.",
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
        desc: "Save any YouTube video in your preferred quality, with no restrictions.",
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

  /* A coloured PS1, the same one in both panes — user in green, working
     directory in cyan, the sigil dimmed. */
  function prompt(path) {
    return '<span class="lab-prompt__user">aria@lab</span>' +
      '<span class="lab-prompt__sign">:</span>' +
      '<span class="lab-prompt__path">' + path + "</span>" +
      '<span class="lab-prompt__sign">$</span>';
  }
  var PROMPT_HTML = prompt("~/aria-tools");

  function renderFixedHeader() {
    var el = document.getElementById("lab-terminal-fixed");
    if (!el) return;
    el.innerHTML =
      '<p class="lab-prompt-line">' + prompt("~") + " whoami</p>" +
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
    if (tool.rtl) cardClass += " lab-card--rtl";
    var statusClass = isActive ? "lab-card__status" : "lab-card__status lab-card__status--off";
    var statusLabel = isActive ? "Live" : "Inactive";
    var icon = ICONS[tool.icon] || ICONS.download;
    var dirAttr = tool.rtl ? ' dir="rtl"' : "";

    var inner =
      '<span class="lab-card__top">' +
      '<span class="lab-card__icon">' + icon + "</span>" +
      '<span class="lab-card__tag">' + escapeHtml(tool.tag) + "</span>" +
      "</span>" +
      '<h3 class="lab-card__name"' + dirAttr + '>' + escapeHtml(tool.name) + "</h3>" +
      '<p class="lab-card__desc"' + dirAttr + '>' + escapeHtml(tool.desc) + "</p>" +
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
     Simulated terminal session.

     Everything below prints what the real tool prints: the command set is
     what you would actually run to deploy one of these bots, and each
     output block is that program's genuine format — apt's three "Done"
     lines, git's counting/compressing/resolving phases, npm's audit
     summary, Vite's build table, pip's ━ progress bar, yt-dlp's percentage
     line, docker compose's ✔ list, the full systemctl status block.

     Human touches are deliberate: a mistyped subcommand that actually
     fails with apt's own error before being retyped, tab completion on a
     half-typed directory, a dev server killed with Ctrl+C, downloads that
     speed up and stall rather than filling at a constant rate, and pauses
     of uneven length between commands.

     A single setTimeout chain drives all of it (never more than one timer
     pending) and the DOM node count is hard-capped, so it can run for as
     long as the page is open without leaking.
     ========================================================================= */
  var logEl = document.getElementById("lab-terminal-log");
  if (!logEl) return;

  var reduceMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) {
    logEl.innerHTML =
      '<div class="lab-log__line lab-log__line--cmd">' + PROMPT_HTML + " systemctl status aria-bot.service</div>" +
      '<div class="lab-log__line"><span class="t-green">●</span> aria-bot.service - Aria Tools Worker</div>' +
      '<div class="lab-log__line">     Active: <span class="t-green">active (running)</span> since Tue 09:14:22 UTC</div>';
    return;
  }

  var MAX_LOG_LINES = 40;
  var timer = null;

  function schedule(fn, ms) { timer = setTimeout(fn, ms); }
  function jitter(base, spread) { return base + Math.random() * spread; }
  function rep(ch, n) { return n > 0 ? new Array(n + 1).join(ch) : ""; }
  function pad2(n) { return (n < 10 ? "0" : "") + n; }
  function padStart(s, n) { s = String(s); while (s.length < n) { s = " " + s; } return s; }

  function trimLog() {
    while (logEl.children.length > MAX_LOG_LINES) { logEl.removeChild(logEl.firstChild); }
  }

  /* Output lines are written in a tiny markup — {colour|text} — so the step
     table below stays readable while still emitting per-token colour. */
  var TOKEN_RE = /\{([a-z]+)\|([^}]*)\}/g;
  function writeMarkup(el, str) {
    el.textContent = "";
    var last = 0, m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(str)) !== null) {
      if (m.index > last) el.appendChild(document.createTextNode(str.slice(last, m.index)));
      var span = document.createElement("span");
      span.className = "t-" + m[1];
      span.textContent = m[2];
      el.appendChild(span);
      last = m.index + m[0].length;
    }
    if (last < str.length) el.appendChild(document.createTextNode(str.slice(last)));
  }

  function newLine(cls) {
    var el = document.createElement("div");
    el.className = "lab-log__line" + (cls ? " " + cls : "");
    logEl.appendChild(el);
    trimLog();
    return el;
  }

  function appendOutputLine(str) {
    var el = newLine();
    /* a blank line in real output still occupies a row */
    if (str === "") { el.textContent = " "; return; }
    writeMarkup(el, str);
  }

  function appendPlainCmdLine(text) {
    var el = newLine("lab-log__line--cmd");
    el.innerHTML = PROMPT_HTML + " ";
    el.appendChild(document.createTextNode(text));
  }

  /* ---- downloads that actually fill ----------------------------------- */
  var PROGRESS = {
    /* git's receive phase: fast, with the odd hitch */
    gitRecv: {
      step: [6, 13], tick: [55, 85], stall: 0.10,
      line: function (p) {
        return "Receiving objects: " + Math.floor(p) + "% (" +
          Math.round(214 * p / 100) + "/214), " +
          (1.42 * p / 100).toFixed(2) + " MiB | 3.10 MiB/s";
      },
      done: "Receiving objects: 100% (214/214), 1.42 MiB | 3.10 MiB/s, done."
    },
    /* pip's rich bar, ━ filled in magenta the way pip renders it */
    pipWheel: {
      step: [4, 10], tick: [70, 110], stall: 0.16,
      line: function (p, speed) {
        var w = 32, f = Math.round(w * p / 100);
        var eta = p >= 100 ? "0:00:00" : "0:00:" + pad2(Math.max(1, Math.ceil((100 - p) / 26)));
        return "   {bar|" + rep("━", f) + "}{barbg|" + rep("━", w - f) + "} " +
          (3.2 * p / 100).toFixed(1) + "/3.2 MB " + speed.toFixed(1) + " MB/s eta " + eta;
      },
      speed: [6.8, 3.2]
    },
    /* yt-dlp's single status line, in its exact column layout */
    ytdlp: {
      step: [3, 9], tick: [75, 120], stall: 0.18,
      line: function (p, speed) {
        var eta = Math.max(0, Math.ceil((100 - p) / 100 * 4));
        return "[download] " + padStart(p.toFixed(1), 5) + "% of " +
          padStart("24.31MiB", 10) + " at " + padStart(speed.toFixed(2) + "MiB/s", 12) +
          " ETA 00:" + pad2(eta);
      },
      speed: [6.4, 2.6]
    },
    /* spotdl runs on rich too, so it gets the same bar with a track count */
    spotdl: {
      step: [4, 9], tick: [90, 140], stall: 0.12,
      line: function (p) {
        var w = 24, f = Math.round(w * p / 100);
        var n = Math.round(24 * p / 100);
        return "Downloading {bar|" + rep("━", f) + "}{barbg|" + rep("━", w - f) + "} " +
          padStart(n, 2) + "/24 0:00:" + pad2(Math.max(0, Math.ceil((100 - p) / 100 * 22)));
      }
    }
  };

  function runProgress(name, done) {
    var spec = PROGRESS[name];
    var el = newLine();
    var pct = 0;
    var speed = spec.speed ? spec.speed[0] : 0;

    function paint() {
      writeMarkup(el, spec.line(pct, speed));
    }

    function tick() {
      /* real transfers pause; a constant fill rate is the tell that it is fake */
      if (pct > 8 && pct < 92 && Math.random() < spec.stall) {
        schedule(tick, jitter(260, 420));
        return;
      }
      pct = Math.min(100, pct + jitter(spec.step[0], spec.step[1]));
      if (spec.speed) speed = Math.max(0.4, spec.speed[0] + (Math.random() - 0.5) * spec.speed[1]);
      paint();
      if (pct < 100) {
        schedule(tick, jitter(spec.tick[0], spec.tick[1]));
      } else {
        if (spec.done) writeMarkup(el, spec.done);
        schedule(done, jitter(280, 240));
      }
    }

    paint();
    schedule(tick, jitter(120, 160));
  }

  /* ---- the session ----------------------------------------------------- */
  var STEPS = [
    {
      cmd: "apt update",
      out: [
        "{dim|Hit:1} http://deb.debian.org/debian bookworm InRelease",
        "{dim|Get:2} http://security.debian.org/debian-security bookworm-security InRelease {dim|[48.0 kB]}",
        "Fetched 48.0 kB in 1s (43.7 kB/s)",
        "Reading package lists... {green|Done}",
        "Building dependency tree... {green|Done}",
        "Reading state information... {green|Done}",
        "All packages are up to date."
      ]
    },
    {
      /* the mistake gets made properly: typed, run, and rejected by apt */
      cmd: "apt insall ffmpeg -y",
      norepeat: true,
      out: ["{red|E: Invalid operation insall}"]
    },
    {
      cmd: "apt install ffmpeg -y",
      out: [
        "Reading package lists... {green|Done}",
        "Building dependency tree... {green|Done}",
        "Reading state information... {green|Done}",
        "ffmpeg is already the newest version (7:5.1.6-0+deb12u1).",
        "0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded."
      ]
    },
    {
      cmd: "git clone https://github.com/aria-labs/yt-downloader-bot.git",
      out: [
        "Cloning into '{cyan|yt-downloader-bot}'...",
        "{dim|remote:} Enumerating objects: 214, done.",
        "{dim|remote:} Counting objects: 100% (214/214), done.",
        "{dim|remote:} Compressing objects: 100% (142/142), done.",
        "{dim|remote:} Total 214 (delta 71), reused 198 (delta 55), pack-reused 0",
        { progress: "gitRecv" },
        "Resolving deltas: 100% (71/71), done."
      ]
    },
    {
      /* half typed, then completed with Tab the way anyone actually does it */
      cmd: "cd yt-downloader-bot",
      tab: 9,
      out: []
    },
    {
      cmd: "npm ci",
      out: [
        "",
        "added 182 packages, and audited 183 packages in 6s",
        "",
        "41 packages are looking for funding",
        "  run `npm fund` for details",
        "",
        "found {green|0 vulnerabilities}"
      ]
    },
    {
      cmd: "npm run dev",
      ctrlC: true,
      out: [
        "{dim|> yt-downloader-bot@1.0.0 dev}",
        "{dim|> vite}",
        "",
        "  {green|VITE v5.4.2}  ready in 320 ms",
        "",
        "  {green|➜}  {bold|Local}:   {cyan|http://localhost:5173/}",
        "  {green|➜}  {bold|Network}: use {dim|--host} to expose"
      ]
    },
    {
      cmd: "npm run build",
      out: [
        "{dim|> yt-downloader-bot@1.0.0 build}",
        "{dim|> tsc -p tsconfig.json && vite build}",
        "",
        "{dim|vite v5.4.2 building for production...}",
        "{green|✓} 148 modules transformed.",
        "dist/index.html                  {dim|0.46 kB │ gzip:  0.30 kB}",
        "dist/assets/index-B7xQ1a2c.js  {dim|142.83 kB │ gzip: 46.12 kB}",
        "{green|✓ built in 2.14s}"
      ]
    },
    {
      cmd: "pip install -U yt-dlp spotdl",
      out: [
        "Collecting yt-dlp",
        "  Downloading yt_dlp-2024.8.6-py3-none-any.whl.metadata {dim|(170 kB)}",
        "Collecting spotdl",
        "  Downloading spotdl-4.2.5-py3-none-any.whl.metadata {dim|(11 kB)}",
        "Downloading yt_dlp-2024.8.6-py3-none-any.whl {dim|(3.2 MB)}",
        { progress: "pipWheel" },
        "Installing collected packages: yt-dlp, spotdl",
        "{green|Successfully installed} spotdl-4.2.5 yt-dlp-2024.8.6"
      ]
    },
    {
      cmd: "yt-dlp -f 'bv*+ba/b' -o '%(title)s.%(ext)s' https://youtu.be/aqz-KE-bpKQ",
      out: [
        "{yellow|[youtube]} Extracting URL: https://youtu.be/aqz-KE-bpKQ",
        "{yellow|[youtube]} aqz-KE-bpKQ: Downloading webpage",
        "{yellow|[youtube]} aqz-KE-bpKQ: Downloading ios player API JSON",
        "{cyan|[info]} aqz-KE-bpKQ: Downloading 1 format(s): 137+251",
        "{cyan|[download]} Destination: Big Buck Bunny.f137.mp4",
        { progress: "ytdlp" },
        "{cyan|[download]} 100% of   24.31MiB in 00:00:03 at 7.42MiB/s",
        "{magenta|[Merger]} Merging formats into \"Big Buck Bunny.mp4\""
      ]
    },
    {
      cmd: "spotdl download https://open.spotify.com/playlist/37i9dQZF1DX",
      out: [
        "Processing query: https://open.spotify.com/playlist/37i9dQZF1DX",
        "Found 24 songs in 1 album",
        { progress: "spotdl" },
        "{green|Downloaded} \"Pink Floyd - Time\": ~/Music/Pink Floyd - Time.mp3"
      ]
    },
    {
      cmd: "docker compose up -d",
      out: [
        "[+] Running 3/3",
        " {green|✔} Network aria_default   {dim|Created}                     {dim|0.1s}",
        " {green|✔} Container aria-redis   {dim|Started}                     {dim|0.4s}",
        " {green|✔} Container aria-api     {dim|Started}                     {dim|0.7s}"
      ]
    },
    {
      cmd: "systemctl status aria-bot.service",
      out: [
        "{green|●} aria-bot.service - Aria Tools Worker",
        "     Loaded: loaded ({cyan|/etc/systemd/system/aria-bot.service}; enabled; preset: enabled)",
        "     Active: {green|active (running)} since Tue 2026-09-02 09:14:22 UTC; 2h 11min ago",
        "   Main PID: 1842 (node)",
        "      Tasks: 11 (limit: 4915)",
        "     Memory: 84.2M",
        "     CGroup: /system.slice/aria-bot.service",
        "             └─1842 /usr/bin/node /srv/aria-bot/dist/index.js"
      ]
    },
    {
      cmd: "journalctl -u aria-bot.service -n 3 --no-pager",
      out: [
        "{dim|Sep 02 11:22:04} aria systemd[1]: Started Aria Tools Worker.",
        "{dim|Sep 02 11:24:41} aria aria-bot[1842]: queue: 3 jobs pending",
        "{dim|Sep 02 11:25:31} aria aria-bot[1842]: job 4f21c8 completed in 3.2s"
      ]
    }
  ];

  var stepIndex = 0;

  /* Types one character at a time at an irregular pace, with the occasional
     hesitation — a constant interval reads as a machine printing, not a
     person typing. */
  function typeInto(span, text, done) {
    var i = 0;
    function tick() {
      if (i >= text.length) { done(); return; }
      span.textContent += text.charAt(i);
      i++;
      var delay = jitter(58, 88);
      if (Math.random() < 0.09) delay += jitter(180, 260);
      schedule(tick, delay);
    }
    tick();
  }

  function runStep() {
    var step = STEPS[stepIndex];

    var lineEl = newLine("lab-log__line--cmd");
    var promptSpan = document.createElement("span");
    var typedSpan = document.createElement("span");
    var cursorSpan = document.createElement("span");
    cursorSpan.className = "lab-log__cursor";
    lineEl.appendChild(promptSpan);
    lineEl.appendChild(typedSpan);
    lineEl.appendChild(cursorSpan);

    /* the line lands empty, then the prompt prints, then typing starts —
       so a command never pops into existence fully formed */
    schedule(function () {
      promptSpan.innerHTML = PROMPT_HTML + " ";
      schedule(beginTyping, jitter(240, 240));
    }, jitter(300, 260));

    function beginTyping() {
      if (step.tab) {
        typeInto(typedSpan, step.cmd.slice(0, step.tab), function () {
          schedule(function () {
            typedSpan.textContent = step.cmd + "/";
            schedule(function () {
              typedSpan.textContent = step.cmd;
              finishTyping();
            }, jitter(260, 200));
          }, jitter(420, 320));
        });
        return;
      }
      typeInto(typedSpan, step.cmd, finishTyping);
    }

    function finishTyping() {
      cursorSpan.remove();

      if (step.ctrlC) {
        schedule(function () {
          printOutput(0, function () {
            schedule(function () {
              appendOutputLine("^C");
              schedule(nextStep, jitter(450, 350));
            }, jitter(900, 700));
          });
        }, jitter(200, 200));
        return;
      }

      schedule(function () { printOutput(0, nextStepDelayed); }, jitter(220, 280));
    }

    function nextStepDelayed() {
      var delay = Math.random() < 0.14 ? jitter(200, 200) : jitter(700, 900);
      schedule(nextStep, delay);
    }

    function printOutput(i, done) {
      if (!step.out || i >= step.out.length) { done(); return; }
      var item = step.out[i];
      if (item && typeof item === "object" && item.progress) {
        runProgress(item.progress, function () {
          schedule(function () { printOutput(i + 1, done); }, jitter(140, 200));
        });
        return;
      }
      appendOutputLine(item);
      /* blank spacer lines land instantly; real output arrives in bursts */
      schedule(function () { printOutput(i + 1, done); }, item === "" ? 40 : jitter(120, 210));
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
    if (stepIndex >= STEPS.length) { clearAndLoop(); return; }
    /* people re-run a command now and then to double-check the result */
    var prev = STEPS[stepIndex - 1];
    if (prev && !prev.norepeat && !prev.tab && Math.random() < 0.1) {
      var repeatIdx = stepIndex - 1;
      schedule(function () { stepIndex = repeatIdx; runStep(); }, jitter(300, 300));
      return;
    }
    schedule(runStep, jitter(350, 350));
  }

  schedule(runStep, 600);
})();
