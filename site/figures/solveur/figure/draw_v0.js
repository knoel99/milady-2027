// Figure « solveur » : un pas du solveur pseudo-spectral MHD 3D (boucle Fourier ↔ espace physique),
// la vie d'une simulation sur un axe de temps, et ce qui est écrit (fichier MFF ↔ catalogue).
// Hero : aucun (boucle de calcul dessinée à plat, P25) ; tranche de |u| de Taylor–Green et facteur
// intégrant calculés (formes analytiques). Sources : docs/facts.md.

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
    a: 'Un pas de temps', b: 'Une simulation dans le temps', c: 'Ce qui est écrit',
    four: 'Espace de Fourier', phys: 'Espace physique', grid: 'grille 64³',
    dealias: 'désaliasage 2/3', leray: 'projection de Leray', rk4: 'RK4 de Lawson', x4: '4 évaluations par pas',
    after: 'puis : forçage aléatoire, nettoyage ∇·', state: 'état',
    diag: 'diagnostics tous les 0,1', snaps: '40 instantanés (u, B)', burn: 'mise en régime', keep: 'fenêtre gardée',
    ckpt: 'point de contrôle (toutes les 900 s de calcul)', sig: 'SIGTERM : point de contrôle, puis reprise',
    resume: 'reprise', opt: 'facultatif', attrs: 'attributs', theWell: 'The Well', milady: 'MilaDy',
  },
  en: {
    a: 'One time step', b: 'One simulation over time', c: 'What is written',
    four: 'Fourier space', phys: 'Physical space', grid: '64³ grid',
    dealias: '2/3 dealiasing', leray: 'Leray projection', rk4: 'Lawson RK4', x4: '4 evaluations per step',
    after: 'then: random forcing, ∇· clean-up', state: 'state',
    diag: 'diagnostics every 0.1', snaps: '40 snapshots (u, B)', burn: 'burn-in', keep: 'kept window',
    ckpt: 'checkpoint (every 900 s of compute)', sig: 'SIGTERM: checkpoint, then resume',
    resume: 'resume', opt: 'optional', attrs: 'attributes', theWell: 'The Well', milady: 'MilaDy',
  },
};

const tgSpeed = (X, Y) => Math.sqrt(Math.sin(2 * X) ** 2 * Math.cos(2 * Y) ** 2 + Math.cos(2 * X) ** 2 * Math.sin(2 * Y) ** 2);

// plan de modes (kx, ky) à 11 × 11 points : modes gardés (|m| ≤ 3 sur 5, image de la coupure 21 sur 32) pleins,
// modes coupés pâles (état) ou en anneaux vides (après le masque)
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

