// Figure "solver": one step of the 3D MHD pseudo-spectral solver (Fourier ↔ physical space loop),
// the life of a simulation on a time axis, and what is written (MFF file ↔ catalog).
// Hero: none (computation loop drawn flat, P25); |u| slice of Taylor–Green and integrating
// factor computed (analytic forms). Sources: docs/facts.md.

export const K = {
  u: '#0072B2', uL: '#dcebf6', B: '#D55E00', BL: '#fbe3d3', lam: '#009E73',
  ink: '#2b2b2b', sub: '#555555', mid: '#7a7a7a', light: '#bdbdbd', faint: '#ececec',
  four: '#eef2f6', fourEdge: '#c3cdd7', phys: '#ffffff', physEdge: '#d3d6da',
  op: '#f7f7f7', opEdge: '#9aa3ab', badge: '#4d4d4d',
  cat: '#E3E8EE', catEdge: '#A9B4C0', catInk: '#34414e', fil: '#EDE8E0', filEdge: '#BDB2A2', filInk: '#4a4136',
  well: '#8a8f94',
};
export const MONO = "'DejaVu Sans Mono', 'Liberation Mono', Consolas, monospace";
export const esc = (s) => s.replace(/([_*^{])/g, '\\$1');
export function mono(L, p, x, y, s, o = {}) { return L.text(p, x, y, esc(s), { size: 5.5, family: MONO, color: K.ink, ...o }); }

const T = {
  fr: {
    a: 'One time step', b: 'One simulation over time', c: 'What is written',
    four: 'Fourier space', phys: 'Physical space', grid: '64³ grid',
    dealias: '2/3 dealiasing', leray: 'Leray projection', rk4: 'Lawson RK4', x4: '4 evaluations per step',
    after: 'then: random forcing, periodic projection', state: 'state',
    diag: 'diagnostics every 0.1', snaps: '40 snapshots (u, B)', burn: 'burn-in', keep: 'kept window',
    ckpt: 'checkpoint (every 900 s of compute)', sig: 'SIGTERM: checkpoint, then resume',
    resume: 'resume', opt: 'optional', attrs: 'attributes', theWell: 'The Well', milady: 'MilaDy', wellNote: 'in grey: The Well convention',
  },
  en: {
    a: 'One time step', b: 'One simulation over time', c: 'What is written',
    four: 'Fourier space', phys: 'Physical space', grid: '64³ grid',
    dealias: '2/3 dealiasing', leray: 'Leray projection', rk4: 'Lawson RK4', x4: '4 evaluations per step',
    after: 'then: random forcing, periodic projection', state: 'state',
    diag: 'diagnostics every 0.1', snaps: '40 snapshots (u, B)', burn: 'burn-in', keep: 'kept window',
    ckpt: 'checkpoint (every 900 s of compute)', sig: 'SIGTERM: checkpoint, then resume',
    resume: 'resume', opt: 'optional', attrs: 'attributes', theWell: 'The Well', milady: 'MilaDy', wellNote: 'in grey: The Well convention',
  },
};

const tgSpeed = (X, Y) => Math.sqrt(Math.sin(2 * X) ** 2 * Math.cos(2 * Y) ** 2 + Math.cos(2 * X) ** 2 * Math.sin(2 * Y) ** 2);

// plane of modes (kx, ky) with 11 × 11 points: kept modes (|m| ≤ 3 out of 5, image of the 21-out-of-32 cutoff) filled,
// cut modes pale (state) or empty rings (after the mask)
function modePlane(L, p, cx, cy, s, color, { cut = 'faint', frame = true } = {}) {
  const n = 11, d = s / (n - 1), r = Math.min(0.32 * d, L.mm(0.32)), x0 = cx - s / 2, y0 = cy - s / 2;
  if (frame) L.rect(p, x0 - d * 0.7, y0 - d * 0.7, s + 1.4 * d, s + 1.4 * d, { r: L.mm(0.6), fill: '#ffffff', stroke: K.fourEdge, width: 0.4 });
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const mi = i - 5, mj = j - 5, kept = Math.abs(mi) <= 3 && Math.abs(mj) <= 3;
    const x = x0 + i * d, y = y0 + j * d;
    if (kept) L.circle(p, x, y, r, { fill: color, stroke: 'none' });
    else if (cut === 'ring') L.circle(p, x, y, r * 0.9, { fill: 'none', stroke: K.light, width: 0.3 });
    else L.circle(p, x, y, r * 0.7, { fill: '#d5d9dd', stroke: 'none' });
  }
  if (cut === 'ring') {
    const h = 3.5 * d;
    L.rect(p, cx - h, cy - h, 2 * h, 2 * h, { fill: 'none', stroke: K.sub, width: 0.45, dash: '1.2 0.7' });
  }
}
function opBox(L, p, x, y, w, h, str, o = {}) {
  L.rect(p, x, y, w, h, { r: L.mm(1.2), fill: o.fill ?? K.op, stroke: o.stroke ?? K.opEdge, width: 0.45 });
  if (str) L.text(p, x + w / 2, y + h / 2, str, { size: o.size ?? 6, anchor: 'middle', valign: 'middle', color: o.color ?? K.ink, weight: o.weight });
}
function badge(L, p, cx, cy, r, s, fill = K.badge) {
  L.circle(p, cx, cy, r, { fill, stroke: 'none' });
  L.text(p, cx, cy, s, { size: 5.2, weight: 'bold', color: '#ffffff', anchor: 'middle', valign: 'middle' });
}

