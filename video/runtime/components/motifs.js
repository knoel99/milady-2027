/* motifs.js: the film's recurring motifs (styles.md §3.5, outline §2), all cue-driven.
 *
 *   M1  Kit.needle(ctx, {x, y, size, corner, start, flips: ['cue', …], dur, at, out})   compass needle, flips
 *       Kit.barcode(ctx, {box, segments: [{a, b, s}] | series: {t, D}, domain, at, dur})  polarity strip
 *   M2  Kit.knob(ctx, {x, y, r, min, max, value | keys: [{at, v, dur}], window, label, fmt, at})
 *   M3  Kit.twoInks(ctx, {box, cells, amp, at, lineY, maxPoints})   blue flow carries a vermillion line
 *   M4  Kit.cloud(ctx, {box, targets: [{pts, at, dur}], range, n, strings, at, size})  violet samples
 *   M5  Kit.histogram(ctx, {box, values, range, bins, ref, at, dur, morph: {values, at, dur}, label})
 *   M6  Kit.projector(ctx, {x, y, at, drop, field, gauge: {label, value}})   vector dropped onto a plane
 *   M7  Kit.staircase(ctx, {x, y, w, h, lit, pending, at})   tiers 0 → 4
 *   M9  Kit.pen(ctx, {kind, box | target | from/to, at, dur, color})   circle, underline, arrow, brace, box, check, cross
 *   M10 Kit.mirror(ctx, {mode: 'plane' | 'point', x, y, at, reflect, ...})  B → −B
 * Polarity is a shade of vermillion (--b, --b-neg), never a new hue. Physical objects (needle, knob) may
 * overshoot by at most 3 % (Scene.spring).
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit;
  const TAU = Math.PI * 2;

  // ======================= M1 needle =======================
  K.needle = function (ctx, o = {}) {
    const corner = !!o.corner, size = o.size ?? (corner ? 96 : 360);
    const x = o.x ?? (corner ? 1772 : 960), y = o.y ?? (corner ? 176 : 470), R = size / 2;
    const svg = K.svgLayer(ctx, o.z ?? (corner ? 52 : 15), o.parent); svg.setAttribute('data-kit', 'needle');
    const g = K.s('g', { transform: `translate(${x},${y})` }, svg);
    const matter = K.c('matter');
    K.s('circle', { r: R, fill: K.c('panel'), stroke: matter, 'stroke-width': corner ? 3 : 6 }, g);
    if (!corner) {
      for (let i = 0; i < 72; i++) {
        const a = i * TAU / 72, l = i % 18 === 0 ? 26 : i % 6 === 0 ? 16 : 8;
        K.s('line', { x1: Math.sin(a) * (R - 12), y1: -Math.cos(a) * (R - 12), x2: Math.sin(a) * (R - 12 - l), y2: -Math.cos(a) * (R - 12 - l), stroke: K.c('matter-dark'), 'stroke-width': i % 18 === 0 ? 4 : 2 }, g);
      }
      K.s('text', { x: 0, y: -R + 76, 'text-anchor': 'middle', class: 'kt-label' }, g, 'N').style.fill = K.c('fg-2');
      K.s('text', { x: 0, y: R - 46, 'text-anchor': 'middle', class: 'kt-label' }, g, 'S').style.fill = K.c('muted');
    }
    const nd = K.s('g', {}, g), L = R * (corner ? 0.78 : 0.58), w = R * (corner ? 0.2 : 0.12);
    K.s('path', { d: `M0,${-L} L${w},0 L${-w},0 Z`, fill: K.c('b') }, nd);          // north half: vermillion
    K.s('path', { d: `M0,${L} L${w},0 L${-w},0 Z`, fill: matter }, nd);               // south half: matter grey
    K.s('circle', { r: corner ? 5 : 12, fill: K.c('fg-2') }, g);
    const flips = (o.flips || []).map((f) => (typeof f === 'object' && f !== null && !('cue' in f) ? { t: ctx.at(f.at), d: f.dur ?? o.dur ?? 0.9 } : { t: ctx.at(f), d: o.dur ?? 0.9 }));
    const base = o.start === 'south' ? 180 : 0, wob = o.wobble ?? (corner ? 0 : 1.2), ph = S.rng('needle').call(null) * TAU;
    const { t0, t1 } = K.times(ctx, o, 0);
    const N = {
      root: svg,
      angle(t) { let a = base; for (const f of flips) a += 180 * S.spring((t - f.t) / f.d, 0.03); return a + wob * Math.sin(TAU * t / 3.7 + ph) * Math.exp(-0.15 * Math.max(0, t - t0)); },
      render(t) {
        const e = K.env(t, t0, t1, 0.4, 0.3); K.show(svg, e.on); svg.style.opacity = e.o;
        nd.setAttribute('transform', `rotate(${N.angle(t).toFixed(3)})`);
      },
    };
    return ctx.add(N);
  };

  K.barcode = function (ctx, o = {}) {
    const box = Object.assign({ x: 360, y: 640, w: 1200, h: 56 }, o.box || {});
    let segs = o.segments;
    if (!segs && o.series) {   // sign runs of a series {t, D}
      segs = []; const T = o.series.t, D = o.series.D; let a = T[0], s = Math.sign(D[0]) || 1;
      for (let i = 1; i < T.length; i++) { const si = Math.sign(D[i]) || s; if (si !== s) { segs.push({ a, b: T[i], s }); a = T[i]; s = si; } }
      segs.push({ a, b: T[T.length - 1], s });
    }
    if (!segs || !segs.length) throw new Error('barcode needs segments or series');
    const dom = o.domain || [segs[0].a, segs[segs.length - 1].b];
    const svg = o.svg || K.svgLayer(ctx, o.z ?? 12, o.parent); const g = K.s('g', { 'data-kit': 'barcode' }, svg);
    const cid = 'bc' + Math.floor(S.rng('bc' + box.y)() * 1e9);
    const cp = K.s('clipPath', { id: cid }, K.s('defs', {}, g)); const cr = K.s('rect', { x: box.x, y: box.y - 4, height: box.h + 8, width: 0 }, cp);
    const gg = K.s('g', { 'clip-path': `url(#${cid})` }, g);
    const X = (v) => box.x + box.w * (v - dom[0]) / (dom[1] - dom[0]);
    for (const s of segs) K.s('rect', { x: X(s.a), y: box.y, width: Math.max(0.5, X(s.b) - X(s.a)), height: box.h, fill: K.c(s.s > 0 ? 'b' : 'b-neg') }, gg);
    K.s('rect', { x: box.x, y: box.y, width: box.w, height: box.h, fill: 'none', stroke: K.c('matter-dark'), 'stroke-width': 2 }, g);
    if (o.label) K.s('text', { x: box.x, y: box.y - 16, class: 'kt-mono' }, g, K.upper(o.label));
    const t0 = ctx.at(o.at ?? 0), dur = o.dur ?? 2;
    return ctx.add({ root: g, render(t) { const p = S.seg(t, t0, t0 + dur, S.ease.inOutSine); cr.setAttribute('width', (box.w * p).toFixed(1)); g.style.display = t >= t0 ? '' : 'none'; g.style.opacity = S.seg(t, t0, t0 + 0.3, S.ease.linear); } });
  };

  // ======================= M2 knob =======================
  K.knob = function (ctx, o = {}) {
    const x = o.x ?? 960, y = o.y ?? 480, R = o.r ?? 120, min = o.min ?? 0, max = o.max ?? 1;
    const A0 = -135, A1 = 135, ang = (v) => A0 + (A1 - A0) * (v - min) / (max - min);
    const svg = K.svgLayer(ctx, o.z ?? 14, o.parent); svg.setAttribute('data-kit', 'knob');
    const g = K.s('g', { transform: `translate(${x},${y})` }, svg);
    const pol = (a, r) => [r * Math.sin(a * Math.PI / 180), -r * Math.cos(a * Math.PI / 180)];
    const arc = (a, b, r) => { const p = pol(a, r), q = pol(b, r); return `M${p[0]},${p[1]} A${r},${r} 0 ${b - a > 180 ? 1 : 0} 1 ${q[0]},${q[1]}`; };
    const green = K.c('param');
    K.s('path', { d: arc(A0, A1, R + 18), fill: 'none', stroke: K.c('matter-dark'), 'stroke-width': 4 }, g);
    if (o.window) K.s('path', { d: arc(ang(o.window[0]), ang(Math.min(max, o.window[1])), R + 18), fill: 'none', stroke: K.rgba(green, 0.32), 'stroke-width': 22 }, g);
    const nt = o.ticks ?? 10;
    for (let i = 0; i <= nt; i++) { const a = A0 + (A1 - A0) * i / nt, p = pol(a, R + 32), q = pol(a, R + 44); K.s('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], stroke: K.c('muted'), 'stroke-width': 2 }, g); }
    K.s('circle', { r: R, fill: K.c('panel'), stroke: K.c('matter'), 'stroke-width': 5 }, g);
    const ptr = K.s('g', {}, g);
    K.s('line', { x1: 0, y1: -R * 0.25, x2: 0, y2: -R + 12, stroke: green, 'stroke-width': 9, 'stroke-linecap': 'round' }, ptr);
    K.s('circle', { r: 10, fill: K.c('matter') }, g);
    const lab = o.label ? K.s('text', { x: 0, y: R + 92, 'text-anchor': 'middle', class: 'kt-axis' }, g, '') : null;
    if (lab) lab.style.fill = green;
    const keys = (o.keys || [{ at: o.at ?? 0, v: o.value ?? min, dur: 0 }]).map((k) => ({ t: ctx.at(k.at), v: k.v, d: k.dur ?? 1.2 }));
    const val = (t) => { let v = keys[0].v; for (let i = 1; i < keys.length; i++) { const k = keys[i]; v = v + (k.v - v) * S.spring((t - k.t) / k.d, 0.02); } return v; };
    const { t0, t1 } = K.times(ctx, o, 0);
    const fmt = o.fmt || ((v) => K.fmt(v, 3));
    return ctx.add({
      root: svg, value: val,
      render(t) {
        const e = K.env(t, t0, t1, 0.4, 0.3); K.show(svg, e.on); svg.style.opacity = e.o;
        const v = val(t); ptr.setAttribute('transform', `rotate(${ang(Math.max(min, Math.min(max, v))).toFixed(3)})`);
        if (lab) lab.textContent = o.showValue === false ? o.label : `${o.label} = ${fmt(v)}`;
      },
    });
  };

  // ======================= M3 two inks =======================
  K.twoInks = function (ctx, o = {}) {
    const box = Object.assign({ x: 240, y: 180, w: 1440, h: 600 }, o.box || {});
    const [cx, cy] = o.cells || [4, 2], amp = o.amp ?? 220, kx = Math.PI * cx / box.w, ky = Math.PI * cy / box.h;
    // cellular flow, stream function psi = sin(kx x) sin(ky y): u = (dpsi/dy, -dpsi/dx), max speed amp px/s
    const F = (X, Y) => { const xx = X - box.x, yy = Y - box.y; return [amp * Math.sin(kx * xx) * Math.cos(ky * yy), -amp * Math.cos(kx * xx) * Math.sin(ky * yy)]; };
    const seeds = []; for (let i = 0; i < cx; i++) for (let j = 0; j < cy; j++) for (const f of [0.18, 0.32, 0.44]) seeds.push([box.x + (i + 0.5) * box.w / cx + f * box.w / cx * 0.9, box.y + (j + 0.5) * box.h / cy]);
    const lines = K.streamlines(F, seeds, { h: 5, n: 900, box, forward: true, closeTol: 6 });
    const dt = 1 / 120, maxPts = o.maxPoints ?? 6000, maxSeg = o.maxSeg ?? 6, ly = box.y + box.h * (o.lineY ?? 0.36);
    const init = () => { const p = []; for (let i = 0; i <= 200; i++) p.push(box.x + box.w * i / 200, ly); return { p }; };
    const step = (s) => {
      const p = s.p;
      for (let i = 0; i < p.length; i += 2) {   // RK2 (midpoint)
        const v1 = F(p[i], p[i + 1]), v2 = F(p[i] + 0.5 * dt * v1[0], p[i + 1] + 0.5 * dt * v1[1]);
        p[i] += dt * v2[0]; p[i + 1] += dt * v2[1];
      }
      if (p.length / 2 < maxPts) {             // refine stretched segments (the line grows as it is stretched)
        const q = [p[0], p[1]];
        for (let i = 2; i < p.length; i += 2) {
          const dx = p[i] - p[i - 2], dy = p[i + 1] - p[i - 1];
          if (dx * dx + dy * dy > maxSeg * maxSeg && q.length / 2 < maxPts) q.push(p[i - 2] + dx / 2, p[i - 1] + dy / 2);
          q.push(p[i], p[i + 1]);
        }
        s.p = q;
      }
      return s;
    };
    const at = S.stepper(init, step, dt);
    const Lc = K.canvasLayer(ctx, o.z ?? 6, null, o.parent); Lc.canvas.setAttribute('data-kit', 'two-inks');
    const { t0, t1 } = K.times(ctx, o, 0);
    const tRun = ctx.at(o.run ?? o.at ?? 0);
    return ctx.add({
      canvas: Lc.canvas, F,
      render(t) {
        const e = K.env(t, t0, t1, 0.6, 0.4); K.show(Lc.canvas, e.on); if (!e.on) return;
        const g = Lc.g; g.clearRect(0, 0, 1920, 1080);
        K.drawLines(g, lines, { color: 'u', width: 2.5, alpha: 0.55 * e.o, progress: S.seg(t, t0, t0 + 1.2, S.ease.inOutSine) });
        const s = at(Math.max(0, t - tRun)), p = s.p;
        g.save(); g.strokeStyle = K.c('b'); g.lineWidth = o.width ?? 4; g.lineJoin = g.lineCap = 'round'; g.globalAlpha = e.o;
        g.beginPath(); g.moveTo(p[0], p[1]); for (let i = 2; i < p.length; i += 2) g.lineTo(p[i], p[i + 1]); g.stroke(); g.restore();
      },
    });
  };

  // ======================= M4 cloud =======================
  K.cloud = function (ctx, o = {}) {
    const box = Object.assign({ x: 560, y: 160, w: 800, h: 640 }, o.box || {});
    const rx = (o.range && o.range.x) || [-3, 3], ry = (o.range && o.range.y) || [-3, 3];
    const pts = (P) => { const a = S.f32(P); if (a instanceof Float32Array) return a; const f = new Float32Array(a.length * 2); a.forEach((p, i) => { f[2 * i] = p[0]; f[2 * i + 1] = p[1]; }); return f; };
    const targets = (o.targets || []).map((T) => ({ p: pts(T.pts), t: ctx.at(T.at), d: T.dur ?? 2.4 }));
    if (!targets.length) throw new Error('cloud needs targets [{pts, at}] (n×2 data coordinates)');
    const n = Math.min(o.n ?? 4000, ...targets.map((T) => T.p.length / 2));
    const rng = S.rng(o.seed ?? 'cloud'), src = new Float32Array(2 * n);
    const mx = (rx[0] + rx[1]) / 2, my = (ry[0] + ry[1]) / 2, sd = o.sd ?? 0.16;
    for (let i = 0; i < n; i++) {   // Box–Muller, seeded: the Gaussian source of the flow
      const u1 = Math.max(1e-12, rng()), u2 = rng(), r = Math.sqrt(-2 * Math.log(u1));
      src[2 * i] = mx + sd * (rx[1] - rx[0]) * r * Math.cos(TAU * u2); src[2 * i + 1] = my + sd * (ry[1] - ry[0]) * r * Math.sin(TAU * u2);
    }
    const PX = (v) => box.x + box.w * (v - rx[0]) / (rx[1] - rx[0]), PY = (v) => box.y + box.h * (1 - (v - ry[0]) / (ry[1] - ry[0]));
    const Lc = K.canvasLayer(ctx, o.z ?? 9, null, o.parent); Lc.canvas.setAttribute('data-kit', 'cloud');
    const { t0, t1 } = K.times(ctx, o, 0);
    const nStr = o.strings ?? 0, size = o.size ?? 3.2;
    const pos = (t, i) => {   // straight-line (conditional flow matching) paths between successive targets
      let x = src[2 * i], y = src[2 * i + 1];
      for (const T of targets) { const s = S.seg(t, T.t, T.t + T.d, S.ease.inOutCubic); if (s <= 0) break; x += (T.p[2 * i] - x) * s; y += (T.p[2 * i + 1] - y) * s; }
      return [x, y];
    };
    return ctx.add({
      canvas: Lc.canvas, toPx: (x, y) => [PX(x), PY(y)],
      render(t) {
        const e = K.env(t, t0, t1, 0.5, 0.4); K.show(Lc.canvas, e.on); if (!e.on) return;
        const g = Lc.g; g.clearRect(0, 0, 1920, 1080);
        const col = K.c(o.color || 'model');
        if (nStr) {
          const T = targets[0], s = S.seg(t, T.t, T.t + T.d, S.ease.inOutCubic);
          const fadeS = 1 - S.seg(t, T.t + T.d, T.t + T.d + 1.0, S.ease.linear);
          g.save(); g.strokeStyle = K.rgba(col, 0.28 * e.o * fadeS); g.lineWidth = 1.5; g.beginPath();
          for (let k = 0; k < nStr; k++) { const i = Math.floor(k * n / nStr), [x, y] = pos(t, i); g.moveTo(PX(src[2 * i]), PY(src[2 * i + 1])); g.lineTo(PX(x), PY(y)); }
          g.stroke(); g.restore();
          void s;
        }
        g.fillStyle = K.rgba(col, (o.alpha ?? 0.7) * e.o);
        for (let i = 0; i < n; i++) { const [x, y] = pos(t, i); g.fillRect(PX(x) - size / 2, PY(y) - size / 2, size, size); }
      },
    });
  };

  // ======================= M5 histogram =======================
  K.histogram = function (ctx, o = {}) {
    const box = Object.assign({ x: 560, y: 260, w: 800, h: 420 }, o.box || {});
    const bins = o.bins ?? 31, range = o.range || [-1, 1];   // odd: 0 sits in the middle of a bin
    const dens = (vals) => {
      const v = S.f32(vals), h = new Float64Array(bins), w = (range[1] - range[0]) / bins; let n = 0;
      for (let i = 0; i < v.length; i++) { const k = Math.floor((v[i] - range[0]) / w); if (k >= 0 && k < bins) { h[k]++; n++; } }
      for (let k = 0; k < bins; k++) h[k] = n ? h[k] / (n * w) : 0;
      return h;
    };
    const H1 = dens(o.values), H2 = o.morph ? dens(o.morph.values) : null, HR = o.ref ? dens(o.ref) : null;
    // the morph target (e.g. the spike of per-sample rescaling) may go off scale: it is clipped at the top of the
    // box with an "off scale" mark, so the reference stays readable (clipSpike: false to rescale instead)
    let ymax = o.yMax || Math.max(...H1, ...(HR || [0])) * 1.12;
    if (H2 && !o.yMax && o.clipSpike === false) ymax = Math.max(ymax, Math.max(...H2) * 1.05);
    const svg = o.svg || K.svgLayer(ctx, o.z ?? 12, o.parent); const g = K.s('g', { 'data-kit': 'histogram' }, svg);
    const bw = box.w / bins, Y = (d) => box.y + box.h - box.h * Math.min(1, d / ymax);
    const col = K.c(o.color || 'metric');
    K.s('line', { x1: box.x, x2: box.x + box.w, y1: box.y + box.h, y2: box.y + box.h, stroke: K.c('muted'), 'stroke-width': 2 }, g);
    const bars = []; for (let k = 0; k < bins; k++) bars.push(K.s('rect', { x: box.x + k * bw + 1.5, width: bw - 3, fill: col }, g));
    let refPath = null;
    if (HR) {
      let d = `M${box.x},${box.y + box.h}`; for (let k = 0; k < bins; k++) d += `L${box.x + k * bw},${Y(HR[k])}L${box.x + (k + 1) * bw},${Y(HR[k])}`;
      refPath = K.s('path', { d: d + `L${box.x + box.w},${box.y + box.h}`, fill: 'none', stroke: K.c('fg-2'), 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
    }
    if (o.label) K.s('text', { x: box.x, y: box.y - 18, class: 'kt-label' }, g, o.label).style.fill = col;
    const off = H2 ? K.s('text', { x: 0, y: box.y + 30, 'text-anchor': 'start', class: 'kt-mono' }, g, '↑ OFF SCALE') : null;   // beside the clipped bar
    if (off) off.style.fill = col;
    if (o.xLabel) K.s('text', { x: box.x + box.w / 2, y: box.y + box.h + 50, 'text-anchor': 'middle', class: 'kt-axis' }, g, o.xLabel);
    const { t0, t1 } = K.times(ctx, o, 0); const dur = o.dur ?? 1.4;
    const tm = o.morph ? ctx.at(o.morph.at) : Infinity, dm = o.morph ? o.morph.dur ?? 1.5 : 1;
    const tr = o.refAt !== undefined ? ctx.at(o.refAt) : t0;
    return ctx.add({
      root: g,
      render(t) {
        const e = K.env(t, t0, t1, 0.3, 0.3); g.style.display = e.on ? '' : 'none'; g.style.opacity = e.o;
        const m = S.seg(t, tm, tm + dm, S.ease.inOutCubic);
        for (let k = 0; k < bins; k++) {
          const grow = S.seg(t, t0 + dur * 0.6 * k / bins, t0 + dur * 0.6 * k / bins + dur * 0.4, S.ease.outCubic);
          const d = (H2 ? H1[k] + (H2[k] - H1[k]) * m : H1[k]) * grow, y = Y(d);
          bars[k].setAttribute('y', y.toFixed(2)); bars[k].setAttribute('height', (box.y + box.h - y).toFixed(2));
        }
        if (off) {   // mark the tallest clipped bar
          let kk = -1, best = 0;
          for (let k = 0; k < bins; k++) { const d = H1[k] + (H2[k] - H1[k]) * m; if (d > ymax && d > best) { best = d; kk = k; } }
          off.style.display = kk >= 0 ? '' : 'none'; if (kk >= 0) off.setAttribute('x', box.x + (kk + 1) * bw + 12);
        }
        if (refPath) refPath.style.opacity = S.seg(t, tr, tr + 0.5, S.ease.linear);
      },
    });
  };

  // ======================= M6 projector =======================
  K.projector = function (ctx, o = {}) {
    const x = o.x ?? 960, y = o.y ?? 560, s = o.scale ?? 1;
    const svg = K.svgLayer(ctx, o.z ?? 14, o.parent); svg.setAttribute('data-kit', 'projector');
    const g = K.s('g', { transform: `translate(${x},${y}) scale(${s})` }, svg);
    const plane = K.s('path', { d: 'M-380,40 L180,40 L380,-80 L-180,-80 Z', fill: K.rgba(K.c('infra'), 0.18), stroke: K.c('infra'), 'stroke-width': 3 }, g);
    const lab = K.s('text', { x: -360, y: 92, class: 'kt-mono' }, g, K.upper(o.planeLabel || 'divergence-free fields'));
    const col = K.c(o.field || 'b'), tip = [60, -330], foot = [60, -20];
    const v = K.s('line', { x1: -120, y1: -20, x2: tip[0], y2: tip[1], stroke: col, 'stroke-width': 7, 'stroke-linecap': 'round' }, g);
    const drop = K.s('line', { x1: tip[0], y1: tip[1], x2: foot[0], y2: foot[1], stroke: K.c('muted'), 'stroke-width': 3, 'stroke-dasharray': '10 8' }, g);
    const pv = K.s('line', { x1: -120, y1: -20, x2: -120, y2: -20, stroke: col, 'stroke-width': 7, 'stroke-linecap': 'round' }, g);
    const head = (el) => K.s('circle', { r: 9, fill: col }, el);
    const h1 = head(g), h2 = head(g);
    const gauge = o.gauge ? K.el('div', { class: 'kit-chip', 'data-kit': 'projector' }, o.parent || ctx.stage, '') : null;
    if (gauge) {   // gauge chip: under the plane (default) or to its right (gaugeAt: 'right')
      gauge.style.position = 'absolute'; gauge.style.zIndex = (o.z ?? 14) + 1;
      if (o.gaugeAt === 'right') { gauge.style.left = (x + 420 * s) + 'px'; gauge.style.top = (y - 60 * s) + 'px'; }
      else { gauge.style.left = (x - 360 * s) + 'px'; gauge.style.top = (y + 130 * s) + 'px'; }
    }
    const { t0, t1 } = K.times(ctx, o, 0), td = ctx.at(o.drop ?? (t0 + 1.0));
    return ctx.add({
      root: svg,
      render(t) {
        const e = K.env(t, t0, t1, 0.5, 0.3); K.show(svg, e.on); svg.style.opacity = e.o;
        const p = S.seg(t, td, td + 0.9, S.ease.inOutCubic);
        drop.style.opacity = S.seg(t, td - 0.2, td + 0.2, S.ease.linear) * (1 - 0.6 * S.seg(t, td + 1.2, td + 1.8, S.ease.linear));
        const px = S.lerp(-120, foot[0], p), py = S.lerp(-20, foot[1], p);
        pv.setAttribute('x2', px); pv.setAttribute('y2', py); h2.setAttribute('cx', px); h2.setAttribute('cy', py); h2.style.opacity = p > 0.02 ? 1 : 0;
        h1.setAttribute('cx', tip[0]); h1.setAttribute('cy', tip[1]);
        v.style.opacity = h1.style.opacity = 1 - 0.65 * S.seg(t, td + 0.9, td + 1.5, S.ease.linear);
        void plane; void lab;
        if (gauge) {
          K.show(gauge, e.on && t >= td + 0.9); gauge.style.opacity = S.seg(t, td + 0.9, td + 1.3, S.ease.linear) * e.o;
          gauge.textContent = K.upper(`${o.gauge.label || '∇·B'} ≈ ${typeof o.gauge.value === 'number' ? K.fmt(o.gauge.value, 2) : o.gauge.value}`);
        }
      },
    });
  };

  // ======================= M7 staircase =======================
  const TIERS = ['three modes', '2D square', '3D box', 'VKS cylinder', 'precessing cylinder'];
  K.staircase = function (ctx, o = {}) {
    const x = o.x ?? 1060, y = o.y ?? 560, w = o.w ?? 760, h = o.h ?? 250, sw = w / 5, base = 64, sh = Math.max(12, (h - 60 - base) / 4);
    const svg = o.svg || K.svgLayer(ctx, o.z ?? 16, o.parent); const g = K.s('g', { 'data-kit': 'staircase' }, svg);
    const lit = o.lit ?? null, pend = new Set(o.pending || []);
    const fg = K.c('fg'), md = K.c('matter-dark'), mu = K.c('muted');
    const steps = TIERS.map((name, i) => {
      const gg = K.s('g', {}, g), top = y + h - base - i * sh - 60, on = i === lit;
      const blk = K.s('rect', { x: x + i * sw + 4, y: top + 60, width: sw - 8, height: y + h - top - 60, fill: on ? K.rgba(fg, 0.12) : K.rgba(md, 0.35), stroke: on ? fg : md, 'stroke-width': on ? 3 : 2 }, gg);
      if (pend.has(i)) blk.setAttribute('stroke-dasharray', '9 7');
      const cx = x + i * sw + sw / 2, cy = top + 28, ic = on ? fg : mu;
      const st = { fill: 'none', stroke: ic, 'stroke-width': 3, 'stroke-linejoin': 'round' };
      if (i === 0) [-24, 0, 24].forEach((d) => K.s('circle', { cx: cx + d, cy, r: 8, ...st }, gg));
      if (i === 1) K.s('rect', { x: cx - 24, y: cy - 24, width: 48, height: 48, ...st }, gg);
      if (i === 2) K.s('path', { d: `M${cx - 22},${cy - 10} l22,-12 l22,12 v26 l-22,12 l-22,-12 Z M${cx - 22},${cy - 10} l22,12 l22,-12 M${cx},${cy + 2} v26`, ...st }, gg);
      if (i === 3) K.s('path', { d: `M${cx - 22},${cy - 18} v36 a22,8 0 0 0 44,0 v-36 a22,8 0 0 0 -44,0 a22,8 0 0 0 44,0`, ...st }, gg);
      if (i === 4) K.s('path', { d: `M${cx - 22},${cy - 18} v36 a22,8 0 0 0 44,0 v-36 a22,8 0 0 0 -44,0 a22,8 0 0 0 44,0`, ...st, transform: `rotate(-20 ${cx} ${cy})` }, gg);
      const tl = K.s('text', { x: cx, y: top + 60 + 42, 'text-anchor': 'middle', class: 'kt-mono' }, gg, 'T' + i);
      if (on) tl.style.fill = fg;
      if (o.labels !== false) {
        const words = name.split(' ');
        const lines = words.length > 1 && name.length > 10 ? [words.slice(0, -1).join(' '), words[words.length - 1]] : [name];
        lines.forEach((l, k) => { const tx = K.s('text', { x: cx, y: y + h + 40 + 34 * k, 'text-anchor': 'middle', class: 'kt-tick' }, gg, l); if (on) tx.style.fill = fg; });
      }
      return gg;
    });
    const { t0, t1 } = K.times(ctx, o, 0);
    return ctx.add({
      root: g,
      render(t) {
        const e = K.env(t, t0, t1, 0.5, 0.3); g.style.display = e.on ? '' : 'none'; g.style.opacity = e.o;
        steps.forEach((s, i) => { const p = S.seg(t, t0 + 0.08 * i, t0 + 0.08 * i + 0.45, S.ease.outCubic); s.style.opacity = p; s.setAttribute('transform', `translate(0 ${(12 * (1 - p)).toFixed(2)})`); });
      },
    });
  };
  K.TIERS = TIERS;

  // ======================= M9 pen =======================
  K.pen = function (ctx, o = {}) {
    const rng = S.rng('pen' + (o.seed ?? JSON.stringify([o.kind, o.box, o.from, o.to]))), jit = (a) => (rng() - 0.5) * 2 * a;
    let b = o.box; if (!b && o.target) b = K.box(o.target, ctx);
    const pad = o.pad ?? 14;
    let d = '';
    const kind = o.kind || 'underline';
    if (kind === 'circle') {
      const cx = b.x + b.w / 2, cy = b.y + b.h / 2, rx = b.w / 2 + pad + 10, ry = b.h / 2 + pad, a0 = -2.2 + jit(0.2), turns = 1.12;
      const N = 64; for (let i = 0; i <= N; i++) { const a = a0 + turns * TAU * i / N, k = 1 + 0.04 * Math.sin(3 * a + 1.3) + jit(0.006); d += `${i ? 'L' : 'M'}${(cx + rx * k * Math.cos(a)).toFixed(1)},${(cy + ry * k * Math.sin(a)).toFixed(1)}`; }
    } else if (kind === 'underline') {
      const y = b.y + b.h + (o.offset ?? 8), x0 = b.x - 6, x1 = b.x + b.w + 6;
      d = `M${x0},${y + jit(2)} Q${(x0 + x1) / 2},${y + 6 + jit(3)} ${x1},${y - 2 + jit(2)}`;
    } else if (kind === 'box') {
      const x0 = b.x - pad, y0 = b.y - pad, x1 = b.x + b.w + pad, y1 = b.y + b.h + pad;
      d = `M${x0 + jit(2)},${y0 + jit(2)} L${x1 + jit(2)},${y0 + jit(2)} L${x1 + jit(2)},${y1 + jit(2)} L${x0 + jit(2)},${y1 + jit(2)} Z`;
    } else if (kind === 'brace') {
      const y = b.y + b.h + 12, x0 = b.x + 4, x1 = b.x + b.w - 4, xm = (x0 + x1) / 2, r = Math.min(18, (x1 - x0) / 4);
      d = `M${x0},${y} q0,${r} ${r},${r} L${xm - r},${y + r} q${r},0 ${r},${r} q0,${-r} ${r},${-r} L${x1 - r},${y + r} q${r},0 ${r},${-r}`;
    } else if (kind === 'arrow') {
      const [x0, y0] = o.from, [x1, y1] = o.to, mx = (x0 + x1) / 2 + (y1 - y0) * (o.bend ?? 0.15), my = (y0 + y1) / 2 - (x1 - x0) * (o.bend ?? 0.15);
      const a = Math.atan2(y1 - my, x1 - mx), hl = 22;
      d = `M${x0},${y0} Q${mx},${my} ${x1},${y1} M${x1 - hl * Math.cos(a - 0.5)},${y1 - hl * Math.sin(a - 0.5)} L${x1},${y1} L${x1 - hl * Math.cos(a + 0.5)},${y1 - hl * Math.sin(a + 0.5)}`;
    } else if (kind === 'check') {
      const cx = b.x + b.w / 2, cy = b.y + b.h / 2, s = Math.min(b.w, b.h) / 2;
      d = `M${cx - s},${cy} L${cx - s * 0.3},${cy + s * 0.7} L${cx + s},${cy - s * 0.8}`;
    } else if (kind === 'cross') {
      const x0 = b.x, y0 = b.y, x1 = b.x + b.w, y1 = b.y + b.h;
      d = `M${x0},${y0} L${x1},${y1} M${x1},${y0} L${x0},${y1}`;
    } else throw new Error('pen kind: circle | underline | box | brace | arrow | check | cross');
    const svg = o.svg || K.svgLayer(ctx, o.z ?? 30, o.parent);
    const p = K.s('path', { d, fill: 'none', stroke: K.c(o.color || 'chalk'), 'stroke-width': o.width ?? 4.5, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'data-kit': 'pen' }, svg);
    const len = p.getTotalLength(); p.style.strokeDasharray = `${len} ${len + 10}`;
    const { t0, t1 } = K.times(ctx, o, 0), dur = o.dur ?? 0.6;
    return ctx.add({
      path: p,
      render(t) {
        const q = S.seg(t, t0, t0 + dur, S.ease.inOutSine), f = t1 === Infinity ? 0 : S.seg(t, t1, t1 + 0.3, S.ease.linear);
        p.style.strokeDashoffset = (len * (1 - q)).toFixed(2); p.style.opacity = (q > 0 ? 1 : 0) * (1 - f) * (o.alpha ?? 0.95);
      },
    });
  };

  // ======================= M10 mirror =======================
  K.mirror = function (ctx, o = {}) {
    const x = o.x ?? 960, y = o.y ?? 470, H = o.h ?? 520, mode = o.mode || 'plane';
    const svg = K.svgLayer(ctx, o.z ?? 14, o.parent); svg.setAttribute('data-kit', 'mirror');
    const g = K.s('g', { transform: `translate(${x},${y})` }, svg);
    const fg = K.c('fg'), bp = K.c('b'), bn = K.c('b-neg');
    const parts = { plane: [], src: [], img: [], link: [] };
    const arrow = (x0, y0, x1, y1, col, w = 8) => {
      const gg = K.s('g', {}, g), a = Math.atan2(y1 - y0, x1 - x0), hl = 26;
      K.s('line', { x1: x0, y1: y0, x2: x1 - 0.7 * hl * Math.cos(a), y2: y1 - 0.7 * hl * Math.sin(a), stroke: col, 'stroke-width': w, 'stroke-linecap': 'round' }, gg);
      K.s('path', { d: `M${x1},${y1} L${x1 - hl * Math.cos(a - 0.45)},${y1 - hl * Math.sin(a - 0.45)} L${x1 - hl * Math.cos(a + 0.45)},${y1 - hl * Math.sin(a + 0.45)} Z`, fill: col }, gg);
      return gg;
    };
    if (mode === 'plane') {
      // a reflecting plane: B on one side, its image −B (other polarity shade) on the other
      parts.plane.push(K.s('line', { x1: 0, y1: -H / 2, x2: 0, y2: H / 2, stroke: fg, 'stroke-width': 4 }, g));
      const hatch = K.s('g', { stroke: K.c('muted'), 'stroke-width': 2 }, g); parts.plane.push(hatch);
      for (let yy = -H / 2 + 10; yy < H / 2; yy += 26) K.s('line', { x1: 0, y1: yy, x2: 16, y2: yy + 16 }, hatch);
      const dx = Math.max(120, 0.55 * H), up = 0.27 * H, dn = 0.23 * H;   // arrows scale with the plane
      parts.src.push(arrow(-dx, dn, -dx, -up, bp));
      parts.img.push(arrow(dx, -up, dx, dn, bn));
      const lk = K.s('path', { d: `M${-dx + 40},-10 Q0,${-0.17 * H} ${dx - 40},-10`, fill: 'none', stroke: K.c('muted'), 'stroke-width': 3, 'stroke-dasharray': '6 9' }, g); parts.link.push(lk);
      const t1 = K.s('text', { x: -dx, y: dn + 50, 'text-anchor': 'middle', class: 'kt-axis' }, g, 'B'); t1.style.fill = bp; parts.src.push(t1);
      const t2 = K.s('text', { x: dx, y: dn + 50, 'text-anchor': 'middle', class: 'kt-axis' }, g, '−B'); t2.style.fill = bn; parts.img.push(t2);
    } else {
      // point reflection through the origin of a (Q, D) phase plane: S = diag(−1, −1, 1) sends (Q, D) to (−Q, −D)
      const R = H / 2;
      parts.plane.push(K.s('line', { x1: -R, y1: 0, x2: R, y2: 0, stroke: K.c('muted'), 'stroke-width': 2 }, g), K.s('line', { x1: 0, y1: -R, x2: 0, y2: R, stroke: K.c('muted'), 'stroke-width': 2 }, g));
      parts.plane.push(K.s('circle', { r: 7, fill: fg }, g));
      const P = o.point || [150, -120];
      parts.src.push(K.s('circle', { cx: P[0], cy: P[1], r: 14, fill: bp }, g));
      parts.img.push(K.s('circle', { cx: -P[0], cy: -P[1], r: 14, fill: bn }, g));
      parts.link.push(K.s('line', { x1: P[0], y1: P[1], x2: -P[0], y2: -P[1], stroke: K.c('muted'), 'stroke-width': 3, 'stroke-dasharray': '6 9' }, g));
      const ax = (txt, xx, yy, anchor) => { const e = K.s('text', { x: xx, y: yy, 'text-anchor': anchor, class: 'kt-tick' }, g, txt); parts.plane.push(e); };
      ax(o.xLabel || 'Q', R - 4, 40, 'end'); ax(o.yLabel || 'D', 18, -R + 28, 'start');
    }
    let sl = null;
    if (o.showS !== false) {
      sl = K.el('div', { class: 'kit-eq-label', 'data-kit': 'mirror', html: window.katex ? K.tex('S=\\mathrm{diag}(-1,-1,1)', false) : 'S = diag(−1, −1, 1)' }, o.parent || ctx.stage);
      sl.style.left = x + 'px'; sl.style.top = (y + H / 2 + 24) + 'px'; sl.style.color = fg; sl.style.zIndex = (o.z ?? 14) + 1;
    }
    const { t0, t1 } = K.times(ctx, o, 0), tr = ctx.at(o.reflect ?? (t0 + 1));
    return ctx.add({
      root: svg,
      render(t) {
        const e = K.env(t, t0, t1, 0.5, 0.3); K.show(svg, e.on); svg.style.opacity = e.o;
        const a = S.seg(t, t0, t0 + 0.6, S.ease.outCubic), r = S.seg(t, tr, tr + 0.8, S.ease.inOutCubic);
        parts.plane.forEach((p) => { p.style.opacity = a; });
        parts.src.forEach((p) => { p.style.opacity = S.seg(t, t0 + 0.3, t0 + 0.8, S.ease.linear); });
        parts.link.forEach((p) => { p.style.opacity = 0.9 * S.seg(t, tr - 0.1, tr + 0.3, S.ease.linear); });
        parts.img.forEach((p) => { p.style.opacity = r; });
        if (sl) { K.show(sl, e.on && t >= tr); sl.style.opacity = S.seg(t, tr + 0.4, tr + 0.8, S.ease.linear) * e.o; }
      },
    });
  };
})();