// ------------------------------------------------------------------------------------ a : un pas
export function stepCycle(F, L, p, S, X0, Y0, W, H) {
  const m = L.mm, fx = (f) => X0 + f * W, fy = (f) => Y0 + f * H, mid = fx(0.515);
  // régions
  L.rect(p, fx(0), fy(0.10), mid - m(1.2) - fx(0), fy(1) - fy(0.10), { r: m(2), fill: K.four, stroke: K.fourEdge, width: 0.5 });
  L.rect(p, mid + m(1.2), fy(0.10), fx(1) - mid - m(1.2), fy(1) - fy(0.10), { r: m(2), fill: K.phys, stroke: K.physEdge, width: 0.5 });
  L.text(p, fx(0) + m(2), fy(0.10) + m(3.4), S.four, { size: 6.2, weight: 'bold', color: '#4f5b66' });
  L.text(p, mid + m(3.2), fy(0.10) + m(3.4), S.phys, { size: 6.2, weight: 'bold', color: '#4f5b66' });
  // équations (en tête)
  const uB = (s) => s.replace(/\bu\b/g, `{${K.u}|**u**}`);
  L.text(p, fx(0.5), fy(0.04), `∂_{t}{${K.u}|**u**} = {${K.u}|**u**} × {${K.u}|**ω**} + {${K.B}|**j**} × {${K.B}|**B**} − ∇Π + ν∇²{${K.u}|**u**} + **f**        ∂_{t}{${K.B}|**B**} = ∇ × ({${K.u}|**u**} × {${K.B}|**B**}) + η∇²{${K.B}|**B**}`,
    { size: 6.3, anchor: 'middle', valign: 'middle', color: K.ink });
  void uB;

  // état (û, B̂)
  const sx = fx(0.085), sy = fy(0.36), ps = m(8.4);
  modePlane(L, p, sx, sy, ps, K.u);
  modePlane(L, p, sx + m(11.2), sy, ps, K.B);
  L.text(p, sx + m(5.6), sy + m(7.4), `{${K.u}|**û**}, {${K.B}|**B̂**}`, { size: 6.4, anchor: 'middle', valign: 'middle' });
  mono(L, p, sx + m(5.6), sy + m(10.0), '(n_traj, 3, 64, 64, 33)', { size: 5.0, anchor: 'middle', valign: 'middle', color: K.sub });
  F.anchor('st.r', p, sx + m(16.6), sy); F.anchor('st.b', p, sx + m(5.6), sy + m(11.6));

  // rotationnels en Fourier
  const cxx = fx(0.30), cyy = sy;
  opBox(L, p, cxx - m(4.4), cyy - m(3.2), m(8.8), m(6.4), 'ik×', { size: 6.4 });
  L.text(p, cxx, cyy + m(5.6), `{${K.u}|**ω̂**}, {${K.B}|**ĵ**}`, { size: 6, anchor: 'middle', valign: 'middle' });
  F.anchor('cu.l', p, cxx - m(4.6), cyy); F.anchor('cu.r', p, cxx + m(4.6), cyy);
  F.relate('st.r', 'cu.l', 'flow'); L.connect(F, 'st.r', 'cu.l', { stroke: '#7f7f7f', width: 0.6, head: 2 });

  // passage en espace physique
  const px = fx(0.62), py = sy;
  F.anchor('if.a', p, cxx + m(4.8), cyy); F.anchor('if.b', p, px - m(1.2), py);
  F.relate('if.a', 'if.b', 'irfftn'); L.connect(F, 'if.a', 'if.b', { stroke: K.ink, width: 0.7, head: 2.3 });
  mono(L, p, (cxx + px) / 2 + m(2), py - m(1.6), 'irfftn', { anchor: 'middle', size: 5.6, color: K.ink, halo: true });

  // champs sur la grille (tranche de |u| de Taylor–Green, kf = 2)
  const ts = m(11.6), tx = px, ty = py - ts / 2;
  const N = 36, lerp = (v) => L.ramp(['#fbfbfb', '#d9dde1', '#9aa3ab', '#4f5862'], Math.min(1, Math.max(0, v)));
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
    const v = tgSpeed(2 * Math.PI * (i + 0.5) / N, 2 * Math.PI * (j + 0.5) / N);
    L.rect(p, tx + i * ts / N, ty + j * ts / N, ts / N + 0.05, ts / N + 0.05, { fill: lerp(v), stroke: 'none' });
  }
  L.rect(p, tx, ty, ts, ts, { fill: 'none', stroke: K.ink, width: 0.45 });
  L.text(p, tx + ts + m(1.6), py - m(1.5), `{${K.u}|**u**}, {${K.B}|**B**}, {${K.u}|**ω**}, {${K.B}|**j**}`, { size: 6.2, valign: 'middle' });
  L.text(p, tx + ts + m(1.6), py + m(1.7), S.grid, { size: 5.5, color: K.sub, valign: 'middle' });

  // produits (forme rotationnelle)
  const qx = fx(0.70), qy = fy(0.76), qw = m(30), qh = m(10.2);
  opBox(L, p, qx, qy - qh / 2, qw, qh, '');
  L.text(p, qx + qw / 2, qy - m(2.2), `{${K.u}|**u**} × {${K.u}|**ω**} + {${K.B}|**j**} × {${K.B}|**B**}`, { size: 6.2, anchor: 'middle', valign: 'middle' });
  L.text(p, qx + qw / 2, qy + m(2.4), `{${K.u}|**u**} × {${K.B}|**B**}`, { size: 6.2, anchor: 'middle', valign: 'middle' });
  F.anchor('pr.t', p, tx + ts / 2, ty + ts + m(0.4)); F.anchor('pr.in', p, tx + ts / 2, qy - qh / 2 - m(0.4));
  F.relate('pr.t', 'pr.in', 'flow'); L.connect(F, 'pr.t', 'pr.in', { stroke: '#7f7f7f', width: 0.6, head: 2 });

  // retour en Fourier
  const dx_ = fx(0.395), dy_ = qy;
  F.anchor('ff.a', p, qx - m(0.6), qy); F.anchor('ff.b', p, dx_ + m(6.6), dy_);
  F.relate('ff.a', 'ff.b', 'rfftn'); L.connect(F, 'ff.a', 'ff.b', { stroke: K.ink, width: 0.7, head: 2.3 });
  mono(L, p, (qx + dx_) / 2 + m(3), qy - m(1.6), 'rfftn', { anchor: 'middle', size: 5.6, color: K.ink, halo: true });

  // désaliasage 2/3
  modePlane(L, p, dx_, dy_, m(8.4), K.ink, { cut: 'ring' });
  L.text(p, dx_, dy_ + m(7.4), S.dealias, { size: 5.8, anchor: 'middle', valign: 'middle' });
  mono(L, p, dx_, dy_ + m(9.9), '|m| ≤ 21', { size: 5.0, anchor: 'middle', valign: 'middle', color: K.sub });

  // deux branches : Leray (quantité de mouvement) et rotationnel (induction)
  const bx = fx(0.205), byU = fy(0.66), byB = fy(0.88);
  // Leray : décomposition d'un vecteur selon k
  {
    const gx = bx - m(3.0), gy = byU;
    const k = [m(5.0), -m(1.6)], v = [m(3.2), -m(4.2)];
    const kk = k[0] * k[0] + k[1] * k[1], dot = (v[0] * k[0] + v[1] * k[1]) / kk;
    const par = [dot * k[0], dot * k[1]], perp = [v[0] - par[0], v[1] - par[1]];
    L.arrow(p, [gx, gy], [gx + k[0], gy + k[1]], { stroke: K.mid, width: 0.5, head: 1.6 });
    L.text(p, gx + k[0] + m(0.6), gy + k[1] + m(0.5), 'k', { size: 5.4, italic: true, color: K.mid, valign: 'middle' });
    L.line(p, [gx + v[0], gy + v[1]], [gx + perp[0], gy + perp[1]], { stroke: K.mid, width: 0.4, dash: '0.9 0.6' });
    L.arrow(p, [gx, gy], [gx + v[0], gy + v[1]], { stroke: K.ink, width: 0.5, head: 1.6 });
    L.arrow(p, [gx, gy], [gx + perp[0], gy + perp[1]], { stroke: K.u, width: 0.8, head: 1.9 });
    L.text(p, bx + m(4.0), gy - m(3.0), S.leray, { size: 5.8, valign: 'middle' });
    L.text(p, bx + m(4.0), gy - m(0.4), 'P = I − kkᵀ/|k|²', { size: 5.6, italic: true, valign: 'middle', color: K.sub });
    L.text(p, bx + m(4.0), gy + m(2.2), `→ {${K.u}|**N̂**_{u}} (+ **f̂**)`, { size: 5.8, valign: 'middle' });
  }
  {
    const gy = byB;
    opBox(L, p, bx - m(3.6), gy - m(2.9), m(14.6), m(5.8), 'ik × ( · )', { size: 5.8 });
    L.text(p, bx + m(12.6), gy, `→ {${K.B}|**N̂**_{B}}`, { size: 5.8, valign: 'middle' });
  }
  F.anchor('de.uo', p, dx_ - m(6.4), dy_ - m(2.2)); F.anchor('le.i', p, bx + m(22.6), byU - m(1.0));
  F.anchor('de.bo', p, dx_ - m(6.4), dy_ + m(2.2)); F.anchor('in.i', p, bx + m(19.0), byB);
  F.relate('de.uo', 'le.i', 'flow'); L.connect(F, 'de.uo', 'le.i', { stroke: '#7f7f7f', width: 0.6, head: 2 });
  F.relate('de.bo', 'in.i', 'flow'); L.connect(F, 'de.bo', 'in.i', { stroke: '#7f7f7f', width: 0.6, head: 2 });

  // RK4 de Lawson : retour vers l'état (boucle, P11)
  const rx = fx(0.03), ryy = fy(0.77);
  const fa = [sx - m(4.6), byB + m(0.2)], fb = [sx - m(4.6), sy + m(4.6)];
  L.path(p, `M${bx - m(4.0)},${byU + m(1.2)} L${fa[0]},${byU + m(1.2)} M${bx - m(4.0)},${byB} L${fa[0]},${byB} L${fa[0]},${fb[1] + m(1.0)}`, { fill: 'none', stroke: K.ink, width: 1.1, cap: 'round', join: 'round' });
  L.arrow(p, [fa[0], fb[1] + m(1.4)], [fa[0], fb[1] - m(1.6)], { stroke: K.ink, width: 1.1, head: 2.6 });
  void rx; void ryy;
  const lx = fa[0] + m(1.6), ly = fy(0.555);
  L.text(p, lx, ly, S.rk4, { size: 6.2, weight: 'bold', valign: 'middle' });
  L.text(p, lx, ly + m(2.7), S.x4, { size: 5.4, color: K.sub, valign: 'middle' });
  // facteur intégrant : e^{−νk²Δt} (courbe analytique décroissante en k)
  {
    const gx = lx + m(23.4), gy = ly - m(2.8), gw = m(8.6), gh = m(5.4);
    L.polyline(p, [[gx, gy], [gx, gy + gh], [gx + gw, gy + gh]], { fill: 'none', stroke: K.mid, width: 0.4 });
    L.polyline(p, L.sample((t) => gy + gh - gh * 0.92 * Math.exp(-3.2 * t * t), 0, 1, 24).map(([t, y]) => [gx + gw * t, y]), { fill: 'none', stroke: K.ink, width: 0.6 });
    L.text(p, gx + gw + m(0.8), gy + m(1.0), 'e^{−νk²Δt}, e^{−ηk²Δt}', { size: 5.4, italic: true, valign: 'middle', color: K.sub });
    L.text(p, gx + gw, gy + gh + m(1.9), 'k', { size: 5, italic: true, anchor: 'end', color: K.mid });
  }
  L.text(p, fx(0) + m(2.0), fy(1) - m(1.8), S.after, { size: 5.4, color: K.sub });
}

