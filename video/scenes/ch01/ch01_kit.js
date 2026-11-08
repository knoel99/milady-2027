/* ch01_kit.js: helpers shared by the scenes of unit ch01. Pure builders, no timing. */
(function () {
  'use strict';
  const K = window.Kit, S = window.Scene, TAU = Math.PI * 2;
  const C1 = {};
  /** dipole field lines r = L sin^2(theta) around (cx, cy), tilted by tiltDeg, cut inside rMin; ordered south -> north
   *  outside the source (the direction of the field of a north-up dipole) */
  C1.dipoleLines = function (cx, cy, Ls, tiltDeg = 0, rMin = 0, n = 180) {
    const c = Math.cos(tiltDeg * Math.PI / 180), s = Math.sin(tiltDeg * Math.PI / 180), lines = [];
    for (const L of Ls) for (const side of [1, -1]) {
      const pts = [];
      for (let i = n - 1; i >= 1; i--) { const th = Math.PI * i / n, r = L * Math.sin(th) ** 2; if (r < rMin) continue;
        const x = side * r * Math.sin(th), y = -r * Math.cos(th); pts.push([cx + c * x - s * y, cy + s * x + c * y]); }
      lines.push(pts);
    }
    return lines;
  };
  /** arrowheads on canvas at fractions fr of each line; dir +1 along the point order, -1 against */
  C1.heads = function (g, lines, o = {}) {
    const fr = o.fr || [0.5], h = o.size ?? 15, dir = o.dir ?? 1, prog = o.progress ?? 1;
    g.fillStyle = K.c(o.color || 'b');
    for (const L of lines) for (const f0 of fr) {
      const f = ((f0 % 1) + 1) % 1; if (f > prog || L.length < 4) continue;
      const i = Math.min(L.length - 2, Math.max(1, Math.floor(f * L.length)));
      const a = Math.atan2(L[i + 1][1] - L[i - 1][1], L[i + 1][0] - L[i - 1][0]) + (dir < 0 ? Math.PI : 0), [x, y] = L[i];
      g.beginPath(); g.moveTo(x + h * Math.cos(a), y + h * Math.sin(a)); g.lineTo(x + 0.6 * h * Math.cos(a + 2.4), y + 0.6 * h * Math.sin(a + 2.4));
      g.lineTo(x + 0.6 * h * Math.cos(a - 2.4), y + 0.6 * h * Math.sin(a - 2.4)); g.closePath(); g.fill();
    }
  };
  /** flat Earth cutaway (grey matter): crust+mantle, liquid outer core ring, solid inner core */
  C1.earth = function (parent, o) {
    const g = K.s('g', { transform: `translate(${o.x} ${o.y})` }, parent), R = o.r;
    K.s('circle', { r: R, fill: K.c('matter-dark'), stroke: K.c('matter'), 'stroke-width': 3 }, g);
    const outer = K.s('circle', { r: R * 0.55, fill: K.c('matter') }, g);
    K.s('circle', { r: R * 0.25, fill: K.c('fg-2'), stroke: K.c('fg'), 'stroke-width': 2 }, g);
    return { g, outer, R };
  };
  /** a closed-form "churn" of particles inside a ring rIn..rOut (pure function of t; seeded) */
  C1.churn = function (n, rIn, rOut, seed) {
    const r = S.rng(seed), P = [];
    for (let i = 0; i < n; i++) P.push({ r0: rIn + (rOut - rIn) * r(), th: TAU * r(), w: 0.25 + 0.35 * r(), k: 3 + Math.floor(4 * r()), ph: TAU * r(), shade: r() });
    return function at(t, i) { const p = P[i], th = p.th + p.w * t * (p.shade > 0.5 ? 1 : -0.7);
      const rr = Math.min(rOut - 2, Math.max(rIn + 2, p.r0 + 0.18 * (rOut - rIn) * Math.sin(p.k * th + 0.8 * t + p.ph)));
      return [rr * Math.cos(th), rr * Math.sin(th), p.shade]; };
  };
  C1.label = function (st, txt, x, y, cls = '') { const e = K.el('div', { class: 'c1-label ' + cls, html: K.markup(txt) }, st); e.style.left = x + 'px'; e.style.top = y + 'px'; return e; };
  C1.fadeEl = function (el, t, a, b, d = 0.25) { const o = S.seg(t, a, a + d, S.ease.linear) * (b === undefined || b === null ? 1 : 1 - S.seg(t, b, b + d, S.ease.linear)); el.style.opacity = o.toFixed(3); K.show(el, o > 0); return o; };
  C1.chipOf = function (ctx, re, fb) { const ch = (ctx.script.onscreen && ctx.script.onscreen.chips) || []; return ch.find((c) => re.test(c)) || fb; };
  C1.labOf = function (ctx, re, fb) { const ch = (ctx.script.onscreen && ctx.script.onscreen.labels) || []; return ch.find((c) => (typeof re === 'string' ? c === re : re.test(c))) || fb; };
  C1.refL2 = (chip) => chip.split('·').slice(1).map((x) => x.trim()).join(' · ');
  window.C1 = C1;
})();
