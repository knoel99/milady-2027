/* ch00_kit.js: helpers shared by the scenes of unit ch00 (cold open). No timing here: pure builders. */
(function () {
  'use strict';
  const K = window.Kit;
  const C0 = {};
  /** polarity runs from the script's params.normal_Ma ([[a, b], …] in Ma ago, normal intervals), clipped to
   *  the window [w0, w1]: [{a, b, s}] with s = +1 normal, -1 reversed, a < b in Ma ago. */
  C0.runs = function (normal, win) {
    const [w0, w1] = win, out = []; let x = w0;
    const N = normal.map(([a, b]) => [Math.max(w0, a), Math.min(w1, b)]).filter(([a, b]) => b > a).sort((p, q) => p[0] - q[0]);
    for (const [a, b] of N) { if (a > x) out.push({ a: x, b: a, s: -1 }); out.push({ a, b, s: +1 }); x = b; }
    if (x < w1) out.push({ a: x, b: w1, s: -1 });
    return out;
  };
  /** boundaries (polarity changes) strictly inside the window, in Ma ago */
  C0.flips = (runs) => runs.slice(1).map((r) => r.a);
  /** a compass-needle-shaped path (same proportions as Kit.needle, size = dial diameter) */
  C0.needlePaths = function (size) { const R = size / 2, L = R * 0.58, w = R * 0.12;
    return { north: `M0,${-L} L${w},0 L${-w},0 Z`, south: `M0,${L} L${w},0 L${-w},0 Z` }; };
  /** dipole field lines r = L sin^2(theta) around (cx, cy), axis tilted by tiltDeg (clockwise), as point lists */
  C0.dipoleLines = function (cx, cy, Ls, tiltDeg = 0, rMin = 0, n = 180) {
    const c = Math.cos(tiltDeg * Math.PI / 180), s = Math.sin(tiltDeg * Math.PI / 180), lines = [];
    for (const L of Ls) for (const side of [1, -1]) {
      const pts = [];
      for (let i = 1; i < n; i++) { const th = Math.PI * i / n, r = L * Math.sin(th) ** 2; if (r < rMin) continue;
        const x = side * r * Math.sin(th), y = -r * Math.cos(th); pts.push([cx + c * x - s * y, cy + s * x + c * y]); }
      lines.push(pts);
    }
    return lines;
  };
  window.C0 = C0;
})();
