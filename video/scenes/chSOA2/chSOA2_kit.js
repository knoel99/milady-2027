/* chSOA2_kit.js: helpers shared by the scenes of unit chSOA2 (copied from ch09_kit.js, plus the map SM below) (labels with entrance/exit, faded groups,
   series lookup, on-screen text taken from the script). Pure functions of t; elements built in setup only.
   Nothing here duplicates a kit component; candidates for promotion are listed in script/_review/scenes_chSOA2.md. */
window.UK = (function () {
  const K = Kit, S = Scene, U = {};
  /** a text label: {text | html, x, y, anchor 'l'|'c'|'r', size, color (token), cls ('mono' | 'display' | 'halo'), at, out, parent, z, maxW, alpha} */
  U.label = function (ctx, o) {
    const e = K.el('div', { class: 'uk-lab ' + (o.cls || ''), html: o.html ?? K.markup(o.text) }, o.parent || ctx.stage);
    e.style.left = o.x + 'px'; e.style.top = o.y + 'px';
    const a = o.anchor || 'l'; e.style.transform = `translate(${a === 'c' ? '-50%' : a === 'r' ? '-100%' : '0'}, ${o.vmid ? '-50%' : '0'})`;
    if (o.size) e.style.fontSize = o.size + 'px';
    if (o.color) e.style.color = K.c(o.color);
    if (o.z !== undefined) e.style.zIndex = o.z;
    if (o.maxW) { e.style.whiteSpace = 'normal'; e.style.width = o.maxW + 'px'; }
    const { t0, t1 } = K.times(ctx, o, 0), din = o.din ?? 0.25;
    return ctx.add({ root: e, el: e, alpha: 1, render(t) { const v = K.env(t, t0, t1, din, 0.25); K.show(e, v.on); e.style.opacity = (v.o * (o.alpha ?? 1) * this.alpha).toFixed(3); } });
  };
  /** fade an element (HTML or SVG) in at `at` and out at `out` (multiplied by el.__dim if set) */
  U.fade = function (ctx, el, o) {
    const { t0, t1 } = K.times(ctx, o, 0), din = o.din ?? 0.35;
    return ctx.add({ root: el, dim: () => 1, render(t) { const v = K.env(t, t0, t1, din, o.dout ?? 0.3); el.style.display = v.on ? '' : 'none'; el.style.opacity = (v.o * this.dim(t)).toFixed(3); } });
  };
  U.series = (D, name) => { const s = D.series.find((x) => x.name === name); if (!s) throw new Error('series not found: ' + name); return s; };
  /** an on-screen label of the script that starts with `prefix` (keeps the writer's text, numbers included) */
  U.onscreen = (ctx, prefix, fallback) => { const L = (ctx.script && ctx.script.onscreen && ctx.script.onscreen.labels) || []; return L.find((x) => x.startsWith(prefix)) || fallback; };
  /** time of a fraction of the sentence whose cue is `cue` (falls back to cue + dt in previews) */
  U.frac = function (ctx, cue, f, dt) {
    const s = ctx.script && ctx.script.sentences && ctx.script.sentences.find((x) => x.cue === cue);
    return s && Number.isFinite(s.end) ? s.start + f * (s.end - s.start) : ctx.at(cue) + (dt ?? 2);
  };
  U.end = (ctx, cue, dt) => U.frac(ctx, cue, 1, dt);
  /** percent label from a fraction (display rounding only) */
  U.pc = (v) => `${Math.round(v)} %`;
  return U;
})();
/** the script's formulas, each split at its top-level ';' into at most two items when it is long (same text, shown
   one after the other: the first on its cue, the second `dt` s later); for Kit.formulaLayer({items}) */