// ------------------------------------------------------------------------------------ a: one step
// coordinates in mm in the panel (183 × 62); Fourier on the left (x 1–121), physical space on the right (x 123–182)
export function stepCycle(F, L, p, S) {
  const m = L.mm, M = (x, y) => [m(x), m(y)];
  const FX1 = 121, PX0 = 123, TOP = 9.4, BOT = 61.4;
  L.rect(p, m(1), m(TOP), m(FX1 - 1), m(BOT - TOP), { r: m(2), fill: K.four, stroke: K.fourEdge, width: 0.5 });
  L.rect(p, m(PX0), m(TOP), m(182 - PX0), m(BOT - TOP), { r: m(2), fill: K.phys, stroke: K.physEdge, width: 0.5 });
  L.text(p, m(3), m(TOP + 3.4), S.four, { size: 6.2, weight: 'bold', color: '#4f5b66' });
  L.text(p, m(PX0 + 2), m(TOP + 3.4), S.phys, { size: 6.2, weight: 'bold', color: '#4f5b66' });
  // equations solved (two relations, P19)
  const u = `{${K.u}|**u**}`, w = `{${K.u}|**ω**}`, j = `{${K.B}|**j**}`, b = `{${K.B}|**B**}`;
  L.text(p, m(54), m(4.8), `∂_{t}${u} = ${u} × ${w} + ${j} × ${b} − ∇Π + ν∇²${u} + **f**`, { size: 6.3, valign: 'middle' });
  L.text(p, m(124), m(4.8), `∂_{t}${b} = ∇ × (${u} × ${b}) + η∇²${b}`, { size: 6.3, valign: 'middle' });

  // state (û, B̂): two planes of modes; the modes outside the 2/3 cube are zero (pale)
  const sy = 21.4;
  modePlane(L, p, m(12.4), m(sy), m(8.4), K.u);
  modePlane(L, p, m(24.0), m(sy), m(8.4), K.B);
  L.text(p, m(18.2), m(29.6), `{${K.u}|**û**}, {${K.B}|**B̂**}`, { size: 6.4, anchor: 'middle', valign: 'middle' });
  mono(L, p, m(18.2), m(32.3), '(n_traj, 3, 64, 64, 33)', { size: 5.0, anchor: 'middle', valign: 'middle', color: K.sub });
  // curls in Fourier space
  opBox(L, p, m(42), m(sy - 3.2), m(9.4), m(6.4), 'ik×', { size: 6.4 });
  F.anchor('st.r', p, m(29.6), m(sy)); F.anchor('cu.l', p, m(41.6), m(sy));
  F.relate('st.r', 'cu.l', 'flow'); L.connect(F, 'st.r', 'cu.l', { stroke: '#7f7f7f', width: 0.6, head: 2 });
  // transform to physical space
  F.anchor('if.a', p, m(51.8), m(sy)); F.anchor('if.b', p, m(129.4), m(sy));
  F.relate('if.a', 'if.b', 'irfftn'); L.connect(F, 'if.a', 'if.b', { stroke: K.ink, width: 0.75, head: 2.4 });
  mono(L, p, m(90), m(sy - 1.7), 'irfftn', { anchor: 'middle', size: 5.8, color: K.ink, halo: true });
  // fields on the grid: computed |u| slice of Taylor–Green (kf = 2)
  const ts = m(12.4), tx = m(130), ty = m(sy) - ts / 2;
  const N = 36, lerp = (v) => L.ramp(['#fbfbfb', '#d9dde1', '#9aa3ab', '#4f5862'], Math.min(1, Math.max(0, v)));
  for (let i = 0; i < N; i++) for (let k = 0; k < N; k++) {
    const v = tgSpeed(2 * Math.PI * (i + 0.5) / N, 2 * Math.PI * (k + 0.5) / N);
    L.rect(p, tx + i * ts / N, ty + k * ts / N, ts / N + 0.05, ts / N + 0.05, { fill: lerp(v), stroke: 'none' });
  }
  L.rect(p, tx, ty, ts, ts, { fill: 'none', stroke: K.ink, width: 0.45 });
  L.text(p, m(144.6), m(sy - 1.6), `${u}, ${b}, ${w}, ${j}`, { size: 6.4, valign: 'middle' });
  L.text(p, m(144.6), m(sy + 1.9), S.grid, { size: 5.6, color: K.sub, valign: 'middle' });
  // products, rotational form
  const qx = 130, qy = 45.6, qw = 36, qh = 11;
  opBox(L, p, m(qx), m(qy - qh / 2), m(qw), m(qh), '');
  L.text(p, m(qx + qw / 2), m(qy - 2.4), `${u} × ${w} + ${j} × ${b}`, { size: 6.4, anchor: 'middle', valign: 'middle' });
  L.text(p, m(qx + qw / 2), m(qy + 2.5), `${u} × ${b}`, { size: 6.4, anchor: 'middle', valign: 'middle' });
  F.anchor('pr.t', p, m(136.2), m(sy + 6.6)); F.anchor('pr.in', p, m(136.2), m(qy - qh / 2 - 0.4));
  F.relate('pr.t', 'pr.in', 'flow'); L.connect(F, 'pr.t', 'pr.in', { stroke: '#7f7f7f', width: 0.6, head: 2 });
  // back to Fourier space, then 2/3 dealiasing
  const dX = 102, dY = 45.6;
  F.anchor('ff.a', p, m(qx - 0.6), m(qy)); F.anchor('ff.b', p, m(dX + 6.4), m(dY));
  F.relate('ff.a', 'ff.b', 'rfftn'); L.connect(F, 'ff.a', 'ff.b', { stroke: K.ink, width: 0.75, head: 2.4 });
  mono(L, p, m(118.6), m(qy - 1.7), 'rfftn', { anchor: 'middle', size: 5.8, color: K.ink, halo: true });
  modePlane(L, p, m(dX), m(dY), m(8.4), K.ink, { cut: 'ring' });
  L.text(p, m(dX), m(dY + 7.6), S.dealias, { size: 5.9, anchor: 'middle', valign: 'middle' });
  mono(L, p, m(dX), m(dY + 10.2), '|m| ≤ 21', { size: 5.0, anchor: 'middle', valign: 'middle', color: K.sub });
  // momentum branch: Leray projection (decomposition along k)
  {
    const ox = 58.0, oy = 41.6;
    const k = [m(6.2), -m(1.8)], v = [m(3.4), -m(5.0)];
    const kk = k[0] * k[0] + k[1] * k[1], dot = (v[0] * k[0] + v[1] * k[1]) / kk;
    const par = [dot * k[0], dot * k[1]], perp = [v[0] - par[0], v[1] - par[1]];
    const O = M(ox, oy);
    L.arrow(p, O, [O[0] + k[0], O[1] + k[1]], { stroke: K.mid, width: 0.5, head: 1.6 });
    L.text(p, O[0] + k[0] + m(0.7), O[1] + k[1] + m(0.2), 'k', { size: 5.6, italic: true, color: K.mid, valign: 'middle' });
    L.line(p, [O[0] + v[0], O[1] + v[1]], [O[0] + perp[0], O[1] + perp[1]], { stroke: K.mid, width: 0.4, dash: '0.9 0.6' });
    L.arrow(p, O, [O[0] + v[0], O[1] + v[1]], { stroke: K.ink, width: 0.5, head: 1.6 });
    L.arrow(p, O, [O[0] + perp[0], O[1] + perp[1]], { stroke: K.u, width: 0.85, head: 1.9 });
    L.text(p, m(68.2), m(35.6), S.leray, { size: 5.9, valign: 'middle' });
    L.text(p, m(68.2), m(38.6), 'P = I − kkᵀ/|k|²', { size: 5.7, italic: true, valign: 'middle', color: K.sub });
  }
  // induction branch: curl in Fourier space
  opBox(L, p, m(60), m(52.6 - 2.9), m(15), m(5.8), 'ik × ( · )', { size: 5.9 });
  F.anchor('de.uo', p, m(dX - 6.6), m(dY - 2.0)); F.anchor('le.i', p, m(89.6), m(37.4));
  F.anchor('de.bo', p, m(dX - 6.6), m(dY + 2.4)); F.anchor('in.i', p, m(75.4), m(52.6));
  F.relate('de.uo', 'le.i', 'flow'); L.connect(F, 'de.uo', 'le.i', { stroke: '#7f7f7f', width: 0.6, head: 2 });
  F.relate('de.bo', 'in.i', 'flow'); L.connect(F, 'de.bo', 'in.i', { stroke: '#7f7f7f', width: 0.6, head: 2 });
  // Lawson RK4: combines the right-hand sides N̂_u, N̂_B (+ constant forcing f̂)
  const rx = 4, ry = 38.0, rw = 31, rh = 19.4;
  L.rect(p, m(rx), m(ry), m(rw), m(rh), { r: m(1.4), fill: '#ffffff', stroke: K.ink, width: 0.7 });
  L.text(p, m(rx + 2), m(ry + 3.4), S.rk4, { size: 6.4, weight: 'bold', valign: 'middle' });
  L.text(p, m(rx + 2), m(ry + 6.4), S.x4, { size: 5.5, color: K.sub, valign: 'middle' });
  {
    const gx = m(rx + 2.4), gy = m(ry + 9.0), gw = m(9.0), gh = m(6.0);
    L.polyline(p, [[gx, gy], [gx, gy + gh], [gx + gw, gy + gh]], { fill: 'none', stroke: K.mid, width: 0.4 });
    L.polyline(p, L.sample((t) => gy + gh - gh * 0.92 * Math.exp(-3.2 * t * t), 0, 1, 24).map(([t, y]) => [gx + gw * t, y]), { fill: 'none', stroke: K.ink, width: 0.65 });
    L.text(p, gx + gw, gy + gh + m(1.7), 'k', { size: 5, italic: true, anchor: 'end', color: K.mid, valign: 'middle' });
    L.text(p, gx + gw + m(1.6), gy + m(1.6), 'e^{−νk²Δt}', { size: 5.6, italic: true, valign: 'middle', color: K.sub });
    L.text(p, gx + gw + m(1.6), gy + m(4.6), 'e^{−ηk²Δt}', { size: 5.6, italic: true, valign: 'middle', color: K.sub });
  }
  // inputs of the combination
  F.anchor('nu.a', p, m(56.6), m(41.6)); F.anchor('nu.b', p, m(rx + rw + 0.4), m(41.6));
  F.anchor('nb.a', p, m(59.6), m(52.6)); F.anchor('nb.b', p, m(rx + rw + 0.4), m(52.6));
  F.relate('nu.a', 'nu.b', 'flow'); L.connect(F, 'nu.a', 'nu.b', { stroke: '#7f7f7f', width: 0.6, head: 2 });
  F.relate('nb.a', 'nb.b', 'flow'); L.connect(F, 'nb.a', 'nb.b', { stroke: '#7f7f7f', width: 0.6, head: 2 });
  L.text(p, m(46.0), m(40.0), `{${K.u}|**N̂**_{u}} + **f̂**`, { size: 5.9, anchor: 'middle', valign: 'middle' });
  L.text(p, m(47.6), m(51.0), `{${K.B}|**N̂**_{B}}`, { size: 5.9, anchor: 'middle', valign: 'middle' });
  // the loop closes on the state (P11: thick return, distinct from the flow)
  F.anchor('rk.t', p, m(18.2), m(ry - 0.4)); F.anchor('st.b', p, m(18.2), m(33.8));
  F.relate('rk.t', 'st.b', 'feedback'); L.connect(F, 'rk.t', 'st.b', { stroke: K.ink, width: 1.2, head: 2.8 });
  L.text(p, m(3), m(BOT - 1.8), S.after, { size: 5.5, color: K.sub });
}

