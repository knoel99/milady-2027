// Hero: none, a conceptual diagram (flat route).
// Figure: why the first generators are over-dispersed and what was tried (linear part of the velocity field).
// Every statement comes from site/teams/claude/figures/FACTS.md. Units inside a panel: pt.
export const figure = { width: 183, height: 104, name: 'linear-part', format: 'journal' };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const m = L.mm;
  // colour key (shared by the team): u blue, B orange/red, forcing grey (not used here)
  const U = C.blue, B = C.vermillion;
  const LIN = '#00896A';      // linear part / exact Gaussian field
  const NET = '#6A4C93';      // network, "the rest"
  const INK = C.ink, MID = C.mid;
  const T = (p, x, y, s, o = {}) => L.text(p, x, y, s, Object.assign({ size: 5.5 }, o));

  // ---------- shared glyph: one Fourier mode = 4 real numbers for u (blue) + 4 for B (orange/red) ----------
  function mode(p, x, y, cw = 1.5, ch = 2.4) {
    for (let i = 0; i < 4; i++) {
      L.rect(p, x + i * cw, y, cw, ch, { fill: U, stroke: '#fff', width: 0.2 });
      L.rect(p, x + i * cw, y + ch, cw, ch, { fill: B, stroke: '#fff', width: 0.2 });
    }
    return 4 * cw;
  }
  function modeBar(p, x, y, w) {                    // a row of mode glyphs with a break
    const g = 4 * 1.5 + 1.2, n = Math.floor(w / g);
    let k = 0;
    for (let i = 0; i < n; i++) {
      const xx = x + i * g + (w - n * g) / 2;
      if (i === n - 4) { T(p, xx + 2, y + 2.6, '⋯', { size: 7, anchor: 'start', valign: 'middle', color: MID }); continue; }
      if (i === n - 3 || i === n - 2) continue;
      mode(p, xx, y);
      k++;
    }
  }
  const box = (p, x, y, w, h, fill, stroke, o = {}) => L.rect(p, x, y, w, h, Object.assign({ fill, stroke, width: 0.6, r: 1.2 }, o));
  const tick = (p, x, y, ok) => {                   // small drawn check / cross
    if (ok) L.polyline(p, [[x - 1.7, y], [x - 0.5, y + 1.4], [x + 1.9, y - 1.8]], { stroke: LIN, width: 1, fill: 'none', cap: 'round', join: 'round' });
    else { L.line(p, [x - 1.5, y - 1.5], [x + 1.5, y + 1.5], { stroke: INK, width: 1, cap: 'round' }); L.line(p, [x - 1.5, y + 1.5], [x + 1.5, y - 1.5], { stroke: INK, width: 1, cap: 'round' }); }
  };

  // =====================================================================================================
  // panel a: the field, its linear part, and the network that is narrower than the latent
  // =====================================================================================================
  const a = F.panel('a', { x: 0, y: 0, w: 66, h: 104 });
  const aw = a.w;
  T(a, 12, 6, '**Optimal velocity field** *v*(*x*, *t*)', { size: 6.5, valign: 'middle' });

  // decomposition v = linear part + the rest (widths are illustrative)
  const dy = 17, dh = 22;
  box(a, 0, dy, 30, dh, '#fff', INK, { width: 0.5 });
  T(a, 15, dy + dh / 2, '*v*', { size: 9, anchor: 'middle', valign: 'middle' });
  T(a, 34, dy + dh / 2, '=', { size: 9, anchor: 'middle', valign: 'middle' });
  box(a, 40, dy, 62, dh, '#D6EEE6', LIN, { width: 0.8 });
  T(a, 71, dy + 7, '**Linear part**', { size: 6.5, anchor: 'middle', valign: 'middle', color: LIN });
  T(a, 71, dy + 15, '*A*(*t*) *x* + *b*(*t*)', { size: 6, anchor: 'middle', valign: 'middle', color: LIN });
  T(a, 106, dy + dh / 2, '+', { size: 9, anchor: 'middle', valign: 'middle' });
  box(a, 111, dy, 42, dh, '#E6DFF0', NET, { width: 0.8 });
  T(a, 132, dy + 7, '**The rest**', { size: 6.5, anchor: 'middle', valign: 'middle', color: NET });
  T(a, 132, dy + 15, 'non-linear', { size: 5.5, anchor: 'middle', valign: 'middle', color: NET });
  T(a, 71, dy + dh + 7, 'Gaussian data:\nexactly affine', { size: 5.5, anchor: 'middle', valign: 'middle', color: LIN, lineGap: 1 });
  T(a, 132, dy + dh + 7, 'Gaussian data:\nnone', { size: 5.5, anchor: 'middle', valign: 'middle', color: NET, lineGap: 1 });

  // network narrower than the latent (neck drawn to scale: 512 / 5320)
  const bx = 8, bw = aw - 16;                       // latent bar
  const ty = 66, bh = 7;
  const cx = bx + bw / 2;
  L.rect(a, bx, ty, bw, bh, { fill: '#fff', stroke: INK, width: 0.5 });
  modeBar(a, bx + 2, ty + 1.2, bw - 4);
  T(a, cx, ty - 5, '**Latent** *x*: 5320 dimensions', { size: 6, anchor: 'middle', valign: 'middle' });
  const nw = bw * 512 / 5320, ny = ty + bh + 22, nh = 12;
  L.polygon(a, [[bx, ty + bh], [bx + bw, ty + bh], [cx + nw / 2, ny], [cx - nw / 2, ny]], { fill: '#EFEFEF', stroke: MID, width: 0.4 });
  L.rect(a, cx - nw / 2, ny, nw, nh, { fill: NET, stroke: NET, width: 0.5 });
  const by = ny + nh + 22;
  L.polygon(a, [[cx - nw / 2, ny + nh], [cx + nw / 2, ny + nh], [bx + bw, by], [bx, by]], { fill: '#EFEFEF', stroke: MID, width: 0.4 });
  L.rect(a, bx, by, bw, bh, { fill: '#fff', stroke: INK, width: 0.5 });
  modeBar(a, bx + 2, by + 1.2, bw - 4);
  T(a, cx, by + bh + 5, '**Velocity** *v*: 5320 dimensions', { size: 6, anchor: 'middle', valign: 'middle' });
  T(a, cx + nw / 2 + 4, ny + nh / 2, '**Network**: width 512', { size: 6, anchor: 'start', valign: 'middle', color: NET });
  // linear part tries to cross the neck
  L.arrow(a, [cx - 12, ty + bh + 3], [cx - 3, ny - 2], { stroke: LIN, width: 1.1, dash: '2.2 1.4', head: 3 });
  T(a, cx - 14, ty + bh + 8, 'linear part', { size: 5.5, anchor: 'end', color: LIN, halo: true });
  L.line(a, [cx - 5.5, ny + 0.5], [cx + 0.5, ny + 6.5], { stroke: INK, width: 1, cap: 'round' });
  L.line(a, [cx - 5.5, ny + 6.5], [cx + 0.5, ny + 0.5], { stroke: INK, width: 1, cap: 'round' });
  // (the cross sits on the neck: drawn in white halo for contrast)
  L.arrow(a, [cx + 2.2, ny + nh + 3], [cx + 2.2, by - 2], { stroke: NET, width: 1.1, head: 3 });
  T(a, cx, by + bh + 14, '*Conjecture*: a network narrower than the latent', { size: 5.5, anchor: 'middle', color: INK });
  T(a, cx, by + bh + 21, 'cannot carry the linear part (width scan pending)', { size: 5.5, anchor: 'middle', color: INK });
  T(a, cx + 6, ny + nh + 9, 'the rest', { size: 5.5, anchor: 'start', color: NET, halo: true });
  // measured evidence: flow-matching loss against the exact linear field
  const ey = 218, lo = 1.55, hi = 1.65, lxp = (v) => bx + (v - lo) / (hi - lo) * bw;
  T(a, cx, ey - 22, '**Measured**: flow-matching loss', { size: 6, anchor: 'middle', valign: 'middle' });
  L.line(a, [bx, ey], [bx + bw, ey], { stroke: INK, width: 0.5 });
  L.rect(a, lxp(1.60), ey - 5, lxp(1.63) - lxp(1.60), 5, { fill: NET, stroke: NET, width: 0.4 });
  L.line(a, [lxp(Math.PI / 2), ey - 9], [lxp(Math.PI / 2), ey + 3], { stroke: LIN, width: 1.1 });
  T(a, lxp(Math.PI / 2) - 2, ey - 12, 'exact linear field, π/2 ≈ 1.571', { size: 5.5, anchor: 'start', valign: 'middle', color: LIN });
  T(a, lxp(1.615), ey + 8, 'W0–W6: 1.60–1.63', { size: 5.5, anchor: 'middle', valign: 'middle', color: NET });
  T(a, cx, ey + 24, 'Samples over-dispersed:', { size: 5.5, anchor: 'middle', valign: 'middle', weight: 'bold' });
  T(a, cx, ey + 31, '2–3× too many null points; dE/dt', { size: 5.5, anchor: 'middle', valign: 'middle' });
  T(a, cx, ey + 38, 'fluctuations 2–14× the reference', { size: 5.5, anchor: 'middle', valign: 'middle' });

  // =====================================================================================================
  // panel b: four remedies, on the same glyphs, with their numbers
  // =====================================================================================================
  const b = F.panel('b', { x: 69, y: 0, w: 114, h: 104 });
  const bW = b.w;
  T(b, 12, 6, '**Four remedies** on the same glyphs', { size: 6.5, valign: 'middle' });

  // shared log axis for "energy distance / floor"
  const axX = 188, axW = bW - axX - 6;
  const lx = (v) => axX + (Math.log10(v) / 3) * axW;
  const axY = 30;
  T(b, axX + axW / 2, 8, '**Energy distance / noise floor**', { size: 5.5, anchor: 'middle', valign: 'middle' });
  T(b, axX + axW / 2, 15, '(log scale; held-out η)', { size: 5, anchor: 'middle', valign: 'middle', color: MID });
  L.line(b, [axX, axY], [axX + axW, axY], { stroke: INK, width: 0.5 });
  for (const [v, s] of [[1, '1'], [10, '10'], [100, '100'], [1000, '1000']]) {
    L.line(b, [lx(v), axY], [lx(v), axY + 2], { stroke: INK, width: 0.5 });
    T(b, lx(v), axY + 6, s, { size: 5, anchor: 'middle', valign: 'middle' });
  }
  // first generators band (5 seeds, GPU)
  const rowH = 55.5, r0 = 34;
  // baseline row
  L.rect(b, lx(177), axY - 7, lx(519) - lx(177), 4.5, { fill: '#C9C9C9', stroke: MID, width: 0.4 });
  T(b, lx(177) - 3, axY - 4.8, 'W0–W6: 177–519 (first generators)', { size: 5.5, anchor: 'end', valign: 'middle', weight: 'bold' });

  // component glyphs
  const bh2 = 15;
  const exact = (p, x, y, w, lab) => { box(p, x, y, w, bh2, LIN, LIN); T(p, x + w / 2, y + bh2 / 2, lab, { size: 5.5, anchor: 'middle', valign: 'middle', color: '#fff', lineGap: 1 }); };
  const learned = (p, x, y, w, lab) => { box(p, x, y, w, bh2, '#D6EEE6', LIN, { dash: '2 1.2', width: 0.8 }); T(p, x + w / 2, y + bh2 / 2, lab, { size: 5.5, anchor: 'middle', valign: 'middle', color: LIN, lineGap: 1 }); };
  const net = (p, x, y, w, lab) => { box(p, x, y, w, bh2, NET, NET); T(p, x + w / 2, y + bh2 / 2, lab, { size: 5.5, anchor: 'middle', valign: 'middle', color: '#fff' }); };
  const plus = (p, x, y) => T(p, x, y + bh2 / 2, '+', { size: 8, anchor: 'middle', valign: 'middle' });
  const rows = [
    { id: 'G0', title: 'no network', pts: [3.3], good: ['spectra, energy balance (residual 0.002)'], bad: ['3.3× too many null points; restart drift 0.21'] },
    { id: 'W9', title: 'learned affine + network', pts: [9.1, 10.6], good: ['fewer spurious nulls (error 1.7); drift 0.12'], bad: ['spectra and balance behind G0'] },
    { id: 'W10', title: 'exact Gaussian field + network', pts: [44.7, 46.3], good: [], bad: ['worse: the network’s linear part perturbs', 'the second-order statistics of the Gaussian field'] },
    { id: 'W11', title: 'exact field + learned affine + network', pts: [9.3, 7.6], good: ['fewer spurious nulls (error 1.7); drift 0.12'], bad: ['spectra and balance behind G0'] },
  ];
  rows.forEach((r, i) => {
    const y0 = r0 + i * 17.5 * 1.0 * 1.0 + 0;
    const y = 46 + i * 62;
    if (i > 0) L.line(b, [0, y - 6], [bW, y - 6], { stroke: C.faint, width: 0.5 });
    T(b, 0, y + 1, r.id, { size: 8, weight: 'bold', anchor: 'start', valign: 'middle' });
    T(b, 0, y + 10, r.id === 'G0' ? '' : '', {});
    const gx = 26, gy = y - 6;
    if (r.id === 'G0') {
      box(b, gx, gy, 118, bh2, LIN, LIN);
      T(b, gx + 59, gy + bh2 / 2, 'Gaussian law per mode: mean + 8×8 covariance', { size: 5.5, anchor: 'middle', valign: 'middle', color: '#fff' });
    } else if (r.id === 'W9') {
      learned(b, gx, gy, 58, 'learned *G*(*t*, η) *x* + *b*'); plus(b, gx + 63, gy); net(b, gx + 68, gy, 50, 'network');
    } else if (r.id === 'W10') {
      exact(b, gx, gy, 58, 'exact Gaussian field'); plus(b, gx + 63, gy); net(b, gx + 68, gy, 50, 'network');
    } else {
      exact(b, gx, gy, 38, 'exact\nGaussian'); plus(b, gx + 42.5, gy); learned(b, gx + 47, gy, 38, 'learned\naffine'); plus(b, gx + 89.5, gy); net(b, gx + 94, gy, 40, 'network');
    }
    T(b, gx, gy + bh2 + 5.5, r.title, { size: 5.5, anchor: 'start', valign: 'middle', color: MID, italic: true });
    // dots on the shared axis
    const ay = gy + bh2 / 2;
    L.line(b, [lx(1), ay], [lx(1), ay], {});
    L.line(b, [axX, ay + 8], [axX + axW, ay + 8], { stroke: C.faint, width: 0.4 });
    r.pts.forEach((v) => L.circle(b, lx(v), ay + 8, 2.1, { fill: NET, stroke: '#fff', width: 0.4 }));
    T(b, axX + axW / 2, ay - 4, r.pts.map((v) => v.toString()).join(' and ') + '×', { size: 6, anchor: 'middle', valign: 'middle', weight: 'bold' });
    // right / wrong
    let ty2 = gy + bh2 + 13;
    r.good.forEach((s) => { tick(b, 4, ty2, true); T(b, 12, ty2, s, { size: 5.5, anchor: 'start', valign: 'middle' }); ty2 += 8; });
    r.bad.forEach((s, k) => { if (k === 0) tick(b, 4, ty2, false); T(b, 12, ty2, s, { size: 5.5, anchor: 'start', valign: 'middle' }); ty2 += 7.5; });
  });
  // floor line over the dot rows
  L.line(b, [lx(1), axY], [lx(1), 46 + 3 * 62 + 22], { stroke: INK, width: 0.5, dash: '1.2 1.2' });
  T(b, bW, 104 * 2.835 - 4, '2 seeds, CPU (W0–W6: 5 seeds, GPU)', { size: 5.5, anchor: 'end', valign: 'middle', color: MID, italic: true });
}
