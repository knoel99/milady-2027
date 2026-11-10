/* threemodes.js: the E1 story's shared pieces, promoted from the ch04 pilot (scenes/ch04/ch04_kit.js, C4.*) so that
 * 05.2, 06.4, 07.x and 09.x reuse them as is. Load after kit.js. Nothing here holds a number of the physics: the
 * coefficients come from the data (e1_finegrid.json config.mu / config.nu).
 *
 *   Kit.threeModes(mu, nu)              Gissinger three-mode model (Q, D, V), RK4 with a fixed step:
 *                                       {F(q, d, v, G, out), step(s, G, dt), run(s, G, units, dt, cb), seed(G, sgn, rng, noise)}
 *   Kit.dial(svgParent, {x, y, r, ticks, nticks, bezel})   a grey dial without numbers and its pointer:
 *                                       .set(angleDeg, colour, alpha); pointer angle of a reading: Kit.dialAngle(v, vmax)
 *   Kit.photo(svgParent, {x, y, w, h, q, d, v, vmax, vmaxV, dialY, stroke, qcolor})
 *                                       a film frame / snapshot "photo" with the three small dials (Q light
 *                                       vermillion --b-light, D --b or --b-neg by sign, V --u)
 *   Kit.shoebox(svgParent, {x, y, w, h}) open grey box (front face, rim, inside): {g, inside, content, front, mouth}
 *                                       put dropped photos in .content (drawn between the inside and the front)
 * These are SVG builders, not timed components: they take an SVG parent (a <g> of your Kit.svgLayer) and you
 * move them in your render. All colours are tokens (Kit.c).
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit, TAU = Math.PI * 2;
  if (!K) throw new Error('threemodes.js must be loaded after runtime/components/kit.js');

  // ---------------- three-mode model (RK4, fixed step) ----------------
  K.threeModes = function (mu, nu) {
    if (!(mu > 0) || !(nu > 0)) throw new Error('Kit.threeModes: coefficients missing (data config.mu, config.nu)');
    const k1 = new Float64Array(3), k2 = new Float64Array(3), k3 = new Float64Array(3), k4 = new Float64Array(3), y = new Float64Array(3);
    const f = (q, d, v, G, o) => { o[0] = mu * q - v * d; o[1] = -nu * d + v * q; o[2] = G - v + q * d; return o; };
    const M = {
      mu, nu, F: f,
      /** one RK4 step of size dt on s = [Q, D, V] (Float64Array, in place) at forcing G */
      step(s, G, dt) {
        f(s[0], s[1], s[2], G, k1);
        y[0] = s[0] + 0.5 * dt * k1[0]; y[1] = s[1] + 0.5 * dt * k1[1]; y[2] = s[2] + 0.5 * dt * k1[2]; f(y[0], y[1], y[2], G, k2);
        y[0] = s[0] + 0.5 * dt * k2[0]; y[1] = s[1] + 0.5 * dt * k2[1]; y[2] = s[2] + 0.5 * dt * k2[2]; f(y[0], y[1], y[2], G, k3);
        y[0] = s[0] + dt * k3[0]; y[1] = s[1] + dt * k3[1]; y[2] = s[2] + dt * k3[2]; f(y[0], y[1], y[2], G, k4);
        s[0] += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
        s[1] += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
        s[2] += dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]);
        return s;
      },
      /** integrate `units` model time units at fixed G; cb(s, n) after each step (return true to stop) */
      run(s, G, units, dt, cb) {
        const n = Math.round(units / dt);
        for (let i = 0; i < n; i++) { M.step(s, G, dt); if (cb && cb(s, i)) break; }
        return s;
      },
      /** a state near the fixed point of polarity sgn (+1: D > 0), with seeded Gaussian noise (start of a transient) */
      seed(G, sgn, rng, noise = 0.5) {
        const r = Math.sqrt(mu * nu), D = sgn * Math.sqrt(mu * (G + r) / r), Q = -Math.sqrt(nu / mu) * D, V = -r;
        const g = () => { const u = Math.max(1e-12, rng()), w = rng(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(TAU * w); };
        return Float64Array.from([Q + noise * g(), D + noise * g(), V + noise * g()]);
      },
    };
    return M;
  };

  // ---------------- dial (three dials of 04.1, the photos' small dials) ----------------
  K.dial = function (parent, o = {}) {
    const x = o.x ?? 0, y = o.y ?? 0, R = o.r ?? 120, g = K.s('g', { transform: `translate(${x},${y})`, 'data-kit': 'dial' }, parent);
    const A0 = -135, A1 = 135, pol = (a, r) => [r * Math.sin(a * Math.PI / 180), -r * Math.cos(a * Math.PI / 180)];
    const sw = Math.max(1.5, R / 30);
    K.s('circle', { r: R, fill: K.c('panel'), stroke: K.c('matter'), 'stroke-width': o.bezel ?? Math.max(2, R / 22) }, g);
    if (o.ticks !== false) {
      const nt = o.nticks ?? 18;
      for (let i = 0; i <= nt; i++) {
        const a = A0 + (A1 - A0) * i / nt, big = i === nt / 2, p = pol(a, R * 0.88), q = pol(a, R * (big ? 0.68 : 0.78));
        K.s('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], stroke: K.c(big ? 'fg-2' : 'matter-dark'), 'stroke-width': big ? sw * 1.6 : sw }, g);
      }
    }
    const ptr = K.s('g', {}, g);
    const line = K.s('line', { x1: 0, y1: R * 0.18, x2: 0, y2: -R * 0.74, stroke: K.c('matter'), 'stroke-width': Math.max(3, R / 13), 'stroke-linecap': 'round' }, ptr);
    K.s('circle', { r: Math.max(3, R / 11), fill: K.c('matter') }, g);
    return {
      g, ptr, line, R,
      set(angle, color, alpha = 1) {
        ptr.setAttribute('transform', `rotate(${angle.toFixed(3)})`);
        if (color) line.setAttribute('stroke', color);
        line.setAttribute('opacity', alpha);
      },
    };
  };
  /** pointer angle of a reading v on a dial that spans ±vmax over ±120 degrees (no numbers on the face) */
  K.dialAngle = (v, vmax) => 120 * Math.max(-1, Math.min(1, v / vmax));

  // ---------------- film frame / photo ----------------
  K.photo = function (parent, o = {}) {
    const w = o.w ?? 160, h = o.h ?? 120, g = K.s('g', { transform: `translate(${o.x ?? 0},${o.y ?? 0})`, 'data-kit': 'photo' }, parent);
    K.s('rect', { x: 0, y: 0, width: w, height: h, rx: Math.max(3, w / 40), fill: K.c('panel'), stroke: K.c('matter'), 'stroke-width': o.stroke ?? 2 }, g);
    const r = Math.min(w / 7.2, h / 2.9), cy = h * (o.dialY ?? 0.5), xs = [w * 0.2, w * 0.5, w * 0.8];
    const vm = o.vmax ?? 3;
    const cols = [o.qcolor || K.c('b-light'), K.c('b'), K.c('u')], vals = [o.q, o.d, o.v];
    const dials = xs.map((dx, i) => {
      const dl = K.dial(g, { x: dx, y: cy, r, nticks: 6, bezel: Math.max(1.5, r / 14) });
      dl.set(K.dialAngle(vals[i] ?? 0, i === 2 ? (o.vmaxV ?? vm) : vm), i === 1 && (o.d ?? 0) < 0 ? K.c('b-neg') : cols[i]);
      return dl;
    });
    return { g, dials, w, h };
  };

  // ---------------- shoebox (first appearance 04.6; returns in 05.2, 06.4) ----------------
  K.shoebox = function (parent, o = {}) {
    const w = o.w ?? 520, h = o.h ?? 260, x = o.x ?? 960, y = o.y ?? 600;   // (x, y) = centre of the front face
    const g = K.s('g', { 'data-kit': 'shoebox' }, parent);
    const d = h * 0.32, x0 = x - w / 2, y0 = y - h / 2;
    const inside = K.s('g', {}, g);   // the open top: back wall and inside, drawn behind the front face
    K.s('path', { d: `M${x0},${y0} L${x0 + d},${y0 - d} L${x0 + w + d},${y0 - d} L${x0 + w},${y0} Z`, fill: K.c('matter-dark'), stroke: K.c('matter'), 'stroke-width': 3, 'stroke-linejoin': 'round' }, inside);
    const content = K.s('g', {}, g);  // photos dropped in the box go here (between inside and front)
    const front = K.s('g', {}, g);
    K.s('path', { d: `M${x0 + w},${y0} L${x0 + w + d},${y0 - d} L${x0 + w + d},${y0 + h - d} L${x0 + w},${y0 + h} Z`, fill: K.c('matter-dark'), stroke: K.c('matter'), 'stroke-width': 3, 'stroke-linejoin': 'round' }, front);
    K.s('rect', { x: x0, y: y0, width: w, height: h, fill: K.c('panel'), stroke: K.c('matter'), 'stroke-width': 3 }, front);
    K.s('line', { x1: x0 + w * 0.08, x2: x0 + w * 0.92, y1: y0 + h * 0.22, y2: y0 + h * 0.22, stroke: K.c('matter-dark'), 'stroke-width': 3 }, front);
    return { g, inside, content, front, x, y, w, h, d, mouth: [x + d / 2, y0 - d / 2] };
  };
  void S;
})();
