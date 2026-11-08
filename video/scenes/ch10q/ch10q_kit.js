/* ch10q_kit.js: helpers shared by the scenes of unit ch10q (labels, fades from ch09_kit.js; the question board CQ below) (labels with entrance/exit, faded groups,
   series lookup, on-screen text taken from the script). Pure functions of t; elements built in setup only.
   Nothing here duplicates a kit component; candidates for promotion are listed in script/_review/scenes_ch10q.md. */
window.UK = (function () {
  const K = Kit, S = Scene, U = {};
  /** a text label: {text | html, x, y, anchor 'l'|'c'|'r', size, color (token), cls ('mono' | 'display' | 'halo'), at, out, parent, z, maxW, alpha} */
  U.label = function (ctx, o) {
    const e = K.el('div', { class: 'uk-lab ' + (o.cls || ''), html: o.html ?? K.markup(o.text) }, o.parent || ctx.stage);
    e.style.left = o.x + 'px'; e.style.top = o.y + 'px';
    const a = o.anchor || 'l'; e.style.transform = `translate(${a === 'c' ? '-50%' : a === 'r' ? '-100%' : '0'}, ${o.vmid ? '-50%' : '0'})`;
    if (o.size) e.style.fontSize = o.size + 'px';
    if (o.color) e.style.color = K.c(o.color);
    if (o.z !== undefined) e.style.zIndex = o.z;
    if (o.maxW) { e.style.whiteSpace = 'normal'; e.style.width = o.maxW + 'px'; }
    const { t0, t1 } = K.times(ctx, o, 0), din = o.din ?? 0.25;
    return ctx.add({ root: e, el: e, alpha: 1, render(t) { const v = K.env(t, t0, t1, din, 0.25); K.show(e, v.on); e.style.opacity = (v.o * (o.alpha ?? 1) * this.alpha).toFixed(3); } });
  };
  /** fade an element (HTML or SVG) in at `at` and out at `out` (multiplied by el.__dim if set) */
  U.fade = function (ctx, el, o) {
    const { t0, t1 } = K.times(ctx, o, 0), din = o.din ?? 0.35;
    return ctx.add({ root: el, dim: () => 1, render(t) { const v = K.env(t, t0, t1, din, o.dout ?? 0.3); el.style.display = v.on ? '' : 'none'; el.style.opacity = (v.o * this.dim(t)).toFixed(3); } });
  };
  U.series = (D, name) => { const s = D.series.find((x) => x.name === name); if (!s) throw new Error('series not found: ' + name); return s; };
  /** an on-screen label of the script that starts with `prefix` (keeps the writer's text, numbers included) */
  U.onscreen = (ctx, prefix, fallback) => { const L = (ctx.script && ctx.script.onscreen && ctx.script.onscreen.labels) || []; return L.find((x) => x.startsWith(prefix)) || fallback; };
  /** time of a fraction of the sentence whose cue is `cue` (falls back to cue + dt in previews) */
  U.frac = function (ctx, cue, f, dt) {
    const s = ctx.script && ctx.script.sentences && ctx.script.sentences.find((x) => x.cue === cue);
    return s && Number.isFinite(s.end) ? s.start + f * (s.end - s.start) : ctx.at(cue) + (dt ?? 2);
  };
  U.end = (ctx, cue, dt) => U.frac(ctx, cue, 1, dt);
  /** percent label from a fraction (display rounding only) */
  U.pc = (v) => `${Math.round(v)} %`;
  return U;
})();

/* ===================== CQ: the question board =====================
   Tickets (80 × 40, a notch on the left, the number in mono 28): solid = a question card, dashed = asked without a
   card, double = asked in the extended cut only. Each ticket moves between layouts given as keyframes
   [{t, pos: {id: {x, y, a, lab}}}] with 0.6-s eased transitions; labels sit to the right of their ticket. */