UK.formulaItems = function (ctx, maxLen = 110, dt = 4) {
  const F = (ctx.script && ctx.script.onscreen && ctx.script.onscreen.formulas) || [];
  const out = [];
  F.forEach((f) => {
    const tex = f.tex, cuts = []; let depth = 0;
    for (let i = 0; i < tex.length; i++) { const c = tex[i]; if (c === '{') depth++; else if (c === '}') depth--; else if (c === ';' && depth === 0) cuts.push(i); }
    if (!cuts.length) { depth = 0; for (let i = 0; i < tex.length; i++) { const c = tex[i]; if (c === '{') depth++; else if (c === '}') depth--; else if (depth === 0 && c === '+' && i > 0) cuts.push(-i); } }   // a sum: cut before a top-level '+'
    if (!cuts.length) { depth = 0; for (let i = 0; i < tex.length; i++) { const c = tex[i]; if (c === '{') depth++; else if (c === '}') depth--; else if (depth === 0 && tex.startsWith('\\ \\ ', i)) cuts.push(i); } }   // a '\ \ ' gap
    if (tex.length <= maxLen || !cuts.length) { out.push({ tex, at: f.cue, out: f.out }); return; }
    const abs = cuts.map(Math.abs), mid = abs.reduce((b, c) => (Math.abs(c - tex.length / 2) < Math.abs(b - tex.length / 2) ? c : b), abs[0]);
    const plus = cuts.includes(-mid);
    const a = tex.slice(0, mid).trim(), b = (plus ? '\\dots ' + tex.slice(mid) : tex.slice(mid + 1)).replace(/^(\\[ ,;!]|\\quad|\\qquad|\s)+/, '').trim();
    out.push({ tex: a, at: f.cue }, { tex: b, at: `${f.cue}+${dt}`, out: f.out });
  });
  return out;
};

/* ===================== SM: the map of the field (zoomed data-driven lanes) =====================
   Lanes are rows; the focused row grows (its pins get stacked labels), the others shrink to thin strips with their
   pins as unlabelled dots. A gate grid (3D · WALLS · LOW Pm · RARE) sits at the right; one row of verdict cells per
   lane. Years and verdicts are the script's dated facts (entry.params of each scene; SM.ALL_PINS / SM.ALL_VERDICTS
   below are a transcript of them, regenerated from script/chSOA2.json by the builder). */
