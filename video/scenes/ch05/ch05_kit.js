/* ch05_kit.js: helpers shared by the scenes of unit ch05 (load after the runtime components).
 * Reusable pieces of the toll-counter motif (car glyph, speedometer, counter box, clock icon; they return in 09.1),
 * a labelled-div helper, an opacity envelope and the schematic D(t) trace of 05.4 (also the backdrop of ch05.Q).
 * No physics number here: every value on screen comes from data/ or the script's params. */
(function () {
  'use strict';
  const K = window.Kit, S = window.Scene;
  const C5 = (window.C5 = {});

  /** absolutely placed HTML label (z 30); cls among c5-label modifiers; html: true takes markup */
  C5.lab = function (ctx, text, x, y, cls = '', o = {}) {
    const e = K.el('div', { class: 'c5-label ' + cls }, o.parent || ctx.stage);
    if (o.html) e.innerHTML = K.markup(text); else e.textContent = text;
    e.style.left = x + 'px'; e.style.top = y + 'px';
    if (o.z) e.style.zIndex = o.z;
    return e;
  };
  /** opacity envelope: in over d from a, out over d from b (seconds); returns the opacity and toggles display */
  C5.fade = function (el, t, a, b = Infinity, d = 0.25, max = 1) {
    const p = S.seg(t, a, a + d, S.ease.linear) * (b === Infinity ? 1 : 1 - S.seg(t, b, b + d, S.ease.linear));
    el.style.opacity = (p * max).toFixed(3);
    el.style.display = p > 0 ? '' : 'none';
    return p;
  };
  /** SVG version (attribute opacity, visibility) */
  C5.fadeS = function (el, t, a, b = Infinity, d = 0.25, max = 1) {
    const p = S.seg(t, a, a + d, S.ease.linear) * (b === Infinity ? 1 : 1 - S.seg(t, b, b + d, S.ease.linear));
    el.setAttribute('opacity', (p * max).toFixed(3));
    el.setAttribute('visibility', p > 0 ? 'visible' : 'hidden');
    return p;
  };
  /** top-down car glyph centred at (0, 0) facing +x: body (matter), roof line (lighter), returns the <g> */
  C5.car = function (parent, w = 64, h = 30) {
    const g = K.s('g', {}, parent);
    K.s('rect', { x: -w / 2, y: -h / 2, width: w, height: h, rx: 8, fill: K.c('matter'), stroke: K.c('matter-dark'), 'stroke-width': 2 }, g);
    K.s('rect', { x: -w * 0.18, y: -h * 0.32, width: w * 0.36, height: h * 0.64, rx: 4, fill: K.c('fg-2'), opacity: 0.55 }, g);
    K.s('line', { x1: w * 0.3, x2: w * 0.3, y1: -h * 0.36, y2: h * 0.36, stroke: K.c('fg-2'), 'stroke-width': 2, opacity: 0.7 }, g);
    return g;
  };
  /** speedometer half-dial centred at (x, y), radius r; .set(frac in [0, 1]) */
  C5.speedo = function (parent, x, y, r = 20, o = {}) {
    const g = K.s('g', { transform: `translate(${x},${y})` }, parent);
    K.s('path', { d: `M${-r},0 A${r},${r} 0 0 1 ${r},0 Z`, fill: K.c('panel'), stroke: K.c(o.rim || 'fg-2'), 'stroke-width': o.sw || 2.5 }, g);
    const nd = K.s('line', { x1: 0, y1: 0, x2: -r * 0.82, y2: 0, stroke: K.c(o.needle || 'fg'), 'stroke-width': o.nw || 3, 'stroke-linecap': 'round' }, g);
    return { g, set(f) { nd.setAttribute('transform', `rotate(${(180 * Math.max(0, Math.min(1, f))).toFixed(2)})`); } };
  };
  /** clock icon (grey) centred at (x, y), radius r */
  C5.clock = function (parent, x, y, r = 24) {
    const g = K.s('g', { transform: `translate(${x},${y})` }, parent);
    K.s('circle', { r, fill: 'none', stroke: K.c('fg-2'), 'stroke-width': 3 }, g);
    K.s('path', { d: `M0,${-r * 0.6} V0 L${r * 0.45},${r * 0.32}`, fill: 'none', stroke: K.c('fg-2'), 'stroke-width': 3, 'stroke-linecap': 'round' }, g);
    return g;
  };
  /** the 04.6 shoebox glyph, closed (a lid on top), centred at (x, y) with front w x h */
  C5.closedBox = function (parent, x, y, w, h, o = {}) {
    const g = K.s('g', {}, parent), d = h * 0.32, x0 = x - w / 2, y0 = y - h / 2;
    const dash = o.dashed ? { 'stroke-dasharray': '7 6', fill: 'none' } : {};
    K.s('path', Object.assign({ d: `M${x0 + w},${y0} L${x0 + w + d},${y0 - d} L${x0 + w + d},${y0 + h - d} L${x0 + w},${y0 + h} Z`, fill: K.c('matter-dark'), stroke: K.c(o.stroke || 'matter'), 'stroke-width': 3, 'stroke-linejoin': 'round' }, dash), g);
    K.s('path', Object.assign({ d: `M${x0},${y0} L${x0 + d},${y0 - d} L${x0 + w + d},${y0 - d} L${x0 + w},${y0} Z`, fill: K.c('matter'), stroke: K.c(o.stroke || 'matter'), 'stroke-width': 3, 'stroke-linejoin': 'round' }, dash), g);
    K.s('rect', Object.assign({ x: x0, y: y0, width: w, height: h, fill: K.c('panel'), stroke: K.c(o.stroke || 'matter'), 'stroke-width': 3 }, dash), g);
    return g;
  };

  /** the schematic D(t) trace of 05.4: a Catmull-Rom spline through knots [[frac, D]], plus a seeded wiggle damped to
   *  zero where |D| < 0.15 (the excursion keeps two zero crossings, the reversal one). Returns n+1 samples {f, D} */
  C5.trace = function (P, n = 600) {
    const k = P.knots, rng = S.rng(P.seed), ph = [rng() * 6.28, rng() * 6.28, rng() * 6.28];
    const at = (f) => {
      let i = 0; while (i < k.length - 2 && f > k[i + 1][0]) i++;
      const p0 = k[Math.max(0, i - 1)], p1 = k[i], p2 = k[i + 1], p3 = k[Math.min(k.length - 1, i + 2)];
      const u = (f - p1[0]) / (p2[0] - p1[0]), u2 = u * u, u3 = u2 * u;
      return 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * u + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3);
    };
    const out = [];
    for (let j = 0; j <= n; j++) {
      const f = j / n, base = at(f);
      const damp = S.seg(Math.abs(base), 0.15, 0.35, S.ease.smooth);
      const w = P.wiggle * (Math.sin(f * 61 + ph[0]) * 0.5 + Math.sin(f * 137 + ph[1]) * 0.3 + Math.sin(f * 251 + ph[2]) * 0.2);
      out.push({ f, D: base + damp * w });
    }
    return out;
  };
  /** zero crossings of a sampled trace (fractions, linear interpolation) */
  C5.crossings = function (tr, level = 0) {
    const c = [];
    for (let j = 1; j < tr.length; j++) {
      const a = tr[j - 1].D - level, b = tr[j].D - level;
      if ((a < 0) !== (b < 0)) c.push({ f: tr[j - 1].f + (tr[j].f - tr[j - 1].f) * a / (a - b), up: b > a, j });
    }
    return c;
  };
})();