window.CQ = (function () {
  const K = Kit, S = Scene, CQ = {};
  CQ.E = () => window.CQ_BOARD.entries;
  CQ.byId = (id) => CQ.E().find((e) => e.id === id);
  CQ.COLS = { a: 110, b: 690, c: 1270 };
  CQ.HEAD = { a: 'RUNS · PARAMETERS', b: 'METRICS · CRITERIA', c: 'DATA · GPUs · BUDGET' };
  /** layout A: priority-1 rows with labels in their category column; the rest in the LATER pile */
  CQ.layoutA = (labs = true) => { const pos = {}, k = { a: 0, b: 0, c: 0 }; let p = 0;
    for (const id of window.CQ_BOARD.order) { const e = CQ.byId(id);
      if (e.pri === 1) { pos[id] = { x: CQ.COLS[e.cat], y: 204 + 44 * k[e.cat]++, a: 0.45, lab: labs ? 0.45 : 0 }; }
      else { pos[id] = { x: 1560 + 22 * (p % 8), y: 700 + 16 * Math.floor(p / 8) + (p % 2) * 4, a: 0.45, lab: 0, pile: true }; p++; } }   // the LATER pile: a deliberate stack
    return pos; };
  /** layout B: shelf 1 as stubs (4 per row), shelf 2 rows with labels, shelf 3 as stubs (hidden until shown) */
  CQ.layoutB = (show3) => { const pos = {}, k1 = { a: 0, b: 0, c: 0 }, k2 = { a: 0, b: 0, c: 0 }, k3 = { a: 0, b: 0, c: 0 };
    for (const id of window.CQ_BOARD.order) { const e = CQ.byId(id), x0 = CQ.COLS[e.cat];
      if (e.pri === 1) { const k = k1[e.cat]++; pos[id] = { x: x0 + 92 * (k % 4), y: 200 + 46 * Math.floor(k / 4), a: 0.85, lab: 0 }; }
      else if (e.pri === 2) { pos[id] = { x: x0, y: 350 + 42 * k2[e.cat]++, a: 0.6, lab: 0.6 }; }
      else { const k = k3[e.cat]++; pos[id] = show3 ? { x: x0 + 92 * (k % 4), y: 740 + 46 * Math.floor(k / 4), a: 0.6, lab: 0 } : { x: 1640, y: 760, a: 0, lab: 0 }; } }
    return pos; };
  /** layout C: the message card (13 priority-1 tickets in two columns) and the others as a dim double row */
  CQ.layoutC = (order1) => { const pos = {}; let o = 0;
    order1.forEach((id, i) => { pos[id] = { x: 270 + 540 * Math.floor(i / 7), y: 260 + 48 * (i % 7), a: 1, lab: 1 }; });
    for (const id of window.CQ_BOARD.order) if (!pos[id]) { pos[id] = { x: 240 + 92 * (o % 12), y: 650 + 46 * Math.floor(o / 12), a: 0.25, lab: 0 }; o++; }
    return pos; };
  CQ.build = function (ctx, frames, o = {}) {
    const lay = K.el('div', {}, ctx.stage); lay.style.cssText = 'position:absolute;inset:0;z-index:31';
    const T = frames.map((f) => ({ t: typeof f.t === 'number' ? f.t : ctx.at(f.t), pos: f.pos, dur: f.dur ?? 0.6, stagger: f.stagger ?? 0 }));
    const tk = CQ.E().map((e, i) => {
      const d = K.el('div', { class: 'cq-t ' + e.kind + (e.ext ? ' ext' : '') }, lay); K.el('span', {}, d, e.id);
      const l = K.el('div', { class: 'uk-lab cq-l' }, lay, e.label);
      return { e, d, l, i, hi: 0 };
    });
    const ix = (id) => window.CQ_BOARD.order.indexOf(id);
    const state = (t, q) => {   // interpolated position of ticket q
      let a = null, b = null;
      for (const f of T) { if (t >= f.t) { a = b ? b : a; b = f; } }
      if (!b) return null;
      const prev = T[T.indexOf(b) - 1], st = b.stagger * Math.max(0, ix(q.e.id));
      const p = prev ? S.seg(t, b.t + st, b.t + st + b.dur, S.ease.inOutCubic) : S.seg(t, b.t + st, b.t + st + 0.35, S.ease.linear);
      const B = b.pos[q.e.id] || { x: 960, y: 1200, a: 0, lab: 0 }, A = prev ? (prev.pos[q.e.id] || B) : Object.assign({}, B, { a: 0, lab: 0 });
      void a; const L = (u, v) => u + (v - u) * p;
      return { x: L(A.x, B.x), y: L(A.y, B.y), a: L(A.a, B.a), lab: L(A.lab ?? 0, B.lab ?? 0), pile: !!(B.pile && p >= 1) };
    };
    const B = { lay, tk, focus: [], hiTicket: (ids, at, out) => B.focus.push({ ids, t0: typeof at === 'number' ? at : ctx.at(at), t1: out === undefined ? 1e9 : (typeof out === 'number' ? out : ctx.at(out)) }) };
    ctx.add({ render(t) {
      for (const q of tk) { const s = state(t, q); if (!s || s.a <= 0.01) { q.d.style.display = 'none'; q.l.style.display = 'none'; continue; }
        let h = 0; for (const f of B.focus) if (f.ids.includes(q.e.id)) h = Math.max(h, S.seg(t, f.t0, f.t0 + 0.3, S.ease.linear) * (1 - S.seg(t, f.t1, f.t1 + 0.3, S.ease.linear)));
        if (s.pile) q.d.setAttribute('data-qa', 'ignore'); else q.d.removeAttribute('data-qa');   // QA: the pile overlaps on purpose
        q.d.style.display = ''; q.d.style.left = s.x.toFixed(1) + 'px'; q.d.style.top = s.y.toFixed(1) + 'px'; q.d.style.opacity = Math.max(s.a, h).toFixed(3);
        q.d.style.borderColor = h > 0.5 ? 'var(--fg)' : '';
        const la = Math.max(s.lab, h); q.l.style.display = la > 0.01 ? '' : 'none'; q.l.style.left = (s.x + 96).toFixed(1) + 'px'; q.l.style.top = (s.y + 2).toFixed(1) + 'px'; q.l.style.opacity = la.toFixed(3); }
    } });
    return B;
  };
  /** the question panel: the full register question of the focused ticket(s), one at a time */
  CQ.panel = function (ctx, box, items) {
    const p = K.el('div', { class: 'uk-card' }, ctx.stage); p.style.cssText += `;left:${box.x0}px;top:${box.y0}px;width:${box.x1 - box.x0}px;height:${box.y1 - box.y0}px;padding:14px 20px;z-index:33`;
    const rows = items.map((it) => { const e = CQ.byId(it.id), r = K.el('div', {}, p); r.style.position = 'absolute'; r.style.left = '20px'; r.style.right = '20px'; r.style.top = '14px';
      K.el('div', { class: 'uk-lab mono' }, r, K.upper(`${e.id} · ${e.card ? 'question card ' + e.card : 'asked without a card'}`)).style.position = 'static';
      const q = K.el('div', { class: 'uk-lab', html: K.markup(e.en) }, r); q.style.cssText += ';position:static;white-space:normal;font-size:28px;margin-top:6px';
      return { r, a: typeof it.at === 'number' ? it.at : ctx.at(it.at), b: it.out === undefined ? 1e9 : (typeof it.out === 'number' ? it.out : ctx.at(it.out)) }; });
    const a0 = Math.min(...rows.map((r) => r.a)), b0 = Math.max(...rows.map((r) => r.b));
    ctx.add({ render(t) { const on = t >= a0 && t < b0 + 0.3; p.style.display = on ? '' : 'none'; p.style.opacity = (S.seg(t, a0, a0 + 0.3, S.ease.linear) * (1 - S.seg(t, b0, b0 + 0.3, S.ease.linear))).toFixed(3);
      rows.forEach((r, i) => { const nx = rows[i + 1], end = Math.min(r.b, nx ? nx.a : 1e9); r.r.style.display = t >= r.a && t < end ? '' : 'none'; }); } });
    return p;
  };
  CQ.heads = function (ctx, at, alpha = (c, t) => 1) {
    const hs = Object.entries(CQ.HEAD).map(([c, h]) => { const e = U0.label(ctx, { text: h, x: CQ.COLS[c], y: 110, cls: 'mono', at }); return { c, e }; });
    ctx.add({ render(t) { hs.forEach(({ c, e }) => { e.alpha = alpha(c, t); e.render(t); }); } });   // re-render: the alpha is a function of this frame (determinism)
    return hs;
  };
  const U0 = window.UK;
  return CQ;
})();
