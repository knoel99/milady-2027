/* hud.js: honesty badge, lower-thirds, altitude rail (M8), formula layer, chips.
 *
 *   Kit.badge(ctx, {kind, confidence, note, at, out})
 *       kind: MEASURED | PROVED | CONJECTURE | PLANNED | CONTEXT (| SCHEMATIC for metaphors)
 *       confidence: high | medium | low (CONJECTURE only). The script's "badge" (kind, confidence, note) wins
 *       over opts; opts.note is used when the script has no note.
 *   Kit.lowerThird(ctx, {kind, l1, l2, color, data, at, hold, out})
 *       kind: chapter | source | reference | stamp. With kind "source" and `data` (a data/*.json
 *       object), l1/l2 default to its meta.stamp and "source: <path> · <sha8>"; that line is kept on ONE
 *       line (shrunk to >= 28 px, then the path's basename), so the box never grows into the scene.
 *   Kit.rail(ctx, {from, to, at, hold})          levels "L0"…"L5", left edge, 3 s by default
 *   Kit.formulaLayer(ctx, {items: [{tex, at, out}], label, at, out, stack, maxWidth})   small-type statements (D8)
 *       Items show ONE AT A TIME: an item without `out` leaves at the next item's `at` (stack: true keeps the
 *       old behaviour, every item stays to the end). Each item is fitted (Kit.fitFormula: split at its most
 *       balanced ";" ":" "," or \quad, then shrunk, never below 28 px). Without items (no `items` and no
 *       script onscreen.formulas, e.g. a preview) it returns null (warned in a built entry).
 *   Kit.chip(ctx, {text, kind, x, y, at, out, anchor, maxWidth, z})
 *       kind: plain | simulated ('') | generated | schematic | measured | param (green: "Γ = 0.93").
 *       maxWidth (px): the chip wraps to two lines within that width instead of growing on one line.
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit;

  // ---------- honesty badge ----------
  const GLYPH = {
    MEASURED: '<circle cx="15" cy="15" r="11" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="15" cy="15" r="4.5" fill="currentColor"/>',
    PROVED: '<rect x="7" y="7" width="16" height="16" fill="currentColor"/>',
    CONJECTURE: '<circle cx="15" cy="15" r="11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-dasharray="4 3.2"/><circle cx="15" cy="15" r="2.6" fill="currentColor"/>',
    PLANNED: '<path d="M5 15 H21 M15 9 L21 15 L15 21" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M25 7 V23" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>',
    CONTEXT: '<path d="M9 21 L21 9 M12 9 H21 V18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><rect x="5" y="5" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.6" opacity=".6"/>',
    SCHEMATIC: '<path d="M6 22 L13 8 L18 17 L24 11" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="3 3"/>',
  };
  const KINDS = Object.keys(GLYPH);
  K.badge = function (ctx, o = {}) {
    const sb = (ctx.script && (ctx.script.badge || (ctx.script.params && ctx.script.params.badge))) || null;
    let kind = String((sb && sb.kind) || o.kind || '').toUpperCase();
    let conf = (sb && sb.confidence !== undefined ? sb.confidence : o.confidence) || null;
    if (sb && o.kind && String(o.kind).toUpperCase() !== kind) S.warn(`badge: scene says ${o.kind}, script says ${kind} (script wins)`);
    if (!KINDS.includes(kind)) throw new Error('badge kind must be one of ' + KINDS.join(', ') + ' (got "' + kind + '")');
    if (kind === 'CONJECTURE' && !['high', 'medium', 'low'].includes(String(conf).toLowerCase())) throw new Error('CONJECTURE badge needs confidence high | medium | low');
    const { t0, t1 } = K.times(ctx, o, 0.2);
    const root = K.el('div', { class: 'kit-badge ' + kind.toLowerCase(), 'data-kit': 'badge' }, o.parent || ctx.stage);
    root.innerHTML = `<svg viewBox="0 0 30 30" aria-hidden="true">${GLYPH[kind]}</svg><span class="kb-kind">${kind}</span>`;
    if (kind === 'CONJECTURE') {
      const n = { high: 3, medium: 2, low: 1 }[String(conf).toLowerCase()];
      const p = K.el('span', { class: 'kb-pips', title: 'confidence ' + conf }, root);
      [12, 19, 26].forEach((h, i) => { const e = K.el('i', { class: i < n ? '' : 'off' }, p); e.style.height = h + 'px'; });
      K.el('span', { class: 'kb-note' }, root, String(conf).toLowerCase());
    }
    const note = (sb && sb.note) || o.note;   // the script's note wins (consistency editor), opts as fallback
    if (note) K.el('span', { class: 'kb-note' }, root, '· ' + note);
    return ctx.add({
      root, kind, confidence: conf,
      render(t) {
        const e = K.env(t, t0, t1, 0.3, 0.25);
        root.style.opacity = e.o; K.show(root, e.on);
        root.style.clipPath = e.p >= 1 ? 'none' : `inset(0 0 0 ${(100 - 100 * e.p).toFixed(2)}%)`;   // reveal from the right edge
      },
    });
  };

  // ---------- lower-thirds ----------
  const LT_COLOR = { chapter: 'muted', source: 'infra', reference: 'chalk', stamp: 'muted' };
  K.lowerThird = function (ctx, o = {}) {
    const kind = o.kind || 'source';
    if (!(kind in LT_COLOR)) throw new Error('lowerThird kind: chapter | source | reference | stamp');
    let l1 = o.l1, l2 = o.l2;
    if (o.data && o.data.meta) {
      const m = o.data.meta;
      l1 = l1 ?? m.stamp ?? ('DATA · ' + m.source);
      l2 = l2 ?? `source: ${m.source}${m.sha256 ? ' · ' + m.sha256.slice(0, 8) : ''}`;
    }
    if (!l1 && !l2) throw new Error('lowerThird needs l1/l2 (or data with meta)');
    const t0 = ctx.at(o.at ?? 0.5), t1 = o.out !== undefined ? ctx.at(o.out) : t0 + (o.hold ?? 5) + 0.35;
    K.claim('lower-third', t0, t1 + 0.25, l1 || l2);
    const root = K.el('div', { class: 'kit-lt ' + kind, 'data-kit': 'lower-third' }, o.parent || ctx.stage);
    root.style.borderLeftColor = K.c(o.color || LT_COLOR[kind]);
    if (l1) K.el('div', { class: 'l1' }, root, K.upper(l1));
    if (l2) {
      const e2 = K.el('div', { class: 'l2', html: K.markup(l2) }, root);
      if (kind === 'source' && o.data && o.data.meta && o.l2 === undefined) {
        // the auto source line stays on one line: shrink (>= 28 px), else print the file's basename
        e2.style.whiteSpace = 'nowrap';
        const maxW = (o.maxWidth ?? 900) - 42, m = o.data.meta;
        if (e2.scrollWidth > maxW + 0.5) {
          const fs0 = parseFloat(getComputedStyle(e2).fontSize);
          let fs = fs0; while (e2.scrollWidth > maxW + 0.5 && fs > 28) { fs = Math.max(28, fs - 1); e2.style.fontSize = fs + 'px'; }
          if (e2.scrollWidth > maxW + 0.5) {
            e2.style.fontSize = fs0 + 'px';
            e2.innerHTML = K.markup(`source: ${String(m.source).split('/').pop()}${m.sha256 ? ' · ' + m.sha256.slice(0, 8) : ''}`);
            fs = fs0; while (e2.scrollWidth > maxW + 0.5 && fs > 28) { fs = Math.max(28, fs - 1); e2.style.fontSize = fs + 'px'; }
          }
        }
      }
    }
    return ctx.add({
      root,
      render(t) {
        const p = S.seg(t, t0, t0 + 0.35, S.ease.outCubic), q = S.seg(t, t1, t1 + 0.25, S.ease.linear);
        K.show(root, t >= t0 && q < 1);
        root.style.clipPath = p >= 1 ? 'none' : `inset(0 ${(100 - 100 * p).toFixed(2)}% 0 0)`;
        root.style.opacity = 1 - q;
      },
    });
  };

  // ---------- altitude rail (M8) ----------
  const LV = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5'];
  const railY = (i) => 740 - i * 104;          // L0 at y 740 … L5 at y 220 (left gutter, above the band)
  K.rail = function (ctx, o = {}) {
    const lvl = (x) => { const i = LV.indexOf(String(x).toUpperCase()); if (i < 0) throw new Error('rail level must be L0…L5'); return i; };
    const sl = ctx.script && ctx.script.level;
    const to = lvl(o.to ?? sl ?? 'L0'), from = o.from !== undefined ? lvl(o.from) : to;
    const t0 = ctx.at(o.at ?? 0), t1 = o.out !== undefined ? ctx.at(o.out) : t0 + (o.hold ?? 3);
    const root = K.el('div', { class: 'kit-rail', 'data-kit': 'rail' }, o.parent || ctx.stage);
    const svg = K.s('svg', { width: 92, height: 1080, viewBox: '0 0 92 1080' }, root);
    svg.style.cssText = 'position:absolute;left:0;top:0;overflow:visible';
    const col = K.c('muted'), fg = K.c('fg');
    K.s('line', { x1: 80, x2: 80, y1: railY(5) - 24, y2: railY(0) + 24, stroke: col, 'stroke-width': 2 }, svg);
    const labels = LV.map((name, i) => {
      K.s('line', { x1: 70, x2: 80, y1: railY(i), y2: railY(i), stroke: col, 'stroke-width': 2 }, svg);
      const d = K.el('div', { class: 'rl' }, root, name); d.style.top = (railY(i) - 18) + 'px';
      return d;
    });
    const mark = K.s('rect', { x: 76, width: 8, height: 44, rx: 2, fill: fg }, svg);
    return ctx.add({
      root,
      render(t) {
        const e = K.env(t, t0, t1, 0.4, 0.4, S.ease.inOutSine);
        K.show(root, e.on);
        const climb = S.seg(t, t0 + 0.5, t0 + 1.7, S.ease.inOutCubic);
        const y = S.lerp(railY(from), railY(to), climb);
        mark.setAttribute('y', (y - 22).toFixed(2));
        // the rail is faint; it brightens to 80 % while the level changes, then settles back
        const bright = from === to ? 0.8 : 0.25 + 0.55 * Math.sin(Math.PI * Math.min(1, S.seg(t, t0, t0 + 2.2, S.ease.linear)));
        root.style.opacity = (e.o * Math.max(0.55, bright)).toFixed(3);
        const cur = Math.round(S.lerp(from, to, climb));
        labels.forEach((d, i) => { d.style.color = i === cur ? fg : ''; });
      },
    });
  };

  // ---------- formula layer (D8) ----------
  K.formulaLayer = function (ctx, o = {}) {
    let items = o.items;
    if (!items && ctx.script && ctx.script.onscreen && ctx.script.onscreen.formulas) {
      items = ctx.script.onscreen.formulas.map((f) => ({ tex: f.tex, at: f.cue, out: f.out }));
    }
    if (!items || !items.length) {
      // preview (no built entry) or a script without formulas: no layer; a built entry that has none is worth a warning
      if (ctx.script && ctx.script.id) S.warn('formulaLayer: no items and no onscreen.formulas in the script: no formula layer drawn');
      return null;
    }
    // one item at a time: an item without `out` leaves when the next one comes in (stack: true = all stay)
    const ts = items.map((it) => ctx.at(it.at ?? 0));
    const t0 = ctx.at(o.at ?? items[0].at ?? 0);
    const root = K.el('div', { class: 'kit-formula', 'data-kit': 'formula' }, o.parent || ctx.stage);
    if (o.maxWidth) root.style.maxWidth = o.maxWidth + 'px';
    if (o.label !== false) K.el('div', { class: 'fl-label' }, root, K.upper(o.label || 'Formula'));
    const rows = items.map((it, i) => {
      const d = K.el('div', { class: 'fl-item', html: K.tex(it.tex, false, o.macros) }, root);
      let b = it.out !== undefined && it.out !== null ? ctx.at(it.out) : Infinity;
      if (b === Infinity && !o.stack) { const nxt = ts.filter((x, j) => j > i && x > ts[i]); if (nxt.length) b = Math.min(...nxt); }
      return { d, tex: it.tex, a: ts[i], b };
    });
    // fit every item in the layer's width (at most two lines, never below 28 px)
    const cs = getComputedStyle(root);
    const avail = parseFloat(cs.maxWidth || '760') - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 4;
    if (o.fit !== false) rows.forEach((r) => K.fitFormula(r.d, r.tex, avail, { macros: o.macros }));
    const tEnd = o.out !== undefined ? ctx.at(o.out) : Infinity;
    K.claim('formula layer', t0, tEnd, 'formula');
    return ctx.add({
      root, rows,
      render(t) {
        const e = K.env(t, t0, tEnd, 0.3, 0.25);
        K.show(root, e.on); root.style.opacity = e.o;
        for (const r of rows) {
          // one at a time: the outgoing item is removed at once when the next one starts (no two rows stacked)
          const nextOn = !o.stack && rows.some((q) => q !== r && q.a > r.a && t >= q.a && q.a <= r.b);
          const on = t >= r.a && t < r.b + 0.25 && !nextOn;
          r.d.style.display = on ? '' : 'none';
          r.d.style.opacity = S.seg(t, r.a, r.a + 0.25, S.ease.linear) * (1 - S.seg(t, r.b, r.b + 0.25, S.ease.linear));
        }
      },
    });
  };

  // ---------- chips ----------
  K.chip = function (ctx, o = {}) {
    if (!o.text) throw new Error('chip needs text');
    const { t0, t1 } = K.times(ctx, o, 0.3);
    const root = K.el('div', { class: 'kit-chip ' + (o.kind || ''), 'data-kit': 'chip' }, o.parent || ctx.stage, o.caps === false ? o.text : K.upper(o.text));
    root.style.position = 'absolute';
    if (o.maxWidth) {   // two lines within maxWidth instead of one long line
      root.classList.add('wrap'); root.style.maxWidth = o.maxWidth + 'px';
      if (root.scrollHeight > 2 * 1.25 * 28 + 16) S.warn(`chip "${o.text.slice(0, 40)}…" needs more than two lines at maxWidth ${o.maxWidth}: shorten it`);
    }
    const anchor = o.anchor || 'tl';   // tl | tr | bl | br | c: which corner sits at (x, y)
    const tx = anchor.includes('r') ? '-100%' : anchor === 'c' ? '-50%' : '0';
    const ty = anchor.includes('b') ? '-100%' : anchor === 'c' ? '-50%' : '0';
    root.style.left = (o.x ?? 96) + 'px'; root.style.top = (o.y ?? 120) + 'px'; root.style.transform = `translate(${tx},${ty})`;
    root.style.zIndex = o.z ?? 45;
    return ctx.add({
      root,
      render(t) { const e = K.env(t, t0, t1, 0.2, 0.2); K.show(root, e.on); root.style.opacity = e.o; },
    });
  };
})();