// ------------------------------------------------------------------------------- b: the timeline
export function timeline(F, L, p, S, X0, Y0, W) {
  const m = L.mm, t0 = X0 + m(5), t1 = X0 + W - m(4), X = (t) => t0 + (t1 - t0) * t / 140;
  const yRun = Y0 + m(4.2), yDiag = Y0 + m(10.6), ySnap = Y0 + m(14.8), yAx = Y0 + m(18.8);
  const ti = 63;
  const chip = (x, y, s, stroke, color) => {
    const w = m(s.length * 1.2 + 2.4);
    L.rect(p, x, y - m(1.9), w, m(3.8), { r: m(1.9), fill: '#ffffff', stroke, width: 0.45 });
    mono(L, p, x + w / 2, y, s, { size: 5.2, anchor: 'middle', valign: 'middle', color });
    return w;
  };
  chip(X0 - m(3.4), yRun - m(4.4), 'queued', K.opEdge, K.sub);
  L.rect(p, X(0), yRun - m(1.3), X(ti) - X(0), m(2.6), { r: m(1.3), fill: '#d9dde1', stroke: 'none' });
  L.rect(p, X(ti) + m(2.0), yRun - m(1.3), X(140) - X(ti) - m(2.0), m(2.6), { r: m(1.3), fill: '#d9dde1', stroke: 'none' });
  mono(L, p, X(33), yRun - m(3.7), 'running', { size: 5.2, anchor: 'middle', valign: 'middle', color: K.sub });
  const dia = (x, y) => L.polygon(p, [[x, y - m(1.3)], [x + m(1.3), y], [x, y + m(1.3)], [x - m(1.3), y]], { fill: K.ink, stroke: '#ffffff', width: 0.4 });
  for (const t of [21, 42, 84, 105, 126]) dia(X(t), yRun);
  dia(X(ti) - m(0.6), yRun);
  L.bolt(p, X(ti) - m(1.6), yRun - m(6.6), m(2.6), m(4.2), {});
  L.path(p, `M${X(ti) - m(0.6)},${yRun + m(1.5)} Q${X(ti) + m(0.8)},${yRun + m(3.6)} ${X(ti) + m(2.4)},${yRun + m(1.0)}`, { fill: 'none', stroke: K.ink, width: 0.5 });
  L.chevron(p, [X(ti) + m(2.5), yRun + m(0.9)], [0.45, -0.89], { len: m(0.9), width: 0.5 });
  L.text(p, X(ti) + m(3.0), yRun + m(3.2), S.resume, { size: 5.2, color: K.sub, valign: 'middle' });
  chip(X(140) - m(8.6), yRun - m(4.4), 'done', K.ink, K.ink);
  // diagnostics every 0.1 from t = 0 (continuous comb at this scale)
  L.rect(p, X(0), yDiag - m(0.8), X(140) - X(0), m(1.6), { fill: '#c9ced4', stroke: 'none' });
  L.text(p, X(1), yDiag - m(2.4), S.diag, { size: 5.6, color: K.sub, valign: 'middle' });
  // fields: 40 snapshots over ]100, 140]
  for (let k = 1; k <= 40; k++) L.line(p, [X(100 + k), ySnap - m(1.5)], [X(100 + k), ySnap + m(1.5)], { stroke: k % 2 ? K.u : K.B, width: 0.45 });
  L.text(p, X(100) - m(1.2), ySnap, S.snaps, { size: 5.6, anchor: 'end', valign: 'middle' });
  // simulated-time axis
  L.arrow(p, [X(0), yAx], [X(140) + m(2.6), yAx], { stroke: K.ink, width: 0.5, head: 1.8 });
  for (const t of [0, 100, 140]) {
    L.line(p, [X(t), yAx - m(0.8)], [X(t), yAx + m(0.8)], { stroke: K.ink, width: 0.5 });
    L.text(p, X(t), yAx + m(2.7), String(t), { size: 5.6, anchor: 'middle', valign: 'middle' });
  }
  L.text(p, X(140) + m(3.0), yAx, 't', { size: 6, italic: true, anchor: 'start', valign: 'middle' });
  L.brace(p, [X(0) + m(0.5), yAx + m(4.6)], [X(100) - m(0.6), yAx + m(4.6)], { depth: m(1.3), side: 1, label: S.burn, size: 5.6 });
  L.brace(p, [X(100) + m(0.6), yAx + m(4.6)], [X(140) - m(0.4), yAx + m(4.6)], { depth: m(1.3), side: 1, label: S.keep, size: 5.6 });
  const ly = yAx + m(11.6);
  dia(X0 + m(1.4), ly); L.text(p, X0 + m(3.6), ly, S.ckpt, { size: 5.5, valign: 'middle', color: K.sub });
  L.bolt(p, X0 + m(0.3), ly + m(1.5), m(2.2), m(3.2), {});
  L.text(p, X0 + m(3.6), ly + m(3.1), S.sig, { size: 5.5, valign: 'middle', color: K.sub });
}

