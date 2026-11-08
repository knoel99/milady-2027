/* equation.js: KaTeX equation builder (styles.md §3.4 and §3.7, "how an equation builds up").
 *
 *   const E = Kit.equation(ctx, {
 *     tex: '\\term{lhs}{\\partial_t \\B} \\term{eq}{=} \\term{adv}{\\nabla\\times(\\U\\times\\B)} \\term{plus}{+} \\term{diff}{\\etaP\\nabla^2\\B}',
 *     x: 960, y: 300, size: 80, anchor: 'center' | 'left',
 *     ghost: 'cue' | false,                // whole equation at 15 % first (only if its shape matters)
 *     reveal: [['lhs', 'c1'], [['eq', 'adv'], 'c2'], ['diff', 'c3']],   // NARRATIVE order, on cues
 *     focus: [{ids: ['adv'], at: 'c4', out: 'c5'}],                     // other terms drop to 35 %
 *     labels: [{id: 'adv', text: 'carried and stretched by the flow', color: 'u', at: 'c2+0.3', out, side: 'below'}],
 *     out: 'cue',                           // optional exit
 *     macros: {'\\Q': '\\cq{Q}'}             // optional extra KaTeX macros (kit macros always available)
 *   })
 * \term{id}{…} makes a term addressable; colour by role with the kit macros (\U \B \Rm \etaP \Gam \vth
 * \Edist, \cu{} \cb{} \cp{} \cm{} \ck{}). Untagged parts appear with the first reveal. A term is
 * written on by a left-to-right wipe (0.45 s) with a chalk dot at its edge; labels hang under a brace
 * drawn on 0.3 s later; at most two labels at once (warned). E.box(id) gives a term's box in stage px.
 *
 *   Kit.morph(ctx, {from: E1, to: E2, at, dur})   T6: matching \term ids glide from E1 to E2, the others
 *                                                 fade; E1 must be fully revealed before `at`.
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit;
  let uid = 0;

  K.equation = function (ctx, o = {}) {
    if (!o.tex) throw new Error('equation needs tex');
    const id = 'eq' + (++uid) + '-';
    // o.macros: extra KaTeX macros for this equation (e.g. {'\\Q': '\\cq{Q}'}); the kit macros and \\term stay
    const html = K.tex(o.tex, true, Object.assign({}, o.macros || {}, { '\\term': `\\htmlId{${id}#1}{#2}` }));
    const mk = (cls) => {
      const d = K.el('div', { class: 'kit-eq ' + (cls || ''), 'data-kit': 'equation', html }, o.parent || ctx.stage);
      d.style.fontSize = (o.size || 72) + 'px'; d.style.top = (o.y ?? 300) + 'px'; d.style.left = (o.x ?? 960) + 'px';
      d.style.zIndex = o.z ?? 20;
      if ((o.anchor || 'center') === 'center') d.style.transform = 'translateX(-50%)';
      return d;
    };
    const ghost = o.ghost ? mk('ghost') : null;
    if (ghost) { ghost.style.opacity = 0.15; ghost.querySelectorAll('[id]').forEach((e) => e.removeAttribute('id')); ghost.setAttribute('data-qa', 'ignore'); }
    const root = mk('main');
    const terms = {};
    root.querySelectorAll(`[id^="${id}"]`).forEach((e) => { terms[e.id.slice(id.length)] = e; });
    const box = (tid) => { if (!terms[tid]) throw new Error('equation: no term ' + tid); return K.box(terms[tid], ctx); };

    // reveal schedule
    const rev = (o.reveal || []).map((r) => {
      const ids = Array.isArray(r) ? (Array.isArray(r[0]) ? r[0] : [r[0]]) : r.ids;
      const at = Array.isArray(r) ? r[1] : r.at;
      ids.forEach((i) => { if (!terms[i]) throw new Error('equation reveal: unknown term ' + i); });
      return { ids, t: ctx.at(at) };
    });
    const tagged = Object.keys(terms), revealT = {};
    for (const r of rev) for (const i of r.ids) revealT[i] = r.t;
    const first = rev.length ? Math.min(...rev.map((r) => r.t)) : ctx.at(o.at ?? 0);
    for (const k of tagged) if (!(k in revealT)) revealT[k] = first;   // tagged but not scheduled: with the first reveal
    const tGhost = o.ghost ? ctx.at(o.ghost === true ? (o.at ?? 0) : o.ghost) : null;
    const tOut = o.out !== undefined ? ctx.at(o.out) : Infinity;
    const WIPE = o.wipe ?? 0.45;
    const dot = K.el('div', { class: 'kit-dot' }, o.parent || ctx.stage); dot.style.zIndex = (o.z ?? 20) + 1;
    const tbox = {}; for (const k of tagged) tbox[k] = box(k);

    // focus windows
    const foc = (o.focus || []).map((f) => ({ ids: f.ids, a: ctx.at(f.at), b: f.out !== undefined ? ctx.at(f.out) : Infinity }));

    // labels with braces (pen M9)
    const svg = K.svgLayer(ctx, (o.z ?? 20) + 1, o.parent);
    svg.setAttribute('data-kit', 'equation');
    const labels = (o.labels || []).map((L) => {
      const b = box(L.id), col = K.c(L.color || 'chalk'), below = (L.side || 'below') === 'below';
      const y = below ? b.y + b.h + 14 : b.y - 14, x0 = b.x + 6, x1 = b.x + b.w - 6, xm = (x0 + x1) / 2, d = below ? 1 : -1, r = Math.min(20, (x1 - x0) / 4);
      const p = K.s('path', { d: `M${x0},${y} q0,${d * r} ${r},${d * r} L${xm - r},${y + d * r} q${r},0 ${r},${d * r} q0,${-d * r} ${r},${-d * r} L${x1 - r},${y + d * r} q${r},0 ${r},${-d * r}`,
        fill: 'none', stroke: col, 'stroke-width': 4, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, svg);
      const len = p.getTotalLength(); p.style.strokeDasharray = len;
      const lab = K.el('div', { class: 'kit-eq-label', 'data-kit': 'equation-label', html: K.markup(L.text) }, o.parent || ctx.stage);
      lab.style.left = xm + 'px'; lab.style.color = col; lab.style.zIndex = (o.z ?? 20) + 1;
      lab.style.top = (below ? y + 2 * r + 10 : y - 2 * r - 52) + 'px';
      const a = ctx.at(L.at ?? revealT[L.id] + 0.3), z = L.out !== undefined ? ctx.at(L.out) : Infinity;
      return { p, len, lab, a, z };
    });
    for (let i = 0; i < labels.length; i++) {
      const on = labels.filter((m) => m.a <= labels[i].a && labels[i].a < m.z);
      if (on.length > 2) S.warn('equation: more than two labels on screen at once (style rule: at most two)');
    }

    const E = {
      root, terms, box, tbox, hidden: new Set(), offsets: {},
      render(t) {
        const ex = tOut === Infinity ? 0 : S.seg(t, tOut, tOut + 0.3, S.ease.linear);
        const live = t >= Math.min(first, tGhost ?? Infinity) && ex < 1;
        K.show(root, t >= first && ex < 1); root.style.opacity = 1 - ex;
        if (ghost) { K.show(ghost, live); ghost.style.opacity = (0.15 * (1 - ex) * S.seg(t, tGhost, tGhost + 0.5, S.ease.linear)).toFixed(3); }
        let dotOn = false;
        const dim = foc.find((f) => t >= f.a && t < f.b + 0.4);
        for (const k of tagged) {
          const el = terms[k], p = S.seg(t, revealT[k], revealT[k] + WIPE, S.ease.outCubic);
          K.wipe(el, p, 300);
          if (E.hidden.has(k)) el.style.visibility = 'hidden';
          if (p > 0 && p < 1) {   // chalk dot rides the wipe edge
            const b = tbox[k]; dot.style.left = (b.x + b.w * p) + 'px'; dot.style.top = (b.y + b.h * 0.55) + 'px'; dotOn = true;
          }
          let op = 1;
          if (dim && !dim.ids.includes(k)) {
            const fa = S.seg(t, dim.a, dim.a + 0.4, S.ease.inOutSine), fb = dim.b === Infinity ? 0 : S.seg(t, dim.b, dim.b + 0.4, S.ease.inOutSine);
            op = 1 - 0.65 * fa * (1 - fb);
          }
          el.style.opacity = op;
          const off = E.offsets[k]; el.style.transform = off ? `translate(${off[0]}px, ${off[1]}px)` : '';
          if (off) el.style.display = 'inline-block';
        }
        K.show(dot, dotOn && live); dot.style.opacity = 0.9;
        for (const L of labels) {
          const p = S.seg(t, L.a, L.a + 0.5, S.ease.inOutSine), q = L.z === Infinity ? 0 : S.seg(t, L.z, L.z + 0.3, S.ease.linear);
          L.p.style.strokeDashoffset = L.len * (1 - p); L.p.style.opacity = (1 - q) * (1 - ex);
          L.lab.style.opacity = S.seg(t, L.a + 0.25, L.a + 0.55, S.ease.linear) * (1 - q) * (1 - ex);
          K.show(L.lab, t >= L.a && q < 1 && ex < 1);
        }
      },
    };
    return ctx.add(E);
  };

  /** T6 equation morph: FLIP of matching \term ids from E1 to E2 */
  K.morph = function (ctx, o) {
    const A = o.from, B = o.to, a = ctx.at(o.at), dur = o.dur ?? 1.0;
    const common = Object.keys(B.terms).filter((k) => k in A.terms);
    const delta = {}; for (const k of common) { const ba = A.tbox[k], bb = B.tbox[k]; delta[k] = [ba.x - bb.x, ba.y - bb.y]; }
    return ctx.add({
      // register this AFTER both equations (it overrides their styles); create E2 with at = morph time
      render(t) {
        if (t < a) { K.show(B.root, false); return; }
        const p = S.seg(t, a, a + dur, S.ease.inOutCubic), handover = S.seg(t, a, a + 0.15, S.ease.linear);
        // A: its glue and unmatched terms fade out; matched terms hand over to B's copies after 0.15 s
        K.show(A.root, p < 1); A.root.style.opacity = 1 - S.seg(t, a, a + dur * 0.6, S.ease.linear);
        for (const k of common) A.terms[k].style.visibility = handover >= 1 ? 'hidden' : 'visible';
        // B: matched terms glide from A's positions; unmatched terms fade in during the second half
        K.show(B.root, true); B.root.style.opacity = handover;
        for (const k of Object.keys(B.terms)) {
          const el = B.terms[k]; el.style.clipPath = 'none'; el.style.visibility = 'visible';
          if (common.includes(k)) { el.style.display = 'inline-block'; el.style.opacity = 1;
            el.style.transform = `translate(${(delta[k][0] * (1 - p)).toFixed(2)}px, ${(delta[k][1] * (1 - p)).toFixed(2)}px)`; }
          else el.style.opacity = S.seg(t, a + dur * 0.5, a + dur, S.ease.linear);
        }
      },
    });
  };
})();
