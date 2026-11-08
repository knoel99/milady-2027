/* ch07_kit.js: helpers shared by the scenes of unit ch07 (load after the runtime components).
 * Labels and fades; the SHELVES device (two planks: 'true for every snapshot' / 'true only for the crowd', three slots
 * each, cards that land in slots; a 'full' centre-stage state and a dimmed 'strip' state at the top-left, labels never
 * below 28 px); the polarity balance bar; run strokes; point clouds revealed in a seeded order. Reusable by ch08/ch09
 * (reported for promotion). No physics number here. */
(function () {
  'use strict';
  const K = window.Kit, S = window.Scene;
  const C7 = (window.C7 = {});
  C7.lab = function (ctx, text, x, y, cls = '', o = {}) {
    const e = K.el('div', { class: 'c7-label ' + cls }, o.parent || ctx.stage);
    if (o.html) e.innerHTML = K.markup(text); else e.textContent = text;
    e.style.left = x + 'px'; e.style.top = y + 'px';
    if (o.z) e.style.zIndex = o.z;
    if (o.w) { e.style.whiteSpace = 'normal'; e.style.width = o.w + 'px'; e.style.lineHeight = '1.22'; }
    return e;
  };
  C7.fade = function (el, t, a, b = Infinity, d = 0.25, max = 1) {
    const p = S.seg(t, a, a + d, S.ease.linear) * (b === Infinity ? 1 : 1 - S.seg(t, b, b + d, S.ease.linear));
    el.style.opacity = (p * max).toFixed(3); el.style.display = p > 0 ? '' : 'none'; return p;
  };
  C7.fadeS = function (el, t, a, b = Infinity, d = 0.25, max = 1) {
    const p = S.seg(t, a, a + d, S.ease.linear) * (b === Infinity ? 1 : 1 - S.seg(t, b, b + d, S.ease.linear));
    el.setAttribute('opacity', (p * max).toFixed(3)); el.setAttribute('visibility', p > 0 ? 'visible' : 'hidden'); return p;
  };
  /** card glyphs drawn in a 120 x 160 card frame */
  const glyph = (g, kind) => {
    const ch = K.c('chalk');
    if (kind === 'mirror') {
      K.s('line', { x1: 30, y1: 110, x2: 90, y2: 50, stroke: K.c('fg-2'), 'stroke-width': 3, 'stroke-dasharray': '6 6' }, g);
      K.s('circle', { cx: 38, cy: 102, r: 9, fill: K.c('b-neg') }, g); K.s('circle', { cx: 82, cy: 58, r: 9, fill: K.c('b') }, g);
      K.s('circle', { cx: 60, cy: 80, r: 4, fill: ch }, g);
    } else if (kind === 'budget') {
      K.s('line', { x1: 60, y1: 40, x2: 60, y2: 112, stroke: ch, 'stroke-width': 4 }, g);
      K.s('line', { x1: 24, y1: 58, x2: 96, y2: 58, stroke: ch, 'stroke-width': 4 }, g);
      [24, 96].forEach((x) => K.s('path', { d: `M${x - 16},${78} Q${x},${98} ${x + 16},${78} Z`, fill: 'none', stroke: ch, 'stroke-width': 3 }, g));
      K.s('line', { x1: 40, y1: 114, x2: 80, y2: 114, stroke: ch, 'stroke-width': 4 }, g);
    }
  };
  /** the two shelves. o.full = {in, out} times to show the full state (centre stage) before shrinking to the strip;
   *  o.cards = [{shelf: 'every'|'crowd', slot, glyph, title, tag, at (landing time; omit = already there), from: [x, y]}];
   *  o.bright = [times] (strip at 100 % for 1.5 s); o.empty = [{shelf, slot, label, at}] lit dashed slots;
   *  o.big = time from which the strip grows to half size at the top centre (07.6 'tell'). Returns {render(t)}. */
  C7.shelves = function (ctx, o = {}) {
    const root = K.el('div', {}, ctx.stage); root.style.cssText = 'position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:22';
    const svg = K.svgLayer(ctx, 1, root);
    const F = { every: [200, 880], crowd: [1040, 1720], y: 560, lab: 300, fs: 44, card: 1 };
    const Sx = { every: [140, 680], crowd: [760, 1300], y: 150, lab: 156, fs: 28, card: 0.45 };
    const Bx = { every: [400, 900], crowd: [1020, 1520], y: 330, lab: 340, fs: 32, card: 0.85 };
    const planks = {}, labs = {}, slots = {};
    for (const sh of ['every', 'crowd']) {
      planks[sh] = K.s('line', { stroke: K.c('fg-2'), 'stroke-width': 6, 'stroke-linecap': 'round' }, svg);
      labs[sh] = K.el('div', { class: 'c7-shelf-lab' }, root, sh === 'every' ? 'true for every snapshot' : 'true only for the crowd');
      slots[sh] = [0, 1, 2].map(() => K.s('rect', { width: 120, height: 160, rx: 10, fill: 'none', stroke: K.c('fg-2'), 'stroke-width': 3, 'stroke-dasharray': '9 8' }, svg));
    }
    const icon = K.s('g', {}, svg);   // single card (chalk) and a stack (amber in full, grey in the strip) beside the labels
    const icon1 = K.s('rect', { width: 34, height: 46, rx: 4, fill: 'none', stroke: K.c('chalk'), 'stroke-width': 3 }, icon);
    const icon2 = [0, 1, 2].map(() => K.s('rect', { width: 34, height: 46, rx: 4, fill: K.c('panel'), 'stroke-width': 3 }, icon));
    const cards = (o.cards || []).map((c) => {
      const g = K.s('g', {}, svg);
      K.s('rect', { width: 120, height: 160, rx: 10, fill: K.c('panel'), stroke: K.c('fg-2'), 'stroke-width': 3 }, g);
      glyph(g, c.glyph);
      const tt = K.s('text', { x: 60, y: 148, 'text-anchor': 'middle', class: 'kt-label', style: 'font-size:34px' }, g, c.title || '');
      const tag = c.tag ? K.el('div', { class: 'c7-tag' }, root, c.tag) : null;
      return Object.assign({}, c, { g, tt, tag, t: c.at !== undefined ? ctx.at(c.at) : -Infinity });
    });
    const empties = (o.empty || []).map((e) => Object.assign({ t: ctx.at(e.at), lab: e.label ? K.el('div', { class: 'c7-tag' }, root, e.label) : null }, e));
    const tIn = o.full ? ctx.at(o.full.in) : -Infinity, tOut = o.full ? ctx.at(o.full.out) : -Infinity;
    const brights = (o.bright || []).map((b) => ctx.at(b)), tBig = o.big !== undefined ? ctx.at(o.big) : Infinity;
    const lerp = (a, b, u) => a + (b - a) * u;
    const R = {
      root, cards,
      slotXY(L, sh, i) { const [x0, x1] = L[sh], w = (x1 - x0) / 3; return [x0 + w * (i + 0.5) - 60 * L.card, L.y - 160 * L.card]; },
      render(t) {
        const u = o.full ? S.seg(t, tOut, tOut + 1.4, S.ease.inOutCubic) : 1;   // 0 full → 1 strip
        const big = tBig === Infinity ? 0 : S.seg(t, tBig, tBig + 1.0, S.ease.inOutCubic);
        const L = {}; for (const k of ['y', 'lab', 'fs', 'card']) L[k] = lerp(lerp(F[k], Sx[k], u), Bx[k], big);
        for (const sh of ['every', 'crowd']) L[sh] = [0, 1].map((i) => lerp(lerp(F[sh][i], Sx[sh][i], u), Bx[sh][i], big));
        let op = o.full ? S.seg(t, tIn, tIn + 0.4, S.ease.linear) : 1;
        let br = 0; for (const b of brights) br = Math.max(br, S.seg(t, b, b + 0.3, S.ease.linear) * (1 - S.seg(t, b + 1.5, b + 1.9, S.ease.linear)));
        const dim = (1 - u) + u * Math.max(0.6, br, big);
        root.style.opacity = (op * dim).toFixed(3); root.style.display = op > 0 ? '' : 'none';
        const draw = o.full ? S.seg(t, tIn, tIn + 0.6, S.ease.inOutSine) : 1;
        for (const sh of ['every', 'crowd']) {
          const [x0, x1] = L[sh];
          planks[sh].setAttribute('x1', x0); planks[sh].setAttribute('x2', x0 + (x1 - x0) * draw); planks[sh].setAttribute('y1', L.y); planks[sh].setAttribute('y2', L.y);
          const lb = labs[sh]; lb.style.fontSize = L.fs.toFixed(1) + 'px'; lb.style.left = (x0 + (sh === 'crowd' ? 0 : 0)) + 'px';
          lb.style.top = (u > 0.5 || big > 0 ? L.y + 8 : L.lab) + 'px';
          const la = o.labAt ? S.seg(t, ctx.at(o.labAt[sh]), ctx.at(o.labAt[sh]) + 0.3, S.ease.linear) : 1; lb.style.opacity = la; lb.style.display = la > 0 ? '' : 'none';
          const sa = o.slotsAt ? S.seg(t, ctx.at(o.slotsAt), ctx.at(o.slotsAt) + 0.2, S.ease.linear) : 1;
          slots[sh].forEach((r, i) => { const [x, y] = R.slotXY(L, sh, i); r.setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${L.card.toFixed(3)})`); r.setAttribute('opacity', sa); });
        }
        // icons beside the labels in the full state only
        const ia = (1 - u) * (o.labAt ? S.seg(t, ctx.at(o.labAt.every), ctx.at(o.labAt.every) + 0.3, S.ease.linear) : 1);
        const ib = (1 - u) * (o.labAt ? S.seg(t, ctx.at(o.labAt.crowd), ctx.at(o.labAt.crowd) + 0.3, S.ease.linear) : 1);
        icon1.setAttribute('x', F.every[0] - 4); icon1.setAttribute('y', F.lab - 62); icon1.setAttribute('opacity', ia);
        icon2.forEach((r, i) => { r.setAttribute('x', F.crowd[0] + i * 10 - 4); r.setAttribute('y', F.lab - 62 - i * 8); r.setAttribute('stroke', K.c('metric')); r.setAttribute('opacity', ib); });
        for (const e of empties) {
          const on = S.seg(t, e.t, e.t + 0.3, S.ease.linear), r = slots[e.shelf][e.slot];
          r.setAttribute('stroke', on > 0 ? K.c('chalk') : K.c('fg-2'));
          if (e.lab) { const [x, y] = R.slotXY(L, e.shelf, e.slot); e.lab.style.left = (x + 60 * L.card) + 'px'; e.lab.style.top = (L.y + 46) + 'px'; e.lab.style.opacity = on; e.lab.style.display = on > 0 ? '' : 'none'; }
        }
        for (const c of cards) {
          const [sx, sy] = R.slotXY(L, c.shelf, c.slot);
          let x = sx, y = sy, sc = L.card, a = 1;
          if (c.hover !== undefined) {   // a card lifted out over the other shelf (07.5)
            const h0 = ctx.at(c.hover[0]), h1 = ctx.at(c.hover[1]), up = S.seg(t, h0, h0 + 0.6, S.ease.inOutCubic) * (1 - S.seg(t, h1, h1 + 0.8, S.ease.inOutCubic));
            const [hx, hy] = R.slotXY(L, c.hover[2], 1); x = sx + (hx - sx) * up; y = sy + (hy - 40 - sy) * up;
          }
          if (c.t > -Infinity) {
            const p = S.seg(t, c.t, c.t + 1.0, S.ease.inOutCubic); a = c.t <= t ? 1 : 0;
            if (c.from) { x = c.from[0] + (x - c.from[0]) * p; y = c.from[1] + (y - c.from[1]) * p; sc = 1 + (sc - 1) * p; }
          }
          c.g.setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${sc.toFixed(3)})`); c.g.setAttribute('opacity', a);
          c.tt.setAttribute('opacity', sc >= 0.82 ? 1 : 0);
          if (c.tag) { const on = a * (u < 1 || br > 0 || big > 0 ? 1 : 0); c.tag.style.left = (x + 60 * sc) + 'px'; c.tag.style.top = (L.y + 46 + (c.slot % 2) * 34) + 'px'; c.tag.style.opacity = on; c.tag.style.display = on > 0 ? '' : 'none'; }
        }
      },
    };
    return ctx.add(R);
  };
  /** polarity balance: a bar split at p (left pan --b-neg 'D < 0', right pan --b 'D > 0'), a chalk tick at one half
   *  and a thin beam above that tilts with p − ½. Returns {g, set(p)} */
  C7.balance = function (parent, b, o = {}) {
    const g = K.s('g', {}, parent), w = b.x1 - b.x0, h = b.y1 - b.y0;
    const L = K.s('rect', { x: b.x0, y: b.y0, height: h, fill: K.c('b-neg') }, g), R = K.s('rect', { y: b.y0, height: h, fill: K.c('b') }, g);
    K.s('line', { x1: b.x0 + w / 2, x2: b.x0 + w / 2, y1: b.y0 - 8, y2: b.y1 + 8, stroke: K.c('chalk'), 'stroke-width': 3 }, g);
    const beam = K.s('line', { stroke: K.c('chalk'), 'stroke-width': 3, 'stroke-linecap': 'round' }, g);
    if (o.labels !== false) {
      const t1 = K.s('text', { x: b.x0 + 10, y: b.y1 - (h - 20) / 2, class: 'kt-label', style: 'font-size:28px' }, g, 'D < 0');
      const t2 = K.s('text', { x: b.x1 - 10, y: b.y1 - (h - 20) / 2, 'text-anchor': 'end', class: 'kt-label', style: 'font-size:28px' }, g, 'D > 0');
      [t1, t2].forEach((e) => { e.style.fill = K.c('fg'); e.setAttribute('data-qa', 'over-ok'); });
    }
    return { g, set(p) {
      const xs = b.x0 + w * (1 - p);
      L.setAttribute('width', Math.max(0, xs - b.x0).toFixed(1)); R.setAttribute('x', xs.toFixed(1)); R.setAttribute('width', Math.max(0, b.x1 - xs).toFixed(1));
      const a = (p - 0.5) * 0.9, cx = b.x0 + w / 2, cy = b.y0 - 18, hw = w / 2 - 10;
      beam.setAttribute('x1', (cx - hw * Math.cos(a)).toFixed(1)); beam.setAttribute('y1', (cy + hw * Math.sin(a)).toFixed(1));
      beam.setAttribute('x2', (cx + hw * Math.cos(a)).toFixed(1)); beam.setAttribute('y2', (cy - hw * Math.sin(a)).toFixed(1));
    } };
  };
  /** a (Q, D) panel: axes through 0 and two labels; returns {X, Y, b} for a box b and ranges */
  C7.panel = function (ctx, parent, b, rq, rd, o = {}) {
    const X = (q) => b.x0 + (q - rq[0]) / (rq[1] - rq[0]) * (b.x1 - b.x0), Y = (d) => b.y1 - (d - rd[0]) / (rd[1] - rd[0]) * (b.y1 - b.y0);
    const g = K.s('g', {}, parent);
    K.s('line', { x1: b.x0, x2: b.x1, y1: Y(0), y2: Y(0), stroke: K.c('grid'), 'stroke-width': 2 }, g);
    K.s('line', { x1: X(0), x2: X(0), y1: b.y0, y2: b.y1, stroke: K.c('grid'), 'stroke-width': 2 }, g);
    if (o.labels !== false) {
      const q = K.s('text', { x: b.x1 - 6, y: Y(0) + 34, 'text-anchor': 'end', class: 'kt-label', style: 'font-size:28px' }, g, 'Q, quadrupole'); q.style.fill = K.c('b-light');
      const d = K.s('text', { x: X(0) - 12, y: b.y0 + 26, 'text-anchor': 'end', class: 'kt-label', style: 'font-size:28px' }, g, 'D, dipole'); d.style.fill = K.c('b');
    }
    return { g, X, Y, b };
  };
  /** draw the first k points (seeded order) of a packed (Q, D, V) array on a canvas context */
  C7.cloud = function (g, XS, n, k, P, col, alpha, px = 2, only = null) {
    g.fillStyle = col; g.globalAlpha = alpha;
    for (let j = 0; j < k; j++) { const i = only ? only[j] : j; if (i >= n) continue; g.fillRect(P.X(XS[3 * i]) - px / 2, P.Y(XS[3 * i + 1]) - px / 2, px, px); }
  };
})();
