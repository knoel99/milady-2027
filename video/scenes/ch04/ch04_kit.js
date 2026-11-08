/* ch04_kit.js: helpers shared by the scenes of unit ch04 (load after the runtime/components files).
 * Candidates for promotion to runtime/components (see script/_review/scenes_ch04.md): the three-mode
 * integrator, the dial, the PREDICT card, the shoebox and the film frame are reused by 05.2, 06.4, 07.x.
 *
 *   C4.model(mu, nu)                 Gissinger three-mode model: {F, step(s, G, dt), run(s, G, units, dt, cb)}
 *   C4.mix(a, b, share)              token colour a mixed with token b ('rgb(…)'), share of a in [0, 1]
 *   C4.qcol(share)                   the quadrupole's light vermillion: --b mixed with --fg (never --b-neg)
 *   C4.dial(parent, {x, y, r, …})    a grey dial (no numbers) with a pointer; .set(angleDeg, colour, alpha)
 *   C4.predict(ctx, {…})             PREDICT card: kicker, question, two outline buttons, the answer lights one
 *   C4.shoebox(parent, {x, y, w, h}) open grey box (front face + rim + inside), returns {g, mouth}
 *   C4.frame(parent, {x, y, w, h, q, d, v, qmax})   a film frame / photo with the three small dials
 * All drawing uses tokens (Kit.c); nothing here holds a number of the physics: coefficients come from data.
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit, TAU = Math.PI * 2;
  const C4 = {};

  /** WORKAROUND (runtime/scene.js bug): ctx.at('cue-0.15') throws "unknown cue" because the cue-name pattern
   *  [\w.:-]* also eats "-0.15". This shim parses "name±x" itself (an exact cue name wins) and leaves every
   *  other spec to the runtime. Call it first in setup(); components then use the patched ctx.at. */
  C4.fixAt = function (ctx) {
    const orig = ctx.at;
    ctx.at = function (s, fb) {
      if (typeof s === 'string' && !(s.trim() in ctx.cues)) {
        const m = s.match(/^\s*([A-Za-z_][\w]*(?:-[A-Za-z_]\w*)*)\s*([+-])\s*([\d.]+)\s*$/);
        if (m) return orig(m[1]) + (m[2] === '+' ? 1 : -1) * Number(m[3]);
      }
      return orig(s, fb);
    };
    return ctx.at;
  };

  // ---------------- three-mode model (RK4, fixed step) ----------------
  C4.model = function (mu, nu) {
    if (!(mu > 0) || !(nu > 0)) throw new Error('C4.model: coefficients missing (data config.mu, config.nu)');
    const k1 = new Float64Array(3), k2 = new Float64Array(3), k3 = new Float64Array(3), k4 = new Float64Array(3), y = new Float64Array(3);
    const f = (q, d, v, G, o) => { o[0] = mu * q - v * d; o[1] = -nu * d + v * q; o[2] = G - v + q * d; };
    const M = {
      mu, nu,
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
      /** a state near the fixed point of polarity sgn (+1: D > 0), with seeded noise (start of a transient) */
      seed(G, sgn, rng, noise = 0.5) {
        const r = Math.sqrt(mu * nu), D = sgn * Math.sqrt(mu * (G + r) / r), Q = -Math.sqrt(nu / mu) * D, V = -r;
        const g = () => { const u = Math.max(1e-12, rng()), w = rng(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(TAU * w); };
        return Float64Array.from([Q + noise * g(), D + noise * g(), V + noise * g()]);
      },
    };
    return M;
  };

  /** WORKAROUND (Kit.formulaLayer): the script's formulas one at a time (each replaced by the next one), so the
   *  layer does not grow upward into the scene as items accumulate (long items wrap to two lines). */
  C4.formulas = function (ctx, o = {}) {
    const f = ctx.script.onscreen && ctx.script.onscreen.formulas;
    if (!f || !f.length) return null;   // preview without a script entry: no formula layer
    const items = f.map((x, i) => ({ tex: x.tex, at: x.cue, out: x.out ?? (o.stack ? undefined : (i + 1 < f.length ? f[i + 1].cue : undefined)) }));
    const L = Kit.formulaLayer(ctx, Object.assign({ items }, o.layer || {}));
    C4.fitFormulas(L.root, items.map((x) => x.tex));
    return L;
  };

  /** REVIEW FIX (Kit.formulaLayer wraps long items only after a relation, e.g. "Γ ≤ | 0.86" or "Γ = | 0.9"):
   *  an item wider than the layer is split at its most balanced separator (";", ":" or "," followed by a
   *  space, inside \text{} or at the top level, or \quad), one KaTeX line per half, nothing broken inside a
   *  relation. If a half is still too wide, the item shrinks (never below 28 px). Items that fit are untouched. */
  C4.breakCandidates = function (tex) {
    const out = [];
    let depth = 0;
    for (let i = 0; i < tex.length; i++) {
      if (depth === 0 && tex.startsWith('\\text{', i)) {
        let j = i + 6, d = 1; while (j < tex.length && d > 0) { if (tex[j] === '{') d++; else if (tex[j] === '}') d--; j++; }
        const inner = tex.slice(i + 6, j - 1), re = /[;:,]\s+/g; let m;
        while ((m = re.exec(inner))) {
          const k = m.index + 1, rest = inner.slice(k).replace(/^\s+/, '');
          out.push({ left: tex.slice(0, i) + (k > 0 ? '\\text{' + inner.slice(0, k) + '}' : ''), right: (rest ? '\\text{' + rest + '}' : '') + tex.slice(j) });
        }
        i = j - 1; continue;
      }
      const ch = tex[i];
      if (ch === '\\' && depth === 0 && /^\\q?quad/.test(tex.slice(i))) { const n = tex.startsWith('\\qquad', i) ? 6 : 5; out.push({ left: tex.slice(0, i), right: tex.slice(i + n).replace(/^\s+/, '') }); i += n - 1; continue; }
      if (ch === '\\') { i++; continue; }   // skip the escaped character (\{, \;, \,)
      if (ch === '{') depth++; else if (ch === '}') depth--;
      else if (depth === 0 && /[;:,]/.test(ch)) {
        const m = tex.slice(i + 1).match(/^(?:\s*(?:\\[ ,;:!]|\\quad|\\qquad|~))+\s*/);
        if (m) out.push({ left: tex.slice(0, i + 1), right: tex.slice(i + 1 + m[0].length) });
      }
    }
    return out.filter((c) => c.left.trim() && c.right.trim());
  };
  C4.fitFormulas = function (root, texs) {
    if (!root) return;
    const rows = Array.from(root.querySelectorAll('.fl-item')), cs = getComputedStyle(root);
    const avail = parseFloat(cs.maxWidth || '760') - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 4;
    const probe = K.el('span', {}, root); probe.style.cssText = 'position:absolute;left:0;top:0;visibility:hidden;white-space:nowrap;display:inline-block;font-size:32px';
    const wOf = (tex) => { probe.innerHTML = K.tex(tex, false); return probe.getBoundingClientRect().width; };
    rows.forEach((row, i) => {
      const tex = texs[i]; if (!tex || wOf(tex) <= avail) return;
      let best = null;
      for (const c of C4.breakCandidates(tex)) { const a = wOf(c.left), b = wOf(c.right), w = Math.max(a, b); if (!best || w < best.w) best = { c, w }; }
      if (!best) return;   // no separator: KaTeX's own break after a relation stays
      row.innerHTML = ''; row.style.whiteSpace = 'nowrap';
      [best.c.left, best.c.right].forEach((x) => K.el('div', { html: K.tex(x, false) }, row));
      if (best.w > avail) row.style.fontSize = Math.max(28, Math.floor(32 * avail / best.w)) + 'px';
    });
    probe.remove();
  };

  /** REVIEW FIX (runtime/theme.css sets font-feature-settings "tnum" on the whole stage, and Inter's tabular
   *  hyphen is a full figure wide: "north-south" renders as "north - south"). Replaces a hyphen between two
   *  letters by U+2011 (non-breaking hyphen, normal width in Inter and JetBrains Mono) in every text node of
   *  `root` outside KaTeX. Call it last in setup(). */
  C4.nbhy = function (root) {
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.parentElement && n.parentElement.closest('.katex') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT) });
    for (let n = w.nextNode(); n; n = w.nextNode()) if (/\p{L}-\p{L}/u.test(n.nodeValue)) n.nodeValue = n.nodeValue.replace(/(\p{L})-(?=\p{L})/gu, '$1‑');
  };

  // ---------------- colours ----------------
  C4.mix = function (a, b, share) {
    const A = K.hex(K.c(a)), B = K.hex(K.c(b));
    return `rgb(${A.map((x, i) => Math.round(x * share + B[i] * (1 - share))).join(',')})`;
  };
  C4.mixRGB = function (a, b, share) { const A = K.hex(K.c(a)), B = K.hex(K.c(b)); return A.map((x, i) => x * share + B[i] * (1 - share)); };
  /** light vermillion of the quadrupole: --b mixed with --fg (share of --b, default 0.6) */
  C4.qcol = (share = 0.6) => C4.mix('b', 'fg', share);
  /** CSS custom properties for the scene CSS (.k-q etc.) */
  C4.tokens = function (ctx, share) { ctx.stage.style.setProperty('--q', C4.qcol(share)); };

  // ---------------- dial (04.1, film frames of 04.6, photos of 04.7) ----------------
  C4.dial = function (parent, o = {}) {
    const x = o.x ?? 0, y = o.y ?? 0, R = o.r ?? 120, g = K.s('g', { transform: `translate(${x},${y})` }, parent);
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
  /** pointer angle of a dial reading v on a dial that spans ±vmax over ±120 degrees (no numbers on the face) */
  C4.angle = (v, vmax) => 120 * Math.max(-1, Math.min(1, v / vmax));

  // ---------------- film frame / photo ----------------
  C4.frame = function (parent, o = {}) {
    const w = o.w ?? 160, h = o.h ?? 120, g = K.s('g', { transform: `translate(${o.x ?? 0},${o.y ?? 0})` }, parent);
    K.s('rect', { x: 0, y: 0, width: w, height: h, rx: Math.max(3, w / 40), fill: K.c('panel'), stroke: K.c('matter'), 'stroke-width': o.stroke ?? 2 }, g);
    const r = Math.min(w / 7.2, h / 2.9), cy = h * (o.dialY ?? 0.5), xs = [w * 0.2, w * 0.5, w * 0.8];
    const vm = o.vmax ?? 3;
    const cols = [C4.qcol(o.qshare), K.c('b'), K.c('u')], vals = [o.q, o.d, o.v];
    const dials = xs.map((dx, i) => {
      const dl = C4.dial(g, { x: dx, y: cy, r, nticks: 6, bezel: Math.max(1.5, r / 14) });
      dl.set(C4.angle(vals[i] ?? 0, i === 2 ? (o.vmaxV ?? vm) : vm), i === 1 && (o.d ?? 0) < 0 ? K.c('b-neg') : cols[i]);
      return dl;
    });
    return { g, dials, w, h };
  };

  // ---------------- shoebox (M-shoebox, first appearance 04.6) ----------------
  C4.shoebox = function (parent, o = {}) {
    const w = o.w ?? 520, h = o.h ?? 260, x = o.x ?? 960, y = o.y ?? 600;   // (x, y) = centre of the front face
    const g = K.s('g', { 'data-kit': 'shoebox' }, parent);
    const d = h * 0.32, x0 = x - w / 2, y0 = y - h / 2;
    const inside = K.s('g', {}, g);   // the open top: back wall and inside, drawn behind the front face
    K.s('path', { d: `M${x0},${y0} L${x0 + d},${y0 - d} L${x0 + w + d},${y0 - d} L${x0 + w},${y0} Z`, fill: K.c('matter-dark'), stroke: K.c('matter'), 'stroke-width': 3, 'stroke-linejoin': 'round' }, inside);
    const content = K.s('g', {}, g);  // frames dropped in the box go here (between inside and front)
    const front = K.s('g', {}, g);
    K.s('path', { d: `M${x0 + w},${y0} L${x0 + w + d},${y0 - d} L${x0 + w + d},${y0 + h - d} L${x0 + w},${y0 + h} Z`, fill: K.c('matter-dark'), stroke: K.c('matter'), 'stroke-width': 3, 'stroke-linejoin': 'round' }, front);
    K.s('rect', { x: x0, y: y0, width: w, height: h, fill: K.c('panel'), stroke: K.c('matter'), 'stroke-width': 3 }, front);
    K.s('line', { x1: x0 + w * 0.08, x2: x0 + w * 0.92, y1: y0 + h * 0.22, y2: y0 + h * 0.22, stroke: K.c('matter-dark'), 'stroke-width': 3 }, front);
    return { g, inside, content, front, x, y, w, h, d, mouth: [x + d / 2, y0 - d / 2] };
  };

  // ---------------- PREDICT card ----------------
  /** opts: {x, y, w, question, options: ['A · …', 'B · …'], at, out, answerAt, pick (index), parent, hideUnder: [elements]} */
  C4.predict = function (ctx, o = {}) {
    const root = K.el('div', { class: 'c4-predict', 'data-kit': 'predict' }, o.parent || ctx.stage);
    root.style.left = (o.x ?? 960) + 'px'; root.style.top = (o.y ?? 96) + 'px'; root.style.width = (o.w ?? 1000) + 'px';
    if ((o.anchor || 'c') === 'c') root.style.marginLeft = (-(o.w ?? 1000) / 2) + 'px';
    K.el('div', { class: 'c4p-kicker' }, root, 'PREDICT');
    const q = K.el('div', { class: 'c4p-q', html: K.markup(o.question || '') }, root);
    if (!o.question) q.style.display = 'none';   // compact card (the answer beat): kicker and buttons only
    const row = K.el('div', { class: 'c4p-row' }, root);
    const btns = (o.options || []).map((t) => K.el('div', { class: 'c4p-btn' }, row, t));
    const t0 = ctx.at(o.at ?? 0), t1 = o.out !== undefined ? ctx.at(o.out) : Infinity, ta = o.answerAt !== undefined ? ctx.at(o.answerAt) : Infinity;
    K.fit(q, (o.w ?? 1000) - 64, null, 36, ctx);
    return ctx.add({
      root, buttons: btns,
      render(t) {
        const e = K.env(t, t0, t1, 0.35, 0.3); K.show(root, e.on); if (!e.on) return;
        root.style.opacity = e.o; root.style.transform = `translateY(${(-18 * (1 - e.p) - 24 * e.q).toFixed(2)}px)`;
        const a = S.seg(t, ta, ta + 0.25, S.ease.linear);
        btns.forEach((b, i) => {
          const lit = i === o.pick ? a : 0;
          b.style.borderColor = lit > 0 ? K.c('fg') : ''; b.style.color = lit > 0 ? K.c('fg') : '';
          b.style.background = lit > 0 ? K.rgba(K.c('fg'), 0.14 * lit) : '';
          b.style.opacity = (i !== o.pick && a > 0) ? (1 - 0.5 * a) : 1;
        });
      },
    });
  };

  window.C4 = C4;
})();
