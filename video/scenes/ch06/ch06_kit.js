/* ch06_kit.js: helpers shared by the scenes of unit ch06 (load after the runtime components).
 * Labels and fades (as in ch05), the exact flow-matching wind of a two-Gaussian target (closed form of
 * assets/interactif/flow-matching.js, step 4, generalised to a centre vector m), Heun transport precomputed in setup,
 * seeded Gaussian noise, and a reader for the string-valued blocks of data/fig_flow_matching.json.
 * The toy file is SCHEMATIC: its numbers shape the pictures and never appear on screen. */
(function () {
  'use strict';
  const K = window.Kit, S = window.Scene;
  const C6 = (window.C6 = {});
  C6.lab = function (ctx, text, x, y, cls = '', o = {}) {
    const e = K.el('div', { class: 'c6-label ' + cls }, o.parent || ctx.stage);
    if (o.html) e.innerHTML = K.markup(text); else e.textContent = text;
    e.style.left = x + 'px'; e.style.top = y + 'px';
    if (o.z) e.style.zIndex = o.z;
    if (o.w) { e.style.whiteSpace = 'normal'; e.style.width = o.w + 'px'; e.style.lineHeight = '1.22'; }
    return e;
  };
  C6.fade = function (el, t, a, b = Infinity, d = 0.25, max = 1) {
    const p = S.seg(t, a, a + d, S.ease.linear) * (b === Infinity ? 1 : 1 - S.seg(t, b, b + d, S.ease.linear));
    el.style.opacity = (p * max).toFixed(3); el.style.display = p > 0 ? '' : 'none'; return p;
  };
  C6.fadeS = function (el, t, a, b = Infinity, d = 0.25, max = 1) {
    const p = S.seg(t, a, a + d, S.ease.linear) * (b === Infinity ? 1 : 1 - S.seg(t, b, b + d, S.ease.linear));
    el.setAttribute('opacity', (p * max).toFixed(3)); el.setAttribute('visibility', p > 0 ? 'visible' : 'hidden'); return p;
  };
  /** a value of data/fig_flow_matching.json that may be stored as a (Python-repr) string */
  C6.val = function (v) {
    if (typeof v !== 'string') return v;
    const n = Number(v); if (Number.isFinite(n)) return n;
    return JSON.parse(v.replace(/'/g, '"').replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false').replace(/\bNone\b/g, 'null'));
  };
  /** seeded standard normal pairs */
  C6.gauss = function (rng) { const u = Math.max(1e-12, rng()), w = rng(), r = Math.sqrt(-2 * Math.log(u)); return [r * Math.cos(2 * Math.PI * w), r * Math.sin(2 * Math.PI * w)]; };
  /** exact marginal velocity of the linear path from N(0, I) to ½N(+m, s²I) + ½N(−m, s²I), in 2D (out = [vx, vy]) */
  C6.wind = function (x, y, t, mx, my, s, out) {
    const tt = Math.min(t, 0.999), s2 = (1 - tt) * (1 - tt) + tt * tt * s * s;
    const th = Math.tanh(tt * (mx * x + my * y) / s2), a = tt * s * s - (1 - tt);
    out[0] = (a * x + (1 - tt) * th * mx) / s2; out[1] = (a * y + (1 - tt) * th * my) / s2; return out;
  };
  /** Heun transport of points pts [[x, y]] over t 0 → 1 in n steps; returns Float32Array per point of (n+1)·2 */
  C6.transport = function (pts, mx, my, s, n) {
    const k1 = [0, 0], k2 = [0, 0], dt = 1 / n;
    return pts.map(([x0, y0]) => {
      const p = new Float32Array(2 * (n + 1)); let x = x0, y = y0; p[0] = x; p[1] = y;
      for (let i = 0; i < n; i++) {
        const t = i * dt; C6.wind(x, y, t, mx, my, s, k1);
        const xp = x + dt * k1[0], yp = y + dt * k1[1]; C6.wind(xp, yp, t + dt, mx, my, s, k2);
        x += 0.5 * dt * (k1[0] + k2[0]); y += 0.5 * dt * (k1[1] + k2[1]); p[2 * i + 2] = x; p[2 * i + 3] = y;
      }
      return p;
    });
  };
  /** position on a precomputed path at transport time tau (linear between Heun steps) */
  C6.at = function (p, tau, out) {
    const n = p.length / 2 - 1, f = Math.max(0, Math.min(1, tau)) * n, i = Math.min(n - 1, Math.floor(f)), u = f - i;
    out[0] = p[2 * i] + (p[2 * i + 2] - p[2 * i]) * u; out[1] = p[2 * i + 1] + (p[2 * i + 3] - p[2 * i + 1]) * u; return out;
  };
  /** an arrow on a canvas context, from (x, y) along (dx, dy) */
  C6.arrow = function (g, x, y, dx, dy, head = 9) {
    const L = Math.hypot(dx, dy); if (L < 1) return;
    const ux = dx / L, uy = dy / L, ex = x + dx, ey = y + dy;
    g.moveTo(x, y); g.lineTo(ex, ey);
    g.moveTo(ex - head * (ux * 0.9 - uy * 0.5), ey - head * (uy * 0.9 + ux * 0.5)); g.lineTo(ex, ey);
    g.lineTo(ex - head * (ux * 0.9 + uy * 0.5), ey - head * (uy * 0.9 - ux * 0.5));
  };
})();