window.SM = (function () {
  const K = Kit, S = Scene, SM = {};
  SM.LABELS = { dynamo: 'DYNAMO TRACKS', 'dynamo.THEORY': 'THEORY', 'dynamo.LAB DYNAMOS': 'LAB DYNAMOS', 'dynamo.SIMULATIONS': 'SIMULATIONS', 'dynamo.REDUCED MODELS': 'REDUCED MODELS',
    surrogates: 'SURROGATES', generative: 'GENERATIVE MODELS', constraints: 'CONSTRAINTS', 'constraints.HARD': 'HARD', 'constraints.SOFT': 'SOFT', 'constraints.DISTRIBUTIONAL': 'DISTRIBUTIONAL',
    'constraints.SYMMETRY': 'SYMMETRY', assimilation: 'ASSIMILATION PRIORS', datadriven: 'DATA-DRIVEN', record: "EARTH'S RECORD" };
  SM.ROWS = ['dynamo', 'surrogates', 'generative', 'constraints.HARD', 'constraints.SOFT', 'constraints.DISTRIBUTIONAL', 'constraints.SYMMETRY', 'assimilation'];
  SM.GATES = [['3d', '3D'], ['walls', 'WALLS'], ['lowpm', 'LOW Pm'], ['rare', 'RARE']];
  SM.ICON = { yes: '✓', partly: '≈', no: '✗', open: '?' };
  SM.year = (y) => parseFloat(String(y));
  SM.col = (c) => K.c(c === 'b-flip' ? 'b' : c || 'chalk');
  /** o: {axis: [y0, y1], x0, x1, rows, y0, y1, small, focus: [{at, key}], at, gates: true, now: 2026.85} */
  SM.map = function (ctx, o = {}) {
    const ax = o.axis || [2012, 2031], X0 = o.x0 ?? 360, X1 = o.x1 ?? 1310, rows = o.rows || SM.ROWS;
    const Y0 = o.y0 ?? 160, Y1 = o.y1 ?? 736, small = o.small ?? 34;
    const x = (yr) => X0 + (X1 - X0) * (SM.year(yr) - ax[0]) / (ax[1] - ax[0]);
    const focus = (o.focus || []).map((f) => ({ t: typeof f.at === 'number' ? f.at : ctx.at(f.at), key: f.key }));
    const t0 = typeof o.at === 'number' ? o.at : ctx.at(o.at ?? -0.3);
    const svg = K.svgLayer(ctx, o.z ?? 11), g = K.s('g', {}, svg), lay = K.el('div', {}, ctx.stage); lay.style.cssText = 'position:absolute;inset:0;z-index:31';
    // weights: the focused row grows (0.6 s), the previous one shrinks
    const weight = (t) => { const w = rows.map(() => 0); let prev = null, tp = -1e9;
      for (const f of focus) { if (t < f.t) break; prev = { key: f.key, t: f.t, from: prev }; }
      if (!prev) return w;
      const p = S.seg(t, prev.t, prev.t + 0.6, S.ease.inOutCubic);
      rows.forEach((k, i) => { if (k === prev.key) w[i] += p; if (prev.from && k === prev.from.key) w[i] += 1 - p; });
      void tp; return w; };
    const layout = (t) => { const w = weight(t), sum = w.reduce((a, b) => a + b, 0), big = (Y1 - Y0) - small * rows.length;
      const eq = (Y1 - Y0) / rows.length; let y = Y0; const out = {};
      rows.forEach((k, i) => { const h = sum > 0 ? small + big * w[i] / Math.max(1, sum) : eq; out[k] = { y0: y, y1: y + h, w: sum > 0 ? w[i] : 0 }; y += h; }); return out; };
    // axis
    const axg = K.s('g', {}, g), muted = K.c('muted');
    const step = ax[1] - ax[0] > 60 ? 25 : ax[1] - ax[0] > 25 ? 10 : 4, first = Math.ceil(ax[0] / step) * step;
    for (let yr = first; yr <= ax[1] - 2; yr += step) { K.s('line', { x1: x(yr), x2: x(yr), y1: Y0 - 8, y2: Y1, stroke: K.c('grid'), 'stroke-width': 1.5 }, axg); K.s('text', { x: x(yr), y: Y0 - 18, 'text-anchor': 'middle', class: 'kt-tick' }, axg, String(yr)); }
    const nowYr = o.now ?? 2026.85, nowL = K.s('line', { x1: x(nowYr), x2: x(nowYr), y1: Y0 - 8, y2: Y1, stroke: K.c('chalk'), 'stroke-width': 2 }, axg);
    K.s('line', { x1: x(nowYr), x2: x(ax[1]), y1: Y1 + 6, y2: Y1 + 6, stroke: muted, 'stroke-width': 2, 'stroke-dasharray': '6 8' }, axg);
    // rows: separators and gutter labels (rebuilt positions every frame)
    const sep = rows.map(() => K.s('line', { x1: 96, x2: X1 + 20, stroke: K.c('grid'), 'stroke-width': 2 }, g));
    const labs = rows.map((k) => { const e = K.el('div', { class: 'uk-lab' }, lay, SM.LABELS[k] || k); e.style.cssText += `;font-size:28px;font-weight:600;color:var(--muted);left:${k.includes('.') ? 150 : 104}px`; return e; });
    const brk = {}; ['constraints', 'dynamo'].forEach((p) => { if (rows.some((k) => k.startsWith(p + '.'))) { brk[p] = { line: K.s('line', { x1: 128, x2: 128, stroke: muted, 'stroke-width': 2 }, g),
      lab: (() => { const e = K.el('div', { class: 'uk-lab' }, lay, SM.LABELS[p]); e.style.cssText += ';font-size:28px;font-weight:600;color:var(--muted);transform-origin:0 0;transform:rotate(-90deg)'; return e; })() }; } });
    // gate grid
    const GX = o.gx ?? 1352, GW = (1824 - GX) / 4, gx = (i) => GX + GW * (i + 0.5);
    const gateG = K.s('g', {}, g), heads = SM.GATES.map(([k, l], i) => { const e = K.el('div', { class: 'uk-lab' }, lay, l); e.style.cssText += `;font-size:28px;font-weight:500;left:${gx(i)}px;top:${Y0 - 52}px;transform:translateX(-50%)`; return e; });
    SM.GATES.forEach((_, i) => K.s('line', { x1: GX + GW * i, x2: GX + GW * i, y1: Y0 - 8, y2: Y1, stroke: K.c('grid'), 'stroke-width': 2 }, gateG));
    const cells = [];
    const M = { x, rows, layout, svg, g, lay, heads, gx, GW, Y0, Y1, X0, X1, t0, nowL, pins: [], cells, items: [] };
    /** pins: [{id, lane, year, label, glyph, color, names, at|cue}] with stacked labels while the row is focused */
    M.addPins = function (pins, po = {}) {
      const byCue = {};
      pins.forEach((p) => {
        const row = rows.includes(p.lane) ? p.lane : rows.find((k) => p.lane.startsWith(k + '.') || k.startsWith(p.lane + '.')) || p.lane;
        let at = p.at; if (at === undefined) { const c = p.cue || 'map'; byCue[c] = (byCue[c] || 0) + 1; at = ctx.at(c + '-0.15') + 0.35 * (byCue[c] - 1); }
        if (typeof at !== 'number') at = ctx.at(at);
        const col = SM.col(p.color), pg = K.s('g', {}, g);
        const gl = p.glyph || 'dot';
        if (gl === 'ring') K.s('circle', { r: 11, fill: K.c('bg'), stroke: col, 'stroke-width': 3.5 }, pg);
        else if (gl === 'diamond') K.s('path', { d: 'M0,-13 L13,0 L0,13 L-13,0 Z', fill: K.c('bg'), stroke: col, 'stroke-width': 3.5 }, pg);
        else if (gl === 'cross') K.s('path', { d: 'M-9,-9 L9,9 M9,-9 L-9,9', stroke: col, 'stroke-width': 4 }, pg);
        else if (gl === 'dashed') K.s('circle', { r: 15, fill: 'none', stroke: col, 'stroke-width': 3, 'stroke-dasharray': '5 5' }, pg);
        else if (gl === 'square') K.s('rect', { x: -11, y: -11, width: 22, height: 22, fill: 'none', stroke: col, 'stroke-width': 3.5 }, pg);
        else K.s('circle', { r: 8, fill: col }, pg);
        const leader = K.s('line', { stroke: K.c('muted'), 'stroke-width': 1.5 }, g);
        let lab = null;
        if (p.label && po.labels !== false) {
          const txt = `${p.names ? p.names + ' · ' : ''}${p.year} · ${p.label}`;
          lab = K.el('div', { class: 'uk-lab halo' }, lay, txt); lab.style.fontSize = '28px';
          if (p.names) lab.style.fontWeight = '600';
        }
        M.pins.push({ p, row, at, pg, leader, lab, w: lab ? lab.offsetWidth : 0, k: 0, out: p.out !== undefined ? (typeof p.out === 'number' ? p.out : ctx.at(p.out)) : 1e9 });
      });
      // stacking order per row: in order of appearance
      const per = {}; M.pins.forEach((q) => { if (!q.lab) return; per[q.row] = per[q.row] || []; q.k = per[q.row].length; per[q.row].push(q); });
      return M;
    };
    /** verdict cells for a row (row key or 'constraints'), filling one by one from `at` */
    M.verdicts = function (key, v, at, opts = {}) {
      const a = typeof at === 'number' ? at : ctx.at(at);
      SM.GATES.forEach(([gk], i) => { const e = K.el('div', { class: 'uk-lab' }, lay, SM.ICON[v[gk]] || ''); e.style.cssText += `;font-size:36px;transform:translate(-50%,-50%);left:${gx(i)}px`;
        const r = K.s('rect', { width: GW - 16, rx: 6, fill: 'none', stroke: K.c('muted'), 'stroke-width': 2, 'stroke-dasharray': '6 6' }, gateG);
        cells.push({ key, e, r, i, at: a + 0.3 * i, dim: opts.dim }); });
    };
    M.rowBox = (key, t) => { const L = layout(t); if (L[key]) return L[key]; const ks = rows.filter((k) => k.startsWith(key + '.')); return { y0: L[ks[0]].y0, y1: L[ks[ks.length - 1]].y1, w: Math.max(...ks.map((k) => L[k].w)) }; };
    const tOut = o.out !== undefined ? (typeof o.out === 'number' ? o.out : ctx.at(o.out)) : 1e9;
    M.dim = () => 1;
    if (o.gates === false) { gateG.style.display = 'none'; heads.forEach((h) => { h.style.display = 'none'; }); }
    M.gatesAlpha = () => 1;
    ctx.add({ render(t) {
      const L = layout(t), on = t >= t0 && t < tOut + 0.5, a = S.seg(t, t0, t0 + 0.4, S.ease.linear) * (1 - S.seg(t, tOut, tOut + 0.5, S.ease.linear)) * M.dim(t);
      if (o.gates !== false) { const ga = M.gatesAlpha(t); gateG.style.opacity = ga; heads.forEach((h) => { h.style.opacity = ga; }); }
      g.style.display = on ? '' : 'none'; lay.style.display = on ? '' : 'none'; g.style.opacity = a; lay.style.opacity = a;
      nowL.setAttribute('opacity', (0.55 + 0.35 * Math.sin(2 * Math.PI * t / 4)).toFixed(3));
      rows.forEach((k, i) => { const r = L[k]; sep[i].setAttribute('y1', r.y0); sep[i].setAttribute('y2', r.y0);
        labs[i].style.top = (r.w > 0.5 && r.y1 - r.y0 > 120 ? r.y0 + 4 : (r.y0 + r.y1) / 2 - 17).toFixed(1) + 'px'; labs[i].style.color = r.w > 0.5 ? 'var(--fg)' : ''; labs[i].style.opacity = (r.y1 - r.y0 < 30 ? 0 : 1); });
      for (const [p, b] of Object.entries(brk)) { const ks = rows.filter((k) => k.startsWith(p + '.')), ya = L[ks[0]].y0 + 4, yb = L[ks[ks.length - 1]].y1 - 4, open = yb - ya > 260;
        b.line.setAttribute('y1', ya); b.line.setAttribute('y2', yb); b.line.style.opacity = open ? 1 : 0; b.lab.style.left = '96px'; b.lab.style.top = ((ya + yb) / 2 + 100).toFixed(1) + 'px'; b.lab.style.display = open ? '' : 'none';
        ks.forEach((k, j) => { const e = labs[rows.indexOf(k)]; if (open) { e.textContent = SM.LABELS[k]; e.style.left = '150px'; e.style.opacity = L[k].y1 - L[k].y0 < 30 ? 0 : 1; }
          else { e.textContent = j ? '' : SM.LABELS[p]; e.style.left = '104px'; e.style.top = (ya + (yb - ya) / 2 - 17).toFixed(1) + 'px'; } }); }
      for (const q of M.pins) {
        const r = L[q.row] || M.rowBox(q.row, t), px = x(q.p.year), py = r.y1 - 16, ap = S.seg(t, q.at, q.at + 0.25, S.ease.outCubic) * (1 - S.seg(t, q.out, q.out + 0.3, S.ease.linear));
        q.pg.setAttribute('transform', `translate(${px.toFixed(1)} ${py.toFixed(1)}) scale(${(0.6 + 0.4 * ap).toFixed(3)})`); q.pg.style.opacity = ap > 0 ? Math.max(0.35, ap * (r.w > 0.5 ? 1 : 0.6)) : 0;
        if (q.lab) { const ly = r.y0 + 42 + 34 * q.k, la = ap * S.seg(r.w, 0.6, 1, S.ease.linear) * (q.hideLab ? q.hideLab(t) : 1);
          q.lab.style.top = ly.toFixed(1) + 'px'; const right = px > 1000; if (!q.wm) { q.lab.style.display = ''; q.w = q.lab.offsetWidth; q.wm = q.w > 0; } const w = q.w;
          q.lab.style.left = Math.max(q.row.includes('.') ? 150 : 104, Math.min(right ? px + 12 - w : px - 12, GX - 16 - w)) + 'px'; q.lab.style.transform = '';
          q.lab.style.opacity = la.toFixed(3); q.lab.style.display = la > 0.01 ? '' : 'none';
          q.leader.setAttribute('x1', px); q.leader.setAttribute('x2', px); q.leader.setAttribute('y1', ly + 32); q.leader.setAttribute('y2', py - 10); q.leader.style.opacity = (0.6 * la).toFixed(3); }
        else q.leader.style.opacity = 0;
      }
      for (const c of cells) { const r = M.rowBox(c.key, t), cy = (r.y0 + r.y1) / 2, h = Math.max(20, Math.min(56, r.y1 - r.y0 - 8)), p = S.seg(t, c.at, c.at + 0.3, S.ease.linear);
        c.r.setAttribute('x', M.gx(c.i) - (M.GW - 16) / 2); c.r.setAttribute('y', cy - h / 2); c.r.setAttribute('height', h); c.r.style.opacity = c.dim ? 0.5 : 1;
        c.e.style.top = cy + 'px'; c.e.style.opacity = (p * (c.dim ? 0.5 : 1) * M.gatesAlpha(t)).toFixed(3); c.e.style.fontSize = (h < 36 ? 28 : 36) + 'px'; }
    } });
    return M;
  };
  return SM;
})();
SM.ALL_PINS = [{"id": "s_pinn", "scene": "SOA2.2", "lane": "surrogates", "year": "2019", "glyph": "dot", "color": "chalk"}, {"id": "s_ops", "scene": "SOA2.2", "lane": "surrogates", "year": "2021", "glyph": "dot", "color": "chalk"}, {"id": "s_found", "scene": "SOA2.2", "lane": "surrogates", "year": "2024", "glyph": "dot", "color": "chalk"}, {"id": "s_mhd23", "scene": "SOA2.2", "lane": "surrogates", "year": "2023", "glyph": "dot", "color": "chalk"}, {"id": "s_mhd25", "scene": "SOA2.2", "lane": "surrogates", "year": "2025", "glyph": "dot", "color": "chalk"}, {"id": "s_alpha", "scene": "SOA2.2", "lane": "surrogates", "year": "2019", "glyph": "dot", "color": "chalk"}, {"id": "s_gwirtz", "scene": "SOA2.2", "lane": "surrogates", "year": "2022", "glyph": "cross", "color": "b-flip"}, {"id": "s_mean", "scene": "SOA2.2", "lane": "surrogates", "year": "2024", "glyph": "dot", "color": "chalk"}, {"id": "g_gan", "scene": "SOA2.3", "lane": "generative", "year": "2014", "glyph": "dot", "color": "model"}, {"id": "g_ddpm", "scene": "SOA2.3", "lane": "generative", "year": "2020", "glyph": "dot", "color": "model"}, {"id": "g_fm", "scene": "SOA2.3", "lane": "generative", "year": "2023", "glyph": "dot", "color": "model"}, {"id": "g_3d", "scene": "SOA2.3", "lane": "generative", "year": "2024", "glyph": "dot", "color": "model"}, {"id": "g_gencast", "scene": "SOA2.3", "lane": "generative", "year": "2025", "glyph": "dot", "color": "model"}, {"id": "g_gencfd", "scene": "SOA2.3", "lane": "generative", "year": "2026", "glyph": "dot", "color": "model"}, {"id": "g_steady", "scene": "SOA2.3", "lane": "generative", "year": "2026", "glyph": "dot", "color": "model"}, {"id": "g_empty", "scene": "SOA2.3", "lane": "generative", "year": "2026", "glyph": "dashed", "color": "model"}, {"id": "c_dfnet", "scene": "SOA2.4", "lane": "constraints.HARD", "year": "2022", "glyph": "dot", "color": "chalk"}, {"id": "c_vecpot", "scene": "SOA2.4", "lane": "constraints.HARD", "year": "2023", "glyph": "dot", "color": "chalk"}, {"id": "c_fundiff", "scene": "SOA2.4", "lane": "constraints.HARD", "year": "2026", "glyph": "dot", "color": "model"}, {"id": "c_proj", "scene": "SOA2.4", "lane": "constraints.HARD", "year": "2025", "glyph": "dot", "color": "chalk"}, {"id": "c_pcdm", "scene": "SOA2.4", "lane": "constraints.HARD", "year": "2026", "glyph": "dot", "color": "model"}, {"id": "c_corona", "scene": "SOA2.4", "lane": "constraints.HARD", "year": "2025", "glyph": "dot", "color": "model"}, {"id": "c_pidm", "scene": "SOA2.4", "lane": "constraints.SOFT", "year": "2025", "glyph": "dot", "color": "model"}, {"id": "c_pbfm", "scene": "SOA2.4", "lane": "constraints.SOFT", "year": "2026", "glyph": "dot", "color": "model"}, {"id": "c_cov", "scene": "SOA2.4", "lane": "constraints.DISTRIBUTIONAL", "year": "2020", "glyph": "dot", "color": "metric"}, {"id": "c_dual", "scene": "SOA2.4", "lane": "constraints.DISTRIBUTIONAL", "year": "2024", "glyph": "dot", "color": "metric"}, {"id": "c_wgs", "scene": "SOA2.4", "lane": "constraints.DISTRIBUTIONAL", "year": "2026", "glyph": "dot", "color": "metric"}, {"id": "c_tilt", "scene": "SOA2.4", "lane": "constraints.DISTRIBUTIONAL", "year": "2026", "glyph": "dot", "color": "metric"}, {"id": "c_eqflow", "scene": "SOA2.4", "lane": "constraints.SYMMETRY", "year": "2020", "glyph": "dot", "color": "chalk"}, {"id": "c_eqfm", "scene": "SOA2.4", "lane": "constraints.SYMMETRY", "year": "2023", "glyph": "dot", "color": "model"}, {"id": "c_cmp", "scene": "SOA2.4", "lane": "constraints", "year": "2026", "glyph": "chip", "color": "chalk"}, {"id": "c_empty", "scene": "SOA2.4", "lane": "constraints.HARD", "year": "2026", "glyph": "dashed", "color": "chalk"}, {"id": "a_latent", "scene": "SOA2.5", "lane": "assimilation", "year": "2021", "glyph": "dot", "color": "chalk"}, {"id": "a_gla", "scene": "SOA2.5", "lane": "assimilation", "year": "2022", "glyph": "ring", "color": "chalk"}, {"id": "a_sda", "scene": "SOA2.5", "lane": "assimilation", "year": "2023", "glyph": "dot", "color": "model"}, {"id": "a_diffda", "scene": "SOA2.5", "lane": "assimilation", "year": "2024", "glyph": "dot", "color": "model"}, {"id": "a_torchda", "scene": "SOA2.5", "lane": "assimilation", "year": "2025", "glyph": "ring", "color": "chalk"}, {"id": "a_empty", "scene": "SOA2.5", "lane": "assimilation", "year": "2026", "glyph": "dashed", "color": "chalk"}, {"id": "r_nore97", "scene": "SOA2.6", "lane": "dynamo.SIMULATIONS", "year": "1997", "glyph": "ring", "color": "chalk"}, {"id": "r_ponty05", "scene": "SOA2.6", "lane": "dynamo.SIMULATIONS", "year": "2005", "glyph": "ring", "color": "param"}, {"id": "r_ponty07", "scene": "SOA2.6", "lane": "dynamo.SIMULATIONS", "year": "2007", "glyph": "ring", "color": "chalk"}, {"id": "r_sfemans", "scene": "SOA2.6", "lane": "dynamo.SIMULATIONS", "year": "2007-", "glyph": "ring", "color": "chalk"}, {"id": "r_nore16", "scene": "SOA2.6", "lane": "dynamo.SIMULATIONS", "year": "2016 / 2018", "glyph": "ring", "color": "chalk"}, {"id": "r_latu", "scene": "SOA2.6", "lane": "dynamo.SIMULATIONS", "year": "2014 / 2017", "glyph": "ring", "color": "chalk"}, {"id": "d_bousquet26", "scene": "SOA2.6", "lane": "dynamo.REDUCED MODELS", "year": "2026", "glyph": "diamond", "color": "b-flip"}, {"id": "d_botez26", "scene": "SOA2.6", "lane": "dynamo.SIMULATIONS", "year": "2026", "glyph": "diamond", "color": "param"}, {"id": "r_lucor07", "scene": "SOA2.6", "lane": "surrogates", "year": "2007", "glyph": "ring", "color": "chalk"}, {"id": "r_lucor24", "scene": "SOA2.6", "lane": "surrogates", "year": "2024", "glyph": "ring", "color": "chalk"}, {"id": "r_bnl25", "scene": "SOA2.6", "lane": "surrogates", "year": "2025", "glyph": "ring", "color": "chalk"}, {"id": "r_cheng_diff", "scene": "SOA2.6", "lane": "generative", "year": "2025 / 2026", "glyph": "ring", "color": "model"}];
SM.ALL_VERDICTS = {"surrogates": {"3d": "partly", "walls": "no", "lowpm": "no", "rare": "no"}, "generative": {"3d": "yes", "walls": "partly", "lowpm": "no", "rare": "partly"}, "constraints": {"3d": "partly", "walls": "no", "lowpm": "no", "rare": "no"}, "assimilation": {"3d": "yes", "walls": "partly", "lowpm": "no", "rare": "open"}, "thesis": {"3d": "open", "walls": "open", "lowpm": "no", "rare": "open"}};

