/* Explorer of team claude (experiment E4). Plain JavaScript, no library: reads the JSON files of data/
   written by experiments/export_explorer.py and draws SVG charts, a sortable table and field slices. */
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const SPLIT = { train: "training", val: "validation", test: "held-out test" };
  const MARK = { train: "●", val: "■", test: "◆" };
  const fmt = (x, n) => (x === null || x === undefined || !isFinite(x)) ? "–"
    : (Math.abs(x) !== 0 && (Math.abs(x) < 1e-3 || Math.abs(x) >= 1e4)) ? x.toExponential(2) : x.toPrecision(n || 3);
  const mean = (a) => { const v = a.filter((x) => x !== null && isFinite(x)); return v.length ? v.reduce((s, x) => s + x, 0) / v.length : null; };
  const se = (a) => {
    const v = a.filter((x) => x !== null && isFinite(x)); if (v.length < 2) return null;
    const m = mean(v); return Math.sqrt(v.reduce((s, x) => s + (x - m) * (x - m), 0) / (v.length - 1) / v.length);
  };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  let D = null, TABLE = null, HYP = null, JOBS = null, SL = null;
  const state = { sort: "ed_ratio", dir: 1 };

  function load(name) { return fetch("data/" + name).then((r) => { if (!r.ok) throw new Error(name + ": " + r.status); return r.json(); }); }

  /* ---------- a small SVG line chart ---------- */
  function chart(series, o) {
    const W = o.w || 320, H = o.h || 220, m = { l: 52, r: 10, t: 22, b: 34 };
    const xs = series.flatMap((s) => s.x), ys = series.flatMap((s) => s.y).filter((y) => y !== null && isFinite(y) && (!o.logy || y > 0));
    if (!ys.length) return '<svg viewBox="0 0 ' + W + " " + H + '" role="img"><text x="10" y="30" class="ex-t">no data</text></svg>';
    const tx = o.logx ? Math.log10 : (v) => v, ty = o.logy ? Math.log10 : (v) => v;
    let x0 = Math.min(...xs.map(tx)), x1 = Math.max(...xs.map(tx)), y0 = Math.min(...ys.map(ty)), y1 = Math.max(...ys.map(ty));
    if (!o.logy && o.zero) { y0 = Math.min(y0, 0); y1 = Math.max(y1, 0); }
    if (y1 === y0) { y1 += 1; y0 -= 1; }
    const py = (y1 - y0) * 0.08; y0 -= py; y1 += py; const px = (x1 - x0) * 0.04 || 0.5; x0 -= px; x1 += px;
    const X = (v) => m.l + (tx(v) - x0) / (x1 - x0) * (W - m.l - m.r), Y = (v) => H - m.b - (ty(v) - y0) / (y1 - y0) * (H - m.t - m.b);
    let s = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + esc(o.title || "") + '">';
    s += '<text x="' + m.l + '" y="14" class="ex-title">' + esc(o.title || "") + "</text>";
    const ticks = [];
    if (o.logy && Math.floor(y1) - Math.ceil(y0) >= 1) {                      // decades
      const step = Math.ceil((Math.floor(y1) - Math.ceil(y0) + 1) / 5);
      for (let e = Math.ceil(y0); e <= Math.floor(y1); e += step) ticks.push([e, "1e" + e]);
    } else {
      for (let i = 0; i <= 4; i++) { const v = y0 + (y1 - y0) * i / 4; ticks.push([v, fmt(o.logy ? Math.pow(10, v) : v, 2)]); }
    }
    ticks.forEach((t) => {
      const y = H - m.b - (t[0] - y0) / (y1 - y0) * (H - m.t - m.b);
      s += '<line x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + y + '" y2="' + y + '" class="ex-grid"/>';
      s += '<text x="' + (m.l - 5) + '" y="' + (y + 3.5) + '" text-anchor="end" class="ex-t">' + t[1] + "</text>";
    });
    (o.xticks || []).forEach((v) => {
      s += '<text x="' + X(v) + '" y="' + (H - m.b + 13) + '" text-anchor="middle" class="ex-t">' + (o.xfmt ? o.xfmt(v) : v) + "</text>";
    });
    if (!o.logy && y0 < 0 && y1 > 0) s += '<line x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + Y(0) + '" y2="' + Y(0) + '" class="ex-axis"/>';
    s += '<text x="' + (m.l + (W - m.l - m.r) / 2) + '" y="' + (H - 4) + '" text-anchor="middle" class="ex-t">' + esc(o.xlabel || "") + "</text>";
    series.forEach((q) => {
      const pts = q.x.map((x, i) => [x, q.y[i]]).filter((p) => p[1] !== null && isFinite(p[1]) && (!o.logy || p[1] > 0));
      if (q.line !== false && pts.length > 1) {
        s += '<polyline fill="none" class="' + q.cls + '" points="' + pts.map((p) => X(p[0]).toFixed(1) + "," + Y(p[1]).toFixed(1)).join(" ") + '"/>';
      }
      if (q.points !== false) {
        pts.forEach((p, i) => {
          const shape = q.shapes ? q.shapes[i] : "train", cx = X(p[0]), cy = Y(p[1]), r = q.r || 3;
          const tip = "<title>" + esc((q.name || "") + " " + (o.xfmt ? o.xfmt(p[0]) : p[0]) + ": " + fmt(p[1], 4)) + "</title>";
          if (shape === "val") s += '<rect x="' + (cx - r) + '" y="' + (cy - r) + '" width="' + 2 * r + '" height="' + 2 * r + '" class="' + q.cls + ' ex-pt">' + tip + "</rect>";
          else if (shape === "test") s += '<path d="M' + cx + " " + (cy - r - 1) + "L" + (cx + r + 1) + " " + cy + "L" + cx + " " + (cy + r + 1) + "L" + (cx - r - 1) + " " + cy + 'Z" class="' + q.cls + ' ex-pt">' + tip + "</path>";
          else s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" class="' + q.cls + ' ex-pt">' + tip + "</circle>";
        });
      }
    });
    return s + "</svg>";
  }

  /* ---------- controls ---------- */
  function fillControls() {
    $("ex-eta").innerHTML = D.etas.map((e) => '<option value="' + e.eta.toFixed(5) + '"' + (e.split === "test" && !fillControls.done ? (fillControls.done = true, " selected") : "") + ">" +
      MARK[e.split] + " η = " + e.eta.toFixed(4) + " (Rm = " + e.rm + ", " + SPLIT[e.split] + ")</option>").join("");
    const groups = { none: "No constraint", design: "Constraint by model design", loss: "Constraint by a training loss", sampling: "Constraint by the sampling procedure", family: "Model family" };
    $("ex-variant").innerHTML = Object.keys(groups).map((g) => {
      const v = D.variants.filter((x) => x.where === g);
      return v.length ? '<optgroup label="' + groups[g] + '">' + v.map((x) => '<option value="' + x.id + '">' + esc(x.label) + "</option>").join("") + "</optgroup>" : "";
    }).join("");
    const pick = D.variants.find((v) => v.id === "W9_skip_sym") || D.variants[0];
    $("ex-variant").value = pick.id;
    $("ex-metric").innerHTML = D.metrics.map((mm) => '<option value="' + mm.key + '">' + esc(mm.label) + " (" + mm.objective + ")</option>").join("");
    ["ex-eta", "ex-variant", "ex-seed", "ex-metric"].forEach((id) => $(id).addEventListener("change", draw));
  }
  function seedsOf(v) { const s = new Set(); Object.values(v.rows).forEach((r) => r.seeds.forEach((k) => s.add(k))); return [...s].sort(); }
  function value(row, key, seed, abs) {
    if (!row) return null;
    const arr = row[key].map((x) => (abs && x !== null) ? Math.abs(x) : x);
    if (seed === "mean") return mean(arr);
    const i = row.seeds.indexOf(+seed); return i < 0 ? null : arr[i];
  }
  function spectrum(row, key, seed) {
    if (!row || !row[key].length) return [];
    if (seed !== "mean") { const i = row.seeds.indexOf(+seed); return i < 0 ? [] : row[key][i]; }
    const ok = row[key].filter((a) => a && a.length); if (!ok.length) return [];
    return ok[0].map((_, k) => mean(ok.map((a) => a[k])));
  }

  /* ---------- views ---------- */
  function draw() {
    const v = D.variants.find((x) => x.id === $("ex-variant").value), eta = $("ex-eta").value, metric = D.metrics.find((x) => x.key === $("ex-metric").value);
    const seeds = seedsOf(v), sel = $("ex-seed"), keep = sel.value || "mean";
    sel.innerHTML = '<option value="mean">mean over the ' + seeds.length + " seeds</option>" + seeds.map((s) => '<option value="' + s + '">seed ' + s + "</option>").join("");
    sel.value = (keep === "mean" || seeds.includes(+keep)) ? keep : "mean";
    const seed = sel.value, row = v.rows[eta], ref = D.reference[eta], k = D.shells;
    const pair = (key, title, logy) => chart([
      { name: "reference", x: k, y: ref[key], cls: "ex-ref" },
      { name: v.label, x: k, y: spectrum(row, key, seed), cls: "ex-gen" }],
      { title: title, xlabel: "shell k", logy: logy, zero: !logy, xticks: [1, 3, 5, 7, 9] });
    $("ex-spectra").innerHTML = pair("spec_u", "kinetic spectrum E_u(k)", true) + pair("spec_b", "magnetic spectrum E_B(k)", true) + pair("H_shell", "magnetic helicity H(k)", false);
    const cell = (name, g, r, note) => "<tr><th scope=\"row\">" + name + "</th><td>" + fmt(g) + "</td><td>" + fmt(r) + "</td><td>" + (note || "") + "</td></tr>";
    $("ex-stats").innerHTML = "<table class=\"ex-table\"><thead><tr><th>Quantity at η = " + (+eta).toFixed(4) + " (" + SPLIT[ref.split] + ")</th><th>generated</th><th>reference</th><th></th></tr></thead><tbody>" +
      cell("kinetic energy E<sub>u</sub>", value(row, "E_u", seed), ref.E_u) +
      cell("magnetic energy E<sub>B</sub>", value(row, "E_B", seed), ref.E_B) +
      cell("magnetic helicity ⟨A·B⟩", value(row, "hel_m", seed), ref.H_M) +
      cell("magnetic null points per snapshot", value(row, "null_count", seed), ref.null_count_mean, "reference ± " + fmt(ref.null_count_se, 2) + " (SE)") +
      cell("residual of the mean energy balance / injection", value(row, "balance_residual_total", seed), ref.balance_residual_total) +
      cell("relative divergence of B (largest)", value(row, "div_rel_b_max", seed), null, "spectral, double precision") +
      cell("magnetic Taylor wavenumber k<sub>λ</sub>", value(row, "k_lambda", seed), ref.k_lambda) +
      cell("energy distance / noise floor", value(row, "ed_ratio", seed), null, "floor " + fmt(ref.ed_floor, 3) + " (two halves of the reference trajectories)") +
      cell("drift of E<sub>B</sub> after a solver restart", value(row, "restart_drift_eb", seed), ref.restart_drift_eb, row && row.split !== "test" ? "computed on the held-out η only" : "") +
      "</tbody></table>" + (row ? "" : "<p>This variant was not evaluated at this η.</p>");
    const etas = D.etas.map((e) => e.eta), keys = etas.map((e) => e.toFixed(5)), shapes = D.etas.map((e) => e.split);
    const series = [];
    if (seed === "mean") seeds.forEach((s) => series.push({ name: "seed " + s, x: etas, y: keys.map((q) => value(v.rows[q], metric.key, s, metric.abs)), cls: "ex-faint", line: false, shapes: shapes, r: 2 }));
    series.push({ name: seed === "mean" ? "seed mean" : "seed " + seed, x: etas, y: keys.map((q) => value(v.rows[q], metric.key, seed, metric.abs)), cls: "ex-gen", shapes: shapes, r: 3.5 });
    const logy = ["ed_ratio", "div_rel_b_max", "balance_residual_total", "hel_m_err_rel", "restart_drift_eb"].includes(metric.key);
    $("ex-trend").innerHTML = chart(series, { w: 640, h: 260, title: metric.label + " — " + v.label, xlabel: "magnetic diffusivity η  (● training, ■ validation, ◆ held-out test)", logx: true, logy: logy, xticks: [0.03, 0.04, 0.05, 0.06, 0.08], xfmt: (x) => (+x).toFixed(3) });
    $("ex-source").textContent = "Source: " + v.source + "/e4_mhd3d_s<k>.json" + (v.fm_loss ? "; flow-matching loss on a training sample " + fmt(v.fm_loss, 4) + " (π/2 = 1.571 for the exact field of independent unit Gaussians)" : "") + (v.training_time_s ? "; training " + fmt(v.training_time_s, 3) + " s." : ".");
    drawSlices();
  }

  function drawTable() {
    const M = TABLE.metrics, rows = TABLE.rows.slice();
    const get = (r) => state.sort === "label" ? r.label : (r[state.sort] && r[state.sort].mean);
    rows.sort((a, b) => { const x = get(a), y = get(b); if (x === null || x === undefined) return 1; if (y === null || y === undefined) return -1; return (x > y ? 1 : x < y ? -1 : 0) * state.dir; });
    const where = { none: "–", design: "design", loss: "loss", sampling: "sampling", family: "family" };
    const head = '<tr><th><button type="button" data-k="label">Variant</button></th><th>Acts through</th>' + M.map((mm) => '<th><button type="button" data-k="' + mm.key + '" title="' + esc(mm.label) + '">' + mm.objective + " · " + esc(mm.label.split(" (")[0].replace("relative ", "").replace(" of the ensemble", "")) + (state.sort === mm.key ? (state.dir > 0 ? " ▲" : " ▼") : "") + "</button></th>").join("") + "<th>n</th><th>Hypotheses</th></tr>";
    const body = rows.map((r) => "<tr><th scope=\"row\">" + esc(r.label) + "</th><td>" + where[r.where] + "</td>" + M.map((mm) => { const c = r[mm.key]; return "<td>" + (c.mean === null ? "–" : fmt(c.mean) + (c.se !== null ? " ± " + fmt(c.se, 2) : "")) + "</td>"; }).join("") +
      "<td>" + r.ed_ratio.n + "</td><td>" + r.hypotheses.map((h) => '<span class="ex-badge ex-' + h.status + '" title="' + h.status + '">' + h.id + " " + h.status + "</span>").join(" ") + "</td></tr>").join("");
    $("ex-comparative").innerHTML = '<div class="ex-scroll"><table class="ex-table ex-wide"><thead>' + head + "</thead><tbody>" + body + "</tbody></table></div>";
    $("ex-comparative").querySelectorAll("button[data-k]").forEach((b) => b.addEventListener("click", () => {
      const key = b.getAttribute("data-k"); state.dir = state.sort === key ? -state.dir : 1; state.sort = key; drawTable();
    }));
  }

  function drawHyp() {
    const f = $("ex-status").value;
    const rows = HYP.filter((h) => f === "all" || h.status === f);
    $("ex-hyp").innerHTML = rows.map((h) => '<details class="ex-h"><summary><span class="ex-badge ex-' + h.status + '">' + h.id + " " + h.status + "</span> " + esc(h.statement) + "</summary><p><strong>Refutation criterion (written before the computation).</strong> " + esc(h.refutation_criterion || "–") + "</p><p><strong>Verdict.</strong> " + esc(h.verdict || "not yet reviewed") + "</p><p><strong>Script.</strong> <code>" + esc(h.script || "–") + "</code>" + (h.seeds ? " · " + h.seeds + " seeds" : "") + (h.commit ? " · commit " + esc(h.commit) : "") + "</p></details>").join("") || "<p>No hypothesis with this status.</p>";
  }

  function drawJobs() {
    const tot = JOBS.reduce((s, j) => s + (j.usd || 0), 0), hrs = JOBS.reduce((s, j) => s + (j.hours || 0), 0);
    $("ex-jobs").innerHTML = "<p>" + JOBS.length + " ledger entries, " + hrs.toFixed(2) + " GPU hours, " + tot.toFixed(2) + " USD (source: <code>research/compute-ledger.jsonl</code>).</p>" +
      '<div class="ex-scroll"><table class="ex-table ex-wide"><thead><tr><th>End (UTC)</th><th>GPU</th><th>USD/h</th><th>Hours</th><th>USD</th><th>Exit</th><th>Commit</th><th>Command</th></tr></thead><tbody>' +
      JOBS.map((j) => "<tr><td>" + esc((j.time || "").replace("T", " ").replace("Z", "")) + "</td><td>" + esc((j.gpu || "").replace("NVIDIA ", "")) + "</td><td>" + fmt(j.usd_per_hour) + "</td><td>" + fmt(j.hours) + "</td><td>" + fmt(j.usd) + "</td><td>" + (j.rc === null || j.rc === undefined ? "–" : j.rc) + "</td><td><code>" + esc(j.commit || "") + "</code></td><td><code>" + esc(j.command || "") + "</code></td></tr>").join("") + "</tbody></table></div>";
  }

  /* ---------- slices of 3D fields ---------- */
  const decoded = {};
  function field(name) {
    if (!decoded[name]) { const b = atob(SL.fields[name]), a = new Int8Array(b.length); for (let i = 0; i < b.length; i++) a[i] = b.charCodeAt(i) << 24 >> 24; decoded[name] = a; }
    return decoded[name];
  }
  function paint(canvas, name, f, comp, snap, z) {
    const n = SL.shape[2], a = field(name), off = document.createElement("canvas"); off.width = off.height = n;
    const ctx = off.getContext("2d"), img = ctx.createImageData(n, n);
    for (let x = 0; x < n; x++) for (let y = 0; y < n; y++) {
      const q = a[((((snap * 2 + f) * n + x) * n + y) * n + z) * 3 + comp] / 127, t = Math.min(1, Math.abs(q)), p = ((n - 1 - y) * n + x) * 4;
      const c = q >= 0 ? [255 - 215 * t, 255 - 160 * t, 255 - 90 * t] : [255 - 40 * t, 255 - 165 * t, 255 - 215 * t];   // blue (+) / vermillion (−), white at 0
      img.data[p] = c[0]; img.data[p + 1] = c[1]; img.data[p + 2] = c[2]; img.data[p + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    const g = canvas.getContext("2d"); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = "high"; g.clearRect(0, 0, canvas.width, canvas.height); g.drawImage(off, 0, 0, canvas.width, canvas.height);
  }
  function drawSlices() {
    if (!SL) { $("ex-slices-note").textContent = "No field samples were exported."; return; }
    const name = $("ex-variant").value, f = +$("ex-field").value, comp = +$("ex-comp").value, snap = +$("ex-snap").value, z = +$("ex-z").value;
    $("ex-z-out").textContent = "z index " + z + " of " + (SL.shape[2] - 1);
    paint($("ex-c-ref"), "reference", f, comp, snap, z);
    const has = !!SL.fields[name];
    if (has) paint($("ex-c-gen"), name, f, comp, snap, z); else $("ex-c-gen").getContext("2d").clearRect(0, 0, 240, 240);
    const v = D.variants.find((x) => x.id === name);
    $("ex-slices-note").textContent = "Seed 0, η = " + SL.eta.toFixed(4) + " (held-out). Left: reference snapshot " + snap + "; right: " + (has ? "sample " + snap + " of " + v.label : "no sample exported for " + v.label) + ". Colour scale ± " + fmt(SL.scale[f], 3) + " for both panels (blue positive, vermillion negative). The two panels are independent draws: compare their statistics, not their details.";
  }

  function init() {
    Promise.all([load("e4.json"), load("table.json"), load("hypotheses.json"), load("jobs.json"), load("slices.json").catch(() => null)]).then((r) => {
      D = r[0]; TABLE = r[1]; HYP = r[2]; JOBS = r[3]; SL = r[4];
      if (D.quick) $("ex-warn").textContent = "Development data (--quick runs): not to be quoted.";
      fillControls();
      const st = [...new Set(HYP.map((h) => h.status))];
      $("ex-status").innerHTML = '<option value="all">all (' + HYP.length + ")</option>" + st.map((s) => '<option value="' + s + '">' + s + " (" + HYP.filter((h) => h.status === s).length + ")</option>").join("");
      $("ex-status").addEventListener("change", drawHyp);
      if (SL) { $("ex-z").max = SL.shape[2] - 1; $("ex-z").value = Math.floor(SL.shape[2] / 2); $("ex-snap").innerHTML = [...Array(SL.shape[0]).keys()].map((i) => '<option value="' + i + '">' + i + "</option>").join(""); }
      ["ex-field", "ex-comp", "ex-snap", "ex-z"].forEach((id) => $(id).addEventListener("input", drawSlices));
      draw(); drawTable(); drawHyp(); drawJobs();
    }).catch((e) => { $("ex-warn").textContent = "The data files could not be loaded (" + e.message + "). The page must be served over HTTP (GitHub Pages, or `python3 -m http.server` in site/)."; });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