// ------------------------------------------------------------------------------- b : la frise
export function timeline(F, L, p, S, X0, Y0, W) {
  const m = L.mm, t0 = X0 + m(6), t1 = X0 + W - m(3), X = (t) => t0 + (t1 - t0) * t / 140;
  const yRun = Y0 + m(4.0), yDiag = Y0 + m(12.2), ySnap = Y0 + m(17.0), yAx = Y0 + m(21.6);
  // statuts et barres de calcul (exemple d'interruption)
  const ti = 63;
  const chip = (x, y, s, fill, stroke, color) => {
    const w = m(s.length * 1.18 + 2.2);
    L.rect(p, x, y - m(1.9), w, m(3.8), { r: m(1.9), fill, stroke, width: 0.45 });
    mono(L, p, x + w / 2, y, s, { size: 5.0, anchor: 'middle', valign: 'middle', color });
    return w;
  };
  chip(X0 - m(1.0), yRun - m(4.6), 'queued', '#ffffff', K.opEdge, K.sub);
  L.rect(p, X(0), yRun - m(1.3), X(ti) - X(0), m(2.6), { r: m(1.3), fill: '#d9dde1', stroke: 'none' });
  L.rect(p, X(ti) + m(1.4), yRun - m(1.3), X(140) - X(ti) - m(1.4), m(2.6), { r: m(1.3), fill: '#d9dde1', stroke: 'none' });
  mono(L, p, X(30), yRun - m(3.6), 'running', { size: 5.0, anchor: 'middle', valign: 'middle', color: K.sub });
  const dia = (x, y) => L.polygon(p, [[x, y - m(1.3)], [x + m(1.3), y], [x, y + m(1.3)], [x - m(1.3), y]], { fill: K.ink, stroke: '#ffffff', width: 0.4 });
  for (const t of [22, 44, 86, 108, 130]) dia(X(t), yRun);
  dia(X(ti) - m(0.2), yRun);
  L.bolt(p, X(ti) - m(1.3), yRun - m(6.4), m(2.6), m(4.0), {});
  L.arrow(p, [X(ti) + m(0.4), yRun + m(2.6)], [X(ti) + m(2.6), yRun + m(1.4)], { stroke: K.ink, width: 0.5, head: 1.5, bend: -0.6 });
  chip(X(140) - m(9.6), yRun - m(4.6), 'done', '#ffffff', K.ink, K.ink);
  // diagnostics (tous les 0,1 depuis t = 0) : peigne continu
  L.rect(p, X(0), yDiag - m(0.8), X(140) - X(0), m(1.6), { fill: '#c9ced4', stroke: 'none' });
  L.text(p, X(2), yDiag - m(2.3), S.diag, { size: 5.5, color: K.sub, valign: 'middle' });
  // champs : 40 instantanés sur ]100, 140]
  for (let k = 1; k <= 40; k++) L.line(p, [X(100 + k), ySnap - m(1.5)], [X(100 + k), ySnap + m(1.5)], { stroke: k % 2 ? K.u : K.B, width: 0.45 });
  L.text(p, X(100) - m(1.0), ySnap, S.snaps, { size: 5.5, anchor: 'end', valign: 'middle' });
  // axe
  L.arrow(p, [X(0), yAx], [X(140) + m(2.4), yAx], { stroke: K.ink, width: 0.5, head: 1.8 });
  for (const t of [0, 100, 140]) {
    L.line(p, [X(t), yAx - m(0.8)], [X(t), yAx + m(0.8)], { stroke: K.ink, width: 0.5 });
    L.text(p, X(t), yAx + m(2.8), String(t), { size: 5.5, anchor: 'middle', valign: 'middle' });
  }
  L.text(p, X(140) + m(2.6), yAx + m(2.8), 't', { size: 5.8, italic: true, anchor: 'start', valign: 'middle' });
  L.brace(p, [X(0) + m(0.5), yAx + m(5.0)], [X(100) - m(0.5), yAx + m(5.0)], { depth: m(1.4), side: 1, label: S.burn });
  L.brace(p, [X(100) + m(0.5), yAx + m(5.0)], [X(140) - m(0.5), yAx + m(5.0)], { depth: m(1.4), side: 1, label: S.keep });
  // légende des signes
  const ly = yAx + m(13.4);
  dia(X0 + m(1.4), ly); L.text(p, X0 + m(3.4), ly, S.ckpt, { size: 5.4, valign: 'middle', color: K.sub });
  L.bolt(p, X0 + m(0.4), ly + m(1.6), m(2.0), m(3.0), {});
  L.text(p, X0 + m(3.4), ly + m(3.2), S.sig, { size: 5.4, valign: 'middle', color: K.sub });
  return { X, yAx };
}

