/* chSOA1_kit.js: helpers shared by the scenes of unit chSOA1 (C2 helpers copied from ch02, and SOA.map, the shared map). Pure builders, no timing. */
(function () {
  'use strict';
  const K = window.Kit, S = window.Scene, TAU = Math.PI * 2;
  const C2 = {};
  /** dipole field lines r = L sin^2(theta) around (cx, cy), tilted by tiltDeg, cut inside rMin; ordered south -> north
   *  outside the source (the direction of the field of a north-up dipole) */
  C2.dipoleLines = function (cx, cy, Ls, tiltDeg = 0, rMin = 0, n = 180) {
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
  C2.heads = function (g, lines, o = {}) {
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
  C2.earth = function (parent, o) {
    const g = K.s('g', { transform: `translate(${o.x} ${o.y})` }, parent), R = o.r;
    K.s('circle', { r: R, fill: K.c('matter-dark'), stroke: K.c('matter'), 'stroke-width': 3 }, g);
    const outer = K.s('circle', { r: R * 0.55, fill: K.c('matter') }, g);
    K.s('circle', { r: R * 0.25, fill: K.c('fg-2'), stroke: K.c('fg'), 'stroke-width': 2 }, g);
    return { g, outer, R };
  };
  /** a closed-form "churn" of particles inside a ring rIn..rOut (pure function of t; seeded) */
  C2.churn = function (n, rIn, rOut, seed) {
    const r = S.rng(seed), P = [];
    for (let i = 0; i < n; i++) P.push({ r0: rIn + (rOut - rIn) * r(), th: TAU * r(), w: 0.25 + 0.35 * r(), k: 3 + Math.floor(4 * r()), ph: TAU * r(), shade: r() });
    return function at(t, i) { const p = P[i], th = p.th + p.w * t * (p.shade > 0.5 ? 1 : -0.7);
      const rr = Math.min(rOut - 2, Math.max(rIn + 2, p.r0 + 0.18 * (rOut - rIn) * Math.sin(p.k * th + 0.8 * t + p.ph)));
      return [rr * Math.cos(th), rr * Math.sin(th), p.shade]; };
  };
  C2.label = function (st, txt, x, y, cls = '') { const e = K.el('div', { class: 's1-label ' + cls, html: K.markup(txt) }, st); e.style.left = x + 'px'; e.style.top = y + 'px'; return e; };
  C2.fadeEl = function (el, t, a, b, d = 0.25) { const o = S.seg(t, a, a + d, S.ease.linear) * (b === undefined || b === null ? 1 : 1 - S.seg(t, b, b + d, S.ease.linear)); el.style.opacity = o.toFixed(3); K.show(el, o > 0); return o; };
  C2.chipOf = function (ctx, re, fb) { const ch = (ctx.script.onscreen && ctx.script.onscreen.chips) || []; return ch.find((c) => re.test(c)) || fb; };
  C2.labOf = function (ctx, re, fb) { const ch = (ctx.script.onscreen && ctx.script.onscreen.labels) || []; return ch.find((c) => (typeof re === 'string' ? c === re : re.test(c))) || fb; };
  C2.refL2 = (chip) => chip.split('·').slice(1).map((x) => x.trim()).join(' · ');
  window.C2 = C2;
})();
/* SOA.map(ctx, o): the shared map of chSOA1 (data: window.SOA_MAP from map.js).
   o = { scene: 'SOA1.k', add: [{id, cue}], present: [ids], lit: [[laneId, from, to]], flips: {id: [time]}, activeFor: {id: s},
         dataLane: false | true | {at}, place: {id: 'ru'|'rd'|'lu'|'ld'}, dim: [[laneIds, from, to, opacity]] } */
(function () {
  'use strict';
  const K = window.Kit, S = window.Scene;
  const SOA = {};
  SOA.map = function (ctx, o) {
    const D = window.SOA_MAP, M = D.map, st = ctx.stage, cat = {}; D.catalog.forEach((p) => { cat[p.id] = p; });
    const segs = M.axis.segments;
    const xOf = (y) => { for (const s of segs) if (y <= s.to) return s.x0 + (s.x1 - s.x0) * (Math.max(y, s.from) - s.from) / (s.to - s.from); const s = segs[segs.length - 1]; return s.x1; };
    const lanes = {}; M.lanes.forEach((L) => { lanes[L.id] = L; });
    const AY = M.axis.y, LB = Math.max(...M.lanes.map((L) => L.y1)), nowX = xOf(M.axis.now.year);
    const svg = K.svgLayer(ctx, 10), g = K.s('g', {}, svg);
    const tRev = o.at !== undefined ? ctx.at(o.at) : null;   // optional draw-on of the whole map (SOA1.1)
    let revRect = null; if (tRev !== null) { const cid = 'soarev'; revRect = K.s('rect', { x: 0, y: 0, width: 0, height: 1080 }, K.s('clipPath', { id: cid }, K.s('defs', {}, svg))); g.setAttribute('clip-path', `url(#${cid})`); }
    const muted = K.c('muted'), chalk = K.c('chalk');
    // axis
    const ax = K.s('g', {}, g);
    segs.forEach((s) => K.s('line', { x1: s.x0, x2: s.x1, y1: AY, y2: AY, stroke: K.c('fg-2'), 'stroke-width': 2, 'stroke-dasharray': s.dashed ? '8 8' : '' }, ax));
    M.axis.ticks.forEach((y) => { const x = xOf(y); K.s('line', { x1: x, x2: x, y1: AY - 8, y2: AY + 8, stroke: muted, 'stroke-width': 2 }, ax);
      K.s('text', { x, y: AY - 18, 'text-anchor': 'middle', class: 'kt-mono' }, ax, String(y)); });
    const now = K.s('line', { x1: nowX, x2: nowX, y1: AY, y2: LB, stroke: K.c('fg-2'), 'stroke-width': 2 }, g);
    const nowL = K.s('text', { x: nowX - 10, y: AY + 36, 'text-anchor': 'end', class: 'kt-mono' }, g, M.axis.now.label); nowL.style.fill = K.c('fg-2');
    // lanes
    const sep = K.s('g', {}, g), laneEls = {};
    M.lanes.forEach((L, i) => {
      const x0 = L.from_year ? xOf(L.from_year) : M.axis.x0;
      const top = K.s('line', { x1: x0, x2: M.axis.x1, y1: L.y0, y2: L.y0, stroke: K.c('grid'), 'stroke-width': 2, 'stroke-dasharray': L.dashed ? '8 8' : '' }, sep);
      const bot = (i === M.lanes.length - 1 || L.dashed) ? K.s('line', { x1: x0, x2: M.axis.x1, y1: L.y1, y2: L.y1, stroke: K.c('grid'), 'stroke-width': 2, 'stroke-dasharray': L.dashed ? '8 8' : '' }, sep) : null;
      const lab = K.el('div', {}, st, L.label); Object.assign(lab.style, { position: 'absolute', right: (1920 - M.gutter.label_x) + 'px', top: ((L.y0 + L.y1) / 2 - 20) + 'px', font: '600 28px Inter', color: 'var(--muted)', whiteSpace: 'nowrap', zIndex: 32 });
      laneEls[L.id] = { top, bot, lab, L };
    });
    const laneY = (id) => (lanes[id].y0 + lanes[id].y1) / 2;
    // pins
    const addT = {}; (o.add || []).forEach((a) => { addT[a.id] = ctx.at(a.cue) - 0.15; });
    const ids = [...(o.present || []), ...(o.add || []).map((a) => a.id)];
    const order = D.order, si = order.indexOf(o.scene), prevKeep = si > 0 ? (D.keep_named[order[si - 1]] || []) : [], keep = D.keep_named[o.scene] || [];
    const addList = (o.add || []).map((a) => ({ id: a.id, t: addT[a.id] })).sort((a, b) => a.t - b.t);
    const pins = {}, obst = [];
    const meas = (txt, font) => { const e = K.el('span', {}, st, txt); Object.assign(e.style, { position: 'absolute', font, whiteSpace: 'nowrap', visibility: 'hidden' }); const w = e.getBoundingClientRect().width; e.remove(); return w; };
    ids.forEach((id) => {
      const p = cat[id]; if (!p) { S.warn('SOA.map: unknown pin ' + id); return; }
      const x = xOf(p.year) + (id === 'L1999K' ? 18 : 0), y = laneY(p.lane), col = p.tint === 'model' ? K.c('model') : chalk;
      const pg = K.s('g', { transform: `translate(${x} ${y})` }, g), gl = K.s('g', {}, pg);
      if (p.glyph === 'dot') K.s('circle', { r: 9, fill: col }, gl);
      if (p.glyph === 'ring') K.s('circle', { r: 11, fill: K.c('bg'), stroke: col, 'stroke-width': 3 }, gl);
      if (p.glyph === 'diamond') K.s('path', { d: 'M0,-12 L12,0 L0,12 L-12,0 Z', fill: col }, gl);
      if (p.glyph === 'cross') K.s('path', { d: 'M-9,-9 L9,9 M9,-9 L-9,9', stroke: col, 'stroke-width': 4, 'stroke-linecap': 'round' }, gl);
      if (p.glyph === 'dashed_ring') K.s('circle', { r: 14, fill: 'none', stroke: col, 'stroke-width': 3, 'stroke-dasharray': '5 5' }, gl);
      let fl = null; if (p.flip) { fl = K.s('g', { transform: 'translate(0 -28)' }, pg); K.s('path', { d: 'M0,-12 V12 M-6,-6 L0,-12 L6,-6 M-6,6 L0,12 L6,6', fill: 'none', stroke: K.c('b'), 'stroke-width': 3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, fl); }
      if (p.tick) K.s('path', { d: 'M12,-20 L17,-14 L27,-27', fill: 'none', stroke: K.c('param'), 'stroke-width': 3.5, 'stroke-linecap': 'round' }, pg);
      const yl = K.s('text', { x, y: y + 42, 'text-anchor': 'middle', class: 'kt-mono' }, g, p.year_label);
      const dupYear = x > nowX - 40 || ids.some((q) => q !== id && cat[q] && cat[q].lane === p.lane && ids.indexOf(q) < ids.indexOf(id) && Math.abs(xOf(cat[q].year) - xOf(p.year)) < 72);   // a year label that would touch an earlier one
      obst.push({ id, x: x - 30, y: y + 16, w: 60, h: 32 }, { id, x: x - 14, y: y - (p.flip ? 42 : 14), w: 28, h: p.flip ? 56 : 28 });
      const w1 = meas(p.line1, '500 28px Inter'), w2 = meas(p.line2, '500 28px "JetBrains Mono"');
      pins[id] = { p, x, y, pg, gl, fl, yl, dupYear, w1, w2, col };
    });
    // states
    const tEnd = ctx.duration;
    addList.forEach((a, i) => { const nx = addList.slice(i + 1).find((b) => b.t > a.t + 0.01); pins[a.id].tIn = a.t;
      pins[a.id].tAct = (o.activeFor && o.activeFor[a.id] !== undefined) ? a.t + o.activeFor[a.id] : (nx ? Math.max(a.t + 2.5, nx.t) : tEnd); });
    // placement. Active callouts (two lines, centred on the pin) and named labels (one line, in the lane's top or
    // bottom row) are placed separately; an active callout hides the named labels it covers while it shows.
    const hit = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
    const okX = (b) => b.x >= 440 && b.x + b.w <= 1824 && !(b.x < nowX && b.x + b.w > nowX);
    const mkBox = (q, b, two) => { const box = K.el('div', {}, st); Object.assign(box.style, { position: 'absolute', left: b.x + 'px', top: b.y + 'px', padding: '2px 10px', background: 'var(--panel)', borderRadius: '6px', zIndex: 33, whiteSpace: 'nowrap' });
      const l1 = K.el('div', {}, box, q.p.line1); Object.assign(l1.style, { font: '500 28px Inter', color: q.p.tint === 'model' ? 'var(--model)' : two ? 'var(--fg)' : 'var(--fg-2)' });
      if (two) { const l2 = K.el('div', {}, box, q.p.line2); Object.assign(l2.style, { font: '500 28px "JetBrains Mono"', color: 'var(--muted)', letterSpacing: '.02em' }); }
      return box; };
    const namedIds = ids.filter((id) => pins[id] && (keep.includes(id) || (pins[id].tIn === undefined && prevKeep.includes(id))));
    // two passes: a named pin's year label is hidden, but only if that pin gets its named label (pass 2 knows)
    let okSet = new Set(namedIds);
    for (let pass = 0; pass < 2; pass++) {
      const placedN = [], got = new Set();
      obst.forEach((ob, i) => { ob.skipN = i % 2 === 0 && okSet.has(ob.id); });
      namedIds.forEach((id) => { if (pins[id].nbox && pins[id].nbox.el) pins[id].nbox.el.remove(); delete pins[id].nbox; });
    namedIds.sort((a, b) => (pins[a].tIn ?? -1) - (pins[b].tIn ?? -1)).forEach((id) => {
      const q = pins[id], L = lanes[q.p.lane], w = q.w1 + 24, h = 40, pref = (o.placeNamed && o.placeNamed[id]) ? [o.placeNamed[id]] : [];
      const C = { ru: { x: q.x + 20, y: L.y0 + 2, w, h }, rd: { x: q.x + 20, y: L.y1 - h - 2, w, h }, lu: { x: q.x - 20 - w, y: L.y0 + 2, w, h }, ld: { x: q.x - 20 - w, y: L.y1 - h - 2, w, h }, lf: { x: Math.min(q.x - 20, nowX - 8) - w, y: L.y0 + 2, w, h }, lfd: { x: Math.min(q.x - 20, nowX - 8) - w, y: L.y1 - h - 2, w, h },
        lb: { x: Math.min(q.x - 20, nowX - 8) - w, y: L.y1 + 2, w, h }, rb: { x: q.x + 20, y: L.y1 + 2, w, h }, la: { x: Math.min(q.x - 20, nowX - 8) - w, y: L.y0 - h - 2, w, h } };
      const k = [...pref, 'ru', 'rd', 'lu', 'ld', 'lf', 'lfd', 'lb', 'rb', 'la'].find((kk) => okX(C[kk]) && C[kk].y + C[kk].h <= 880 && C[kk].y >= AY + 6 && !placedN.some((pb) => hit(pb, C[kk])) && !obst.some((ob) => ob.id !== id && !ob.skipN && hit(ob, C[kk])));
      if (!k) { if (pass === 1) S.warn('SOA.map: no room for the named label of ' + id + ' (it stays a year)'); return; }
      got.add(id); placedN.push(C[k]); q.nbox = Object.assign({}, C[k], { el: mkBox(q, C[k], false) });
    });
      okSet = got;
    }
    const placedA = [];
    ids.filter((id) => pins[id] && pins[id].tIn !== undefined).sort((a, b) => pins[a].tIn - pins[b].tIn).forEach((id) => {
      const q = pins[id], L = lanes[q.p.lane], w = Math.max(q.w1, q.w2) + 24, h = 78, pref = (o.place && o.place[id]) ? [o.place[id]] : [];
      const C = { rc: { x: q.x + 22, y: q.y - h / 2, w, h }, lc: { x: q.x - 22 - w, y: q.y - h / 2, w, h }, ru: { x: q.x + 22, y: L.y0 + 2, w, h }, lu: { x: q.x - 22 - w, y: L.y0 + 2, w, h }, lf: { x: Math.min(q.x - 22, nowX - 8) - w, y: q.y - h / 2, w, h } };
      const fits = (b) => okX(b) && !placedA.some((pb) => pb.t0 < q.tAct && q.tIn < pb.t1 && hit(pb, b)) && !obst.some((ob) => ob.id !== id && hit(ob, b));
      let k = [...pref, 'rc', 'lc', 'ru', 'lu', 'lf'].find((kk) => fits(C[kk]));
      if (!k) k = [...pref, 'rc', 'lc', 'ru', 'lu', 'lf'].find((kk) => okX(C[kk]) && !placedA.some((pb) => pb.t0 < q.tAct && q.tIn < pb.t1 && hit(pb, C[kk]))) || 'rc';
      const b = Object.assign({}, C[k], { t0: q.tIn, t1: q.tAct }); placedA.push(b); q.abox = Object.assign({}, b, { el: mkBox(q, b, true) });
    });
    // which named labels each active callout hides
    for (const id in pins) { const q = pins[id]; if (!q.abox) continue; q.hides = []; for (const jd in pins) { const r = pins[jd]; if (jd !== id && r.nbox && hit(r.nbox, q.abox)) q.hides.push(jd); }
      // and other pins' year labels and glyphs under it
      q.hidesY = []; for (const jd in pins) { const r = pins[jd]; if (jd !== id && hit({ x: r.x - 30, y: r.y - 42, w: 60, h: 90 }, q.abox)) q.hidesY.push(jd); } }
    const flipTimes = {}; for (const id in (o.flips || {})) flipTimes[id] = o.flips[id].map((s) => ctx.at(s));
    const arrows = (o.arrows || []).map((A) => { const a = pins[A.from], b = pins[A.to];
      const x0 = a ? a.x : xOf(A.fromYear), y0 = a ? a.y : laneY(A.fromLane), x1 = b ? b.x : xOf(A.toYear), y1 = b ? b.y - 16 : (A.toY ?? laneY(A.toLane));
      const d = `M${x0},${y0 + (y1 > y0 ? 16 : -16)} Q${(x0 + x1) / 2 + 30},${(y0 + y1) / 2} ${x1},${y1}`;
      const pth = K.s('path', { d, fill: 'none', stroke: muted, 'stroke-width': 2.5, 'stroke-dasharray': A.dashed ? '6 7' : '' }, g); const L = pth.getTotalLength();
      if (!A.dashed) pth.style.strokeDasharray = `${L} ${L + 10}`;
      return { pth, L, t: ctx.at(A.at), dur: A.dur ?? 0.7, dashed: A.dashed, frac: A.frac ?? 1, t2: A.complete ? ctx.at(A.complete) : null }; });
    const M0 = {
      xOf, laneY, pins, nowX, g, svg, lanes: laneEls,
      render(t) {
        const S_ = S;
        now.style.opacity = (0.7 + 0.1 * Math.sin(2 * Math.PI * t / 4)).toFixed(3);
        let rev = 1; if (revRect) { rev = S_.seg(t, tRev, tRev + 1.6, S_.ease.inOutSine); revRect.setAttribute('width', (1920 * rev).toFixed(1)); }
        const labIn = revRect ? S_.seg(t, tRev + 0.8, tRev + 1.8, S_.ease.linear) : 1;
        // lanes: lit / dim / data lane
        const dl = o.dataLane === true ? 1 : (o.dataLane && o.dataLane.at !== undefined ? S_.seg(t, ctx.at(o.dataLane.at), ctx.at(o.dataLane.at) + 0.8, S_.ease.linear) : 0);
        for (const id in laneEls) { const E = laneEls[id];
          let lit = false; (o.lit || []).forEach(([lid, a, b]) => { if (lid === id && t >= ctx.at(a) && (b === undefined || t < ctx.at(b))) lit = true; });
          let op = 1; (o.dim || []).forEach(([lids, a, b, v]) => { if (lids.includes(id) && t >= ctx.at(a) && (b === undefined || t < ctx.at(b))) op = Math.min(op, v); });
          E.lab.style.color = lit ? 'var(--fg)' : 'var(--muted)'; E.lab.style.opacity = op * (typeof labIn === 'number' ? labIn : 1);
          if (E.L.dashed) { [E.top, E.bot].forEach((e) => { if (e) e.style.opacity = dl; }); E.lab.style.opacity = dl * op; K.show(E.lab, dl > 0); }
          E.op = op; }

        for (const id in pins) { const q = pins[id], E = laneEls[q.p.lane], lop = E.op;
          const inT = q.tIn, on = inT === undefined ? 1 : S_.seg(t, inT, inT + 0.3, S_.ease.outCubic);
          q.pg.style.opacity = (on * lop).toFixed(3); K.show(q.pg, on > 0);
          q.gl.setAttribute('transform', `scale(${(1 + 0.6 * (1 - on)).toFixed(3)})`);
          if (q.fl && flipTimes[id]) { let a = 0; flipTimes[id].forEach((ft) => { a += 180 * S_.spring((t - ft) / 0.8, 0.03); }); q.fl.setAttribute('transform', `translate(0 -28) rotate(${a.toFixed(2)})`); }
          let state = 'year';
          if (inT === undefined) state = q.nbox ? 'named' : 'year';
          else if (t < inT) state = 'hidden'; else if (t < q.tAct) state = 'active'; else state = q.nbox ? 'named' : 'year';
          q.state = state; q.on = on * lop;
        }
        const hidN = {}, hidY = {};
        for (const id in pins) { const q = pins[id]; if (q.state === 'active' && q.abox) { q.hides.forEach((j) => { hidN[j] = 1; }); q.hidesY.forEach((j) => { hidY[j] = 1; }); } }
        for (const id in pins) { const q = pins[id];
          if (q.abox) { const vis = q.state === 'active'; K.show(q.abox.el, vis); if (vis) q.abox.el.style.opacity = q.on.toFixed(3); }
          if (q.nbox) { const vis = q.state === 'named' && !hidN[id]; K.show(q.nbox.el, vis); if (vis) q.nbox.el.style.opacity = q.on.toFixed(3); }
          const showY = q.state === 'year' || (q.state === 'named' && hidN[id]);
          q.yl.style.opacity = (showY && !q.dupYear && !hidY[id] ? q.on : 0).toFixed(3);
          if (hidY[id]) q.pg.style.opacity = 0;
        }
        arrows.forEach((A) => { const p = S_.seg(t, A.t, A.t + A.dur, S_.ease.inOutSine), p2 = A.t2 !== null ? S_.seg(t, A.t2, A.t2 + 0.6, S_.ease.inOutSine) : 0;
          const f = A.frac + (1 - A.frac) * p2; if (!A.dashed) A.pth.style.strokeDashoffset = (A.L * (1 - p * f)).toFixed(1); A.pth.style.opacity = t >= A.t ? 1 : 0; });
      },
    };
    return ctx.add(M0);
  };
  window.SOA = SOA;
})();
