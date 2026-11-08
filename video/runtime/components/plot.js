/* plot.js: SVG plot helper reading data JSON (curve schema of tools/data_*.py).
 *
 *   const P = Kit.plot(ctx, {box: {x0, x1, y0, y1}, x: {label, min, max, ticks|n, log, param, fmt},
 *                            y: {...}, at, out, grid, parent})
 *   P.curve({x, y, field, kind: 'simulated'|'generated'|'ghost', width, at, dur})   drawn on left → right
 *   P.dots({x, y, filled: [bool], field, at, dur, r})           filled = training value, open = test value
 *   P.errorbars({x, lo, hi, field, at})
 *   P.band({y: [lo, hi]} | {x: [lo, hi]}, kind: 'window'|'floor'|'success', label, at)
 *   P.hline({y, label, kind: 'floor'|'zero'|'ref', at})   dashed grey floor line = noise floor (motif)
 *   P.legend([{label, field, kind}], {at, x, y})
 *   P.fromData(D, {at, dur, gen})  draws every series of a curve file + train/test dots + legend
 * Axes: x axis green when it is a control parameter (x.param = true); y title sits horizontally above
 * the y axis (easier to read in a video than a rotated title). All text >= 28 px.
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit;
  let uid = 0;

  /** "nice" linear ticks (1, 2, 2.5, 5 × 10^k) covering [a, b] with about n intervals */
  K.niceTicks = function (a, b, n = 5) {
    const span = b - a; if (!(span > 0)) return [a];
    const raw = span / n, mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => span / s <= n + 0.01) || 10 * mag;
    const out = [];
    for (let v = Math.ceil(a / step - 1e-9) * step; v <= b + step * 1e-6; v += step) out.push(+v.toPrecision(12));
    return out;
  };

  K.plot = function (ctx, o = {}) {
    const box = Object.assign({ x0: 300, x1: 1640, y0: 190, y1: 690 }, o.box || {});
    const X = Object.assign({ min: 0, max: 1, n: 5 }, o.x || {}), Y = Object.assign({ min: 0, max: 1, n: 4 }, o.y || {});
    const svg = o.svg || K.svgLayer(ctx, o.z ?? 12, o.parent);
    const root = K.s('g', { 'data-kit': 'plot' }, svg);
    const id = 'kp' + (++uid);
    const tr = (A, v) => (A.log ? Math.log10(Math.max(v, 1e-300)) : v);
    const sx = (v) => box.x0 + (box.x1 - box.x0) * (tr(X, v) - tr(X, X.min)) / (tr(X, X.max) - tr(X, X.min));
    const sy = (v) => box.y1 - (box.y1 - box.y0) * (tr(Y, v) - tr(Y, Y.min)) / (tr(Y, Y.max) - tr(Y, Y.min));
    const t0 = ctx.at(o.at ?? 0), tEnd = o.out !== undefined ? ctx.at(o.out) : Infinity;
    const items = [];
    const reg = (it) => { items.push(it); return it; };

    // ---- axes, grid, ticks, titles ----
    const axes = K.s('g', {}, root);
    const ticks = (A) => A.ticks || (A.log ? (() => { const r = []; for (let e = Math.ceil(Math.log10(A.min)); e <= Math.floor(Math.log10(A.max)); e++) r.push(Math.pow(10, e)); return r; })() : K.niceTicks(A.min, A.max, A.n));
    const lab = (A, v) => (A.fmt ? A.fmt(v) : A.log ? K.pow10(v) : K.fmt(v, 4, { minExp: -4 }));
    const muted = K.c('muted'), grid = K.c('grid');
    if (o.grid !== false) for (const v of ticks(Y)) K.s('line', { x1: box.x0, x2: box.x1, y1: sy(v), y2: sy(v), stroke: grid, 'stroke-width': 1.5 }, axes);
    let lastR = -Infinity;
    for (const v of ticks(X)) {   // a tick label that would touch its left neighbour is dropped (the tick stays)
      K.s('line', { x1: sx(v), x2: sx(v), y1: box.y1, y2: box.y1 + 10, stroke: muted, 'stroke-width': 2 }, axes);
      const tx = K.s('text', { x: sx(v), y: box.y1 + 46, 'text-anchor': 'middle', class: 'kt-tick' }, axes, lab(X, v));
      const bb = tx.getBBox();
      if (bb.x < lastR + 12) tx.remove(); else lastR = bb.x + bb.width;
    }
    for (const v of ticks(Y)) {
      K.s('line', { x1: box.x0 - 10, x2: box.x0, y1: sy(v), y2: sy(v), stroke: muted, 'stroke-width': 2 }, axes);
      K.s('text', { x: box.x0 - 18, y: sy(v) + 10, 'text-anchor': 'end', class: 'kt-tick' }, axes, lab(Y, v));
    }
    const xcol = X.param ? K.c('param') : muted;
    K.s('line', { x1: box.x0, x2: box.x1 + 16, y1: box.y1, y2: box.y1, stroke: xcol, 'stroke-width': X.param ? 3 : 2 }, axes);
    K.s('line', { x1: box.x0, x2: box.x0, y1: box.y1, y2: box.y0 - 16, stroke: Y.param ? K.c('param') : muted, 'stroke-width': 2 }, axes);
    if (X.label) { const tx = K.s('text', { x: (box.x0 + box.x1) / 2, y: box.y1 + 96, 'text-anchor': 'middle', class: 'kt-axis' }, axes, X.label); if (X.param) tx.style.fill = K.c('param'); }
    if (Y.label) K.s('text', { x: box.x0 - 18, y: box.y0 - 34, 'text-anchor': 'start', class: 'kt-axis' }, axes, Y.label);
    const defs = K.s('defs', {}, root);

    const P = {
      root, svg, box, sx, sy, X, Y,
      render(t) {
        const a = S.seg(t, t0, t0 + 0.5, S.ease.outCubic), q = tEnd === Infinity ? 0 : S.seg(t, tEnd, tEnd + 0.3, S.ease.linear);
        axes.style.opacity = a; root.style.display = t >= t0 && q < 1 ? '' : 'none'; root.style.opacity = 1 - q;
        for (const it of items) it.render(t);
      },
      /** a curve drawn on left → right by a growing clip (works for dashed lines too) */
      curve(c) {
        const xs = c.x, ys = c.y, col = K.c(c.field || 'fg');
        const pts = []; for (let i = 0; i < xs.length; i++) if (ys[i] !== null && Number.isFinite(+ys[i]) && (!Y.log || ys[i] > 0)) pts.push([sx(xs[i]), sy(ys[i])]);
        const cid = `${id}c${items.length}`;
        const cp = K.s('clipPath', { id: cid }, defs); const rect = K.s('rect', { x: box.x0 - 20, y: box.y0 - 8, height: box.y1 - box.y0 + 16, width: 0 }, cp);   // clipped to the box vertically
        const kind = c.kind || 'simulated';
        const d = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join('');
        const path = K.s('path', { d, fill: 'none', stroke: kind === 'ghost' ? muted : col, 'stroke-width': c.width || (kind === 'ghost' ? 3 : 5),
          'stroke-linejoin': 'round', 'stroke-linecap': 'round', 'clip-path': `url(#${cid})` }, root);
        if (kind === 'generated') path.setAttribute('stroke-dasharray', '16 11');
        if (kind === 'ghost') { path.setAttribute('stroke-dasharray', '6 8'); path.setAttribute('opacity', 0.75); }
        const a = ctx.at(c.at ?? o.at ?? 0), dur = c.dur ?? 1.8, xmax = pts.length ? pts[pts.length - 1][0] : box.x1;
        return reg({ path, render(t) { const p = S.seg(t, a, a + dur, S.ease.inOutSine); rect.setAttribute('width', ((xmax - box.x0 + 40) * p).toFixed(1)); path.style.display = p > 0 ? '' : 'none'; } });
      },
      /** markers: filled (training) or open (test) dots, revealed with the matching curve */
      dots(c) {
        const col = K.c(c.field || 'fg'), r = c.r || 7, g = K.s('g', {}, root);
        const a = ctx.at(c.at ?? o.at ?? 0), dur = c.dur ?? 1.8;
        const ds = []; for (let i = 0; i < c.x.length; i++) {
          if (c.y[i] === null || !Number.isFinite(+c.y[i]) || (Y.log && c.y[i] <= 0) || c.y[i] < Math.min(Y.min, Y.max) || c.y[i] > Math.max(Y.min, Y.max)) continue;
          const filled = c.filled ? !!c.filled[i] : true;
          const e = K.s('circle', { cx: sx(c.x[i]), cy: sy(c.y[i]), r, fill: filled ? col : K.c('bg'), stroke: col, 'stroke-width': 3 }, g);
          ds.push({ e, f: (sx(c.x[i]) - box.x0) / (box.x1 - box.x0) });
        }
        return reg({ g, render(t) { for (const d of ds) d.e.style.opacity = S.seg(t, a + dur * d.f, a + dur * d.f + 0.2, S.ease.linear); } });
      },
      errorbars(c) {
        const col = K.c(c.field || 'fg'), g = K.s('g', { stroke: col, 'stroke-width': 2.5 }, root), a = ctx.at(c.at ?? o.at ?? 0);
        for (let i = 0; i < c.x.length; i++) {
          const x = sx(c.x[i]), y0 = sy(c.lo[i]), y1 = sy(c.hi[i]);
          K.s('line', { x1: x, x2: x, y1: y0, y2: y1 }, g); K.s('line', { x1: x - 8, x2: x + 8, y1: y0, y2: y0 }, g); K.s('line', { x1: x - 8, x2: x + 8, y1: y1, y2: y1 }, g);
        }
        return reg({ g, render(t) { g.style.opacity = S.seg(t, a, a + 0.4, S.ease.linear); } });
      },
      /** shaded region: window (green 12 %), floor (grey, noise floor), success (chalk 10 %, dashed edge) */
      band(c) {
        const kind = c.kind || 'window', g = K.s('g', {}, root), a = ctx.at(c.at ?? o.at ?? 0);
        const fill = { window: K.rgba(K.c('param'), 0.12), floor: K.rgba(K.c('muted'), 0.14), success: K.rgba(K.c('chalk'), 0.10) }[kind];
        let r;
        if (c.x) { const xa = sx(c.x[0]), xb = sx(c.x[1]); r = { x: Math.min(xa, xb), y: box.y0, w: Math.abs(xb - xa), h: box.y1 - box.y0 }; }
        else { const ya = sy(c.y[0]), yb = sy(c.y[1]); r = { x: box.x0, y: Math.min(ya, yb), w: box.x1 - box.x0, h: Math.abs(yb - ya) }; }
        r.y = Math.max(r.y, box.y0); r.h = Math.min(r.h, box.y1 - r.y);
        K.s('rect', { x: r.x, y: r.y, width: r.w, height: r.h, fill }, g);
        if (kind === 'success') K.s('rect', { x: r.x, y: r.y, width: r.w, height: r.h, fill: 'none', stroke: K.c('chalk'), 'stroke-width': 2, 'stroke-dasharray': '10 8', opacity: 0.8 }, g);
        if (kind === 'floor' && c.y) K.s('line', { x1: box.x0, x2: box.x1, y1: r.y, y2: r.y, stroke: muted, 'stroke-width': 3, 'stroke-dasharray': '12 9' }, g);
        if (c.label) {   // x band: label centred above the plot box; y band: inside, top-left
          const above = !!c.x && c.labelX === undefined && c.labelY === undefined;
          const tx = K.s('text', { x: c.labelX ?? (above ? r.x + r.w / 2 : r.x + 14), y: c.labelY ?? (above ? box.y0 - 26 : r.y + 40), 'text-anchor': above ? 'middle' : 'start', class: 'kt-mono' }, g, K.upper(c.label));
          if (kind === 'window') tx.style.fill = K.c('param');
          if (kind === 'success') tx.style.fill = K.c('chalk');
        }
        return reg({ g, render(t) { g.style.opacity = S.seg(t, a, a + 0.5, S.ease.linear); } });
      },
      hline(c) {
        const g = K.s('g', {}, root), a = ctx.at(c.at ?? o.at ?? 0), y = sy(c.y);
        const kind = c.kind || 'floor';
        K.s('line', { x1: box.x0, x2: box.x1, y1: y, y2: y, stroke: kind === 'ref' ? K.c(c.field || 'fg') : muted, 'stroke-width': kind === 'zero' ? 2 : 3,
          'stroke-dasharray': kind === 'zero' ? 'none' : '12 9' }, g);
        if (c.label) K.s('text', { x: c.labelX ?? box.x1 - 8, y: c.labelY ?? y + 36, 'text-anchor': 'end', class: 'kt-mono' }, g, K.upper(c.label));   // below the line
        return reg({ g, render(t) { g.style.opacity = S.seg(t, a, a + 0.4, S.ease.linear); } });
      },
      /** legend rows at the top-left of the plot box (or x, y); kind 'dots' shows filled+open markers */
      legend(rows, c = {}) {
        const g = K.s('g', {}, root), a = ctx.at(c.at ?? o.at ?? 0);
        const x0 = c.x ?? box.x0 + 30, y = c.y ?? box.y0 + 20;
        let xo = 0;   // c.row: entries side by side instead of stacked
        rows.forEach((r, i) => {
          const yy = c.row ? y : y + 48 * i, col = K.c(r.field || 'fg'), x = x0 + xo;
          if (r.kind === 'dots') { K.s('circle', { cx: x + 12, cy: yy, r: 7, fill: col, stroke: col, 'stroke-width': 3 }, g); K.s('circle', { cx: x + 46, cy: yy, r: 7, fill: K.c('bg'), stroke: col, 'stroke-width': 3 }, g); }
          else if (r.kind === 'band') K.s('rect', { x, y: yy - 12, width: 60, height: 24, fill: K.rgba(K.c(r.field || 'muted'), 0.25) }, g);
          else K.s('line', { x1: x, x2: x + 60, y1: yy, y2: yy, stroke: r.kind === 'ghost' || r.kind === 'floor' ? muted : col, 'stroke-width': r.kind === 'ghost' ? 3 : 5,
            'stroke-dasharray': r.kind === 'generated' ? '16 11' : r.kind === 'ghost' ? '6 8' : r.kind === 'floor' ? '12 9' : 'none' }, g);
          const tx = K.s('text', { x: x + 78, y: yy + 10, class: 'kt-label' }, g, r.label);
          if (c.row) xo += 78 + tx.getBBox().width + 48;
        });
        return reg({ g, render(t) { g.style.opacity = S.seg(t, a, a + 0.4, S.ease.linear); } });
      },
      /** free text in plot coordinates */
      text(c) {
        const g = K.s('text', { x: c.px ?? sx(c.x), y: c.py ?? sy(c.y), 'text-anchor': c.anchor || 'start', class: c.mono ? 'kt-mono' : 'kt-label' }, root, c.text);
        if (c.field) g.style.fill = K.c(c.field);
        const a = ctx.at(c.at ?? o.at ?? 0);
        return reg({ g, render(t) { g.style.opacity = S.seg(t, a, a + 0.3, S.ease.linear); } });
      },
      /** every series of a curve-schema file: simulated solid, generated dashed, dots on the first series */
      fromData(D, c = {}) {
        const xs = D.x.values, at = c.at ?? o.at ?? 0;
        D.series.forEach((s, k) => {
          if (c.only && !c.only.includes(s.name)) return;
          const a = s.kind === 'generated' && c.gen !== undefined ? c.gen : at;
          P.curve({ x: xs, y: s.y, field: s.field, kind: s.kind, at: a, dur: c.dur });
          if (k === 0 && D.x.train && c.dots !== false) P.dots({ x: xs, y: s.y, filled: D.x.train, field: s.field, at: a, dur: c.dur });
        });
        if (c.legend !== false) P.legend(D.series.filter((s) => !c.only || c.only.includes(s.name)).map((s) => ({ label: s.name, field: s.field, kind: s.kind })), { at, x: c.legendX, y: c.legendY });
        return P;
      },
    };
    return ctx.add(P);
  };
})();