// ------------------------------------------------------------------------ c : fichier ↔ catalogue
export function mapping(F, L, p, S, X0, Y0, W, H) {
  const m = L.mm;
  const fx0 = X0, fw = W * 0.50, tx0 = X0 + W * 0.60, tw = W * 0.40;
  // arbre du fichier
  const rows = [
    { s: 'fields.h5', w: 'bold', c: K.ink, lvl: 0 },
    { s: 'dataset_name, grid_type…', c: K.well, lvl: 1, part: 'well' },
    { s: 'milady_uuid', c: K.ink, lvl: 1, part: 'mil', key: 'uuid' },
    { s: 'milady_parameters', c: K.ink, lvl: 1, part: 'mil', key: 'par' },
    { s: 'milady_git_commit', c: K.ink, lvl: 1, part: 'mil', key: 'git' },
    { s: 'dimensions/', c: K.well, lvl: 1, part: 'well' },
    { s: 'boundary_conditions/', c: K.well, lvl: 1, part: 'well' },
    { s: 't1_fields/ velocity, magnetic_field', c: K.u, lvl: 1, part: 'well' },
    { s: 'milady_diagnostics/', c: K.ink, lvl: 1, part: 'mil', key: 'dia' },
    { s: 'milady_spectral/', c: K.ink, lvl: 1, part: 'mil' },
  ];
  const rh = m(3.25), ry = (i) => Y0 + m(3.0) + i * rh;
  L.rect(p, fx0, Y0, fw, ry(rows.length - 1) - Y0 + m(3.2), { r: m(1.4), fill: K.fil, stroke: K.filEdge, width: 0.45 });
  const pos = {};
  rows.forEach((r, i) => {
    const x = fx0 + m(1.6) + r.lvl * m(2.4), y = ry(i);
    if (r.lvl) L.polyline(p, [[fx0 + m(2.4), y - rh * 0.9], [fx0 + m(2.4), y], [x - m(0.4), y]], { fill: 'none', stroke: K.filEdge, width: 0.35 });
    mono(L, p, x, y, r.s, { size: 5.1, valign: 'middle', color: r.c, weight: r.w });
    if (r.key) pos[r.key] = [fx0 + fw, y];
  });
  pos.file = [fx0 + fw, ry(0)];
  // tables du catalogue
  const tables = [
    { name: 'simulation', cols: [['id', 'uuid'], ['parameters', 'par'], ['git_commit', 'git'], ['status'], ['wall_time_s']] },
    { name: 'file', cols: [['uri', 'file'], ['sha256'], ['size_bytes'], ['n_t']] },
    { name: 'diagnostic', cols: [['name', 'dia'], ['t'], ['value']] },
    { name: 'job', cols: [['scheduler'], ['external_id'], ['status']] },
  ];
  let y = Y0;
  const tpos = {};
  for (const t of tables) {
    const h = m(3.0) + t.cols.length * m(2.55) + m(0.6);
    L.rect(p, tx0, y, tw, h, { r: m(1.1), fill: K.cat, stroke: K.catEdge, width: 0.45 });
    L.rect(p, tx0, y, tw, m(3.0), { r: m(1.1), fill: '#ccd5df', stroke: 'none' });
    mono(L, p, tx0 + m(1.4), y + m(1.6), t.name, { size: 5.2, weight: 'bold', valign: 'middle', color: K.catInk });
    t.cols.forEach(([c, key], i) => {
      const yy = y + m(3.0) + m(1.4) + i * m(2.55);
      mono(L, p, tx0 + m(2.0), yy, c, { size: 4.9, valign: 'middle', color: K.catInk });
      if (key) tpos[key] = [tx0, yy];
    });
    y += h + m(1.4);
  }
  // correspondances fichier → catalogue
  for (const key of ['file', 'uuid', 'par', 'git', 'dia']) {
    const a = pos[key], b = tpos[key];
    if (!a || !b) continue;
    const c1 = [a[0] + (b[0] - a[0]) * 0.5, a[1]], c2 = [a[0] + (b[0] - a[0]) * 0.5, b[1]];
    L.path(p, `M${a[0] + m(0.4)},${a[1]} C${c1[0]},${c1[1]} ${c2[0]},${c2[1]} ${b[0] - m(0.4)},${b[1]}`, { fill: 'none', stroke: '#7f8a95', width: 0.45 });
    L.circle(p, b[0] - m(0.4), b[1], m(0.35), { fill: '#7f8a95', stroke: 'none' });
  }
  return { bottom: y };
}

