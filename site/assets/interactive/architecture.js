/*
 * architecture.js — MilaDy 2027, interactive "architecture" widget.
 * The chain of a simulation campaign (seven stages, two stores) and how it runs on three targets:
 * interactive version of the "architecture" figure of the Computing and data page.
 * Usage: <div class="widget" data-widget="architecture"></div> + <script defer src=".../architecture.js"></script>
 *
 * Content (sources in the repository, paths relative to the root):
 * - stages and modules: computing/index.qmd (table "The processing chain"); src/milady/sweep.py, src/milady/sim/run.py,
 *   src/milady/storage.py, src/milady/catalog/, src/milady/train/fm3d.py, src/milady/eval/metrics.py;
 * - campaign followed: infra/configs/stage2_tg3d.yaml (Re × Pm = 4 × 3, 64³) and infra/configs/train_fm3d.yaml
 *   (validation Re = 100, Pm = 1; test Re = 50, Pm = 2);
 * - services per target: docs/ARCHITECTURE.md § 2, infra/docker/docker-compose.yml, infra/slurm/env.sh,
 *   infra/slurm/*.sbatch, Makefile (targets sweep, train, eval).
 * Nothing is simulated here: the widget shows where each stage runs and what it writes.
 */
(function () {
  "use strict";
  var NAME = "architecture";
  var GH = "https://github.com/knoel99/milady-2027/blob/main/";

  var TXT = {
    title: "The simulation pipeline, target by target",
    targets: ["Laptop", "Cloud GPU VM", "Slurm cluster"],
    play: "Follow a campaign", pause: "Pause", next: "Next stage",
    catalog: "Catalog", files: "Files", exec: "Execution",
    what: "What it does", writesCat: "Writes to the catalog", writesFiles: "Writes to storage",
    onTarget: "On this target", command: "Command", code: "Code", none: "nothing",
    stageWord: "Stage", choose: "Click a stage (or use the arrow keys); pick a target above.",
    svgLabel: "Pipeline diagram: seven stages, catalog and files",
    note: "Campaign followed: stage2_tg3d (Re × Pm = 4 × 3, 64³), trained by train_fm3d. The widget simulates nothing: it shows where each stage runs and what it writes.",
    stages: ["Campaign", "Launch", "Simulation", "Storage", "Dataset", "Training", "Evaluation"],
    does: [
      "Describes the parameter grid and the time settings: here 4 values of Re × 3 values of Pm, 64³ grid, burn-in 100, kept window 40.",
      "Expands the grid into 12 simulations with deterministic identifiers (UUID v5), records them as queued and launches them; relaunching the campaign skips finished simulations.",
      "Integrates 3D MHD (pseudo-spectral, Lawson RK4): diagnostics every 0.1, 40 snapshots of (u, B), a checkpoint every 900 s of compute and on SIGTERM.",
      "Writes the MFF file (HDF5 compatible with The Well), validates it, uploads it as {campaign}/{uuid}/fields.h5 and records its SHA-256 digest.",
      "Selects the finished simulations and splits them by (Re, Pm) point: validation (100; 1), test (50; 2), training for the other 10.",
      "Conditional flow matching on (Re, Pm) over vector potentials truncated at |m| ≤ 8 (divergence-free by construction), exact B → −B symmetry; one or several GPUs (DDP).",
      "Samples the model and compares with the simulations: spectra, helicities, energy budgets, energy distance, sliced Wasserstein.",
    ],
    cat: [["campaign"], ["simulation", "job"], ["diagnostic"], ["file"], ["dataset", "dataset_member"], ["model"], ["evaluation"]],
    fil: [null, null, null, "fields.h5", null, "last.pt, final.pt", "JSON report"],
    rails: [
      { cat: "SQLite · data/catalog.sqlite", fil: "data/store/", exec: "venv, one process per simulation" },
      { cat: "PostgreSQL 16 · :5432", fil: "MinIO (S3) · :9000", exec: "worker-gpu container (milady:gpu)" },
      { cat: "SQLite on $WORK", fil: "$SCRATCH, then copy to S3", exec: "job array, 1 GPU per simulation" },
    ],
    targetNotes: [
      "No GPU, no Docker: a virtual environment (make setup); catalog and files in data/.",
      "Docker Compose: PostgreSQL, MinIO, MLflow and the compute container; ports bound to 127.0.0.1, access through an SSH tunnel (make up, or sudo infra/deploy/bootstrap_vm.sh).",
      "Apptainer image converted from milady:gpu (make sif); nodes without Internet: SQLite catalog on $WORK, files on $SCRATCH, later copied to S3 and ingested into PostgreSQL (milady.catalog ingest).",
    ],
    cmd: [
      ["edit infra/configs/stage2_tg3d.yaml", "edit infra/configs/stage2_tg3d.yaml", "edit infra/configs/stage2_tg3d.yaml"],
      ["python -m milady.sweep infra/configs/stage2_tg3d.yaml --scheduler local", "make sweep CONFIG=infra/configs/stage2_tg3d.yaml", "python -m milady.sweep infra/configs/stage2_tg3d.yaml --scheduler slurm"],
      ["python -m milady.sim.run infra/configs/stage2_tg3d.yaml --index i   (launched by milady.sweep)", "python -m milady.sim.run … --index i   (in the container, launched by milady.sweep)", "sbatch --array=0-11%12 infra/slurm/gen_data.sbatch infra/configs/stage2_tg3d.yaml   (submitted by milady.sweep)"],
      ["automatic, at the end of the simulation (milady.storage)", "automatic, to s3://milady-data (MinIO)", "automatic, to $SCRATCH; then copy to S3 and python -m milady.catalog ingest <uri> --campaign <campaign>"],
      ["automatic when training starts (auto_dataset in train_fm3d.yaml)", "automatic when training starts (auto_dataset)", "automatic when training starts (auto_dataset)"],
      ["python -m milady.train.fm3d --config infra/configs/train_fm3d.yaml", "make train CONFIG=infra/configs/train_fm3d.yaml   (torchrun, all GPUs)", "sbatch infra/slurm/train.sbatch infra/configs/train_fm3d.yaml   (torchrun per node)"],
      ["python -m milady.eval --config infra/configs/train_fm3d.yaml", "make eval CONFIG=infra/configs/train_fm3d.yaml", "sbatch infra/slurm/eval.sbatch infra/configs/train_fm3d.yaml"],
    ],
    onT: [
      ["YAML file versioned with the code", "same", "same"],
      ["one subprocess per simulation", "inside the compute container (SCHEDULER=local) or one container per simulation (SCHEDULER=docker)", "one job-array element per simulation, at most 12 at a time (max_parallel)"],
      ["CPU; a few threads", "the VM's GPU", "1 GPU per array element, Apptainer image; SIGTERM 120 s before the time limit"],
      ["data/store/ folder", "MinIO milady-data bucket", "$SCRATCH/milady/store"],
      ["local SQLite catalog", "the VM's PostgreSQL", "the cluster's SQLite catalog, or PostgreSQL after ingestion"],
      ["CPU (slow); tracking in metrics.jsonl", "all the VM's GPUs; tracking in the MLflow server", "several nodes (DDP); tracking in MLflow SQLite on $WORK"],
      ["CPU", "the VM's GPU", "1 GPU (eval.sbatch)"],
    ],
    codePaths: [["infra/configs/stage2_tg3d.yaml"], ["src/milady/sweep.py"], ["src/milady/sim/run.py", "src/milady/sim/mhd3d.py"], ["src/milady/storage.py", "src/milady/data/format.py"], ["src/milady/train/data.py", "src/milady/catalog/api.py"], ["src/milady/train/fm3d.py"], ["src/milady/eval/metrics.py"]],
    sep: ": ", filShort: [null, null, null, "fields.h5", null, "last.pt", "JSON"],
  };

  var SVGNS = "http://www.w3.org/2000/svg";
  function mk(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function sv(tag, attrs, parent) {
    var e = document.createElementNS(SVGNS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function svText(parent, x, y, s, o) {
    o = o || {};
    var t = sv("text", { x: x, y: y, "font-size": o.size || 13, fill: o.fill || "currentColor", "text-anchor": o.anchor || "start",
      "dominant-baseline": o.baseline || "middle", "font-weight": o.weight || "normal" }, parent);
    if (o.family) t.setAttribute("font-family", o.family);
    t.textContent = s;
    return t;
  }
  function cssVar(cs, name, fb) { var v = cs.getPropertyValue(name); v = v ? v.trim() : ""; return v || fb; }
  function luminance(hex) {
    var m = /^#?([0-9a-f]{6})$/i.exec(hex);
    if (!m) { var r = /rgba?\((\d+)[ ,]+(\d+)[ ,]+(\d+)/i.exec(hex); return r ? (0.2126 * r[1] + 0.7152 * r[2] + 0.0722 * r[3]) / 255 : 1; }
    var n = parseInt(m[1], 16);
    return (0.2126 * ((n >> 16) & 255) + 0.7152 * ((n >> 8) & 255) + 0.0722 * (n & 255)) / 255;
  }
  function reducedMotion() { return !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches); }
  function styleButton(b, pressed) {
    b.setAttribute("aria-pressed", pressed ? "true" : "false");
    b.style.background = pressed ? "var(--ink)" : "transparent";
    b.style.color = pressed ? "var(--bg)" : "var(--ink)";
  }
  var MONO = "'DejaVu Sans Mono', 'Liberation Mono', Consolas, Menlo, monospace";

  function Widget(el) {
    var self = this;
    this.el = el; var T = this.T = TXT;
    this.target = 1; this.stage = 2; this.timer = null;
    el.textContent = "";
    el.appendChild(mk("p", "widget-title", T.title));
    var controls = mk("div", "widget-controls");
    el.appendChild(controls);
    this.tButtons = T.targets.map(function (name, i) {
      var b = mk("button", null, name); b.type = "button";
      b.addEventListener("click", function () { self.target = i; self.update(); });
      controls.appendChild(b); return b;
    });
    var play = this.playBtn = mk("button", null, T.play); play.type = "button";
    play.addEventListener("click", function () { self.togglePlay(); });
    controls.appendChild(play);
    this.wrap = mk("div"); el.appendChild(this.wrap);
    this.tnote = mk("p", "widget-note"); el.appendChild(this.tnote);
    this.details = mk("div", "widget-readout"); this.details.setAttribute("aria-live", "polite");
    this.details.style.marginTop = ".6rem";
    el.appendChild(this.details);
    el.appendChild(mk("p", "widget-note", T.note));
    this.readTheme();
    this.update();
    if (window.ResizeObserver) {
      var lastW = 0;
      new ResizeObserver(function () { var w = Math.round(self.wrap.clientWidth); if (Math.abs(w - lastW) > 4) { lastW = w; self.draw(); } }).observe(this.wrap);
    } else window.addEventListener("resize", function () { self.draw(); });
  }

  Widget.prototype.readTheme = function () {
    var cs = getComputedStyle(document.documentElement);
    var bg = cssVar(cs, "--bg", "#ffffff"), dark = luminance(bg) < 0.4;
    this.C = {
      ink: cssVar(cs, "--ink", "#0a0a0a"), bg: bg, soft: cssVar(cs, "--muted", "#374151"), rule: cssVar(cs, "--rule", "#d1d5db"),
      dark: dark,
      lam: dark ? "#3fd0a2" : "#009E73", u: dark ? "#6cb6ff" : "#0072B2", B: dark ? "#ff9a5c" : "#D55E00", z: dark ? "#b49cf0" : "#6C4BA0",
      cat: dark ? "#25303b" : "#E3E8EE", catEdge: dark ? "#5c6b7a" : "#A9B4C0",
      fil: dark ? "#352f27" : "#EDE8E0", filEdge: dark ? "#7a6d5c" : "#BDB2A2",
      node: dark ? "#1b1f24" : "#ffffff", nodeSel: dark ? "#14352a" : "#e6f5ef",
    };
  };

  Widget.prototype.update = function () {
    var T = this.T, self = this;
    this.tButtons.forEach(function (b, i) { styleButton(b, i === self.target); });
    this.tnote.textContent = T.targetNotes[this.target];
    this.draw();
    this.renderDetails();
  };

  Widget.prototype.select = function (k) { this.stage = Math.max(0, Math.min(6, k)); this.draw(); this.renderDetails(); };

  Widget.prototype.togglePlay = function () {
    var self = this, T = this.T;
    if (reducedMotion()) { this.select(this.stage >= 6 ? 0 : this.stage + 1); this.playBtn.textContent = T.next; return; }
    if (this.timer) { clearInterval(this.timer); this.timer = null; this.playBtn.textContent = T.play; return; }
    this.select(0);
    this.playBtn.textContent = T.pause;
    this.timer = setInterval(function () {
      if (self.stage >= 6) { clearInterval(self.timer); self.timer = null; self.playBtn.textContent = T.play; return; }
      self.select(self.stage + 1);
    }, 1600);
  };

  Widget.prototype.draw = function () {
    var T = this.T, C = this.C, self = this, W = Math.max(300, Math.round(this.wrap.clientWidth || 640));
    this.wrap.textContent = "";
    var wide = W >= 620;
    var H = wide ? 262 : 40 + 7 * 46 + 66;
    var svg = sv("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "group", "aria-label": T.svgLabel }, null);
    svg.style.color = C.ink;
    this.wrap.appendChild(svg);
    var R = T.rails[this.target];
    var nodes = [];
    function stageNode(k, x, y, w, h) {
      var sel = k === self.stage;
      var g = sv("g", { tabindex: "0", role: "button", "aria-pressed": sel ? "true" : "false",
        "aria-label": T.stageWord + " " + (k + 1) + T.sep + T.stages[k] }, svg);
      g.style.cursor = "pointer";
      sv("rect", { x: x, y: y, width: w, height: h, rx: 8, fill: sel ? C.nodeSel : C.node, stroke: sel ? C.lam : C.rule, "stroke-width": sel ? 2.4 : 1.4 }, g);
      var bxc = wide ? x + w / 2 : x + 15, byc = wide ? y + 15 : y + h / 2;
      sv("circle", { cx: bxc, cy: byc, r: 10, fill: sel ? C.lam : (C.dark ? "#6b7280" : "#4d4d4d") }, g);
      svText(g, bxc, byc + 0.5, String(k + 1), { size: 12, weight: "700", fill: "#ffffff", anchor: "middle" });
      if (wide) {
        var name = T.stages[k], fs = 12, maxw = w - 8, lines = [name];
        if (name.length * fs * 0.6 > maxw && name.indexOf(" ") > 0) { var cut = name.lastIndexOf(" ", Math.ceil(name.length / 2) + 2); if (cut < 1) cut = name.indexOf(" "); lines = [name.slice(0, cut), name.slice(cut + 1)]; }
        lines.forEach(function (ln, i) { svText(g, x + w / 2, y + 36 + i * 14 - (lines.length - 1) * 4, ln, { size: fs, weight: "700", fill: C.ink, anchor: "middle" }); });
      }
      if (!wide) svText(g, x + 30, y + h / 2, T.stages[k], { size: 14, weight: "700", fill: C.ink });
      g.addEventListener("click", function () { if (self.timer) self.togglePlay(); self.select(k); });
      g.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); self.select(k); }
        else if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); self.select(k + 1); self.focusStage(k + 1); }
        else if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); self.select(k - 1); self.focusStage(k - 1); }
      });
      nodes.push(g);
      return g;
    }
    function arrow(x1, y1, x2, y2, color, width, dash) {
      var l = sv("line", { x1: x1, y1: y1, x2: x2, y2: y2, stroke: color, "stroke-width": width || 1.6 }, svg);
      if (dash) l.setAttribute("stroke-dasharray", dash);
      var a = Math.atan2(y2 - y1, x2 - x1), hs = 7;
      sv("path", { d: "M" + x2 + "," + y2 + " L" + (x2 - hs * Math.cos(a - 0.45)) + "," + (y2 - hs * Math.sin(a - 0.45)) +
        " L" + (x2 - hs * Math.cos(a + 0.45)) + "," + (y2 - hs * Math.sin(a + 0.45)) + " Z", fill: color }, svg);
    }
    if (wide) {
      var gap = 12, nw = (W - 20 - 6 * gap) / 7, nh = 64, ny = 10;
      for (var k = 0; k < 7; k++) {
        var x = 10 + k * (nw + gap);
        stageNode(k, x, ny, nw, nh);
        if (k < 6) arrow(x + nw + 2, ny + nh / 2, x + nw + gap - 2, ny + nh / 2, C.soft, 1.6);
      }
      // rails
      var cy = 124, fy = 192, rh = 34;
      sv("rect", { x: 10, y: cy, width: W - 20, height: rh, rx: rh / 2, fill: C.cat, stroke: C.catEdge }, svg);
      sv("rect", { x: 10, y: fy, width: W - 20, height: rh, rx: rh / 2, fill: C.fil, stroke: C.filEdge }, svg);
      svText(svg, 14, cy - 10, T.catalog + " · " + R.cat, { size: 12.5, weight: "700", fill: C.ink });
      svText(svg, 14, fy - 10, T.files + " · " + R.fil, { size: 12.5, weight: "700", fill: C.ink });
      svText(svg, W - 12, cy - 10, T.exec + T.sep + R.exec, { size: 12, fill: C.soft, anchor: "end" });
      for (var j = 0; j < 7; j++) {
        var cx = 10 + j * (nw + gap) + nw / 2, sel = j === this.stage;
        var col = sel ? C.lam : C.catEdge;
        sv("line", { x1: cx, y1: ny + nh, x2: cx, y2: cy, stroke: col, "stroke-width": sel ? 2.4 : 1.2 }, svg);
        sv("circle", { cx: cx, cy: cy, r: 3.5, fill: col }, svg);
        svText(svg, cx, cy + rh / 2, T.cat[j][0] + (T.cat[j].length > 1 ? " +" : ""), { size: 11.5, anchor: "middle", family: MONO, fill: C.ink, weight: sel ? "700" : "normal" });
        if (T.fil[j]) {
          var fcol = sel ? C.lam : C.filEdge;
          sv("line", { x1: cx, y1: cy + rh, x2: cx, y2: fy, stroke: fcol, "stroke-width": sel ? 2.4 : 1.2 }, svg);
          sv("circle", { cx: cx, cy: fy, r: 3.5, fill: fcol }, svg);
          svText(svg, cx, fy + rh / 2, T.fil[j].split(",")[0], { size: 11.5, anchor: "middle", family: MONO, fill: C.ink, weight: sel ? "700" : "normal" });
        }
      }
      // campaign token above the selected stage
      var tx = 10 + this.stage * (nw + gap) + nw - 9;
      sv("circle", { cx: tx, cy: ny + 9, r: 4.5, fill: C.lam }, svg);
    } else {
      // vertical table: stage | catalog | files
      var c1 = 6, c1w = Math.min(170, Math.round(W * 0.42)), c2 = c1 + c1w + 8, c3 = c2 + Math.round((W - c2) * 0.56);
      svText(svg, c2, 20, T.catalog, { size: 13, weight: "700", fill: C.ink });
      svText(svg, c3, 20, T.files, { size: 13, weight: "700", fill: C.ink });
      for (var q = 0; q < 7; q++) {
        var yy = 34 + q * 46, s2 = q === this.stage;
        stageNode(q, c1, yy, c1w, 36);
        if (q < 6) arrow(c1 + 15, yy + 36 + 1, c1 + 15, yy + 46 - 1, C.soft, 1.4);
        sv("rect", { x: c2, y: yy + 5, width: c3 - c2 - 8, height: 26, rx: 13, fill: C.cat, stroke: s2 ? C.lam : C.catEdge, "stroke-width": s2 ? 2 : 1 }, svg);
        svText(svg, c2 + 8, yy + 18, T.cat[q][0], { size: 10.5, family: MONO, fill: C.ink, weight: s2 ? "700" : "normal" });
        if (T.fil[q]) {
          sv("rect", { x: c3, y: yy + 5, width: W - c3 - 6, height: 26, rx: 13, fill: C.fil, stroke: s2 ? C.lam : C.filEdge, "stroke-width": s2 ? 2 : 1 }, svg);
          svText(svg, c3 + 7, yy + 18, T.filShort[q], { size: 10.5, family: MONO, fill: C.ink, weight: s2 ? "700" : "normal" });
        }
      }
      
    }
    if (!wide) {
      [[T.catalog, R.cat], [T.files, R.fil], [T.exec, R.exec]].forEach(function (kv, i) {
        svText(svg, 8, H - 50 + i * 17, kv[0] + T.sep + kv[1], { size: 11.5, fill: C.soft });
      });
    }
    this.nodes = nodes;
  };

  Widget.prototype.focusStage = function (k) {
    k = Math.max(0, Math.min(6, k));
    if (this.nodes && this.nodes[k]) this.nodes[k].focus();
  };

  Widget.prototype.renderDetails = function () {
    var T = this.T, k = this.stage, t = this.target, d = this.details;
    d.textContent = "";
    var h = mk("p"); h.style.margin = "0 0 .3rem"; h.style.fontWeight = "700";
    h.textContent = (k + 1) + ". " + T.stages[k] + " — " + T.targets[t];
    d.appendChild(h);
    function row(label, content, code) {
      var p = mk("p"); p.style.margin = ".15rem 0";
      var b = mk("strong", null, label + T.sep); p.appendChild(b);
      if (code) { var c = mk("code", null, content); c.style.wordBreak = "break-word"; p.appendChild(c); }
      else p.appendChild(document.createTextNode(content));
      d.appendChild(p);
    }
    row(T.what, T.does[k]);
    row(T.writesCat, T.cat[k].join(", "), true);
    row(T.writesFiles, T.fil[k] ? T.fil[k] : T.none, !!T.fil[k]);
    row(T.onTarget, T.onT[k][t]);
    row(T.command, T.cmd[k][t], true);
    var p = mk("p"); p.style.margin = ".15rem 0";
    p.appendChild(mk("strong", null, T.code + T.sep));
    T.codePaths[k].forEach(function (path, i) {
      if (i) p.appendChild(document.createTextNode(", "));
      var a = mk("a", null, path); a.href = GH + path; a.rel = "noopener"; p.appendChild(a);
    });
    d.appendChild(p);
  };

  var instances = [];
  function refreshAll() { instances.forEach(function (w) { w.readTheme(); w.draw(); }); }
  function init() {
    var els = document.querySelectorAll('div.widget[data-widget="' + NAME + '"]');
    for (var i = 0; i < els.length; i++) {
      if (els[i].getAttribute("data-ready") === "1") continue;
      els[i].setAttribute("data-ready", "1");
      instances.push(new Widget(els[i]));
    }
    if (instances.length && !init.observing) {
      init.observing = true;
      new MutationObserver(refreshAll).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
      if (window.matchMedia) {
        var mq = window.matchMedia("(prefers-color-scheme: dark)");
        if (mq.addEventListener) mq.addEventListener("change", refreshAll); else if (mq.addListener) mq.addListener(refreshAll);
      }
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
  window.addEventListener("load", init);
})();