/** a lane scene of SOA2.2-SOA2.5: map focused on P.lane (or on o.focus), earlier scenes' pins as unlabelled dots and
   their verdict rows dimmed, this scene's pins on their cues, its verdict row at P.verdict_at, reference
   lower-thirds from P.lower_thirds, the 'our reading' chip */
SM.laneScene = function (ctx, P, o = {}) {
  const K = Kit, order = ['SOA2.2', 'SOA2.3', 'SOA2.4', 'SOA2.5', 'SOA2.6'], me = ctx.script && ctx.script.id ? ctx.script.id : o.id;
  const before = order.slice(0, Math.max(0, order.indexOf(me)));
  const M = SM.map(ctx, Object.assign({ focus: o.focus || [{ at: -1, key: P.lane }], at: -0.3 }, o.map || {}));
  M.addPins(SM.ALL_PINS.filter((p) => before.includes(p.scene) && !p.lane.startsWith('dynamo')).map((p) => Object.assign({}, p, { label: null, at: -0.3 })), { labels: false });
  M.addPins(P.pins || []);
  const laneOf = { 'SOA2.2': 'surrogates', 'SOA2.3': 'generative', 'SOA2.4': 'constraints', 'SOA2.5': 'assimilation' };
  before.forEach((s) => { const l = laneOf[s]; if (l && SM.ALL_VERDICTS[l]) M.verdicts(l, SM.ALL_VERDICTS[l], -0.3, { dim: true }); });
  if (P.verdicts) M.verdicts(P.lane, P.verdicts, P.verdict_at);
  if (P.verdicts) K.chip(ctx, { text: 'gate verdicts: our reading of abstracts', kind: 'plain', x: 96, y: 52, at: before.length ? -0.3 : P.verdict_at });
  (P.lower_thirds || []).forEach((l) => { const pin = (P.pins || []).find((p) => p.id === l.pin); if (pin && pin.ref) K.lowerThird(ctx, { kind: 'reference', l1: 'Reference', l2: pin.ref, at: l.cue + '+0.3', hold: l.hold }); });
  return M;
};
/** WORKAROUND (kit issue: Kit.formulaLayer keeps its empty frame and label between an item's `out` and the next
   item): one layer per item, each with its own at/out (out = the item's out, else the next item's start) */
UK.formulaLayers = function (ctx, label, items) {
  items = items || UK.formulaItems(ctx);
  items.forEach((it, i) => { const nxt = items[i + 1]; const out = it.out ?? (nxt ? nxt.at : undefined);
    Kit.formulaLayer(ctx, { label, items: [{ tex: it.tex, at: it.at }], at: it.at, out: out === undefined ? undefined : (typeof out === 'number' ? out : ctx.at(out) - 0.25) }); });
};