export function make(lang, concept = 'A') {
  const S = T[lang];
  return async function draw(F, L) {
    const m = L.mm;
    if (concept === 'A') {
      const pa = F.panel('a', { x: 0, y: 0, w: 183, h: 62 });
      L.text(pa, 12, 7.6, S.a, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
      stepCycle(F, L, pa, S, m(1), m(3.6), m(181), m(58));
      const pb = F.panel('b', { x: 0, y: 64, w: 92, h: 46 });
      L.text(pb, 12, 7.6, S.b, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
      timeline(F, L, pb, S, m(4), m(9), m(86));
      const pc = F.panel('c', { x: 93, y: 64, w: 90, h: 46 });
      L.text(pc, 12, 7.6, S.c, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
      mapping(F, L, pc, S, m(2), m(6.0), m(86), m(38));
    } else {
      const pa = F.panel('a', { x: 0, y: 0, w: 183, h: 34 });
      L.text(pa, 12, 7.6, S.b, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
      const tl = timeline(F, L, pa, S, m(30), m(5), m(150));
      // coin de zoom d'un pas de temps vers b
      const zx = tl.X(70);
      L.rect(pa, zx - m(0.6), tl.yAx - m(1.6), m(1.2), m(3.2), { fill: 'none', stroke: K.ink, width: 0.5 });
      const pb = F.panel('b', { x: 0, y: 36, w: 120, h: 64 });
      L.text(pb, 12, 7.6, S.a, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
      stepCycle(F, L, pb, S, m(1), m(4), m(118), m(58));
      L.zoomLines(F.root, { x: zx - m(0.6), y: tl.yAx - m(1.6), w: m(1.2), h: m(3.2) }, { x: m(1), y: m(36) + m(4) + m(58) * 0.10, w: m(118), h: m(58) * 0.9 }, { dash: '1.2 0.8' });
      const pc = F.panel('c', { x: 121, y: 36, w: 62, h: 64 });
      L.text(pc, 12, 7.6, S.c, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
      mapping(F, L, pc, S, m(1), m(6.0), m(60), m(56));
    }
  };
}
