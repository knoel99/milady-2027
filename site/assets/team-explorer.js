/* MilaDy 2027 — team result explorer, shared by every site/teams/<team>/explorer/ page.
   Reads data/bundle.json (written by experiments/export_explorer.py --team <team>) and fills the
   elements with the ids below when the page has them. Numbers are only read from the bundle;
   means and standard errors over seeds are computed here (SE = sample std / sqrt(n)). */
(function () {
  "use strict";

  var METRICS = {
    c1: "Energy-distance ratio (C1)",
    div_max: "Max relative divergence",
    c4: "Spectrum + helicity error (C4)",
    spectrum_l2: "Shell spectrum, relative L2",
    helicity_rel: "Mean helicity, relative error",
    c3: "Absolute magnetic balance residual"
  };
  var TARGETS = { c1: 1.2, c4: 0.1 };
  var VARIANTS = {
    projected: "sampling constraint", free: "free baseline", learned: "learned flow",
    midpoint: "Fourier midpoint", kmax4: "perfect cutoff kmax=4", kmax6: "perfect cutoff kmax=6",
    kmax7: "perfect cutoff kmax=7"
  };
  var FOURIER = { midpoint: 1, kmax4: 1, kmax6: 1, kmax7: 1 };

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function fmt(x) {
    if (x == null || typeof x !== "number" || !isFinite(x)) return "—";
    if (Number.isInteger(x) && Math.abs(x) < 1e6) return String(x);
    var a = Math.abs(x);
    if (a >= 1e4 || a < 1e-3) return x.toExponential(3);
    return x.toPrecision(4);
  }
  function stats(xs) {
    xs = xs.filter(function (x) { return typeof x === "number" && isFinite(x); });
    var n = xs.length;
    if (!n) return null;
    var m = xs.reduce(function (a, b) { return a + b; }, 0) / n;
    var v = n > 1 ? xs.reduce(function (a, b) { return a + (b - m) * (b - m); }, 0) / (n - 1) : 0;
    return { n: n, mean: m, se: Math.sqrt(v / n), min: Math.min.apply(null, xs), max: Math.max.apply(null, xs), xs: xs };
  }
  function short(file, team) {
    return file.replace(/\.json$/, "").replace(new RegExp("^" + team + "_"), "").replace(/_/g, " ");
  }
  function describe(file, data, team) {
    var d = [];
    if (data.kmax != null) d.push("kmax=" + data.kmax);
    if (data.hidden != null) d.push("width " + data.hidden);
    if (data.steps != null) d.push(data.steps + " steps");
    if (data.train_rm) d.push("train Rm " + data.train_rm.join(", "));
    return short(file, team) + (d.length ? " (" + d.join(", ") + ")" : "");
  }

  /* sortable table: cols = [{k, label, num}] ; rows = objects */
  function table(el, cols, rows, sortKey, desc, limit) {
    if (!el) return;
    var state = { k: sortKey, desc: !!desc, all: !limit };
    function draw() {
      var rs = rows.slice();
      if (state.k) {
        rs.sort(function (a, b) {
          var x = a[state.k], y = b[state.k];
          if (typeof x === "number" && typeof y === "number") return state.desc ? y - x : x - y;
          return state.desc ? String(y).localeCompare(String(x)) : String(x).localeCompare(String(y));
        });
      }
      var h = "<thead><tr>" + cols.map(function (c) {
        return '<th data-k="' + c.k + '" scope="col">' + esc(c.label) + "</th>";
      }).join("") + "</tr></thead><tbody>";
      var hidden = state.all ? 0 : Math.max(0, rs.length - limit);
      if (hidden) rs = rs.slice(0, limit);
      h += rs.map(function (r) {
        return "<tr>" + cols.map(function (c) {
          var v = r[c.k];
          var html = c.html ? c.html(r) : (c.num ? fmt(v) : esc(v));
          return "<td" + (c.num ? ' class="num"' : "") + ">" + html + "</td>";
        }).join("") + "</tr>";
      }).join("");
      el.innerHTML = h + "</tbody>" + (hidden ? '<caption style="caption-side:bottom;text-align:left;padding:.5rem 0">' +
        '<button type="button" class="tb-more">Show the ' + hidden + " other rows</button></caption>" : "");
      var more = el.querySelector(".tb-more");
      if (more) more.addEventListener("click", function () { state.all = true; draw(); });
      el.querySelectorAll("th[data-k]").forEach(function (th) {
        th.addEventListener("click", function () {
          var k = th.getAttribute("data-k");
          state.desc = state.k === k ? !state.desc : false;
          state.k = k;
          draw();
        });
      });
    }
    draw();
  }

  /* horizontal log-scale dot chart: rows = [{label, s (stats) | v (value)}] */
  function chart(el, rows, target, unit) {
    if (!el) return;
    var vals = [];
    rows.forEach(function (r) {
      (r.s ? r.s.xs.concat([r.s.mean - r.s.se, r.s.mean + r.s.se]) : [r.v]).forEach(function (x) {
        if (typeof x === "number" && x > 0 && isFinite(x)) vals.push(x);
      });
    });
    if (target) vals.push(target);
    if (!vals.length) { el.innerHTML = '<p class="xp-note">No positive value to draw on a log axis.</p>'; return; }
    var lo = Math.floor(Math.log10(Math.min.apply(null, vals)));
    var hi = Math.ceil(Math.log10(Math.max.apply(null, vals)));
    if (hi === lo) hi = lo + 1;
    var L = 340, W = 820, R = 20, rowH = 26, top = 24, H = top + rows.length * rowH + 30;
    function x(v) { return L + (Math.log10(v) - lo) / (hi - lo) * (W - L - R); }
    var s = '<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" xmlns="http://www.w3.org/2000/svg">';
    var step = Math.max(1, Math.ceil((hi - lo) / 10));
    for (var e = lo; e <= hi; e += step) {
      var gx = x(Math.pow(10, e));
      s += '<g class="grid"><line x1="' + gx + '" x2="' + gx + '" y1="' + (top - 6) + '" y2="' + (H - 24) + '"/></g>';
      s += '<text x="' + gx + '" y="' + (H - 8) + '" text-anchor="middle">1e' + e + "</text>";
    }
    if (target) {
      var tx = x(target);
      s += '<line class="target" x1="' + tx + '" x2="' + tx + '" y1="' + (top - 10) + '" y2="' + (H - 24) + '"/>';
      s += '<text class="target-label" x="' + (tx + 4) + '" y="' + (top - 10) + '">target ' + target + "</text>";
    }
    rows.forEach(function (r, i) {
      var y = top + i * rowH + rowH / 2;
      s += '<text x="' + (L - 8) + '" y="' + (y + 4) + '" text-anchor="end">' + esc(r.label) + "</text>";
      if (r.s) {
        r.s.xs.forEach(function (v) { if (v > 0) s += '<circle class="seed" cx="' + x(v) + '" cy="' + y + '" r="3"/>'; });
        var a = r.s.mean - r.s.se, b = r.s.mean + r.s.se;
        if (a > 0 && b > 0) s += '<line class="err" x1="' + x(a) + '" x2="' + x(b) + '" y1="' + y + '" y2="' + y + '"/>';
        if (r.s.mean > 0) s += '<circle class="mean" cx="' + x(r.s.mean) + '" cy="' + y + '" r="5.5"><title>' +
          esc(r.label) + ": " + fmt(r.s.mean) + " ± " + fmt(r.s.se) + "</title></circle>";
      } else if (r.v > 0) {
        s += '<circle class="mean" cx="' + x(r.v) + '" cy="' + y + '" r="5.5"><title>' + esc(r.label) + ": " + fmt(r.v) + "</title></circle>";
      }
    });
    el.innerHTML = s + "</svg>" + (unit ? '<p class="xp-note">' + esc(unit) + "</p>" : "");
  }

  function setup(B) {
    var team = B.team || "";
    var R = B.results || {};
    var loading = $("xp-loading");
    if (loading) loading.hidden = true;

    /* ---- stored objectives ---- */
    var M = R[team + "_metrics.json"];
    if ($("xp-kpis") && M) {
      $("xp-kpis").innerHTML = ["c1", "c2", "c3", "c4", "c5"].filter(function (k) { return k in M; }).map(function (k) {
        var src = M[k + "_source"] || M.source || "";
        return '<div class="xp-kpi"><b>' + k.toUpperCase() + '</b><span class="v">' + fmt(M[k]) +
          "</span><small>" + esc(src.replace(/^experiments\/results\//, "")) + "</small></div>";
      }).join("") + (M.model ? '<p class="xp-note" style="grid-column:1/-1">' + esc(M.model) + "</p>" : "");
    }

    /* ---- mechanisms: every result file whose seeds hold variant objects with metrics ---- */
    var series = [];
    Object.keys(R).forEach(function (file) {
      var d = R[file];
      if (!d || !Array.isArray(d.seeds) || !d.seeds.length) return;
      var s0 = d.seeds[0];
      Object.keys(s0).forEach(function (v) {
        if (s0[v] && typeof s0[v] === "object" && "c1" in s0[v]) {
          series.push({ file: file, exp: describe(file, d, team), variant: v, data: d });
        }
      });
    });
    var mSel = $("xp-metric"), sSel = $("xp-seed"), fSel = $("xp-family");
    if (mSel && series.length) {
      Object.keys(METRICS).forEach(function (k) {
        mSel.insertAdjacentHTML("beforeend", '<option value="' + k + '">' + esc(METRICS[k]) + "</option>");
      });
      var seeds = {};
      series.forEach(function (s) { s.data.seeds.forEach(function (x) { seeds[x.seed] = 1; }); });
      Object.keys(seeds).sort(function (a, b) { return a - b; }).forEach(function (k) {
        sSel.insertAdjacentHTML("beforeend", '<option value="' + k + '">seed ' + k + "</option>");
      });
      var drawCompare = function () {
        var m = mSel.value, seed = sSel.value, fam = fSel ? fSel.value : "all";
        var rows = series.filter(function (s) {
          return fam === "all" || (fam === "fourier") === !!FOURIER[s.variant];
        }).map(function (s) {
          var vals = s.data.seeds.map(function (x) { return x[s.variant] ? x[s.variant][m] : null; });
          var st = stats(vals);
          var one = null;
          if (seed !== "mean") {
            var row = s.data.seeds.filter(function (x) { return String(x.seed) === seed; })[0];
            one = row && row[s.variant] ? row[s.variant][m] : null;
          }
          return {
            label: (VARIANTS[s.variant] || s.variant) + " · " + short(s.file, team),
            exp: s.exp, variant: VARIANTS[s.variant] || s.variant, file: s.file,
            s: seed === "mean" ? st : null, v: one,
            mean: seed === "mean" ? (st && st.mean) : one, se: seed === "mean" ? (st && st.se) : null,
            min: st && st.min, max: st && st.max, n: st ? st.n : 0
          };
        });
        rows.sort(function (a, b) { return (a.mean == null) - (b.mean == null) || a.mean - b.mean; });
        chart($("xp-chart"), rows, TARGETS[m]);
        table($("xp-table"), [
          { k: "exp", label: "Experiment (file)" }, { k: "variant", label: "Variant" },
          { k: "mean", label: seed === "mean" ? "Mean" : "Seed " + seed, num: true },
          { k: "se", label: "SE", num: true }, { k: "min", label: "Min", num: true },
          { k: "max", label: "Max", num: true }, { k: "n", label: "Seeds", num: true }
        ], rows, "mean");
      };
      [mSel, sSel, fSel].forEach(function (e) { if (e) e.addEventListener("change", drawCompare); });
      drawCompare();
    }

    /* ---- energy balance ---- */
    var S = R[team + "_stationary.json"];
    if ($("xp-balance") && S) {
      var rows = S.seeds.map(function (x) {
        return { seed: x.seed, ft: x.first.total, fm: x.first.magnetic, st: x.second.total, sm: x.second.magnetic };
      });
      var cols = [{ k: "seed", label: "Seed", num: true }, { k: "ft", label: "First half, total", num: true },
        { k: "fm", label: "First half, magnetic", num: true }, { k: "st", label: "Second half, total", num: true },
        { k: "sm", label: "Second half, magnetic", num: true }];
      table($("xp-balance"), cols, rows, "seed");
      var foot = "<tfoot><tr><th>|mean| ± SE</th>" + ["ft", "fm", "st", "sm"].map(function (k) {
        var st = stats(rows.map(function (r) { return Math.abs(r[k]); }));
        return '<td class="num">' + fmt(st.mean) + " ± " + fmt(st.se) + "</td>";
      }).join("") + "</tr></tfoot>";
      $("xp-balance").insertAdjacentHTML("beforeend", foot);
    }

    /* ---- null counts ---- */
    var nullFiles = Object.keys(R).filter(function (f) { return /nulls/.test(f) && Array.isArray(R[f].seeds); }).sort();
    if ($("xp-nulls") && nullFiles.length) {
      var nrows = nullFiles.map(function (f) {
        var st = stats(R[f].seeds.map(function (x) { return x.relative_error; }));
        var r = { label: short(f, team) + (R[f].kmax != null ? "" : ""), file: f, s: st, mean: st.mean, se: st.se, n: st.n };
        R[f].seeds.forEach(function (x) { r["s" + x.seed] = x.relative_error; });
        return r;
      });
      chart($("xp-nulls-chart"), nrows, 0.1);
      var seedKeys = {};
      nullFiles.forEach(function (f) { R[f].seeds.forEach(function (x) { seedKeys[x.seed] = 1; }); });
      var ncols = [{ k: "label", label: "File" }].concat(Object.keys(seedKeys).sort().map(function (k) {
        return { k: "s" + k, label: "Seed " + k, num: true };
      })).concat([{ k: "mean", label: "Mean", num: true }, { k: "se", label: "SE", num: true }]);
      table($("xp-nulls"), ncols, nrows, "mean");
    }

    /* ---- hypothesis register ---- */
    var H = B.hypotheses || [];
    if ($("xp-hyp") && H.length) {
      var hs = $("xp-hstatus"), hq = $("xp-hq");
      var statuses = {};
      H.forEach(function (h) { statuses[h.status] = (statuses[h.status] || 0) + 1; });
      Object.keys(statuses).sort().forEach(function (k) {
        hs.insertAdjacentHTML("beforeend", '<option value="' + esc(k) + '">' + esc(k) + " (" + statuses[k] + ")</option>");
      });
      var drawH = function () {
        var q = (hq.value || "").toLowerCase(), st = hs.value;
        var rows = H.filter(function (h) {
          return (!st || h.status === st) &&
            (!q || (h.id + " " + h.statement + " " + (h.refutation_criterion || "")).toLowerCase().indexOf(q) >= 0);
        }).map(function (h) {
          return { id: h.id, num: parseInt(String(h.id).replace(/\D/g, ""), 10) || 0, status: h.status, h: h };
        });
        $("xp-hcount").textContent = rows.length + " of " + H.length + " hypotheses";
        table($("xp-hyp"), [
          { k: "num", label: "Id", html: function (r) {
            return "<details><summary><b>" + esc(r.id) + "</b></summary><p><b>Refuted if:</b> " +
              esc(r.h.refutation_criterion) + "</p>" + (r.h.verdict ? "<p><b>Verdict:</b> " + esc(r.h.verdict) + "</p>" : "") +
              (r.h.script ? "<p><code>" + esc(r.h.script) + "</code></p>" : "") + "</details>";
          } },
          { k: "status", label: "Status", html: function (r) {
            return '<span class="xp-status ' + esc(r.status) + '">' + esc(r.status) + "</span>";
          } },
          { k: "statement", label: "Statement", html: function (r) { return esc(r.h.statement); } }
        ], rows, "num", true, 20);
      };
      hs.addEventListener("change", drawH);
      hq.addEventListener("input", drawH);
      drawH();
    }

    /* ---- GPU jobs ---- */
    var J = B.gpu_jobs || [];
    if ($("xp-gpu") && J.length) {
      var sum = function (a, k) { return a.reduce(function (t, r) { return t + (r[k] || 0); }, 0); };
      var ok = J.filter(function (r) { return r.rc === 0; });
      var gpus = {};
      J.forEach(function (r) { gpus[r.gpu] = (gpus[r.gpu] || 0) + 1; });
      var top = Object.keys(gpus).sort(function (a, b) { return gpus[b] - gpus[a]; })[0];
      $("xp-gpu-kpis").innerHTML = [
        ["Jobs", J.length + "", ok.length + " with exit code 0"],
        ["GPU hours", sum(J, "hours").toFixed(2), "all finished jobs"],
        ["Cost", "$" + sum(J, "usd").toFixed(2), "USD, RunPod, from the ledger"],
        ["Most used GPU", top || "—", (gpus[top] || 0) + " jobs"]
      ].map(function (k) {
        return '<div class="xp-kpi"><b>' + esc(k[0]) + '</b><span class="v">' + esc(k[1]) + "</span><small>" + esc(k[2]) + "</small></div>";
      }).join("");
      var rc = $("xp-rc");
      var drawJ = function () {
        var f = rc.value;
        var rows = J.filter(function (r) { return !f || (f === "0" ? r.rc === 0 : r.rc !== 0); }).map(function (r) {
          return { time: r.time, gpu: r.gpu, hours: r.hours, usd: r.usd, rc: r.rc, command: r.command, commit: (r.commit || "").slice(0, 7) };
        });
        table($("xp-gpu"), [
          { k: "time", label: "Finished (UTC)" }, { k: "gpu", label: "GPU" }, { k: "hours", label: "Hours", num: true },
          { k: "usd", label: "USD", num: true }, { k: "rc", label: "Exit", num: true },
          { k: "command", label: "Command", html: function (r) { return "<code>" + esc(r.command) + "</code>"; } },
          { k: "commit", label: "Commit", html: function (r) { return "<code>" + esc(r.commit) + "</code>"; } }
        ], rows, "time", true, 20);
      };
      rc.addEventListener("change", drawJ);
      drawJ();
    }
  }

  /* ---- figures: listed in the bundle by the export script ---- */
  function gallery(B) {
    var g = $("xp-gallery");
    if (!g || !B.figures) return;
    g.innerHTML = B.figures.map(function (f) {
      var href = "../" + f.path;
      return '<figure><a href="' + esc(href) + '"><img loading="lazy" src="' + esc(href) + '" alt="' + esc(f.name) +
        '"></a><figcaption><a href="' + esc(href) + '">' + esc(f.name) + "</a> · " + esc(f.kind) + "</figcaption></figure>";
    }).join("");
  }

  function start() {
    fetch("data/bundle.json", { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error(r.status + " " + r.statusText); return r.json(); })
      .then(function (B) { setup(B); gallery(B); })
      .catch(function (e) {
        var l = $("xp-loading");
        if (l) l.textContent = "Could not load data/bundle.json (" + e.message + ").";
      });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
