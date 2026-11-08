/* cards.js: chapter card (transition T4) and question card (end of every chapter, brief §3.1).
 *
 *   Kit.chapterCard(ctx, {num: '04', title, level: 'L2', levelFrom: 'L1', tier: 0..4 | null,
 *                         pending: [3, 4], at, out, note})
 *       field lines of a dipole sweep in behind the title (vermillion, faint), the chapter number in mono,
 *       the title in Inter Display ExtraBold, the staircase (M7) with the current tier lit, the altitude
 *       rail (M8) climbing from levelFrom to level. 3–5 s; the scene's duration sets the hold.
 *   Kit.questionCard(ctx, {n, chapter, question, why, unblocks, category, ask, at, whyAt, unblocksAt, out})
 *       the "ask your supervisor" ticket: warm card, perforated stub with the question number, the
 *       question (<= 18 words; *word* gets the pen underline), WHY IT MATTERS and WHAT IT UNBLOCKS.
 *       category: runs (which simulations, which parameters) | framing (constraints, metrics, criteria)
 *       | logistics (data access, GPUs, Jean Zay, budget). Reads ctx.script.question when present: the script
 *       wins for every field (n, chapter, category, text, who); opts are the fallback. In a preview without a
 *       script question (make serve), a placeholder ticket is drawn instead of an error.
 *   Kit.predictCard(ctx, {x, y, w, anchor: 'c' | 'l', question, options: ['A · …', 'B · …'], at, out, answerAt,
 *                         pick, parent, z})
 *       the PREDICT beat (CONTRACT §3): mono kicker, the question in Inter Display 44, two (or more) grey
 *       outline buttons; on answerAt the picked button lights and the others dim. question: '' gives the
 *       compact card (kicker and buttons) for the answer beat. Put the question on its cue and answerAt on the
 *       next paragraph's cue: the hold between them is the script's hold_after, never a number in the scene.
 */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit;

  K.chapterCard = function (ctx, o = {}) {
    if (!o.title) throw new Error('chapterCard needs a title');
    const t0 = ctx.at(o.at ?? 0), t1 = o.out !== undefined ? ctx.at(o.out) : Infinity;
    const root = K.el('div', { class: 'kit-ccard', 'data-kit': 'chapter-card' }, o.parent || ctx.stage);
    // dipole field lines r = L sin^2(theta), centred off-frame right, faint vermillion
    const L = K.canvasLayer(ctx, 1, null, root);
    const cx = 1500, cy = 470, lines = [];
    for (const Ls of [140, 200, 270, 360, 470, 600, 760, 950]) for (const side of [1, -1]) {
      const pts = []; for (let i = 1; i < 180; i++) { const th = Math.PI * i / 180, r = Ls * Math.sin(th) ** 2; pts.push([cx + side * r * Math.sin(th), cy - r * Math.cos(th)]); }
      lines.push(pts);
    }
    const num = K.el('div', { class: 'cc-num' }, root, `CHAPTER ${o.num ?? ''}`.trim());
    const title = K.el('div', { class: 'cc-title', html: K.markup(o.title) }, root);
    K.fit(title, 1400, 2 * 1.04 * 112 + 4, 72);
    const tb = K.box(title, ctx);
    const lev = o.level ? K.el('div', { class: 'cc-level' }, root, `LEVEL ${o.level}${o.note ? ' · ' + o.note : ''}`) : null;
    if (lev) lev.style.top = (tb.y + tb.h + 36) + 'px';
    let stair = null;
    if (o.tier !== undefined) stair = K.staircase(ctx, { x: 1060, y: 530, w: 700, h: 230, lit: o.tier, pending: o.pending, at: (o.at ?? 0), parent: root });
    if (o.level) K.rail(ctx, { from: o.levelFrom ?? o.level, to: o.level, at: o.at ?? 0, hold: o.railHold ?? 3.2, parent: o.parent });
    void stair;
    return ctx.add({
      root,
      render(t) {
        const e = K.env(t, t0, t1, 0.4, 0.35); K.show(root, e.on); root.style.opacity = 1 - (t1 === Infinity ? 0 : S.seg(t, t1, t1 + 0.35, S.ease.linear));
        if (!e.on) return;
        const g = L.g; g.clearRect(0, 0, 1920, 1080);
        const p = S.seg(t, t0, t0 + 1.4, S.ease.inOutSine), breathe = 1 + 0.01 * Math.sin((t - t0) * 0.9);
        g.save(); g.translate(cx, cy); g.scale(breathe, breathe); g.translate(-cx, -cy);
        K.drawLines(g, lines, { color: 'b', width: 2, alpha: 0.18, progress: p }); g.restore();
        num.style.opacity = S.seg(t, t0 + 0.2, t0 + 0.5, S.ease.linear);
        K.wipe(title, S.seg(t, t0 + 0.4, t0 + 1.0, S.ease.outCubic), 60);
        if (lev) lev.style.opacity = S.seg(t, t0 + 0.9, t0 + 1.2, S.ease.linear);
      },
    });
  };

  const CAT = { runs: 'RUNS · PARAMETERS', framing: 'METRICS · CRITERIA', logistics: 'DATA · GPUs · BUDGET' };
  const GLY = {   // tiny pictograms for the unblocks tag
    runs: '<path d="M4 18 L10 8 L14 14 L20 4" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    framing: '<rect x="4" y="4" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M8 12 L11 15 L16 9" fill="none" stroke="currentColor" stroke-width="2.4"/>',
    logistics: '<rect x="3" y="7" width="18" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M8 7 V4 H16 V7" fill="none" stroke="currentColor" stroke-width="2.4"/>',
  };
  K.questionCard = function (ctx, o = {}) {
    const sq = (ctx.script && ctx.script.question) || {};
    // the script wins for every field (CONTRACT §4: "n and category from opts unless the script has them")
    const q = { n: sq.n ?? o.n, chapter: sq.chapter ?? o.chapter ?? (ctx.script && ctx.script.unit), question: sq.en || o.question, why: sq.why || o.why,
      unblocks: sq.unblocks || o.unblocks, category: sq.category || o.category, ask: sq.ask_who || o.ask || 'the supervisors' };
    if ((!q.question || !q.why || !q.unblocks) && !(ctx.script && ctx.script.id)) {
      // preview without a built entry (make serve): a placeholder ticket, so the page still renders
      S.warn('questionCard: no script question (preview): placeholder text drawn');
      q.question = q.question || 'The *question* comes from the script (question.en) in a built entry';
      q.why = q.why || 'question.why of the script.'; q.unblocks = q.unblocks || 'question.unblocks of the script.';
    }
    if (!q.question || !q.why || !q.unblocks) throw new Error('questionCard needs question, why, unblocks (script "question" or opts)');
    const words = q.question.replace(/[*{}/]|\b(u|b|param|model|metric)\b(?=\})/g, '').split(/\s+/).filter(Boolean).length;
    if (words > 18) S.warn(`question card: ${words} words on screen (brief: at most 18)`);
    if (q.category && !(q.category in CAT)) throw new Error('question category: runs | framing | logistics');
    const t0 = ctx.at(o.at ?? 0.2), tw = ctx.at(o.whyAt ?? t0 + 2.4), tu = ctx.at(o.unblocksAt ?? tw + 2.2), t1 = o.out !== undefined ? ctx.at(o.out) : Infinity;
    const root = K.el('div', { class: 'kit-qcard', 'data-kit': 'question-card' }, o.parent || ctx.stage);
    K.el('div', { class: 'qc-paper' }, root);
    const svg = K.s('svg', { class: 'qc-svg', viewBox: '0 0 1600 676' }, root);
    // perforation between stub and body: a dashed rule with two half-moon notches
    K.s('line', { x1: 252, x2: 252, y1: 26, y2: 650, stroke: getComputedStyle(root).getPropertyValue('--card-rule'), 'stroke-width': 3, 'stroke-dasharray': '2 11', 'stroke-linecap': 'round' }, svg);
    K.s('circle', { cx: 252, cy: 0, r: 18, fill: K.c('bg') }, svg); K.s('circle', { cx: 252, cy: 676, r: 18, fill: K.c('bg') }, svg);
    const stub = K.el('div', { class: 'qc-stub' }, root);
    K.el('div', { class: 'qc-ask' }, stub, 'ASK');
    const num = K.el('div', { class: 'qc-num' }, stub, q.n !== undefined && q.n !== null ? 'Q' + q.n : 'Q');
    if (q.chapter) K.el('div', { class: 'qc-ch' }, stub, String(q.chapter).toUpperCase());
    // who to ask: one unbreakable group per name ("D. Lucor" never splits after the initial), breaks only at " / " and ", "
    const who = String(q.ask).split(/(\s*\/\s*|,\s+)/).map((x, i) => (i % 2 ? K.esc(x) : `<span style="white-space:nowrap">${K.esc(x)}</span>`)).join('');
    K.el('div', { class: 'qc-who', html: `<small>WHO</small>${who}` }, stub);
    const main = K.el('div', { class: 'qc-main' }, root);
    K.el('div', { class: 'qc-kicker' }, main, 'A QUESTION TO SETTLE BEFORE WE COMPUTE');
    const qq = K.el('div', { class: 'qc-q', html: K.markup(q.question) }, main);
    K.fit(qq, 1236, 3 * 1.14 * 60 + 6, 44);
    const rows = K.el('div', { class: 'qc-rows' }, main);
    const r1 = K.el('div', { class: 'qc-row' }, rows); K.el('h4', {}, r1, 'WHY IT MATTERS'); const p1 = K.el('p', { html: K.markup(q.why) }, r1);
    const r2 = K.el('div', { class: 'qc-row' }, rows); K.el('h4', {}, r2, 'WHAT IT UNBLOCKS');
    if (q.category) K.el('div', { class: 'qc-tag', html: `<svg viewBox="0 0 24 24" width="24" height="24" style="vertical-align:-3px;margin-right:8px">${GLY[q.category]}</svg>${CAT[q.category]}` }, r2);
    const p2 = K.el('p', { html: K.markup(q.unblocks) }, r2);
    K.fit(p1, 590, 4 * 1.24 * 34 + 4, 28); K.fit(p2, 590, (q.category ? 3 : 4) * 1.24 * 34 + 4, 28);
    const qb = K.box(qq, ctx), rb = K.box(rows, ctx);
    if (qb.y + qb.h > rb.y - 16) S.warn('question card: question text runs into the rows; shorten it');
    // pen underline under every *emphasised* word group (graphite on the card)
    const pens = Array.from(qq.querySelectorAll('em')).map((em, i) => {
      const b = K.box(em, ctx), rr = K.box(root, ctx);
      const y = b.y - rr.y + b.h + 2, x0 = b.x - rr.x - 4, x1 = b.x - rr.x + b.w + 4, rng = S.rng('qpen' + i);
      const p = K.s('path', { d: `M${x0},${y + (rng() - 0.5) * 3} Q${(x0 + x1) / 2},${y + 7} ${x1},${y - 2 + (rng() - 0.5) * 3}`, fill: 'none', stroke: '#1F2937', 'stroke-width': 5, 'stroke-linecap': 'round' }, svg);
      const len = p.getTotalLength(); p.style.strokeDasharray = `${len} ${len + 10}`; return { p, len };
    });
    return ctx.add({
      root,
      render(t) {
        const e = K.env(t, t0, t1, 0.55, 0.35); K.show(root, e.on); if (!e.on) return;
        root.style.opacity = e.o; root.style.transform = `translateY(${(28 * (1 - e.p)).toFixed(2)}px)`;
        K.wipe(qq, S.seg(t, t0 + 0.35, t0 + 1.25, S.ease.inOutSine), 40);
        const tp = t0 + 1.35; pens.forEach((pp) => { pp.p.style.strokeDashoffset = (pp.len * (1 - S.seg(t, tp, tp + 0.5, S.ease.inOutSine))).toFixed(2); });
        const st = S.seg(t, t0 + 0.9, t0 + 1.5, S.ease.linear);
        num.style.opacity = st; num.style.transform = `scale(${(1.04 - 0.04 * S.spring(st, 0.03)).toFixed(4)})`;
        r1.style.opacity = S.seg(t, tw, tw + 0.4, S.ease.linear); r1.style.transform = `translateY(${(10 * (1 - S.seg(t, tw, tw + 0.4, S.ease.outCubic))).toFixed(2)}px)`;
        r2.style.opacity = S.seg(t, tu, tu + 0.4, S.ease.linear); r2.style.transform = `translateY(${(10 * (1 - S.seg(t, tu, tu + 0.4, S.ease.outCubic))).toFixed(2)}px)`;
      },
    });
  };

  // ---------- PREDICT card (predict beats, CONTRACT §3; promoted from the ch04 pilot, C4.predict) ----------
  K.predictCard = function (ctx, o = {}) {
    const w = o.w ?? 1000;
    const root = K.el('div', { class: 'kit-predict', 'data-kit': 'predict' }, o.parent || ctx.stage);
    root.style.left = (o.x ?? 960) + 'px'; root.style.top = (o.y ?? 96) + 'px'; root.style.width = w + 'px';
    if (o.z !== undefined) root.style.zIndex = o.z;
    if ((o.anchor || 'c') === 'c') root.style.marginLeft = (-w / 2) + 'px';
    K.el('div', { class: 'kp-kicker' }, root, o.kicker ? K.upper(o.kicker) : 'PREDICT');
    const q = K.el('div', { class: 'kp-q', html: K.markup(o.question || '') }, root);
    if (!o.question) q.style.display = 'none';   // compact card (the answer beat): kicker and buttons only
    const row = K.el('div', { class: 'kp-row' }, root);
    const btns = (o.options || []).map((t) => K.el('div', { class: 'kp-btn', html: K.markup(t) }, row));
    if (!btns.length) S.warn('predictCard: no options');
    const t0 = ctx.at(o.at ?? 0), t1 = o.out !== undefined ? ctx.at(o.out) : Infinity, ta = o.answerAt !== undefined ? ctx.at(o.answerAt) : Infinity;
    if (o.question) K.fit(q, w - 64, null, 36, ctx);
    if (ta < Infinity && t1 < Infinity && t1 - ta < 1.2) S.warn(`predictCard: the answer is lit for only ${(t1 - ta).toFixed(2)} s before the card leaves (give it >= 1.2 s)`);
    return ctx.add({
      root, buttons: btns, question: q,
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
})();
