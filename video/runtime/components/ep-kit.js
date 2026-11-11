/* ep-kit.js: the film's episode components (accepted deviations, storyboard ep01 section 5). Load after kit.js
 * (and after field.js when Kit.levelLines is used). Everything is a pure function of t, drawn in stage px; the physics
 * is computed in MATHEMATICAL coordinates (y up) and mapped to the stage by the scene's own toPx(x, y) (storyboard
 * ep01 section 0, "Coordonnées"): a component never flips an axis by itself.
 *
 *   Kit.fmtFr(x, digits = 2, {zero: '0'})       French decimal comma, U+2212 minus, never "−0": a value that rounds
 *                                              to zero prints `zero` ('0')
 *   Kit.readout(ctx, {label, value: (t) => number | string, digits, x, y | pos: (t) => [x, y], anchor: 'l'|'c'|'r',
 *                     size, color, at, out, z, parent})
 *       the counter: mono label in capitals (Kit.upper: Greek keeps its case) over a value in tabular figures (.tnum)
 *   Kit.probe(ctx, {toPx, F: (x, y) => [vx, vy], mode: 'flux'|'circulation', perArea: true, n: 256,
 *                   circle: {c: [x, y] | (t) => [x, y], r: number | (t) => number} | gamma: (s, t) => [x, y]
 *                   [, dgamma: (s, t) => [dx/ds, dy/ds]], parts: {n: 16, phase (turns), scale (px per field unit),
 *                   other: 'dashed' | null, signs: true, at, out}, draw: true, color, width, dash, at, out, z, svg})
 *       the dashed probe circle (any closed contour, counter-clockwise in s ∈ [0, 1)) and its flux or circulation by
 *       quadrature on n points, each weighted by the arc element |γ'(s)| Δs (outward normal, counter-clockwise
 *       travel), divided by the enclosed area when perArea. P.value(t) feeds a readout; P.flux(t), P.circulation(t),
 *       P.area(t), P.points(t). Parts: the normal (flux) or tangent (circulation) part of the field at n points, solid
 *       --u, the other part dashed --muted (other: 'dashed'), "+" --chalk / "−" --muted at the tip, no sign under 2 px.
 *   Kit.paddleWheel(ctx, {toPx, pos: [x, y] | (t) => [x, y], angle: (t) => α (rad, counter-clockwise), r: 46, at,
 *                         out, flow: {F, scale, at, out}, ghosts: [{t, alpha}], z, svg})
 *       four aubes --chalk, a hub, the marked aube --fg (with a dot at its tip); α is the angle of the marked aube,
 *       counter-clockwise positive, a closed-form function of t given by the scene; flow: arrows --u of the field at
 *       the four aube tips; ghosts: faded copies at earlier times (pos and angle of those times)
 *   Kit.marchingSquares(f, {x0, x1, y0, y1, nx, ny}, level) → polylines [[x, y], …] (math coordinates), the level
 *       set f = level by marching squares on an (nx + 1) × (ny + 1) grid, linear interpolation on the cell edges,
 *       saddles resolved by the cell-centre value, segments chained into polylines (closed ones end on their start)
 *   Kit.levelLines(ctx, {f, domain: {x0, x1, y0, y1, nx, ny}, levels: [...], toPx, color, width, alpha, dash, at,
 *                        dur, out, z})   level lines drawn on (Canvas) by progress
 *   Kit.compressLength(I, k, Is)        L(I) = k·I if I <= Is, k·Is·(2 − Is/I) above: strictly increasing, C¹, < 2·k·Is
 *                                       (used by Kit.arrows({compress: {k, threshold}}), field.js)
 * Colours are tokens (Kit.c): --u for the field, --chalk for probes and wheels, --muted for what does not count;
 * --fg-2 is the neutral field colour (a field not yet named, ep02), class .k-fg2 and KaTeX macro \cn{…}.
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit, TAU = Math.PI * 2;
  if (!K) throw new Error('ep-kit.js must be loaded after runtime/components/kit.js');
  K.MACROS['\\cn'] = '\\htmlClass{k-fg2}{#1}';   // neutral field (--fg-2)

  // ---------- numbers ----------
  K.fmtFr = function (x, digits = 2, o = {}) {
    if (typeof x === 'string') return x;
    if (x === null || x === undefined || !Number.isFinite(+x)) return '–';
    let s = (+x).toFixed(digits);
    if (+s === 0) return o.zero ?? '0';              // never "−0", never "-0,00"
    return s.replace('.', ',').replace(/^-/, '−');
  };

  K.compressLength = function (I, k, Is) {
    if (!(I > 0)) return 0;
    return I <= Is ? k * I : k * Is * (2 - Is / I);
  };

  // ---------- readout (counter) ----------
  K.readout = function (ctx, o = {}) {
    const root = K.el('div', { class: 'kit-readout', 'data-kit': 'readout' }, o.parent || ctx.stage);
    root.style.zIndex = o.z ?? 46;
    if (o.color) root.style.color = K.c(o.color);
    const lab = o.label ? K.el('div', { class: 'ro-label mono' }, root, K.upper(o.label)) : null;
    const val = K.el('div', { class: 'ro-value tnum' }, root, '');
    if (o.size) val.style.fontSize = o.size + 'px';
    const anchor = o.anchor || 'l', tx = anchor === 'r' ? '-100%' : anchor === 'c' ? '-50%' : '0';
    if (anchor !== 'l') root.style.textAlign = anchor === 'r' ? 'right' : 'center';
    const { t0, t1 } = K.times(ctx, o, 0);
    const value = typeof o.value === 'function' ? o.value : () => o.value;
    const pos = typeof o.pos === 'function' ? o.pos : () => [o.x ?? 1200, o.y ?? 400];
    return ctx.add({
      root, label: lab, el: val,
      render(t) {
        const e = K.env(t, t0, t1, 0.25, 0.25); K.show(root, e.on); if (!e.on) return;
        root.style.opacity = e.o;
        const [x, y] = pos(t);
        root.style.left = x.toFixed(1) + 'px'; root.style.top = y.toFixed(1) + 'px'; root.style.transform = `translateX(${tx})`;
        val.textContent = K.fmtFr(value(t), o.digits ?? 2, o);
      },
    });
  };

  // ---------- SVG arrow helper (shared by probe and wheel) ----------
  function arrowPath(x0, y0, x1, y1, hl = 14) {
    const m = Math.hypot(x1 - x0, y1 - y0); if (m < 0.5) return '';
    const a = Math.atan2(y1 - y0, x1 - x0), h = Math.min(hl, m * 0.45);
    const bx = x1 - h * 0.8 * Math.cos(a), by = y1 - h * 0.8 * Math.sin(a);
    return `M${x0.toFixed(2)},${y0.toFixed(2)}L${bx.toFixed(2)},${by.toFixed(2)}`
      + `M${x1.toFixed(2)},${y1.toFixed(2)}L${(x1 - h * Math.cos(a - 0.45)).toFixed(2)},${(y1 - h * Math.sin(a - 0.45)).toFixed(2)}`
      + `L${(x1 - h * Math.cos(a + 0.45)).toFixed(2)},${(y1 - h * Math.sin(a + 0.45)).toFixed(2)}Z`;
  }
  K.arrowPath = arrowPath;

  // ---------- probe ----------
  K.probe = function (ctx, o = {}) {
    if (!o.toPx || !o.F) throw new Error('probe needs toPx and F');
    const N = o.n ?? 256, mode = o.mode || 'flux', perArea = o.perArea !== false;
    const fn = (v) => (typeof v === 'function' ? v : () => v);
    let gamma, dgamma, areaF;
    if (o.circle) {
      const C = fn(o.circle.c), R = fn(o.circle.r);
      gamma = (s, t) => { const c = C(t), r = R(t); return [c[0] + r * Math.cos(TAU * s), c[1] + r * Math.sin(TAU * s)]; };
      dgamma = (s, t) => { const r = R(t); return [-TAU * r * Math.sin(TAU * s), TAU * r * Math.cos(TAU * s)]; };
      areaF = (t) => Math.PI * R(t) * R(t);
    } else if (o.gamma) {
      gamma = o.gamma;
      dgamma = o.dgamma || ((s, t) => { const d = 1e-4, a = gamma(s - d, t), b = gamma(s + d, t); return [(b[0] - a[0]) / (2 * d), (b[1] - a[1]) / (2 * d)]; });
      areaF = (t) => { let A = 0; for (let i = 0; i < N; i++) { const p = gamma(i / N, t), q = gamma((i + 1) / N, t); A += p[0] * q[1] - q[0] * p[1]; } return A / 2; };
    } else throw new Error('probe needs circle {c, r} or gamma(s, t)');
    // quadrature, cached per t (several readers per frame)
    let cacheT = NaN, cache = null;
    const integrals = (t) => {
      if (t === cacheT) return cache;
      let flux = 0, circ = 0; const ds = 1 / N;
      for (let i = 0; i < N; i++) {
        const s = (i + 0.5) / N, p = gamma(s, t), d = dgamma(s, t), v = o.F(p[0], p[1]);
        flux += (v[0] * d[1] - v[1] * d[0]) * ds;     // F · (γ'_y, −γ'_x) Δs = F·n |γ'| Δs
        circ += (v[0] * d[0] + v[1] * d[1]) * ds;     // F · γ' Δs = F·t |γ'| Δs
      }
      cacheT = t; cache = { flux, circ, area: areaF(t) };
      return cache;
    };
    const svg = o.svg || K.svgLayer(ctx, o.z ?? 13, o.parent); svg.setAttribute('data-kit', 'probe');
    const g = K.s('g', {}, svg);
    const col = K.c(o.color || 'chalk');
    const path = o.draw === false ? null : K.s('path', { fill: 'none', stroke: col, 'stroke-width': o.width ?? 3,
      'stroke-dasharray': (o.dash || [12, 9]).join(' '), 'stroke-linecap': 'butt', 'stroke-linejoin': 'round' }, g);
    const P = o.parts || null, np = P ? (P.n ?? 16) : 0;
    const pg = K.s('g', {}, g), parts = [];
    for (let k = 0; k < np; k++) {
      const other = P.other ? K.s('path', { fill: 'none', stroke: K.c('muted'), 'stroke-width': 3, 'stroke-dasharray': '7 6' }, pg) : null;
      const kept = K.s('path', { fill: K.c('u'), stroke: K.c('u'), 'stroke-width': 4, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, pg);
      const sign = P.signs === false ? null : K.s('text', { class: 'kt-label', 'text-anchor': 'middle', 'dominant-baseline': 'central' }, pg, '');
      if (sign) sign.style.cssText = `paint-order: stroke; stroke: ${K.c('bg')}; stroke-width: 6px; stroke-linejoin: round`;   // halo over field arrows
      parts.push({ other, kept, sign });
    }
    const { t0, t1 } = K.times(ctx, o, 0);
    const pt0 = P ? ctx.at(P.at ?? o.at ?? 0) : 0, pt1 = P && P.out !== undefined ? ctx.at(P.out) : Infinity;
    const keep = P && P.kept ? P.kept : (mode === 'flux' ? 'normal' : 'tangent');
    const Pr = {
      root: svg,
      flux: (t) => integrals(t).flux,
      circulation: (t) => integrals(t).circ,
      area: (t) => integrals(t).area,
      value: (t) => { const I = integrals(t), v = mode === 'flux' ? I.flux : I.circ; return perArea ? v / I.area : v; },
      points: (t) => Array.from({ length: N }, (_, i) => gamma(i / N, t)),
      render(t) {
        const e = K.env(t, t0, t1, 0.35, 0.3); K.show(svg, e.on); if (!e.on) return;
        svg.style.opacity = e.o;
        if (path) {
          let d = '';
          for (let i = 0; i <= N; i++) { const q = o.toPx(...gamma((i % N) / N, t)); d += (i ? 'L' : 'M') + q[0].toFixed(2) + ',' + q[1].toFixed(2); }
          path.setAttribute('d', d + 'Z');
        }
        if (!np) return;
        const pe = K.env(t, pt0, pt1, P.dur ?? 0.6, 0.3); pg.style.opacity = pe.o; K.show(pg, pe.on); if (!pe.on) return;
        const sc = P.scale ?? 100, ph = P.phase ?? 0;
        for (let k = 0; k < np; k++) {
          const s = (k / np + ph) % 1, p = gamma(s, t), d = dgamma(s, t), L = Math.hypot(d[0], d[1]) || 1;
          const tx = d[0] / L, ty = d[1] / L, nx = ty, ny = -tx, v = o.F(p[0], p[1]);
          const vn = v[0] * nx + v[1] * ny, vt = v[0] * tx + v[1] * ty;
          // growth staggered round the contour (counter-clockwise), like a hand going round
          const grow = S.seg(t, pt0 + 0.6 * k / np, pt0 + 0.6 * k / np + (P.dur ?? 0.6), S.ease.outCubic);
          const [bx, by] = o.toPx(p[0], p[1]);
          const kv = keep === 'normal' ? [nx * vn, ny * vn] : [tx * vt, ty * vt], ov = keep === 'normal' ? [tx * vt, ty * vt] : [nx * vn, ny * vn];
          const ex = bx + kv[0] * sc * grow, ey = by - kv[1] * sc * grow;      // math → screen: y flipped by hand (vector)
          parts[k].kept.setAttribute('d', arrowPath(bx, by, ex, ey));
          if (parts[k].other) parts[k].other.setAttribute('d', `M${bx.toFixed(2)},${by.toFixed(2)}L${(bx + ov[0] * sc * grow).toFixed(2)},${(by - ov[1] * sc * grow).toFixed(2)}`);
          const sg = parts[k].sign;
          if (sg) {
            const len = Math.hypot(ex - bx, ey - by), val = keep === 'normal' ? vn : vt;
            if (len < 2 || grow < 0.95) { sg.style.display = 'none'; continue; }
            sg.style.display = '';
            // the sign sits beyond the tip, outward along the part (or along the normal for a tangent part)
            const ux = (ex - bx) / len, uy = (ey - by) / len, off = 24;
            sg.setAttribute('x', (ex + ux * off).toFixed(1)); sg.setAttribute('y', (ey + uy * off).toFixed(1));
            sg.textContent = val > 0 ? '+' : '−'; sg.style.fill = K.c(val > 0 ? 'chalk' : 'muted');
          }
        }
      },
    };
    return ctx.add(Pr);
  };

  // ---------- paddle wheel ----------
  K.paddleWheel = function (ctx, o = {}) {
    if (!o.toPx) throw new Error('paddleWheel needs toPx');
    const R = o.r ?? 46, hub = o.hub ?? Math.max(6, R * 0.17);
    const pos = typeof o.pos === 'function' ? o.pos : () => o.pos || [0, 0];
    const ang = typeof o.angle === 'function' ? o.angle : () => o.angle || 0;
    const svg = o.svg || K.svgLayer(ctx, o.z ?? 15, o.parent); svg.setAttribute('data-kit', 'paddle-wheel');
    const chalk = K.c('chalk'), fg = K.c('fg');
    const build = (parent, alpha) => {
      const g = K.s('g', { opacity: alpha }, parent);
      const rot = K.s('g', {}, g);
      for (let i = 0; i < 4; i++) {
        const a = i * 90, marked = i === 0;
        const b = K.s('g', { transform: `rotate(${-a})` }, rot);
        K.s('line', { x1: hub * 0.6, y1: 0, x2: R, y2: 0, stroke: marked ? fg : chalk, 'stroke-width': marked ? 7 : 5, 'stroke-linecap': 'round' }, b);
        K.s('line', { x1: R, y1: -R * 0.16, x2: R, y2: R * 0.16, stroke: marked ? fg : chalk, 'stroke-width': marked ? 6 : 4, 'stroke-linecap': 'round' }, b);
        if (marked) K.s('circle', { cx: R + 9, cy: 0, r: 5.5, fill: fg }, b);
      }
      K.s('circle', { r: hub, fill: K.c('bg'), stroke: chalk, 'stroke-width': 3 }, g);
      return { g, rot };
    };
    const ghosts = (o.ghosts || []).map((gh) => ({ t: ctx.at(gh.t), alpha: gh.alpha ?? 0.3, w: build(svg, 0) }));
    const W = build(svg, 1);
    const fl = o.flow ? { F: o.flow.F, sc: o.flow.scale ?? 100, a: ctx.at(o.flow.at ?? o.at ?? 0), b: o.flow.out !== undefined ? ctx.at(o.flow.out) : Infinity } : null;
    const arrows = fl ? [0, 1, 2, 3].map(() => K.s('path', { fill: K.c('u'), stroke: K.c('u'), 'stroke-width': 4, 'stroke-linecap': 'round' }, svg)) : [];
    const { t0, t1 } = K.times(ctx, o, 0);
    const place = (w, t) => { const [x, y] = o.toPx(...pos(t)); w.g.setAttribute('transform', `translate(${x.toFixed(2)},${y.toFixed(2)})`);
      w.rot.setAttribute('transform', `rotate(${(-ang(t) * 180 / Math.PI).toFixed(3)})`); return [x, y]; };
    return ctx.add({
      root: svg, angle: ang, pos,
      render(t) {
        const e = K.env(t, t0, t1, 0.35, 0.3); K.show(svg, e.on); if (!e.on) return;
        svg.style.opacity = e.o;
        const [x, y] = place(W, t);
        for (const gh of ghosts) { const on = t >= gh.t; gh.w.g.setAttribute('opacity', on ? gh.alpha * S.seg(t, gh.t, gh.t + 0.3, S.ease.linear) : 0); if (on) place(gh.w, gh.t); }
        if (fl) {
          const fe = K.env(t, fl.a, fl.b, 0.4, 0.3), a0 = ang(t), [mx, my] = pos(t);
          // tips of the four aubes in math coordinates: the stage px radius R converted by the local scale of toPx
          const q = o.toPx(mx + 1, my), unit = Math.hypot(q[0] - x, q[1] - y) || 1;
          arrows.forEach((ar, i) => {
            if (!fe.on) { ar.style.display = 'none'; return; }
            ar.style.display = ''; ar.style.opacity = fe.o;
            const a = a0 + i * Math.PI / 2, px = mx + (R / unit) * Math.cos(a), py = my + (R / unit) * Math.sin(a), v = fl.F(px, py);
            const [bx, by] = o.toPx(px, py);
            ar.setAttribute('d', arrowPath(bx, by, bx + v[0] * fl.sc * fe.p, by - v[1] * fl.sc * fe.p, 12));
          });
        }
      },
    });
  };

  // ---------- marching squares ----------
  K.marchingSquares = function (f, dom, level = 0) {
    const nx = dom.nx ?? 96, ny = dom.ny ?? 96, x0 = dom.x0, y0 = dom.y0, dx = (dom.x1 - x0) / nx, dy = (dom.y1 - y0) / ny;
    const v = new Float64Array((nx + 1) * (ny + 1));
    for (let j = 0; j <= ny; j++) for (let i = 0; i <= nx; i++) v[j * (nx + 1) + i] = f(x0 + i * dx, y0 + j * dy) - level;
    const V = (i, j) => v[j * (nx + 1) + i];
    const pts = new Map();    // edge key -> crossing point
    const edge = (kind, i, j) => {
      const key = kind + i + ',' + j;
      if (!pts.has(key)) {
        const a = V(i, j), b = kind === 'h' ? V(i + 1, j) : V(i, j + 1), s = a / (a - b);
        pts.set(key, kind === 'h' ? [x0 + (i + s) * dx, y0 + j * dy] : [x0 + i * dx, y0 + (j + s) * dy]);
      }
      return key;
    };
    const segs = [];
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const a = V(i, j), b = V(i + 1, j), c = V(i + 1, j + 1), d = V(i, j + 1);   // corners: bottom-left, bottom-right, top-right, top-left
      const idx = (a > 0 ? 1 : 0) | (b > 0 ? 2 : 0) | (c > 0 ? 4 : 0) | (d > 0 ? 8 : 0);
      if (idx === 0 || idx === 15) continue;
      const B = () => edge('h', i, j), T = () => edge('h', i, j + 1), L = () => edge('v', i, j), Rr = () => edge('v', i + 1, j);
      const centre = (a + b + c + d) / 4;
      switch (idx) {
        case 1: case 14: segs.push([L(), B()]); break;
        case 2: case 13: segs.push([B(), Rr()]); break;
        case 3: case 12: segs.push([L(), Rr()]); break;
        case 4: case 11: segs.push([Rr(), T()]); break;
        case 6: case 9: segs.push([B(), T()]); break;
        case 7: case 8: segs.push([L(), T()]); break;
        case 5: if (centre > 0) segs.push([L(), T()], [B(), Rr()]); else segs.push([L(), B()], [Rr(), T()]); break;
        case 10: if (centre > 0) segs.push([L(), B()], [Rr(), T()]); else segs.push([L(), T()], [B(), Rr()]); break;
        default: break;
      }
    }
    // chain the segments through their shared edge points
    const adj = new Map();
    segs.forEach((s, k) => { for (const e of s) { if (!adj.has(e)) adj.set(e, []); adj.get(e).push(k); } });
    const used = new Uint8Array(segs.length), lines = [];
    const extend = (from) => {   // follow unused segments from an edge point; returns the points after `from`
      const out = []; let cur = from;
      for (;;) {
        const k = (adj.get(cur) || []).find((m) => !used[m]); if (k === undefined) return out;
        used[k] = 1; cur = segs[k][0] === cur ? segs[k][1] : segs[k][0]; out.push(cur);
      }
    };
    for (let k = 0; k < segs.length; k++) {
      if (used[k]) continue;
      used[k] = 1;
      const fwd = extend(segs[k][1]), back = extend(segs[k][0]);
      const chain = back.reverse().concat([segs[k][0], segs[k][1]], fwd);
      lines.push(chain.map((key) => pts.get(key)));
    }
    return lines;
  };

  K.levelLines = function (ctx, o = {}) {
    if (!o.f || !o.domain || !o.toPx) throw new Error('levelLines needs f, domain and toPx');
    const lines = [];
    for (const lv of o.levels || [0]) for (const L of K.marchingSquares(o.f, o.domain, lv)) lines.push(L.map((p) => o.toPx(p[0], p[1])));
    const Lc = K.canvasLayer(ctx, o.z ?? 6, null, o.parent, { reset: true }); Lc.canvas.setAttribute('data-kit', 'level-lines');
    const { t0, t1 } = K.times(ctx, o, 0), dur = o.dur ?? 1.2;
    return ctx.add({
      lines, canvas: Lc.canvas,
      render(t) {
        const e = K.env(t, t0, t1, 0.2, 0.4); K.show(Lc.canvas, e.on); if (!e.on) return;
        Lc.g.clearRect(0, 0, 1920, 1080);
        if (o.dash) Lc.g.setLineDash(o.dash);
        K.drawLines(Lc.g, lines, { color: o.color || 'u', width: o.width ?? 2.5, alpha: (o.alpha ?? 0.9) * e.o, progress: S.seg(t, t0, t0 + dur, S.ease.inOutSine) });
      },
    });
  };
})();
