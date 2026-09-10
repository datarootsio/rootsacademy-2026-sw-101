/* Deck engine: navigation, chrome, day rail, syntax highlighting.
   Each deck page sets window.DECK = { track, code, title } before loading this. */

(() => {
  const CFG = window.DECK || { track: "py", code: "PY", title: "Deck" };

  // Minutes per track, so the rail shows position in the whole six-hour day.
  const DAY = [
    { key: "git", label: "Git",    weight: 125, ink: "var(--git)" },
    { key: "py",  label: "Python", weight: 140, ink: "var(--py)" },
    { key: "nix", label: "Linux",  weight: 55,  ink: "var(--nix)" },
  ];

  const deck = document.getElementById("deck");
  const slides = [...deck.querySelectorAll(".slide")];
  let current = 0;

  document.documentElement.style.setProperty("--track", `var(--${CFG.track})`);

  /* ── Chrome: each .part slide names the section for the slides that follow ── */

  const titleOf = (s) =>
    s.dataset.title || s.querySelector("h1, h2")?.textContent.trim() || "";

  let where = "";
  slides.forEach((s, i) => {
    if (s.classList.contains("part") || s.classList.contains("opener")) where = titleOf(s);
    if (s.classList.contains("opener")) return;

    const bar = document.createElement("div");
    bar.className = "chrome";
    bar.innerHTML =
      `<span class="code">${CFG.code}</span>` +
      `<span class="where"></span>` +
      `<span class="idx">${String(i + 1).padStart(2, "0")} / ${slides.length}</span>`;
    bar.querySelector(".where").textContent = where;
    s.prepend(bar);
  });

  /* ── Day rail ── */

  const rail = document.createElement("div");
  rail.id = "rail";
  rail.innerHTML = DAY.map(
    (t) => `<div class="seg" data-key="${t.key}" style="flex:${t.weight};--seg:${t.ink}">
              <span>${t.label}</span></div>`
  ).join("");
  deck.append(rail);

  const segs = [...rail.children];
  const trackIdx = DAY.findIndex((t) => t.key === CFG.track);

  function paintRail() {
    const progress = slides.length > 1 ? current / (slides.length - 1) : 1;
    segs.forEach((seg, i) => {
      const fill = i < trackIdx ? 1 : i > trackIdx ? 0 : progress;
      seg.style.setProperty("--fill", `${fill * 100}%`);
      seg.toggleAttribute("data-here", i === trackIdx);
    });
  }

  /* ── Navigation ── */

  function show(n, push = true) {
    current = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((s, i) => s.toggleAttribute("data-active", i === current));
    deck.toggleAttribute("data-opener", slides[current].classList.contains("opener"));
    paintRail();
    help.hidden = current !== 0;
    if (push) history.replaceState(null, "", `#${current + 1}`);
    document.title = `${CFG.title} · ${current + 1}/${slides.length}`;
  }

  const go = (d) => show(current + d);

  /* ── Contents overlay ── */

  const toc = document.createElement("div");
  toc.id = "toc";
  toc.hidden = true;
  toc.innerHTML =
    `<h2>${CFG.title}</h2><ol>` +
    slides
      .map((s, i) => {
        const part = s.classList.contains("part") || s.classList.contains("opener");
        return `<li class="${part ? "is-part" : ""}"><button data-go="${i}">
                  <span class="n">${String(i + 1).padStart(2, "0")}</span>${titleOf(s)}
                </button></li>`;
      })
      .join("") +
    `</ol>`;
  document.body.append(toc);

  toc.addEventListener("click", (e) => {
    const b = e.target.closest("[data-go]");
    if (!b) return;
    toc.hidden = true;
    show(+b.dataset.go);
  });

  const toggleToc = () => {
    toc.hidden = !toc.hidden;
    if (!toc.hidden) toc.querySelector(`[data-go="${current}"]`)?.focus();
  };

  document.addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const keys = {
      ArrowRight: () => go(1), ArrowDown: () => go(1), PageDown: () => go(1),
      " ": () => go(1), n: () => go(1),
      ArrowLeft: () => go(-1), ArrowUp: () => go(-1), PageUp: () => go(-1), p: () => go(-1),
      Home: () => show(0), End: () => show(slides.length - 1),
      o: toggleToc, Escape: () => (toc.hidden = true),
      f: () => (document.fullscreenElement
        ? document.exitFullscreen()
        : document.documentElement.requestFullscreen()),
    };
    const fn = keys[e.key];
    if (!fn) return;
    e.preventDefault();
    fn();
  });

  deck.addEventListener("click", (e) => {
    if (e.target.closest("button, a, pre, table, input")) return;
    go(e.clientX < deck.getBoundingClientRect().left + deck.clientWidth * 0.25 ? -1 : 1);
  });

  // The hint lives on the title slide only; after that the rail owns the footer.
  const help = document.createElement("div");
  help.id = "help";
  help.textContent = "← →  move     o  contents     f  fullscreen";
  deck.append(help);

  /* ── Syntax highlighting ─────────────────────────────────────────────────
     Deliberately dependency-free: a classroom laptop with no network still
     gets readable code. Sticky regexes are tried in order at each position. */

  const esc = (s) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  const rx = (src) => new RegExp(src, "y");

  const PY_KW = "False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|match|case|self|cls";
  const PY_BI = "abs|all|any|bool|bytes|callable|chr|dict|dir|divmod|enumerate|filter|float|format|frozenset|getattr|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|map|max|min|next|object|open|ord|pow|print|range|repr|reversed|round|set|setattr|slice|sorted|str|sum|super|tuple|type|vars|zip|Exception|ValueError|TypeError|KeyError|IndexError|StopIteration|ZeroDivisionError|FileNotFoundError";

  const PYTHON = [
    ["com", rx("#[^\\n]*")],
    ["str", rx("[fFrRbBuU]{0,2}('''[\\s\\S]*?'''|\"\"\"[\\s\\S]*?\"\"\")")],
    ["str", rx("[fFrRbBuU]{0,2}(\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*')")],
    ["dec", rx("@[A-Za-z_][\\w.]*")],
    ["num", rx("\\b\\d[\\d_]*(?:\\.\\d*)?(?:[eE][+-]?\\d+)?[jJ]?\\b|\\b0[xob][0-9a-fA-F_]+\\b")],
    ["kw",  rx(`(?:${PY_KW})\\b`)],
    ["bi",  rx(`(?:${PY_BI})\\b`)],
    ["fn",  rx("[A-Za-z_]\\w*(?=\\s*\\()")],
    [null,  rx("[A-Za-z_]\\w*")],
    ["op",  rx("[-+*/%=<>!&|^~:]+")],
  ];

  const SH_KW = "if|then|else|elif|fi|for|in|do|done|while|until|case|esac|function|return|local|export|source|declare|readonly|shift|break|continue|exit|set|trap|eval";
  const SH_CMD = "ls|cd|pwd|cat|less|more|head|tail|touch|mkdir|rmdir|cp|mv|rm|ln|find|grep|egrep|sed|awk|sort|uniq|wc|cut|tr|tee|xargs|chmod|chown|chgrp|ps|top|htop|kill|killall|jobs|fg|bg|nohup|df|du|free|uname|whoami|which|whereis|man|echo|printf|read|test|date|sleep|history|alias|env|apt|apt-get|brew|yum|dnf|pip|pip3|python|python3|uv|node|npm|git|ssh|ssh-keygen|ssh-copy-id|ssh-add|scp|rsync|curl|wget|tar|gzip|zip|unzip|sudo|su|mount|systemctl|service|journalctl|docker|make|diff|stat|file|basename|dirname|realpath|mktemp|seq|jq|nano|vim|code|open|tree|column";

  const BASH = [
    ["com", rx("#[^\\n]*")],
    ["str", rx("\"(?:\\\\.|[^\"\\\\])*\"|'[^']*'")],
    ["bi",  rx("\\$\\{[^}]*\\}|\\$[\\w@*?#!$-]+|\\$\\((?:[^()]|\\([^()]*\\))*\\)")],
    ["kw",  rx(`(?:${SH_KW})\\b`)],
    ["bi",  rx(`(?:${SH_CMD})\\b`)],
    ["flg", rx("(?<=[\\s=])--?[A-Za-z][\\w-]*")],
    ["num", rx("\\b\\d+\\b")],
    [null,  rx("[A-Za-z_][\\w.-]*")],
    ["op",  rx("[|><&;=!]+")],
  ];

  function tokenize(src, rules) {
    let out = "", i = 0;
    while (i < src.length) {
      let hit = false;
      for (const [cls, re] of rules) {
        re.lastIndex = i;
        const m = re.exec(src);
        if (!m || !m[0].length) continue;
        out += cls ? `<span class="tok-${cls}">${esc(m[0])}</span>` : esc(m[0]);
        i += m[0].length;
        hit = true;
        break;
      }
      if (!hit) { out += esc(src[i]); i++; }
    }
    return out;
  }

  const PROMPT = /^(\s*)([$#])(\s)/;

  function byLine(src, { output }) {
    return src
      .split("\n")
      .map((line) => {
        const p = line.match(PROMPT);
        if (p) {
          return esc(p[1]) + `<span class="tok-pr">${p[2]}</span>` + esc(p[3]) +
            tokenize(line.slice(p[0].length), BASH);
        }
        if (/^@@/.test(line)) return `<span class="tok-hd">${esc(line)}</span>`;
        if (/^\+/.test(line)) return `<span class="tok-add">${esc(line)}</span>`;
        if (/^-{1,2}(?!-)/.test(line) && output) return `<span class="tok-del">${esc(line)}</span>`;
        if (/^(diff|index|commit|Author|Date)\b/.test(line))
          return `<span class="tok-hd">${esc(line)}</span>`;
        return output ? esc(line) : tokenize(line, BASH);
      })
      .join("\n");
  }

  const HIGHLIGHT = {
    python: (s) => tokenize(s, PYTHON),
    bash: (s) => byLine(s, { output: false }),
    console: (s) => byLine(s, { output: true }),
    diff: (s) => byLine(s, { output: true }),
  };

  document.querySelectorAll("pre[data-lang]").forEach((pre) => {
    const fn = HIGHLIGHT[pre.dataset.lang];
    const src = pre.textContent.replace(/^\n+|\s+$/g, "");
    pre.innerHTML = fn ? fn(src) : esc(src);
  });

  /* ── Copy buttons on code plates ── */

  document.querySelectorAll(".plate").forEach((plate) => {
    const pre = plate.querySelector("pre");
    if (!pre) return;
    const b = document.createElement("button");
    b.className = "copy";
    b.textContent = "copy";
    b.addEventListener("click", async () => {
      await navigator.clipboard.writeText(pre.textContent);
      b.textContent = "copied";
      setTimeout(() => (b.textContent = "copy"), 1200);
    });
    plate.append(b);
  });

  show(Math.max(0, (parseInt(location.hash.slice(1), 10) || 1) - 1), false);
  addEventListener("hashchange", () =>
    show((parseInt(location.hash.slice(1), 10) || 1) - 1, false)
  );
})();
