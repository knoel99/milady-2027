/* seat.js: the "empty seat" for results that do not exist yet (brief §3.2, outline §2 "pending device").
 *
 *   Kit.seat(ctx, {
 *     type: 'curve' | 'map' | 'lamps' | 'gauge',      vary it from seat to seat
 *     variant: ctx.variant,                            'pending' (now) | 'result' (data file present)
 *     data: ctx.data.seat,                             result variant: a file written by tools/data_cloud.py
 *     tag: 'palier2_abc3d',                            data tag (the campaign or evaluation that fills the seat)
 *     frame: {x, y, w, h},                             chart area (default: left 60 % of the frame)
 *     // curve:  x: {label, min, max, ticks, param, log}, y: {...}, band: {y: [lo, hi]} | {x: [lo, hi]},
 *     //         ghost: {x, y, label}  (a READY anchor drawn grey and dashed, e.g. the E3 32³ curve)
 *     // map:    map: {xLabel, yLabel, kind: 'u'|'b', title}
 *     // lamps:  lamps: [{id, label, rule}]            data.lamps: [{id, state: met|not_met|inconclusive, value}]
 *     // gauge:  gauge: {label, min, max, band: [lo, hi], log, unit}   data.value
 *     bet, confidence: 'high'|'medium'|'low', criterion, source ('T:917'), ask (the question that decides the run),
 *     cues: {frame, bet, criterion, ask, data}         time specs (defaults staggered from `at`); out: exit time
 *   })
 * Pending: dashed grey frame, axes labelled, success band shaded, grey data tag, no data drawn.
 * Result: the same frame with the data drawn (solid = simulated, dashed = generated) and the verdict
 * computed by the converter (data.verdict: met | not_met | inconclusive) — never by the scene.
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit;
  const VERDICT = { met: 'CRITERION MET', not_met: 'CRITERION NOT MET', inconclusive: 'INCONCLUSIVE' };

  K.seat = function (ctx, o = {}) {
    const type = o.type || 'curve', variant = o.variant || ctx.variant || 'pending';
    const D = variant === 'result' ? o.data : null;
    if (variant === 'result' && !D) throw new Error('seat: result variant without data (status ready but data file missing)');
    const fr = Object.assign({ x: 216, y: 196, w: 900, h: 520 }, o.frame || {});
    const c = o.cues || {}, tb = ctx.at(o.at ?? 0);
    const T = { frame: ctx.at(c.frame ?? tb), bet: ctx.at(c.bet ?? tb + 1.2), criterion: ctx.at(c.criterion ?? tb + 3),
      ask: ctx.at(c.ask ?? tb + 5), data: ctx.at(c.data ?? tb + 1) };
    const svg = K.svgLayer(ctx, 12, o.parent); svg.setAttribute('data-kit', 'seat');
    const items = [];
    const reg = (it) => { items.push(it); return it; };
    const muted = K.c('muted');

    // ---- frame and data tag ----
    const frame = K.s('rect', { x: fr.x - 120, y: fr.y - 70, width: fr.w + 170, height: fr.h + 190, rx: 10, fill: 'none', stroke: muted, 'stroke-width': 2.5, 'stroke-dasharray': '14 10' }, svg);
    if (variant === 'result') frame.setAttribute('stroke-dasharray', 'none');
    // result: the data tag carries the provenance stamp and the first 8 hex digits of the data's SHA-256 (styles §3.10)
    const tagTxt = variant === 'result' ? `${(D.meta && D.meta.stamp) || 'DATA · ' + o.tag}${D.meta && D.meta.sha256 ? ' · ' + D.meta.sha256.slice(0, 8) : ''}` : `DATA · ${o.tag} · AWAITING`;
    const tag = K.el('div', { class: 'kit-chip ' + (variant === 'result' ? '' : 'schematic'), 'data-kit': 'seat' }, o.parent || ctx.stage, K.upper(tagTxt));
    tag.style.position = 'absolute'; tag.style.left = (fr.x - 120 + 16) + 'px'; tag.style.top = (fr.y - 70 - 23) + 'px'; tag.style.zIndex = 13;
    tag.style.background = K.c('bg');
    if (variant === 'result' && D.meta && o.stampLowerThird) {   // optional extra stamp lower-third (keep the frame's bottom clear)
      K.lowerThird(ctx, { kind: 'stamp', data: D, at: c.data ?? T.data, hold: o.stampHold ?? 5, parent: o.parent });
    }

    // ---- chart by type ----
    if (type === 'curve') {
      const P = K.plot(ctx, { svg, parent: o.parent, box: { x0: fr.x, x1: fr.x + fr.w, y0: fr.y + 40, y1: fr.y + fr.h - 60 }, x: o.x, y: o.y, at: T.frame });
      if (o.band) P.band(Object.assign({ kind: 'success', label: o.band.label || 'success band', at: T.criterion }, o.band));
      if (o.ghost) { P.curve({ x: o.ghost.x, y: o.ghost.y, kind: 'ghost', at: T.frame, dur: 1.2 }); if (o.ghost.label) P.legend([{ label: o.ghost.label, kind: 'ghost' }], { at: T.frame, x: o.ghost.legendX, y: o.ghost.legendY }); }
      if (o.zero) P.hline({ y: 0, kind: 'zero', at: T.frame });
      if (D) {
        D.series.forEach((s, k) => {
          P.curve({ x: s.x || D.x.values, y: s.y, field: s.field, kind: s.kind, at: T.data, dur: 1.6 });
          if (s.points !== false) P.dots({ x: s.x || D.x.values, y: s.y, filled: s.filled || null, field: s.field, at: T.data, dur: 1.6 });
          void k;
        });
        if (D.legend !== false) P.legend(D.series.map((s) => ({ label: s.name, field: s.field, kind: s.kind })), { at: T.data, x: o.legendX, y: o.legendY ?? (fr.y + 80 + (o.ghost ? 48 : 0)), row: o.legendRow });
      }
      reg(P);
    } else if (type === 'map') {
      const m = o.map || {}, side = Math.min(fr.w - 160, fr.h - 60), mx = fr.x + 40, my = fr.y + 10;
      const g = K.s('g', {}, svg);
      K.s('rect', { x: mx, y: my, width: side, height: side, fill: 'none', stroke: muted, 'stroke-width': 2.5, 'stroke-dasharray': variant === 'result' ? 'none' : '10 8' }, g);
      K.s('text', { x: mx + side / 2, y: my + side + 44, 'text-anchor': 'middle', class: 'kt-axis' }, g, m.xLabel || 'x');
      K.s('text', { x: mx - 18, y: my + side / 2, 'text-anchor': 'end', class: 'kt-axis' }, g, m.yLabel || 'y');
      // colour key: silver (−) → background (0) → hue (+); numbers only once the data exist
      const cbx = mx + side + 50, kind = m.kind || 'b', gid = 'sg' + Math.floor(S.rng('seatmap' + o.tag)() * 1e9);
      const lg = K.s('linearGradient', { id: gid, x1: 0, y1: 1, x2: 0, y2: 0 }, K.s('defs', {}, g));
      [[0, K.c('silver')], [0.5, K.c('bg')], [1, K.c(kind === 'u' ? 'u-hi' : 'b-hi')]].forEach(([off, col]) => K.s('stop', { offset: off, 'stop-color': col }, lg));
      K.s('rect', { x: cbx, y: my, width: 28, height: side, fill: `url(#${gid})`, stroke: muted, 'stroke-width': 2 }, g);
      const vmax = D && D.map ? D.map.vmax : null;
      [['+', my + 24], ['0', my + side / 2 + 10], ['−', my + side - 4]].forEach(([s, yy], i) => K.s('text', { x: cbx + 42, y: yy, class: 'kt-tick' }, g, vmax ? [K.fmt(vmax, 2), '0', K.fmt(-vmax, 2)][i] : s));
      if (m.title) K.s('text', { x: mx, y: my - 16, class: 'kt-mono' }, g, K.upper(m.title));
      if (!D) { const aw = K.s('text', { x: mx + side / 2, y: my + side / 2 + 10, 'text-anchor': 'middle', class: 'kt-mono' }, g, 'AWAITING DATA'); void aw; }
      else K.fieldMap(ctx, { grid: D.map.grid, x: mx, y: my, w: side, h: side, kind, vmax: D.map.vmax, at: T.data, generated: !!D.map.generated, z: 11 });
      reg({ render(t) { g.style.opacity = S.seg(t, T.frame, T.frame + 0.5, S.ease.linear); } });
    } else if (type === 'lamps') {
      const L = o.lamps || []; if (!L.length) throw new Error('seat lamps: list the criteria');
      const g = K.s('g', {}, svg), row = Math.min(118, (fr.h - 20) / L.length), y0 = fr.y + (fr.h - row * L.length) / 2;
      if (o.lampsTitle) K.s('text', { x: fr.x + 12, y: y0 - 28, class: 'kt-mono' }, g, K.upper(o.lampsTitle));
      const state = {}; if (D) for (const l of D.lamps || []) state[l.id] = l;
      const lamps = L.map((l, i) => {
        const y = y0 + row * i + row / 2, x = fr.x + 40, st = state[l.id] ? state[l.id].state : null, fg = K.c('fg');
        const gg = K.s('g', {}, g);
        const ring = K.s('circle', { cx: x, cy: y, r: 28, fill: 'none', stroke: st ? fg : muted, 'stroke-width': 3, 'stroke-dasharray': st ? 'none' : '7 6' }, gg);
        let mark;
        if (!st) mark = K.s('text', { x, y: y + 11, 'text-anchor': 'middle', class: 'kt-label' }, gg, '?');
        else if (st === 'met') { K.s('circle', { cx: x, cy: y, r: 28, fill: fg }, gg); mark = K.s('path', { d: `M${x - 12},${y} l8,9 l16,-18`, fill: 'none', stroke: K.c('bg'), 'stroke-width': 5, 'stroke-linecap': 'round' }, gg); }
        else if (st === 'not_met') mark = K.s('path', { d: `M${x - 11},${y - 11} l22,22 M${x + 11},${y - 11} l-22,22`, stroke: fg, 'stroke-width': 4.5, 'stroke-linecap': 'round' }, gg);
        else { K.s('path', { d: `M${x},${y - 28} a28,28 0 0 0 0,56 Z`, fill: fg }, gg); mark = null; }
        if (mark && !st) mark.style.fill = muted;
        K.s('text', { x: x + 56, y: y - 4, class: 'kt-label' }, gg, l.label).style.fill = K.c('fg');
        const sub = l.rule + (D && state[l.id] && state[l.id].value !== undefined ? '  ·  ' + (typeof state[l.id].value === 'number' ? K.fmt(state[l.id].value, 3) : state[l.id].value) : '');
        K.s('text', { x: x + 56, y: y + 34, class: 'kt-tick' }, gg, sub);
        void ring;
        return gg;
      });
      reg({ render(t) { lamps.forEach((l, i) => { l.style.opacity = S.seg(t, T.frame + 0.15 * i, T.frame + 0.15 * i + 0.4, S.ease.linear); }); g.style.display = t >= T.frame ? '' : 'none'; } });
    } else if (type === 'gauge') {
      const G = o.gauge || {}, cx = fr.x + fr.w / 2, cy = fr.y + fr.h - 120, R = Math.min(fr.w / 2 - 80, fr.h - 200);
      const tr = (v) => (G.log ? Math.log10(v) : v), lo = tr(G.min ?? 0), hi = tr(G.max ?? 1);
      const ang = (v) => Math.PI * (1 - (tr(v) - lo) / (hi - lo));   // left = min, right = max
      const pt = (a, r) => [cx + r * Math.cos(a), cy - r * Math.sin(a)];
      const g = K.s('g', {}, svg);
      const arcD = (a0, a1, r) => { const p = pt(a0, r), q = pt(a1, r); return `M${p[0]},${p[1]} A${r},${r} 0 0 1 ${q[0]},${q[1]}`; };
      K.s('path', { d: arcD(Math.PI, 0, R), fill: 'none', stroke: muted, 'stroke-width': 4, 'stroke-dasharray': variant === 'result' ? 'none' : '12 9' }, g);
      if (G.band) {
        const band = K.s('path', { d: arcD(ang(G.band[0]), ang(G.band[1]), R - 22), fill: 'none', stroke: K.rgba(K.c('chalk'), 0.28), 'stroke-width': 40 }, g);
        const am = (ang(G.band[0]) + ang(G.band[1])) / 2, lp = pt(am, R - 92);
        const bl = K.s('text', { x: lp[0], y: lp[1] + 10, 'text-anchor': 'middle', class: 'kt-mono' }, g, K.upper(G.bandLabel || 'success'));
        bl.style.fill = K.c('chalk');
        reg({ render(t) { const a = S.seg(t, T.criterion, T.criterion + 0.5, S.ease.linear); band.style.opacity = a; bl.style.opacity = a; } });
      }
      const ticks = G.ticks || (G.log ? (() => { const r = []; for (let e = Math.ceil(lo); e <= Math.floor(hi); e++) r.push(Math.pow(10, e)); return r; })() : K.niceTicks(G.min ?? 0, G.max ?? 1, 4));
      for (const v of ticks) { const a = ang(v), p = pt(a, R + 6), q = pt(a, R + 24), l = pt(a, R + 62); K.s('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], stroke: muted, 'stroke-width': 3 }, g); K.s('text', { x: l[0], y: l[1] + 10, 'text-anchor': 'middle', class: 'kt-tick' }, g, G.log ? K.fmt(v, 2, { minExp: 0, maxExp: 0 }) : K.fmt(v, 3)); }
      K.s('text', { x: cx, y: cy + 116, 'text-anchor': 'middle', class: 'kt-axis' }, g, G.label || '');
      K.s('circle', { cx, cy, r: 12, fill: K.c('matter') }, g);
      let needle = null, readout = null;
      if (D && Number.isFinite(+D.value)) {
        needle = K.s('line', { x1: cx, y1: cy, x2: cx, y2: cy - R + 30, stroke: K.c(o.field || 'metric'), 'stroke-width': 8, 'stroke-linecap': 'round' }, g);
        readout = K.s('text', { x: cx, y: cy + 64, 'text-anchor': 'middle', class: 'kt-axis' }, g, K.fmt(D.value, 3) + (G.unit ? ' ' + G.unit : '')); readout.style.fill = K.c(o.field || 'metric');
      } else K.s('text', { x: cx, y: cy + 64, 'text-anchor': 'middle', class: 'kt-mono' }, g, 'AWAITING DATA');
      const aEnd = D && Number.isFinite(+D.value) ? ang(Math.min(G.max, Math.max(G.min, D.value))) : Math.PI;
      reg({ render(t) {
        g.style.opacity = S.seg(t, T.frame, T.frame + 0.5, S.ease.linear);
        if (needle) { const a = Math.PI + (aEnd - Math.PI) * S.spring(S.seg(t, T.data, T.data + 1.2, S.ease.linear), 0.02), p = pt(a, R - 30); needle.setAttribute('x2', p[0]); needle.setAttribute('y2', p[1]); readout.style.opacity = S.seg(t, T.data + 1, T.data + 1.3, S.ease.linear); }
      } });
    } else throw new Error('seat type: curve | map | lamps | gauge');

    // ---- the right column: bet, confidence, criterion, the question (or the verdict) ----
    const col = K.el('div', { class: 'kit-seat-col', 'data-kit': 'seat' }, o.parent || ctx.stage);
    const block = (label, html, extra) => { const d = K.el('div', {}, col); const h = K.el('h4', {}, d, label); if (extra) h.appendChild(extra); if (html) K.el('p', { html }, d); return d; };
    let pips = null;
    if (o.confidence) {
      const n = { high: 3, medium: 2, low: 1 }[o.confidence]; if (!n) throw new Error('seat confidence: high | medium | low');
      pips = K.el('span', { class: 'pips' }); [10, 16, 22].forEach((h, i) => { const e = K.el('i', { class: i < n ? '' : 'off' }, pips); e.style.height = h + 'px'; });
    }
    const confLabel = o.confidence ? K.el('span', {}, null, 'CONFIDENCE ' + o.confidence.toUpperCase()) : null;
    const hdr = K.el('span', { style: 'display:inline-flex;gap:12px;align-items:center' }); if (pips) hdr.appendChild(pips); if (confLabel) hdr.appendChild(confLabel);
    const bBet = block('THE BET', K.markup(o.bet || ''), null);
    const bConf = o.confidence ? (() => { const d = K.el('div', {}, col); const h = K.el('h4', {}, d); h.appendChild(hdr); return d; })() : null;
    const bCrit = block('SUCCESS CRITERION', K.markup(o.criterion || ''), null);
    if (o.source) K.el('div', { class: 'src' }, bCrit, 'source ' + o.source);
    let bAsk = null, bVer = null;
    if (D && D.verdict) {
      bVer = K.el('div', {}, col); K.el('h4', {}, bVer, 'RESULT');
      K.el('div', { class: 'verdict' }, bVer, VERDICT[D.verdict] || D.verdict);
      if (D.verdict_text) K.el('p', { html: K.markup(D.verdict_text) }, bVer).style.marginTop = '10px';
    } else if (o.ask) {
      bAsk = K.el('div', { class: 'ask' }, col); K.el('h4', {}, bAsk, 'ASK BEFORE WE COMPUTE'); K.el('p', { html: K.markup(o.ask) }, bAsk);
    }
    if (!o.bet || !o.criterion) throw new Error('seat needs bet and criterion');
    const cb = K.box(col, ctx); if (cb.y + cb.h > K.SAFE.y1 + 0.5) S.warn(`seat: the right column ends at y = ${Math.round(cb.y + cb.h)} (> 880): shorten bet / criterion / question`);
    const fade = (el, a) => { if (!el) return; reg({ render(t) { el.style.opacity = S.seg(t, a, a + 0.4, S.ease.linear); el.style.transform = `translateY(${(8 * (1 - S.seg(t, a, a + 0.4, S.ease.outCubic))).toFixed(2)}px)`; } }); };
    fade(bBet, T.bet); fade(bConf, T.bet + 0.3); fade(bCrit, T.criterion); fade(bAsk, T.ask); fade(bVer, T.data + 1.8);
    const tEnd = o.out !== undefined ? ctx.at(o.out) : Infinity;
    return ctx.add({
      root: svg, col,
      render(t) {
        const q = tEnd === Infinity ? 0 : S.seg(t, tEnd, tEnd + 0.3, S.ease.linear), on = t >= T.frame && q < 1;
        for (const e of [svg, tag, col]) K.show(e, on);
        svg.style.opacity = S.seg(t, T.frame, T.frame + 0.4, S.ease.linear) * (1 - q);
        tag.style.opacity = S.seg(t, T.frame + 0.2, T.frame + 0.5, S.ease.linear) * (1 - q); col.style.opacity = 1 - q;
        for (const it of items) it.render(t);
      },
    });
  };
})();
