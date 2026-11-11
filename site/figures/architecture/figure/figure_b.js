// Brouillon B : trois couloirs (portable, VM, cluster) ; les étapes sont placées dans le couloir où elles
// tournent pour une campagne simulée sur le cluster puis entraînée et évaluée sur la VM.
// Hero : aucun (architecture logicielle).
import { K, badge, mono, sheet, paramGrid, laptop, server, cloud, dbGlyph, folderGlyph, tgSpeed } from './draw.js';
export const figure = { width: 183, height: 128, name: 'architecture_b', format: 'journal', illustrate: true };

export default async function draw(F, L) {
  const m = L.mm;
  const P = F.panel('', { x: 0, y: 0, w: 183, h: 128 });
  const lanes = [
    { name: 'Portable', sub: 'sans GPU', y: 4, h: 30 },
    { name: 'VM cloud GPU', sub: 'Docker Compose', y: 36, h: 46 },
    { name: 'Cluster Slurm', sub: 'Apptainer, nœuds sans Internet', y: 84, h: 42 },
  ];
  for (const ln of lanes) {
    L.rect(P, m(1), m(ln.y), m(181), m(ln.h), { r: m(2), fill: '#f6f7f8', stroke: K.frame, width: 0.6 });
    L.text(P, m(4), m(ln.y + 13), ln.name, { size: 6.4, weight: 'bold', color: K.ink, valign: 'middle' });
    L.text(P, m(4), m(ln.y + 16.6), ln.sub, { size: 5.2, color: K.sub, valign: 'middle' });
  }
  laptop(L, P, m(9), m(9.6), m(6));
  cloud(L, P, m(9), m(43), m(9.2), m(6.4)); server(L, P, m(9), m(43.4), m(3.4), { n: 2, gpu: true });
  for (let k = 0; k < 3; k++) server(L, P, m(5.2 + k * 2.6), m(91.6), m(2.6), { n: 3, gpu: true });

  const X = (k) => m(40 + k * 21.2);
  const stage = (k, laneY, name, sub, mod) => {
    badge(L, P, X(k) - m(8.6), m(laneY + 4.4), m(1.7), k + 1, 5.6);
    L.text(P, X(k) - m(6.4), m(laneY + 4.4), name, { size: 6, weight: 'bold', color: K.ink, valign: 'middle' });
    if (sub) L.text(P, X(k), m(laneY + 20.8), sub, { size: 5, color: K.sub, anchor: 'middle' });
    mono(L, P, X(k), m(laneY + 23.6), mod, { size: 5, anchor: 'middle', color: K.sub });
    F.anchor(`b${k}`, P, X(k), m(laneY + 12.6));
  };
  // 1 : campagne écrite sur le portable
  {
    const x = X(0) - m(6.5), y = m(9);
    sheet(L, P, x, y, m(13), m(13.2), { fold: m(2.4) });
    paramGrid(L, P, x + m(2.4), y + m(10.4), m(2.6), m(0.7));
    stage(0, 4, 'Campagne', '4 × 3 = 12 simulations', 'infra/configs/');
  }
  // 2, 3, 4 : cluster
  {
    const Y = 84;
    for (let k = 2; k >= 0; k--) L.rect(P, X(1) - m(6) + k * m(1.6), m(Y + 8) + k * m(2), m(9), m(6), { r: m(0.7), fill: '#fff', stroke: '#9aa3ab', width: 0.45 });
    L.circle(P, X(1) - m(4.2), m(Y + 11), m(0.7), { fill: K.lam, stroke: 'none' });
    stage(1, Y, 'Lancement', 'tableau de jobs', 'milady.sweep');
    const e = m(10), P3 = L.obliqueProj({ preset: 'angles', angle: 32, depth: 0.55 });
    const box = L.obliqueBox(P, P3, [e, e, e], { at: [X(2), m(Y + 12.6)], anchor: 'center', fill: '#ffffff', stroke: K.ink, width: 0.5 });
    stage(2, Y, 'Simulation', '1 GPU par simulation', 'milady.sim');
    sheet(L, P, X(3) - m(6), m(Y + 7.6), m(12), m(11), { fold: m(2.2) });
    mono(L, P, X(3) - m(4.6), m(Y + 11), 'fields.h5', { size: 5, weight: 'bold' });
    stage(3, Y, 'Stockage', '$SCRATCH', 'milady.storage');
    L.rect(P, m(132), m(Y + 28), m(46), m(10), { r: m(1.4), fill: K.cat, stroke: K.catEdge, width: 0.4 });
    dbGlyph(L, P, m(136), m(Y + 33), m(3));
    L.text(P, m(139.4), m(Y + 33), 'SQLite sur $WORK', { size: 5.4, color: K.catInk, valign: 'middle' });
  }
  // 5, 6, 7 : VM
  {
    const Y = 36;
    paramGrid(L, P, X(4) - m(4), m(Y + 15.6), m(2.6), m(0.7), (i, j, x, y) => L.circle(P, x, y, m(0.7), { fill: i === 1 && j === 2 ? '#fff' : K.lam, stroke: K.lam, width: 0.5 }));
    stage(4, Y, 'Jeu de données', 'train · val · test', 'milady.catalog');
    L.rect(P, X(5) - m(5), m(Y + 7.8), m(10), m(10), { r: m(1.2), fill: K.zl, stroke: K.z, width: 0.55 });
    L.network(P, X(5) - m(4), m(Y + 8.8), { layers: [3, 4, 3], w: m(8), h: m(8), r: m(0.5), colors: [K.z, K.z, K.z], edges: true });
    stage(5, Y, 'Entraînement', 'worker-gpu', 'milady.train.fm3d');
    L.polyline(P, [[X(6) - m(6), m(Y + 7.6)], [X(6) - m(6), m(Y + 17.6)], [X(6) + m(6), m(Y + 17.6)]], { fill: 'none', stroke: K.ink, width: 0.45 });
    L.polyline(P, L.sample((t) => m(Y + 8.6) + m(8.4) * t, 0, 1, 12).map(([t, y]) => [X(6) - m(5.4) + m(11) * t, y]), { fill: 'none', stroke: '#6f6f6f', width: 0.6 });
    stage(6, Y, 'Évaluation', 'spectres, bilans', 'milady.eval');
    const svc = [['PostgreSQL 16', K.cat, K.catEdge, dbGlyph], ['MinIO (S3)', K.fil, K.filEdge, folderGlyph], ['MLflow', '#eef0f2', '#b9c0c7', null]];
    svc.forEach(([s, f, e, g], i) => {
      const x = m(38 + i * 48);
      L.rect(P, x, m(Y + 31), m(44), m(10), { r: m(1.4), fill: f, stroke: e, width: 0.4 });
      if (g) g(L, P, x + m(4), m(Y + 36), m(3));
      L.text(P, x + m(7.6), m(Y + 36), s, { size: 5.6, color: K.ink, valign: 'middle' });
    });
  }
  // flux des étapes (traversent les couloirs)
  for (let k = 0; k < 6; k++) { F.relate(`b${k}`, `b${k + 1}`, 'flow'); }
  L.connect(F, 'b0', 'b1', { stroke: '#8a8a8a', width: 0.6, head: 2.2, via: [[X(0) + m(9), m(16.6)], [X(0) + m(9), m(96.6)]] });
  L.connect(F, 'b1', 'b2', { stroke: '#8a8a8a', width: 0.6, head: 2.2 });
  L.connect(F, 'b2', 'b3', { stroke: '#8a8a8a', width: 0.6, head: 2.2 });
  L.connect(F, 'b3', 'b4', { stroke: '#8a8a8a', width: 0.6, head: 2.2, dash: '1.4 0.8' });
  L.connect(F, 'b4', 'b5', { stroke: '#8a8a8a', width: 0.6, head: 2.2 });
  L.connect(F, 'b5', 'b6', { stroke: '#8a8a8a', width: 0.6, head: 2.2 });
  L.text(P, X(3) + m(6), m(76), 'copie vers S3 · ingest', { size: 5.2, color: K.sub, anchor: 'start' });
  L.text(P, m(60), m(25.5), 'git, ssh, tunnel SSH', { size: 5.2, color: K.sub, anchor: 'start' });
}