// ------------------------------------------------------------------------ c: file ↔ catalog
export function mapping(F, L, p, S, X0, Y0, W) {
  const m = L.mm, fw = W * 0.53, tx0 = X0 + W * 0.635, tw = W * 0.365;
  const rows = [
    { s: 'fields.h5', w: 'bold', c: K.ink, lvl: 0, key: 'file' },
    { s: 'dataset_name, grid_type, …', c: K.well, lvl: 1 },
    { s: 'milady_uuid', c: K.ink, lvl: 1, key: 'uuid' },
    { s: 'milady_parameters', c: K.ink, lvl: 1, key: 'par' },
    { s: 'milady_git_commit', c: K.ink, lvl: 1, key: 'git' },
    { s: 'dimensions/', c: K.well, lvl: 1 },
    { s: 'boundary_conditions/', c: K.well, lvl: 1 },
    { s: 't1_fields/', c: K.well, lvl: 1 },
    { s: 'velocity, magnetic_field', c: K.u, lvl: 2 },
    { s: 'milady_diagnostics/', c: K.ink, lvl: 1, key: 'dia' },
    { s: 'milady_spectral/', c: K.ink, lvl: 1 },
  ];
  const rh = m(2.95), ry = (i) => Y0 + m(2.8) + i * rh;
  const boxH = ry(rows.length - 1) - Y0 + m(2.6);
  L.rect(p, X0, Y0, fw, boxH, { r: m(1.4), fill: K.fil, stroke: K.filEdge, width: 0.45 });
  const pos = {};
  rows.forEach((r, i) => {
    const x = X0 + m(1.6) + r.lvl * m(2.3), y = ry(i);
    if (r.lvl) L.polyline(p, [[x - m(1.5), y - rh * 0.85], [x - m(1.5), y], [x - m(0.4), y]], { fill: 'none', stroke: K.filEdge, width: 0.35 });
    mono(L, p, x, y, r.s, { size: 5.1, valign: 'middle', color: r.c, weight: r.w });
    if (r.key) pos[r.key] = [X0 + fw, y];
  });
  L.text(p, X0 + m(1.6), Y0 + boxH + m(2.4), S.wellNote, { size: 5.3, color: K.sub, valign: 'middle' });
  const tables = [
    { name: 'file', key: 'file', cols: [['uri'], ['sha256'], ['size_bytes'], ['n_t']] },
    { name: 'simulation', cols: [['id', 'uuid'], ['parameters', 'par'], ['git_commit', 'git'], ['status']] },
    { name: 'diagnostic', cols: [['name', 'dia'], ['t'], ['value']] },
  ];
  let y = Y0;
  const tpos = {};
  for (const t of tables) {
    const h = m(3.0) + t.cols.length * m(2.3) + m(0.7);
    L.rect(p, tx0, y, tw, h, { r: m(1.1), fill: K.cat, stroke: K.catEdge, width: 0.45 });
    L.rect(p, tx0, y, tw, m(3.0), { r: m(1.1), fill: '#ccd5df', stroke: 'none' });
    mono(L, p, tx0 + m(1.4), y + m(1.6), t.name, { size: 5.3, weight: 'bold', valign: 'middle', color: K.catInk });
    if (t.key) tpos[t.key] = [tx0, y + m(1.6)];
    t.cols.forEach(([c, key], i) => {
      const yy = y + m(3.0) + m(1.35) + i * m(2.3);
      mono(L, p, tx0 + m(2.0), yy, c, { size: 5.0, valign: 'middle', color: K.catInk });
      if (key) tpos[key] = [tx0, yy];
    });
    y += h + m(1.3);
  }
  for (const key of ['file', 'uuid', 'par', 'git', 'dia']) {
    const a = pos[key], b = tpos[key];
    const mx = (a[0] + b[0]) / 2;
    L.path(p, `M${a[0] + m(0.5)},${a[1]} C${mx},${a[1]} ${mx},${b[1]} ${b[0] - m(0.5)},${b[1]}`, { fill: 'none', stroke: '#7f8a95', width: 0.45 });
    L.circle(p, b[0] - m(0.5), b[1], m(0.35), { fill: '#7f8a95', stroke: 'none' });
  }
}

export function make(lang) {
  const S = T[lang];
  return async function draw(F, L) {
    const m = L.mm;
    const pa = F.panel('a', { x: 0, y: 0, w: 183, h: 62 });
    L.text(pa, 12, 7.6, S.a, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
    stepCycle(F, L, pa, S);
    const pb = F.panel('b', { x: 0, y: 64, w: 92, h: 46 });
    L.text(pb, 12, 7.6, S.b, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
    timeline(F, L, pb, S, m(5), m(9.4), m(84));
    const pc = F.panel('c', { x: 94, y: 64, w: 89, h: 46 });
    L.text(pc, 12, 7.6, S.c, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
    mapping(F, L, pc, S, m(2), m(5.6), m(86));
  };
}
