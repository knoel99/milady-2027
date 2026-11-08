/* field.js: Canvas helpers for fields (deterministic, fixed-step).
 *
 *   Kit.cmap(kind, v)            v in [−1, 1] → [r, g, b]; kind 'u' | 'b' (silver → bg → hue, styles §3.2),
 *                                'metric' | 'model' (bg → hue, v in [0, 1])
 *   Kit.fieldMap(ctx, {grid, nx, ny, x, y, w, h, kind, vmax, at, dur, frame, label, generated})
 *                                scalar map (ω, j, ψ, a…) from a Float32Array (row-major, ny rows of nx);
 *                                key colour map, symmetric range ±vmax; violet frame when generated
 *   Kit.streamlines(F, seeds, {h, n, box})   → polylines (precompute in setup); F(x, y) → [vx, vy] in px
 *   Kit.fieldLines(ctx, {lines | F + seeds, color, width, at, dur, alpha, z})   drawn on by progress
 *   Kit.arrows(ctx, {F, box, nx, ny, scale, color, at})                         vector arrows on a grid
 *   Kit.tracers(ctx, {F, n, box, color, at, trail, dt, seed, size})            particles advected by F
 * All drawing is in stage px. F must be a pure function (no randomness, no time unless passed in).
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit;

  K.cmap = function (kind, v) {
    const bg = K.hex(K.c('bg'));
    const hue = K.hex(K.c({ u: 'u-hi', b: 'b-hi', metric: 'metric', model: 'model', param: 'param' }[kind] || 'fg'));
    const neg = K.hex(K.c('silver'));
    const a = Math.min(1, Math.abs(v)), to = v >= 0 ? hue : neg;
    return [bg[0] + (to[0] - bg[0]) * a, bg[1] + (to[1] - bg[1]) * a, bg[2] + (to[2] - bg[2]) * a];
  };

  /** draw a scalar grid into g at (x, y, w, h), smooth upscaling */
  K.drawGrid = function (g, grid, nx, ny, o) {
    const off = document.createElement('canvas'); off.width = nx; off.height = ny;
    const og = off.getContext('2d'), im = og.createImageData(nx, ny);
    let vmax = o.vmax; if (!vmax) { vmax = 1e-30; for (let i = 0; i < grid.length; i++) vmax = Math.max(vmax, Math.abs(grid[i])); }
    const gamma = o.gamma ?? 0.85;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const v = grid[j * nx + i] / vmax, s = Math.sign(v) * Math.pow(Math.min(1, Math.abs(v)), gamma);
      const c = K.cmap(o.kind || 'b', o.kind === 'metric' || o.kind === 'model' ? Math.abs(s) : s), q = 4 * ((o.flipY ? ny - 1 - j : j) * nx + i);
      im.data[q] = c[0]; im.data[q + 1] = c[1]; im.data[q + 2] = c[2]; im.data[q + 3] = 255;
    }
    og.putImageData(im, 0, 0);
    g.save(); g.imageSmoothingEnabled = o.smooth !== false; g.imageSmoothingQuality = 'high';
    g.drawImage(off, o.x, o.y, o.w, o.h); g.restore();
    return vmax;
  };

  K.fieldMap = function (ctx, o = {}) {
    const grid = S.f32(o.grid), shape = grid.shape || [o.ny, o.nx];
    const ny = o.ny || shape[0], nx = o.nx || shape[1];
    if (!nx || !ny || nx * ny !== grid.length) throw new Error('fieldMap: grid size does not match nx*ny');
    const box = { x: o.x ?? 360, y: o.y ?? 160, w: o.w ?? 640, h: o.h ?? 640 };
    const pad = 8;
    const L = K.canvasLayer(ctx, o.z ?? 8, { x: box.x - pad, y: box.y - pad, w: box.w + 2 * pad, h: box.h + 2 * pad }, o.parent);
    L.canvas.setAttribute('data-kit', 'field-map');
    const vmax = K.drawGrid(L.g, grid, nx, ny, { x: pad, y: pad, w: box.w, h: box.h, kind: o.kind || 'b', vmax: o.vmax, flipY: o.flipY, gamma: o.gamma, smooth: o.smooth });
    L.g.lineWidth = o.generated ? 4 : 2;
    L.g.strokeStyle = o.generated ? K.c('model') : K.c('matter');
    if (o.generated) L.g.setLineDash([]);
    L.g.strokeRect(pad - 1, pad - 1, box.w + 2, box.h + 2);
    const t0 = ctx.at(o.at ?? 0), dur = o.dur ?? 0.6, t1 = o.out !== undefined ? ctx.at(o.out) : Infinity;
    let lab = null;
    if (o.label) {
      lab = K.el('div', { class: 'mono', 'data-kit': 'field-map' }, o.parent || ctx.stage, K.upper(o.label));
      lab.style.cssText += `;position:absolute;left:${box.x}px;top:${box.y + box.h + 16}px;width:${box.w}px;text-align:center;color:${o.generated ? K.c('model') : K.c('muted')};z-index:${(o.z ?? 8) + 1}`;
    }
    return ctx.add({
      canvas: L.canvas, vmax, box,
      render(t) {
        const e = K.env(t, t0, t1, dur, 0.3, S.ease.inOutSine);
        L.canvas.style.opacity = e.o; K.show(L.canvas, e.on);
        if (lab) { lab.style.opacity = e.o; K.show(lab, e.on); }
      },
    });
  };

  /** RK4 streamlines from seed points, both directions unless o.forward */
  K.streamlines = function (F, seeds, o = {}) {
    const h = o.h ?? 4, n = o.n ?? 300, box = o.box || { x: 0, y: 0, w: 1920, h: 1080 };
    const inside = (p) => p[0] >= box.x && p[0] <= box.x + box.w && p[1] >= box.y && p[1] <= box.y + box.h;
    const unit = (x, y, sgn) => { const v = F(x, y); const m = Math.hypot(v[0], v[1]) || 1e-12; return [sgn * v[0] / m, sgn * v[1] / m]; };
    const trace = (p, sgn) => {
      const pts = [p.slice()]; let [x, y] = p;
      for (let i = 0; i < n; i++) {
        const k1 = unit(x, y, sgn), k2 = unit(x + h * k1[0] / 2, y + h * k1[1] / 2, sgn), k3 = unit(x + h * k2[0] / 2, y + h * k2[1] / 2, sgn), k4 = unit(x + h * k3[0], y + h * k3[1], sgn);
        x += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6; y += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6;
        if (!inside([x, y])) break;
        pts.push([x, y]);
        if (o.closeTol && i > 20 && Math.hypot(x - p[0], y - p[1]) < o.closeTol) { pts.push(p.slice()); break; }
      }
      return pts;
    };
    return seeds.map((s) => (o.forward ? trace(s, 1) : trace(s, -1).reverse().concat(trace(s, 1).slice(1))));
  };

  /** polyline drawing helper: draws the first fraction p of each line (by point count) */
  K.drawLines = function (g, lines, o = {}) {
    g.save(); g.strokeStyle = K.c(o.color || 'b'); g.lineWidth = o.width ?? 3; g.lineCap = 'round'; g.lineJoin = 'round';
    g.globalAlpha = o.alpha ?? 1;
    const p = o.progress ?? 1;
    for (const L of lines) {
      const m = Math.max(2, Math.floor(L.length * p)); if (p <= 0 || L.length < 2) continue;
      g.beginPath(); g.moveTo(L[0][0], L[0][1]);
      for (let i = 1; i < Math.min(m, L.length); i++) g.lineTo(L[i][0], L[i][1]);
      g.stroke();
    }
    g.restore();
  };

  K.fieldLines = function (ctx, o = {}) {
    const lines = o.lines || K.streamlines(o.F, o.seeds, o);
    const L = K.canvasLayer(ctx, o.z ?? 6, null, o.parent); L.canvas.setAttribute('data-kit', 'field-lines');
    const t0 = ctx.at(o.at ?? 0), dur = o.dur ?? 1.5, t1 = o.out !== undefined ? ctx.at(o.out) : Infinity;
    return ctx.add({
      lines, canvas: L.canvas,
      render(t) {
        const e = K.env(t, t0, t1, 0.2, 0.4);
        K.show(L.canvas, e.on); if (!e.on) return;
        L.g.clearRect(0, 0, 1920, 1080);
        K.drawLines(L.g, lines, { color: o.color || 'b', width: o.width, alpha: (o.alpha ?? 0.9) * e.o, progress: S.seg(t, t0, t0 + dur, S.ease.inOutSine) });
      },
    });
  };

  K.arrows = function (ctx, o = {}) {
    const box = o.box || { x: 360, y: 160, w: 1200, h: 640 }, nx = o.nx || 16, ny = o.ny || 9;
    const L = K.canvasLayer(ctx, o.z ?? 7, null, o.parent); L.canvas.setAttribute('data-kit', 'arrows');
    const t0 = ctx.at(o.at ?? 0), t1 = o.out !== undefined ? ctx.at(o.out) : Infinity;
    const pts = [];
    let vmax = 1e-12;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const x = box.x + (i + 0.5) * box.w / nx, y = box.y + (j + 0.5) * box.h / ny, v = o.F(x, y);
      vmax = Math.max(vmax, Math.hypot(v[0], v[1])); pts.push([x, y, v[0], v[1]]);
    }
    const cell = Math.min(box.w / nx, box.h / ny), sc = (o.scale ?? 0.8) * cell / vmax;
    return ctx.add({
      canvas: L.canvas,
      render(t) {
        const e = K.env(t, t0, t1, 0.5, 0.3); K.show(L.canvas, e.on); if (!e.on) return;
        const g = L.g; g.clearRect(0, 0, 1920, 1080); g.save(); g.strokeStyle = g.fillStyle = K.c(o.color || 'u'); g.globalAlpha = e.o; g.lineWidth = o.width ?? 3;
        for (const [x, y, vx, vy] of pts) {
          const ex = x + vx * sc * e.p, ey = y + vy * sc * e.p, a = Math.atan2(vy, vx), m = Math.hypot(vx, vy) * sc * e.p;
          if (m < 4) continue;
          g.beginPath(); g.moveTo(x, y); g.lineTo(ex, ey); g.stroke();
          const hl = Math.min(14, m * 0.4);
          g.beginPath(); g.moveTo(ex, ey); g.lineTo(ex - hl * Math.cos(a - 0.45), ey - hl * Math.sin(a - 0.45)); g.lineTo(ex - hl * Math.cos(a + 0.45), ey - hl * Math.sin(a + 0.45)); g.closePath(); g.fill();
        }
        g.restore();
      },
    });
  };

  /** tracer particles advected by F (px/s) with a fixed-step RK2 integrator through Scene.stepper */
  K.tracers = function (ctx, o = {}) {
    const box = o.box || { x: 0, y: 0, w: 1920, h: 1080 }, n = o.n ?? 600, trail = o.trail ?? 10, dt = o.dt ?? 1 / 60;
    const init = () => {   // a fresh seeded stream on every (re)initialisation: backward seeks replay exactly
      const x = new Float32Array(n), y = new Float32Array(n), hx = new Float32Array(n * trail), hy = new Float32Array(n * trail);
      const r = S.rng(o.seed ?? 'tracers');
      for (let i = 0; i < n; i++) { x[i] = box.x + r() * box.w; y[i] = box.y + r() * box.h; for (let k = 0; k < trail; k++) { hx[i * trail + k] = x[i]; hy[i * trail + k] = y[i]; } }
      return { x, y, hx, hy, k: 0 };
    };
    const wrap = (v, a, w) => (v < a ? v + w : v >= a + w ? v - w : v);
    const step = (s) => {
      for (let i = 0; i < n; i++) {
        const v1 = o.F(s.x[i], s.y[i]), xm = s.x[i] + 0.5 * dt * v1[0], ym = s.y[i] + 0.5 * dt * v1[1], v2 = o.F(xm, ym);
        let nx = s.x[i] + dt * v2[0], ny = s.y[i] + dt * v2[1];
        const jumped = nx < box.x || nx >= box.x + box.w || ny < box.y || ny >= box.y + box.h;
        nx = wrap(nx, box.x, box.w); ny = wrap(ny, box.y, box.h);
        s.x[i] = nx; s.y[i] = ny;
        if (jumped) for (let k = 0; k < trail; k++) { s.hx[i * trail + k] = nx; s.hy[i * trail + k] = ny; }
      }
      s.k = (s.k + 1) % trail;
      for (let i = 0; i < n; i++) { s.hx[i * trail + s.k] = s.x[i]; s.hy[i * trail + s.k] = s.y[i]; }
      return s;
    };
    const at = S.stepper(init, step, dt);
    const L = K.canvasLayer(ctx, o.z ?? 6, null, o.parent); L.canvas.setAttribute('data-kit', 'tracers');
    const t0 = ctx.at(o.at ?? 0), t1 = o.out !== undefined ? ctx.at(o.out) : Infinity;
    return ctx.add({
      canvas: L.canvas, state: at,
      render(t) {
        const e = K.env(t, t0, t1, 0.6, 0.4, S.ease.inOutSine); K.show(L.canvas, e.on); if (!e.on) return;
        const s = at(Math.max(0, t - t0) + (o.warmup ?? 0)), g = L.g;
        g.clearRect(0, 0, 1920, 1080); g.save(); g.strokeStyle = K.c(o.color || 'u'); g.lineWidth = o.size ?? 2.2; g.lineCap = 'round';
        g.globalAlpha = (o.alpha ?? 0.85) * e.o;
        g.beginPath();
        for (let i = 0; i < n; i++) {
          let k = (s.k + 1) % trail; g.moveTo(s.hx[i * trail + k], s.hy[i * trail + k]);
          for (let m = 1; m < trail; m++) { k = (k + 1) % trail; g.lineTo(s.hx[i * trail + k], s.hy[i * trail + k]); }
        }
        g.stroke(); g.restore();
      },
    });
  };
})();
