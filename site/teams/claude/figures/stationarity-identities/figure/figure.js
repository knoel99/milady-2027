// Hero: none, a conceptual diagram (flat route).
// Figure: law-level stationarity identities. Content from site/teams/claude/figures/FACTS.md only.
// All curves and bars are schematic (no measured values). Units inside a panel: pt.
export const figure = { width: 183, height: 84, name: 'stationarity-identities', format: 'journal' };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const U = C.blue, B = C.vermillion, FG = '#6f6f6f';     // colour key: u blue, B orange/red, forcing grey
  const NET = '#6A4C93', LIN = '#00896A', INK = C.ink, MID = C.mid;
  const T = (p, x, y, s, o = {}) => L.text(p, x, y, s, Object.assign({ size: 5.5, valign: 'middle' }, o));
  const box = (p, x, y, w, h, fill, stroke, o = {}) => L.rect(p, x, y, w, h, Object.assign({ fill, stroke, width: 0.6, r: 1.2 }, o));

  // ================================ panel a: the mean is zero, the snapshot is not ================================
  const a = F.panel('a', { x: 0, y: 0, w: 58, h: 84 });
  T(a, 12, 6, '**Energy balance** of a stationary state', { size: 6.5 });
  const ax = 14, aw = 144;
  const sig = (t) => 0.55 * Math.sin(2.1 * t) + 0.4 * Math.sin(5.3 * t + 1.0) + 0.28 * Math.sin(11.5 * t + 2.0);
  // top: the stationary signal
  const y0 = 66, amp = 24;
  L.line(a, [ax, y0 - 34], [ax, y0 + 34], { stroke: INK, width: 0.5 });
  L.arrow(a, [ax, y0], [ax + aw + 4, y0], { stroke: INK, width: 0.5, head: 2.4 });
  const pts = Array.from({ length: 221 }, (_, i) => { const t = (5 * i) / 220; return [ax + (t / 6) * aw, y0 - amp * sig(t)]; });
  L.polyline(a, pts, { stroke: INK, width: 0.9, fill: 'none', join: 'round' });
  L.line(a, [ax, y0], [ax + aw, y0], { stroke: LIN, width: 1.1, dash: '2.5 1.5' });
  T(a, ax + aw + 3, y0 + 8, 'time', { size: 5.5, anchor: 'end' });
  T(a, ax + 3, y0 - 36, 'd*E*/d*t*', { size: 5.5, anchor: 'start' });
  T(a, ax + aw + 3, y0 - 8, '**mean = 0**', { size: 6, anchor: 'end', color: LIN, halo: true });
  T(a, ax + 3, 17, 'each snapshot: not zero', { size: 5.5, anchor: 'start', color: INK });
  // bottom: the per-sample constraint (flat), not imposed
  const y1 = 132;
  T(a, ax + 3, 106, '**Per-sample constraint**: not what the law says', { size: 5.5, anchor: 'start', color: MID });
  L.line(a, [ax, y1 - 14], [ax, y1 + 14], { stroke: MID, width: 0.5 });
  L.arrow(a, [ax, y1], [ax + aw + 4, y1], { stroke: MID, width: 0.5, head: 2.4 });
  L.line(a, [ax, y1], [ax + aw, y1], { stroke: MID, width: 1.1 });
  const mx = ax + aw / 2;
  L.line(a, [mx - 3, y1 - 12], [mx + 3, y1 - 6], { stroke: INK, width: 1, cap: 'round' });
  L.line(a, [mx - 3, y1 - 6], [mx + 3, y1 - 12], { stroke: INK, width: 1, cap: 'round' });
  T(a, mx + 8, y1 - 9, 'flat: every sample balanced', { size: 5.5, anchor: 'start', color: MID });
  // identity, coloured by the key
  box(a, 0, 158, a.w, 62, '#F6F6F6', C.light, { width: 0.4 });
  T(a, a.w / 2, 168, '**Identity of the stationary law**', { size: 5.5, anchor: 'middle' });
  T(a, a.w / 2, 183, `E[ {#${FG.slice(1)}|⟨*f*·*u*⟩} − {#${U.slice(1)}|ν⟨|ω|²⟩} − {#${B.slice(1)}|η⟨|*j*|²⟩} ] = 0`, { size: 6.5, anchor: 'middle' });
  T(a, a.w / 2, 198, `{#${FG.slice(1)}|forcing} · {#${U.slice(1)}|viscous, *u*} · {#${B.slice(1)}|Joule, *B*}`, { size: 5.5, anchor: 'middle' });
  T(a, a.w / 2, 210, 'a few 10^{−4} of the dissipation (measured on the reference)', { size: 5, anchor: 'middle', color: MID });

  // ================================ panel b: helicity by shell =====================================================
  const b = F.panel('b', { x: 62, y: 0, w: 61, h: 84 });
  T(b, 12, 6, '**Magnetic helicity** by shell', { size: 6.5 });
  const vals = [-3.0, -0.3, 1.5, 2.2, 1.3, 0.6, 0.25, 0.15];   // schematic; positive and negative parts cancel
  const bx = 22, bw = 150, by0 = 100, sc = 14;                   // zero line
  L.line(b, [bx, 36], [bx, 170], { stroke: INK, width: 0.5 });
  L.arrow(b, [bx, by0], [bx + bw + 4, by0], { stroke: INK, width: 0.5, head: 2.4 });
  const step = bw / 8;
  vals.forEach((v, i) => {
    const x = bx + i * step + step * 0.15, w = step * 0.7;
    const h = Math.abs(v) * sc;
    const neg = v < 0;
    L.rect(b, x, neg ? by0 : by0 - h, w, h, { fill: neg ? '#F4C9A8' : B, stroke: B, width: 0.9 });
    T(b, x + w / 2, by0 + (neg ? -6 : 7) + (neg ? 0 : 0), '', {});
    T(b, x + w / 2, 177, String(i + 1), { size: 5.5, anchor: 'middle' });
  });
  T(b, bx + bw / 2, 187, 'shell *k*', { size: 5.5, anchor: 'middle' });
  T(b, bx + 2, 40, '*k*² *H*(*k*)  (schematic)', { size: 5.5, anchor: 'start' });
  // zero line drawn over bars
  L.line(b, [bx, by0], [bx + bw, by0], { stroke: INK, width: 0.5 });
  // sign brackets
  const x12 = bx + 2 * step, x38 = bx + 8 * step;
  T(b, bx + step, by0 + 49 + 0, '', {});
  const lx = bx + 2 * step + 4;
  T(b, lx, 112, '**large scales**', { size: 5.5, anchor: 'start', color: B });
  T(b, lx, 119, '*k* = 1, 2: negative', { size: 5.5, anchor: 'start', color: B });
  T(b, lx, 126, '*k* = 2: 3 to 16 times smaller', { size: 5, anchor: 'start', color: B });
  T(b, lx, 136, 'registered hypothesis H11', { size: 5, anchor: 'start', color: MID });
  T(b, lx, 142, '(negative at *k* = 1 only) refuted:', { size: 5, anchor: 'start', color: MID });
  T(b, lx, 148, '*k* = 2 is negative too', { size: 5, anchor: 'start', color: MID });
  T(b, bx + step * 5.5, 56, '**small scales**', { size: 5.5, anchor: 'middle', color: B });
  T(b, bx + step * 5.5, 63, '*k* ≥ 3: positive', { size: 5.5, anchor: 'middle', color: B });
  L.callout(b, [bx + 3 * step + step * 0.5, by0 - 2.2 * sc], [bx + 5.2 * step, 76], 'peak at *k* = 4', { anchor: 'start', size: 5.5 });
  // cancellation identity
  box(b, 0, 196, b.w, 24, '#F6F6F6', C.light, { width: 0.4 });
  T(b, b.w / 2, 205, `{#${B.slice(1)}|Σ_{k} *k*² *H*(*k*) = E[⟨*j*·*B*⟩] = 0}`, { size: 6.5, anchor: 'middle' });
  T(b, b.w / 2, 214, 'zero mean = cancellation between scales', { size: 5.5, anchor: 'middle' });

  // ================================ panel c: how the identities are used ==========================================
  const c = F.panel('c', { x: 127, y: 0, w: 56, h: 84 });
  const cw = c.w, cx = cw / 2;
  T(c, 12, 6, '**Use of the identities**', { size: 6.5 });
  // generator
  box(c, 14, 20, cw - 28, 18, NET, NET);
  T(c, cx, 29, 'Generator at η without data', { size: 5.5, anchor: 'middle', color: '#fff' });
  L.arrow(c, [cx, 38], [cx, 52], { stroke: INK, width: 0.8, head: 3 });
  // batch of generated snapshots (mode glyph)
  const gx = cx - 6 * 9 / 2 + 0.5;
  for (let i = 0; i < 6; i++) {
    const x = gx + i * 9;
    for (let k = 0; k < 4; k++) {
      L.rect(c, x + k * 1.6, 54, 1.6, 2.6, { fill: U, stroke: '#fff', width: 0.2 });
      L.rect(c, x + k * 1.6, 56.6, 1.6, 2.6, { fill: B, stroke: '#fff', width: 0.2 });
    }
  }
  T(c, cx, 66, 'generated samples (*u*, *B*)', { size: 5.5, anchor: 'middle' });
  L.arrow(c, [cx, 71], [cx, 85], { stroke: INK, width: 0.8, head: 3 });
  box(c, 6, 87, cw - 12, 30, '#F6F6F6', INK, { width: 0.6 });
  T(c, cx, 96, '**Means over samples**', { size: 5.5, anchor: 'middle' });
  T(c, cx, 104, 'energy and magnetic-helicity', { size: 5.5, anchor: 'middle' });
  T(c, cx, 111, 'balances, to be zero', { size: 5.5, anchor: 'middle' });
  // two uses
  const ux = 3, uw = cw / 2 - 6;
  L.arrow(c, [cx - 12, 117], [ux + uw / 2, 134], { stroke: INK, width: 0.8, head: 3 });
  L.arrow(c, [cx + 12, 117], [cw - 3 - uw / 2, 134], { stroke: INK, width: 0.8, head: 3 });
  box(c, ux, 136, uw, 30, '#EDE8F4', NET, { width: 0.8 });
  T(c, ux + uw / 2, 145, '**Training loss**', { size: 5.5, anchor: 'middle', color: NET });
  T(c, ux + uw / 2, 153, 'on the means', { size: 5.5, anchor: 'middle' });
  T(c, ux + uw / 2, 160, '(W5)', { size: 5.5, anchor: 'middle', color: MID });
  box(c, cw - 3 - uw, 136, uw, 30, '#EDE8F4', NET, { width: 0.8, dash: '2 1.2' });
  T(c, cw - 3 - uw / 2, 145, '**Sampling weights**', { size: 5.5, anchor: 'middle', color: NET });
  T(c, cw - 3 - uw / 2, 153, 'tilt the samples', { size: 5.5, anchor: 'middle' });
  T(c, cw - 3 - uw / 2, 160, '(W7)', { size: 5.5, anchor: 'middle', color: MID });
  // loss feeds back to the generator
  L.arrow(c, [ux + 1, 136], [8, 29], { stroke: NET, width: 0.9, via: [[8, 136]], head: 3, dash: '2 1.2' });
  L.arrow(c, [cw - 3 - uw / 2, 166], [cw - 3 - uw / 2, 174], { stroke: NET, width: 0.9, head: 3 });
  T(c, cw - 3 - uw / 2, 180, 'reweighted samples', { size: 5.5, anchor: 'middle', color: NET });
  T(c, cx, 189, '**collapsed**: comparison H8 dropped', { size: 5, anchor: 'middle', color: MID });
  // measured result
  box(c, 0, 196, cw, 24, '#F6F6F6', C.light, { width: 0.4 });
  T(c, cx, 205, '**Measured** (5 seeds, GPU)', { size: 5.5, anchor: 'middle' });
  T(c, cx, 214, 'W5: energy residual 0.29 → 0.19', { size: 5.5, anchor: 'middle' });
}
